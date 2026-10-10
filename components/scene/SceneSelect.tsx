'use client'

import { sceneMenu } from '@/content/site'
import { setScene, useScene } from '@/lib/scene'
import { isEnvironment } from '@/lib/seasons'

/**
 * Picks the pixel scene. It opens on the calendar's scene for today; a pick here lasts for
 * the session. Only the pixel art changes. It needs JavaScript, so it is hidden without it.
 *
 * The label and the menu are one framed control: the frame, the focus ring and the arrow are
 * the label's (.scene-menu in app/globals.css), and the menu inside has no box of its own.
 */
export function SceneSelect({ className = '' }: { className?: string }) {
  const scene = useScene()

  return (
    <label className={`scene-menu js-only ${className}`}>
      <span className="scene-menu-label max-sm:sr-only">{sceneMenu.label}</span>
      <select
        value={scene}
        onChange={(event) => {
          if (isEnvironment(event.target.value)) setScene(event.target.value)
        }}
      >
        {sceneMenu.options.map((option) => (
          <option key={option.scene} value={option.scene}>
            {option.name}
          </option>
        ))}
      </select>
    </label>
  )
}
