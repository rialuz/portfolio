'use client'

import { useSyncExternalStore } from 'react'
import { heroStyle, type HeroStyle } from '@/content/site'
import { HERO_KEY } from './hero-view-script'

// Which hero the visitor sees lives on <html data-hero="dialogue|card">. It is the site's
// default, heroStyle in content/site.ts, until they use the switch on the hero; their choice
// then lasts for the session, as the animation switch's does.

const listeners = new Set<() => void>()

function heroView(): HeroStyle {
  const chosen = document.documentElement.dataset.hero
  return chosen === 'card' || chosen === 'dialogue' ? chosen : heroStyle
}

export function setHeroView(view: HeroStyle) {
  try {
    sessionStorage.setItem(HERO_KEY, view)
  } catch {
    // Storage can be blocked; the choice then lasts until the page reloads.
  }
  document.documentElement.dataset.hero = view
  listeners.forEach((notify) => notify())
}

function subscribe(notify: () => void) {
  listeners.add(notify)
  return () => {
    listeners.delete(notify)
  }
}

/** The hero to show. Always the default on the server; CSS hides it until hydration if the visitor chose the other. */
export function useHeroView(): HeroStyle {
  return useSyncExternalStore(subscribe, heroView, () => heroStyle)
}
