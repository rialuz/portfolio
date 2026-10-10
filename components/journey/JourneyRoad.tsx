'use client'

import { useEffect, type CSSProperties, type ReactNode } from 'react'
import { fadedStop, journey, stopName, type StopKind } from '@/content/journey'
import { Sprite, Strip } from '@/components/sprite/Sprite'
import { PixelNumber } from '@/components/ui/PixelNumber'
import { setMotion, useMotion } from '@/lib/motion'
import { useScene } from '@/lib/scene'
import { seasons, seasonSpriteUrl } from '@/lib/seasons'
import type { SpriteName } from '@/lib/sprites'
import type { Facing } from './path'
import { roadSize, roadTiles } from './path'
import { StopDetail } from './StopDetail'
import { useJourney, type Phase } from './useJourney'

const stops = journey.map((s) => ({ x: s.tile.col, y: s.tile.row }))
const tiles = roadTiles(stops, journey.findIndex((s) => s.id === fadedStop) - 1)
const size = roadSize(tiles)

/** The longest level stretch of travelled road, in tiles: where a season's creature paces. */
const stretch = tiles
  .filter((t) => t.kind === 'straight' && t.turns === 0 && !t.faded)
  .sort((a, b) => a.row - b.row || a.col - b.col)
  .reduce<{ row: number; from: number; to: number }[]>((runs, t) => {
    const last = runs.at(-1)
    if (last && last.row === t.row && t.col === last.to + 1) last.to = t.col
    else runs.push({ row: t.row, from: t.col, to: t.col })
    return runs
  }, [])
  .reduce<{ row: number; from: number; to: number } | null>(
    (best, run) => (run.to > run.from && (!best || run.to - run.from > best.to - best.from) ? run : best),
    null,
  )

const badge: Record<StopKind, string> = {
  done: 'border-solid border-navy bg-navy text-cream',
  current: 'border-solid border-navy bg-coral text-white',
  future: 'border-dashed border-navy bg-cream text-navy',
}

const WALK_STRIP: Record<Facing, SpriteName> = {
  right: 'luz-walk',
  left: 'luz-walk',
  up: 'luz-walk-up',
  down: 'luz-walk-down',
}

/** Strips she switches to mid-walk, loaded ahead so a change of strip never flashes empty. */
const PRELOAD: SpriteName[] = [
  'luz-walk',
  'luz-walk-up',
  'luz-walk-down',
  'luz-hop',
  ...journey.flatMap((s) => [s.emote, s.bubble]),
]

function walkerStrip(phase: Phase, facing: Facing, emote: SpriteName): SpriteName {
  if (phase === 'walk') return WALK_STRIP[facing]
  if (phase === 'hop') return 'luz-hop'
  return emote
}

export function JourneyRoad({ intro }: { intro: ReactNode }) {
  const { current, target, phase, facing, arrivals, announcement, start, roadRef, walkerRef, select, onKeyDown } =
    useJourney()
  const stop = journey[current]
  const motion = useMotion()
  const scene = useScene()
  // A season sends one of its creatures to pace the road: a crab on the sand, a ghost on the cobbles.
  const critter = scene === 'candy' ? undefined : seasons[scene].roadWalkers[0]

  useEffect(() => {
    PRELOAD.forEach((name) => {
      new Image().src = seasonSpriteUrl(scene, name)
    })
  }, [scene])

  return (
    <div className="flex flex-col gap-7">
      {/* The heading, with the road's hint in the top right corner wherever the road is drawn. */}
      <div className="flex items-start justify-between gap-6">
        {intro}
        <p className="js-only hidden max-w-[300px] flex-none flex-col items-end gap-1.5 pt-1.5 text-right text-sm font-medium tracking-wide text-slate md:flex lg:max-w-none lg:pt-[11px]">
          {motion ? (
            'Use the left and right arrow keys to walk the road.'
          ) : (
            <>
              {/* Motion follows the system setting, so say why she is standing still. */}
              <span>Animation is off, so I jump between stops.</span>
              <button
                type="button"
                onClick={() => setMotion(true)}
                className="inline-flex min-h-11 cursor-pointer items-center rounded border-[3px] border-navy bg-cream px-3 font-bold text-navy shadow-pixel-sm hover:bg-petal"
              >
                Turn animation on to watch me walk
              </button>
            </>
          )}
        </p>
      </div>

      {/* The road: tablets and up. */}
      <div className="hidden md:block">
        <div
          ref={roadRef}
          role="group"
          aria-label="Experience road"
          onKeyDown={onKeyDown}
          className="road"
          style={{ '--cols': size.cols, '--rows': size.rows } as CSSProperties}
        >
          <Sprite sheet="prop-cloud" className="road-puff" style={{ '--rest': 'calc(var(--tile) * 2)' } as CSSProperties} />
          <Sprite
            sheet="prop-cloud"
            className="road-puff"
            style={
              { '--top': 'calc(var(--tile) * 0.75)', '--d': '70s', '--at': '-30s', '--rest': 'calc(var(--tile) * 7)' } as CSSProperties
            }
          />

          {tiles.map((tile) => (
            <Sprite
              key={`${tile.col},${tile.row}`}
              sheet={tile.kind === 'corner' ? 'tile-road-corner' : tile.faded ? 'tile-road-faded' : 'tile-road-straight'}
              className="road-tile"
              data-washed={(tile.faded && tile.kind === 'corner') || undefined}
              style={{ '--col': tile.col, '--row': tile.row, '--turns': tile.turns } as CSSProperties}
            />
          ))}

          <Sprite sheet="prop-flag" className="road-flag" />

          {scene !== 'candy' && critter && stretch && (
            <span
              aria-hidden="true"
              className="road-critter"
              style={
                {
                  '--col': stretch.from,
                  '--row': stretch.row,
                  '--w': seasons[scene].sprites[critter].w,
                  '--h': seasons[scene].sprites[critter].h,
                  '--steps': (stretch.to - stretch.from) * 32,
                } as CSSProperties
              }
            >
              <Strip url={seasonSpriteUrl(scene, critter)} facts={seasons[scene].sprites[critter]} />
            </span>
          )}

          {journey.map((s, i) => {
            const selected = target === i
            return (
              <button
                key={s.id}
                type="button"
                aria-pressed={selected}
                aria-label={stopName(i)}
                onClick={() => select(i)}
                className="road-stop flex w-[124px] cursor-pointer flex-col items-center gap-1 lg:w-[168px] lg:gap-1.5"
                style={{ '--col': s.tile.col, '--row': s.tile.row } as CSSProperties}
              >
                <span
                  className={`road-stop-badge flex size-9 items-center justify-center rounded border-[3px] font-pixel text-lg font-bold lg:size-[52px] lg:text-[22px] ${badge[s.kind]} ${
                    selected
                      ? 'shadow-[0_0_0_3px_var(--color-cream),0_0_0_6px_var(--color-coral)]'
                      : 'shadow-sand'
                  }`}
                >
                  <PixelNumber value={i + 1} />
                </span>
                <span
                  className={`rounded border-2 border-navy px-2 py-0.5 text-xs font-bold whitespace-nowrap lg:px-2.5 lg:text-[13px] ${
                    selected ? 'bg-petal' : 'bg-white'
                  }`}
                >
                  {s.label}
                </span>
                <span className="text-xs font-bold text-coral-ink">{s.when}</span>
              </button>
            )
          })}

          <div
            ref={walkerRef}
            aria-hidden="true"
            className="road-walker"
            data-phase={phase}
            style={{ '--x': start.x, '--y': start.y } as CSSProperties}
          >
            {phase === 'rest' && (
              <Sprite key={arrivals} sheet={stop.bubble} rest="last" className="road-bubble" />
            )}
            <Sprite
              // A new key restarts the strip from its first frame.
              key={`${phase}-${facing}-${arrivals}`}
              sheet={walkerStrip(phase, facing, stop.emote)}
              flipped={phase !== 'rest' && facing === 'left'}
            />
          </div>
        </div>
      </div>

      {/* Small screens: the stops as a list, with the character beside the selected one. */}
      <ol aria-label="Experience road" className="flex list-none flex-col md:hidden">
        {[...journey.keys()].reverse().map((i) => {
          const s = journey[i]
          const selected = target === i
          const lastInList = i === 0
          return (
            <li key={s.id} className="flex gap-3">
              <div aria-hidden="true" className="flex w-7 flex-none flex-col items-center">
                <span
                  className={`size-7 flex-none rounded-full border-[3px] border-navy ${
                    s.kind === 'current' ? 'bg-coral' : s.kind === 'future' ? 'border-dashed bg-cream' : 'bg-navy'
                  }`}
                />
                {!lastInList && (
                  <span className="w-1.5 flex-auto bg-[repeating-linear-gradient(180deg,var(--color-rose)_0_12px,transparent_12px_20px)]" />
                )}
              </div>
              <button
                type="button"
                aria-pressed={selected}
                aria-label={stopName(i)}
                onClick={() => select(i)}
                className={`mb-3 flex min-h-11 flex-auto cursor-pointer items-center justify-between gap-2 rounded-md border-[3px] px-3 py-2 text-left ${
                  selected ? 'border-navy bg-white shadow-pixel-sm' : 'border-transparent'
                }`}
              >
                <span className="flex min-w-0 flex-col gap-0.5">
                  <span className="text-xs font-bold text-coral-ink">{s.period}</span>
                  <strong className="text-base leading-snug">{s.title}</strong>
                  {s.summary && <span className="text-sm font-medium tracking-wide text-slate">{s.summary}</span>}
                </span>
                {selected && <Sprite sheet={s.emote} scale={1} className="-my-3 -mr-2" />}
              </button>
            </li>
          )
        })}
      </ol>

      <p role="status" aria-live="polite" className="sr-only">
        {announcement}
      </p>

      <section
        aria-label="Selected stop"
        className="rounded-md border-[3px] border-navy bg-white p-5 shadow-coral-lg sm:p-7"
      >
        <div className="flex flex-col gap-10">
          {journey.map((s, i) => (
            <StopDetail key={s.id} stop={s} collapsed={i !== current} />
          ))}
        </div>
      </section>
    </div>
  )
}
