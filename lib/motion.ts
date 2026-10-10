'use client'

import { useSyncExternalStore } from 'react'
import { MOTION_KEY, MOTION_QUERY } from './motion-script'

// The motion preference lives on <html data-motion="on|off">. It follows the system setting
// until the visitor uses the header switch; their choice then lasts for the session.

const listeners = new Set<() => void>()

function stored(): string | null {
  try {
    return sessionStorage.getItem(MOTION_KEY)
  } catch {
    return null
  }
}

function apply(on: boolean) {
  document.documentElement.dataset.motion = on ? 'on' : 'off'
  listeners.forEach((notify) => notify())
}

export function motionEnabled(): boolean {
  return document.documentElement.dataset.motion !== 'off'
}

export function setMotion(on: boolean) {
  try {
    sessionStorage.setItem(MOTION_KEY, on ? 'on' : 'off')
  } catch {
    // Storage can be blocked; the choice then lasts until the page reloads.
  }
  apply(on)
}

function subscribe(notify: () => void) {
  listeners.add(notify)
  const media = window.matchMedia(MOTION_QUERY)
  const onSystemChange = () => {
    if (stored() === null) apply(!media.matches)
  }
  media.addEventListener('change', onSystemChange)
  return () => {
    listeners.delete(notify)
    media.removeEventListener('change', onSystemChange)
  }
}

/** True when animation is on. Always true on the server; CSS holds the stills until hydration. */
export function useMotion(): boolean {
  return useSyncExternalStore(subscribe, motionEnabled, () => true)
}
