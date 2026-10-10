// Sprite manifest: the single source for frame sizes, frame counts and timings.
// Every strip is a horizontal PNG in public/sprites/, played with CSS steps().
// Swapping a strip later means changing one line here.

export interface SpriteSheet {
  /** Width of one frame, in sprite pixels. */
  w: number
  /** Height of one frame, in sprite pixels. */
  h: number
  frames: number
  /** Seconds for one pass over the strip. 0 for stills. */
  duration: number
  loop: boolean
}

const still = (w: number, h: number): SpriteSheet => ({ w, h, frames: 1, duration: 0, loop: false })
const luz = (frames: number, duration: number, loop: boolean): SpriteSheet => ({
  w: 64,
  h: 64,
  frames,
  duration,
  loop,
})
const small = (frames: number, duration: number, loop: boolean): SpriteSheet => ({
  w: 32,
  h: 32,
  frames,
  duration,
  loop,
})

export const sprites = {
  // Character. In every 64x64 frame the feet rest on row 61.
  'luz-base-front': still(64, 64),
  'luz-side-right': still(64, 64),
  'luz-idle': luz(4, 1.7, true),
  'luz-wave': luz(6, 0.9, false),
  'luz-walk': luz(8, 0.8, true),
  'luz-walk-down': luz(8, 0.8, true),
  'luz-walk-up': luz(8, 0.8, true),
  'luz-hop': luz(4, 0.45, false),
  'luz-celebrate': luz(6, 0.7, false),
  'luz-emote-wow': luz(4, 1.7, true),
  'luz-emote-grin': luz(4, 1.7, true),
  'luz-emote-happy': luz(4, 1.7, true),
  'luz-emote-starry': luz(4, 1.7, true),
  'luz-emote-student': luz(4, 1.7, true),
  'luz-emote-cheer': luz(6, 0.9, true),

  // Speech bubbles: pop in once, then hold the last frame.
  'emote-wow': small(4, 0.36, false),
  'emote-grin': small(4, 0.36, false),
  'emote-cheer': small(4, 0.36, false),
  'emote-happy': small(4, 0.36, false),
  'emote-starry': small(4, 0.36, false),

  // Props
  'prop-flag': small(4, 0.7, true),
  'prop-sparkle': small(4, 0.8, true),
  'prop-gumdrop': still(32, 32),
  'prop-lollipop': still(32, 32),
  'prop-candy-cane-sign': still(32, 32),
  'prop-cloud': still(32, 32),

  // Road tiles. The straight tiles run left to right; the corner joins left and top.
  'tile-road-straight': still(32, 32),
  'tile-road-corner': still(32, 32),
  'tile-road-faded': still(32, 32),

  // Hero
  'bg-hero': still(344, 192),
  'bg-cloud-1': still(39, 18),
  'bg-cloud-2': still(67, 31),
  'bg-cloud-3': still(61, 27),

  // Dialogue hero: the detailed portrait and the two small markers. The frame and name plate
  // (ui-dialogue-frame, ui-nameplate) are 9-slice border images, used straight from CSS.
  'luz-portrait': still(128, 168),
  'ui-continue': still(9, 6),
  'ui-pointer': still(7, 9),
} as const satisfies Record<string, SpriteSheet>

export type SpriteName = keyof typeof sprites

export const spriteUrl = (name: SpriteName) => `/sprites/${name}.png`

/** Row of a 64x64 character frame that the feet rest on. */
export const LUZ_FEET_ROW = 61
