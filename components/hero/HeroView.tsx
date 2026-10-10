'use client'

import type { ReactNode } from 'react'
import { SceneSelect } from '@/components/scene/SceneSelect'
import { Switch } from '@/components/ui/Switch'
import { setHeroView, useHeroView } from '@/lib/hero-view'

/**
 * The hero, in whichever of its two versions the visitor wants, with its two controls in the
 * scene's top right corner: the Season menu, which changes the pixel art, and the switch
 * between the heroes, on for the game dialogue and off for the plain text card. The page
 * starts on heroStyle from content/site.ts and on the calendar's scene for today.
 *
 * The controls come first so keyboard and screen reader users reach them before the dialogue.
 */
export function HeroView({ card, dialogue, container }: { card: ReactNode; dialogue: ReactNode; container: string }) {
  const view = useHeroView()

  return (
    <div className="hero-view relative" data-view={view}>
      {/* On a phone the two fit side by side without the switch's On/Off word; if a screen is
          narrower still, the switch drops under the menu instead of running off the side. */}
      <div className={`${container} pointer-events-none absolute inset-x-0 top-3 z-10 flex flex-wrap justify-end gap-2`}>
        <SceneSelect className="pointer-events-auto" />
        <Switch
          label={
            <>
              <span className="sm:hidden">Dialogue</span>
              <span className="max-sm:hidden">Interactive dialogue</span>
            </>
          }
          on={view === 'dialogue'}
          onChange={(on) => setHeroView(on ? 'dialogue' : 'card')}
          className="pointer-events-auto border-[3px] border-navy bg-cream px-3 shadow-pixel-sm max-sm:[&>span:last-child]:hidden"
        />
      </div>
      {view === 'dialogue' ? dialogue : card}
    </div>
  )
}
