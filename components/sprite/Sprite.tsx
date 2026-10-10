import type { CSSProperties, HTMLAttributes } from 'react'
import { characterPieces, replaced, seasonIds, seasonSpriteUrl } from '@/lib/seasons'
import { sprites, spriteUrl, type SpriteName, type SpriteSheet } from '@/lib/sprites'

interface StripOptions extends Omit<HTMLAttributes<HTMLSpanElement>, 'children'> {
  /** Play the strip. A paused strip shows its first frame. */
  playing?: boolean
  /** Mirror left to right. */
  flipped?: boolean
  /** Whole-number scale. Leave out to take --s from the scene, which can change at a breakpoint. */
  scale?: number
  /** Frame to hold when motion is off. Strips that pop in, like speech bubbles, rest on the last. */
  rest?: 'first' | 'last'
}

interface StripProps extends StripOptions {
  url: string
  facts: SpriteSheet
}

/**
 * One strip of frames from any file, played with CSS steps(). No JavaScript runs for it.
 * Sprite is this for the kit in lib/sprites.ts; a season's own pieces use it directly.
 */
export function Strip({
  url,
  facts,
  playing = true,
  flipped = false,
  scale,
  rest = 'first',
  className,
  style,
  ...props
}: StripProps) {
  const { w, h, frames, duration, loop } = facts
  const play = frames > 1 && playing ? (loop ? 'loop' : 'once') : undefined
  const vars = {
    '--sheet': `url(${url})`,
    '--w': w,
    '--h': h,
    '--n': frames,
    '--t': `${duration}s`,
    ...(scale ? { '--s': scale } : null),
    ...style,
  } as CSSProperties

  return (
    <span
      aria-hidden="true"
      {...props}
      className={className ? `sprite ${className}` : 'sprite'}
      data-play={play}
      data-flipped={flipped || undefined}
      data-rest={rest === 'last' ? 'last' : undefined}
      style={vars}
    />
  )
}

/**
 * One sprite of the kit. Sprites are decorative: anything they show is also on the page as
 * text.
 *
 * A piece that the seasons replace, Luz in her outfit included, also carries each season's
 * file as --sheet-<season>, and the rules from SceneStyles pick the one for the scene on
 * <html data-scene>. So a change of scene needs no script here and is right from the first
 * paint.
 */
export function Sprite({ sheet, style, ...props }: StripOptions & { sheet: SpriteName }) {
  const seasonal = replaced.includes(sheet) || characterPieces.includes(sheet)
    ? Object.fromEntries(seasonIds.map((id) => [`--sheet-${id}`, `url(${seasonSpriteUrl(id, sheet)})`]))
    : null

  return <Strip url={spriteUrl(sheet)} facts={sprites[sheet]} style={{ ...seasonal, ...style } as CSSProperties} {...props} />
}
