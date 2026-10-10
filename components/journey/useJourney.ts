'use client'

import { useCallback, useEffect, useMemo, useRef, useState, type KeyboardEvent } from 'react'
import { initialStop, journey, stopName, type StopId } from '@/content/journey'
import { motionEnabled, useMotion } from '@/lib/motion'
import { sprites } from '@/lib/sprites'
import { advance, buildPath, facingAt, keyTarget, positionAt, type Facing } from './path'

export type Phase = 'rest' | 'walk' | 'hop'

const HASH_PREFIX = 'experience-'
const HOP_MS = sprites['luz-hop'].duration * 1000
const stops = journey.map((s) => ({ x: s.tile.col, y: s.tile.row }))
const rows = journey.map((s) => s.tile.row)
const indexOf = (id: string) => journey.findIndex((s) => s.id === id)

export const journeyPath = buildPath(stops)
export const initialIndex = indexOf(initialStop)

/** Elements that use Left and Right themselves. */
const ARROW_KEY_OWNERS =
  'input, textarea, select, [contenteditable=""], [contenteditable="true"], [role="slider"], [role="tablist"], [role="radiogroup"], [role="menu"]'

/** True when at least 60% of the element, or of the window if that is shorter, is on screen. */
function mostlyInView(el: Element): boolean {
  const rect = el.getBoundingClientRect()
  const visible = Math.min(rect.bottom, window.innerHeight) - Math.max(rect.top, 0)
  return visible >= Math.min(rect.height, window.innerHeight) * 0.6
}

function stopFromHash(): number {
  const hash = window.location.hash.slice(1)
  return hash.startsWith(HASH_PREFIX) ? indexOf(hash.slice(HASH_PREFIX.length)) : -1
}

/**
 * Holds the stop the character is at, the stop she is heading for and whether she is walking,
 * and turns key presses and clicks into walks.
 *
 * While she walks, her position is written straight to the walker element as --x and --y
 * (in tiles) so the page does not re-render on every frame.
 */
export function useJourney() {
  const path = journeyPath
  const motion = useMotion()

  /** The stop she is at, or last left. The detail panel shows this one. */
  const [current, setCurrent] = useState(initialIndex)
  /** The stop she is heading for. The pressed button is this one. */
  const [target, setTarget] = useState(initialIndex)
  const [phase, setPhase] = useState<Phase>('rest')
  const [facing, setFacing] = useState<Facing>('right')
  /** Counts arrivals, so the bubble can replay its pop each time. */
  const [arrivals, setArrivals] = useState(0)
  const [announcement, setAnnouncement] = useState('')

  const roadRef = useRef<HTMLDivElement>(null)
  const walkerRef = useRef<HTMLDivElement>(null)
  const distance = useRef(path.stopDistances[initialIndex])
  const targetRef = useRef(initialIndex)
  const facingRef = useRef<Facing>('right')
  const frame = useRef(0)
  const hopTimer = useRef<ReturnType<typeof setTimeout>>(undefined)

  const place = useCallback(
    (d: number) => {
      distance.current = d
      const p = positionAt(path, d)
      // Snap to whole sprite pixels so she never sits between two screen pixels.
      walkerRef.current?.style.setProperty('--x', String(Math.round(p.x * 32) / 32))
      walkerRef.current?.style.setProperty('--y', String(Math.round(p.y * 32) / 32))
    },
    [path],
  )

  const stopWalking = useCallback(() => {
    cancelAnimationFrame(frame.current)
    frame.current = 0
    clearTimeout(hopTimer.current)
  }, [])

  const arrive = useCallback((index: number, announce: boolean) => {
    setCurrent(index)
    setPhase('rest')
    setArrivals((n) => n + 1)
    if (announce) setAnnouncement(stopName(index))
  }, [])

  const walk = useCallback(() => {
    let last = performance.now()
    const tick = (now: number) => {
      const goal = path.stopDistances[targetRef.current]
      const from = distance.current
      const direction = goal >= from ? 1 : -1
      // A long gap means the tab was in the background; do not leap ahead.
      const seconds = Math.min((now - last) / 1000, 0.05)
      last = now
      const d = advance(from, goal, seconds)
      place(d)

      if (d === goal) {
        frame.current = 0
        const index = targetRef.current
        setPhase('hop')
        hopTimer.current = setTimeout(() => arrive(index, true), HOP_MS)
        return
      }
      const next = facingAt(path, d, direction)
      if (next !== facingRef.current) {
        facingRef.current = next
        setFacing(next)
      }
      frame.current = requestAnimationFrame(tick)
    }
    frame.current = requestAnimationFrame(tick)
  }, [arrive, path, place])

  /**
   * Head for a stop. Returns false when she is already heading there, so callers can leave
   * the browser's default action alone.
   */
  const select = useCallback(
    (index: number, options: { announce?: boolean; updateHash?: boolean; instant?: boolean } = {}) => {
      if (index < 0 || index >= journey.length || index === targetRef.current) return false
      const { announce = true, updateHash = true, instant = false } = options
      targetRef.current = index
      setTarget(index)
      if (updateHash) {
        window.history.replaceState(null, '', `#${HASH_PREFIX}${journey[index].id}`)
      }

      // The road is not drawn on small screens, where the stops are a list: no walking there.
      const roadVisible = roadRef.current !== null && roadRef.current.offsetParent !== null
      if (instant || !motionEnabled() || !roadVisible) {
        stopWalking()
        place(path.stopDistances[index])
        arrive(index, announce)
        return true
      }

      clearTimeout(hopTimer.current)
      const direction = path.stopDistances[index] >= distance.current ? 1 : -1
      facingRef.current = facingAt(path, distance.current, direction)
      setFacing(facingRef.current)
      setPhase('walk')
      if (!frame.current) walk()
      return true
    },
    [arrive, path, place, stopWalking, walk],
  )

  const selectId = useCallback((id: StopId) => select(indexOf(id)), [select])

  /** Arrow keys (all four), Home and End. Attached to the road only, so the rest of the page scrolls as usual. */
  const onKeyDown = useCallback(
    (event: KeyboardEvent) => {
      if (event.altKey || event.ctrlKey || event.metaKey) return
      const next = keyTarget(event.key, targetRef.current, journey.length, rows)
      // The default action is cancelled only when a walk actually starts.
      if (next !== null && select(next)) event.preventDefault()
    },
    [select],
  )

  // Left and Right also work without focusing a stop, whenever the road is on screen. Those two
  // keys do not scroll the page, so nothing is taken from the visitor. Up, Down, Home and End
  // stay with the road's own handler above: anywhere else they scroll.
  useEffect(() => {
    const onWindowKey = (event: globalThis.KeyboardEvent) => {
      if (event.key !== 'ArrowLeft' && event.key !== 'ArrowRight') return
      if (event.defaultPrevented || event.altKey || event.ctrlKey || event.metaKey || event.shiftKey) return
      const road = roadRef.current
      // Not drawn on small screens, where the stops are a list.
      if (!road || road.offsetParent === null) return
      const from = event.target instanceof Element ? event.target : null
      // Inside the road its own handler has the key; text fields and the like keep theirs.
      if (from && (road.contains(from) || from.closest(ARROW_KEY_OWNERS))) return
      if (!mostlyInView(road)) return
      const next = keyTarget(event.key, targetRef.current, journey.length, rows)
      if (next !== null && select(next)) event.preventDefault()
    }
    window.addEventListener('keydown', onWindowKey)
    return () => window.removeEventListener('keydown', onWindowKey)
  }, [select])

  // A link can open on a stop: #experience-lead. Later hash changes walk there.
  useEffect(() => {
    const fromHash = stopFromHash()
    if (fromHash >= 0) {
      // She is already there when the page opens, rather than walking from the default stop.
      select(fromHash, { announce: false, updateHash: false, instant: true })
      document.getElementById('experience')?.scrollIntoView()
    }
    const onHashChange = () => {
      const index = stopFromHash()
      if (index >= 0) select(index, { updateHash: false })
    }
    window.addEventListener('hashchange', onHashChange)
    return () => {
      window.removeEventListener('hashchange', onHashChange)
      stopWalking()
    }
  }, [select, stopWalking])

  // Turning motion off mid-walk puts her straight on the stop she was heading for.
  useEffect(() => {
    if (!motion && frame.current) {
      stopWalking()
      place(path.stopDistances[targetRef.current])
      arrive(targetRef.current, true)
    }
  }, [arrive, motion, path, place, stopWalking])

  const start = useMemo(() => positionAt(path, path.stopDistances[initialIndex]), [path])

  return {
    current,
    target,
    phase,
    facing,
    arrivals,
    announcement,
    start,
    roadRef,
    walkerRef,
    select,
    selectId,
    onKeyDown,
  }
}
