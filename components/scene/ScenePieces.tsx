import type { CSSProperties } from 'react'
import { Strip } from '@/components/sprite/Sprite'
import { seasons, seasonSpriteUrl, type AmbientPiece, type SeasonId } from '@/lib/seasons'

type Vars = Record<`--${string}`, string | number>

/** Background pixels the sky's travellers cross, as the clouds do: 70 off the left edge to 344. */
const CROSSING = 414

/** The negative delay that starts a crossing at background column x. */
export function crossingDelay(x: number, seconds: number, to: 'left' | 'right' = 'right'): string {
  const along = (x + 70) / CROSSING
  return `${(-(to === 'right' ? along : 1 - along) * seconds).toFixed(2)}s`
}

function Piece({ season, piece }: { season: SeasonId; piece: AmbientPiece }) {
  const facts = seasons[season].sprites[piece.sheet]
  const x = piece.x
  // --px is the piece's column, and --px-low its other column for the short stage the dialogue
  // hero has on phones. app/globals.css picks between them, so no script runs for it.
  const vars: Vars = { '--px': x, '--y': piece.y, '--fh': facts.h }
  if (piece.low) vars['--px-low'] = piece.low.x
  // The hero's two pixel sizes are 4 and 3 at desktop width: step counts are whole at that ratio.
  if (piece.motion === 'drift' && piece.seconds) {
    vars['--d'] = `${piece.seconds}s`
    vars['--at'] = crossingDelay(x, piece.seconds, piece.to)
    if (piece.low) vars['--at-low'] = crossingDelay(piece.low.x, piece.seconds, piece.to)
  } else if (piece.motion === 'hover') {
    vars['--at'] = `${piece.delay ?? 0}s`
  } else if (piece.motion === 'stride' && piece.stride && piece.x2 !== undefined) {
    vars['--stride'] = piece.stride
    vars['--loops'] = Math.ceil(((piece.x2 - x) * 4) / (piece.stride * 3))
    vars['--loop'] = `${facts.duration}s`
    vars['--rest'] = piece.rest ?? x
  } else if (piece.motion === 'patrol' && piece.x2 !== undefined) {
    vars['--steps'] = Math.round(((piece.x2 - x) * 4) / 3)
  }

  return (
    <span className="scene-piece" data-move={piece.motion} data-scale={piece.scale} data-to={piece.to} style={vars as CSSProperties}>
      <Strip
        url={seasonSpriteUrl(season, piece.sheet)}
        facts={facts}
        flipped={piece.flipped}
        style={piece.delay && piece.motion === 'still' ? { animationDelay: `${piece.delay}s` } : undefined}
      />
    </span>
  )
}

/**
 * A season's moving pieces for one layer of the hero scene. They are placed by app/globals.css
 * ("Scenes").
 */
export function ScenePieces({ season, layer }: { season: SeasonId; layer: AmbientPiece['layer'] }) {
  return seasons[season].ambient
    .filter((piece) => piece.layer === layer)
    .map((piece, i) => <Piece key={`${piece.sheet}-${i}`} season={season} piece={piece} />)
}

/** The scenery a season's clouds and flyers pass behind, if it has any. */
export function SceneForeground({ season }: { season: SeasonId }) {
  if (!seasons[season].foreground) return null
  return (
    <Strip
      url={seasonSpriteUrl(season, 'fg-hero')}
      facts={{ w: 344, h: 192, frames: 1, duration: 0, loop: false }}
      className="hero-bg"
    />
  )
}
