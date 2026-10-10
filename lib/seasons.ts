import manifest from '@/public/sprites/seasons/manifest.json'
import type { SpriteName, SpriteSheet } from './sprites'

// Seasonal scenes. A season swaps the pixel art only: the painting behind the hero, the sky
// pieces, the road tiles, the flag, the dialogue box's frame and name plate, a set of props
// and moving pieces, and what Luz is wearing. The site's own colours stay as they are, and so
// does she: only her clothes change.
//
// Each season is a folder, public/sprites/seasons/<id>/, holding its own copy of the pieces
// in `replaced` and `interfacePieces` under the same names and sizes as the candy originals
// in public/sprites/, plus pieces of its own. So switching is a matter of where a sprite is
// read from (seasonSpriteUrl) and three colours: sky and ground, which are --color-sky and
// --color-ground in app/globals.css, and the name plate's centre.
//
// The data is written by pixel-assets/tools/seasons.py; lib/seasons.test.ts checks it against
// the files. lib/scene.ts holds which one the visitor is looking at.

/** A moving piece of a season's hero scene. Positions are in background pixels. */
export interface AmbientPiece {
  sheet: string
  /** Top left of the sprite in the 344x192 painting. */
  x: number
  y: number
  /**
   * Another x for the dialogue hero. Its stage shows only the foot of the painting, so there a
   * drifting piece also comes down to the highest row in view (app/globals.css, "Scenes").
   */
  low?: { x: number }
  /** Where a stride or patrol ends. */
  x2?: number
  /** Which of the scene's two pixel sizes it is drawn at: --bs or --cs. */
  scale: 'bg' | 'character'
  /** `back` sits behind the season's foreground layer (fg-hero), `front` in front of it. */
  layer: 'back' | 'front'
  /**
   * still: stays put. hover: a small loop in place. drift: crosses the sky as the clouds do,
   * in `seconds`, starting from x, which is also where it rests with animation off.
   * stride: crosses the ground from x to x2, `stride` sprite pixels per loop of its strip,
   * which carries the travel within a loop; with animation off it stands at `rest`.
   * patrol: x to x2 and back, a sprite pixel a frame.
   */
  motion: 'still' | 'hover' | 'drift' | 'stride' | 'patrol'
  to?: 'left' | 'right'
  seconds?: number
  /** Seconds to offset a strip or a hover by, so twins do not move in step. */
  delay?: number
  stride?: number
  rest?: number
  flipped?: boolean
}

export interface Season {
  label: string
  /** Top row of the painting: the colour beside it on very wide screens. */
  sky: string
  /** The flat colour of the ground's face, which the dialogue box sits on. */
  ground: string
  /** The dark centre of the season's name plate, painted behind the name. */
  plate: string
  /** True when the folder has fg-hero.png: scenery that clouds and flying things pass behind. */
  foreground: boolean
  /** Where the three clouds rest, in background pixels. */
  clouds: { sheet: SpriteName; x: number; y: number }[]
  /** The season's own pieces: props (prop-*) and moving pieces (fx-*). */
  sprites: Record<string, SpriteSheet>
  ambient: AmbientPiece[]
  /** Pieces that can walk or float along the Experience road. */
  roadWalkers: string[]
}

export type SeasonId = keyof typeof manifest.seasons
/** 'candy' is the site as it is: the pieces in public/sprites/ and lib/sprites.ts. */
export type Environment = 'candy' | SeasonId

export const seasons = manifest.seasons as unknown as Record<SeasonId, Season>
export const seasonIds = Object.keys(manifest.seasons) as SeasonId[]

/** The candy sprites every season has its own copy of. */
export const replaced: readonly string[] = manifest.replaces
/** The dialogue box's frame and name plate, which CSS uses as border images. */
export const interfacePieces: readonly string[] = manifest.interface
/**
 * Luz in the scene's outfit: her strips, stills and portrait. The copies in public/sprites/
 * are her candy-land outfit; each season's folder holds the same pieces in its own.
 */
export const characterPieces: readonly string[] = manifest.character

export function isEnvironment(value: unknown): value is Environment {
  return value === 'candy' || seasonIds.includes(value as SeasonId)
}

/** Where a sprite is read from in an environment: the season's copy if it has one, else the candy original. */
export function seasonSpriteUrl(environment: Environment, name: string): string {
  if (environment !== 'candy') {
    const season = seasons[environment]
    if (
      replaced.includes(name) ||
      interfacePieces.includes(name) ||
      characterPieces.includes(name) ||
      name in season.sprites ||
      (name === 'fg-hero' && season.foreground)
    ) {
      return `/sprites/seasons/${environment}/${name}.png`
    }
  }
  return `/sprites/${name}.png`
}
