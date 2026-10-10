'use client'

import { useEffect, useRef, useState, type CSSProperties } from 'react'
import { hero } from '@/content/site'
import { crossingDelay, SceneForeground, ScenePieces } from '@/components/scene/ScenePieces'
import { Sprite } from '@/components/sprite/Sprite'
import { motionEnabled } from '@/lib/motion'
import { useScene } from '@/lib/scene'
import { seasons } from '@/lib/seasons'

// Where each cloud sat in the candy painting, in background pixels, and how many seconds it
// takes to cross. A season rests its clouds where its own sky is open. A negative delay
// starts each one at its spot: (x + 70) / 414 of its duration.
const candyClouds = [
  { sheet: 'bg-cloud-1', x: 33, y: 22 },
  { sheet: 'bg-cloud-2', x: 221, y: 25 },
  { sheet: 'bg-cloud-3', x: 81, y: 53 },
] as const
const crossings = [90, 130, 110]

/**
 * The hero art, back to front: background, clouds, flag, character, bubble. She waves once
 * on load, and again on hover or when focus moves into the hero. The dialogue hero leaves
 * out the flag and the bubble: its own box does the talking.
 *
 * In a season the painting, clouds and flag are the season's own (see Sprite), and the season
 * adds its moving pieces: some behind its foreground scenery, some in front of it.
 */
export function HeroScene({ flag = true, bubble = true }: { flag?: boolean; bubble?: boolean }) {
  const scene = useScene()
  const season = scene === 'candy' ? null : scene
  const clouds = season ? seasons[season].clouds : candyClouds
  // Starting on the wave means it plays on load with no script needed.
  const [waving, setWaving] = useState(true)
  const [waves, setWaves] = useState(0)
  const sceneRef = useRef<HTMLDivElement>(null)

  const wave = () => {
    if (!motionEnabled()) return
    setWaving(true)
    setWaves((n) => n + 1)
  }

  useEffect(() => {
    const section = sceneRef.current?.closest('section')
    section?.addEventListener('focusin', wave)
    return () => section?.removeEventListener('focusin', wave)
  }, [])

  return (
    <div ref={sceneRef} aria-hidden="true" className="hero-scene">
      <Sprite sheet="bg-hero" className="hero-bg" />
      {clouds.map((c, i) => (
        <Sprite
          key={c.sheet}
          sheet={c.sheet}
          className="hero-cloud"
          style={
            { '--x': c.x, '--y': c.y, '--d': `${crossings[i]}s`, '--at': crossingDelay(c.x, crossings[i]) } as CSSProperties
          }
        />
      ))}
      {season && <ScenePieces season={season} layer="back" />}
      {season && <SceneForeground season={season} />}
      {season && <ScenePieces season={season} layer="front" />}
      {flag && <Sprite sheet="prop-flag" className="hero-flag" />}
      <div className="hero-luz" onMouseEnter={wave}>
        {waving ? (
          <Sprite key={waves} sheet="luz-wave" onAnimationEnd={() => setWaving(false)} />
        ) : (
          <Sprite sheet="luz-idle" />
        )}
      </div>
      {bubble && (
        <div className="hero-bubble rounded-md border-[3px] border-navy bg-white px-2.5 py-1 font-pixel text-[15px] whitespace-nowrap lg:px-3.5 lg:py-1.5 lg:text-lg">
          {hero.bubble}
        </div>
      )}
    </div>
  )
}
