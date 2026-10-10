// The palette, mirrored from the @theme block in app/globals.css so the contrast test can
// measure it. Change a colour in both places.

export const colors = {
  navy: '#23304D',
  blush: '#FBE9E5',
  cream: '#FFF7EE',
  white: '#FFFFFF',
  // Decorative coral: shadows, bullets, borders, and large badge numbers only.
  coral: '#C65F4E',
  // Coral for text and for filled chips with white text. The wireframe's #B84E38 measured
  // 4.3:1 on blush, so this is one step darker.
  coralInk: '#A9432F',
  slate: '#4A5470',
  plum: '#6B5560',
  mist: '#E9DCE0',
  chip: '#F6F2F0',
  placeholder: '#FDEDEA',
  petal: '#F7C6C0',
} as const
