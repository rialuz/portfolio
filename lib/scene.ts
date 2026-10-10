'use client'

import { useSyncExternalStore } from 'react'
import { scene as sceneBeforeDate } from '@/content/site'
import { sceneOn } from './scene-calendar'
import { SCENE_KEY } from './scene-script'
import { isEnvironment, type Environment } from './seasons'

// Which pixel scene the visitor is looking at lives on <html data-scene>. It is the calendar's
// scene for today, sceneByMonth in content/site.ts, until they use the Season menu on the
// hero; their choice then lasts for the session, as the animation switch's does.

const listeners = new Set<() => void>()

function currentScene(): Environment {
  const chosen = document.documentElement.dataset.scene
  return isEnvironment(chosen) ? chosen : sceneOn(new Date())
}

export function setScene(scene: Environment) {
  try {
    sessionStorage.setItem(SCENE_KEY, scene)
  } catch {
    // Storage can be blocked; the choice then lasts until the page reloads.
  }
  document.documentElement.dataset.scene = scene
  listeners.forEach((notify) => notify())
}

function subscribe(notify: () => void) {
  listeners.add(notify)
  return () => {
    listeners.delete(notify)
  }
}

/**
 * The scene to show. The server does not know the visitor's date, so there it is always the
 * scene from before the date is known; the art itself follows <html data-scene> in CSS.
 */
export function useScene(): Environment {
  return useSyncExternalStore(subscribe, currentScene, () => sceneBeforeDate)
}
