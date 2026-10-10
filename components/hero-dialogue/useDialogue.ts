'use client'

import { useCallback, useEffect, useRef, useState } from 'react'
import { motionEnabled } from '@/lib/motion'

/** Letters per second while a page types itself out. */
const TYPE_SPEED = 70

/** Things that use Space or Enter themselves. */
const KEY_OWNERS = 'a, button, input, textarea, select, summary, [contenteditable=""], [contenteditable="true"], [role="button"]'

/** True when at least 60% of the element, or of the window if that is shorter, is on screen. */
function mostlyInView(el: Element): boolean {
  const rect = el.getBoundingClientRect()
  const visible = Math.min(rect.bottom, window.innerHeight) - Math.max(rect.top, 0)
  return visible >= Math.min(rect.height, window.innerHeight) * 0.6
}

/**
 * Pages through the dialogue. A new page types itself out; advancing while it types finishes
 * the page at once, and advancing again moves on. The first page is shown whole on load, so
 * the server-rendered text and the first paint match.
 */
export function useDialogue(pages: readonly string[]) {
  const [page, setPage] = useState(0)
  /** Letters of the current page shown so far. */
  const [typed, setTyped] = useState(pages[0].length)
  const boxRef = useRef<HTMLDivElement>(null)
  const frame = useRef(0)
  const pageRef = useRef(0)
  const typedRef = useRef(pages[0].length)

  const show = useCallback((count: number) => {
    typedRef.current = count
    setTyped(count)
  }, [])

  const stopTyping = useCallback(() => {
    cancelAnimationFrame(frame.current)
    frame.current = 0
  }, [])

  const open = useCallback(
    (index: number) => {
      stopTyping()
      pageRef.current = index
      setPage(index)
      const length = pages[index].length
      if (!motionEnabled()) {
        show(length)
        return
      }
      show(0)
      let shown = 0
      let last = performance.now()
      const tick = (now: number) => {
        // A long gap means the tab was in the background; do not leap ahead.
        shown = Math.min(length, shown + Math.min((now - last) / 1000, 0.05) * TYPE_SPEED)
        last = now
        show(Math.floor(shown))
        frame.current = shown < length ? requestAnimationFrame(tick) : 0
      }
      frame.current = requestAnimationFrame(tick)
    },
    [pages, show, stopTyping],
  )

  /** Finish the page if it is still typing, otherwise move to the next. False on the last page. */
  const advance = useCallback(() => {
    const index = pageRef.current
    if (typedRef.current < pages[index].length) {
      stopTyping()
      show(pages[index].length)
      return true
    }
    if (index >= pages.length - 1) return false
    open(index + 1)
    return true
  }, [open, pages, show, stopTyping])

  const restart = useCallback(() => open(0), [open])

  // Space and Enter continue the dialogue while it is on screen, unless a button, link or
  // field has the key. On the last page they are left to the browser, so Space scrolls again.
  useEffect(() => {
    const onKey = (event: KeyboardEvent) => {
      if (event.key !== ' ' && event.key !== 'Enter') return
      if (event.defaultPrevented || event.repeat || event.altKey || event.ctrlKey || event.metaKey || event.shiftKey) return
      const from = event.target instanceof Element ? event.target : null
      if (from?.closest(KEY_OWNERS)) return
      if (!boxRef.current || !mostlyInView(boxRef.current)) return
      if (advance()) event.preventDefault()
    }
    window.addEventListener('keydown', onKey)
    return () => {
      window.removeEventListener('keydown', onKey)
      stopTyping()
    }
  }, [advance, stopTyping])

  const typing = typed < pages[page].length
  return { page, typed, typing, last: page === pages.length - 1, boxRef, advance, restart }
}
