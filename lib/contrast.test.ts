import { describe, expect, it } from 'vitest'
import { colors as c } from './colors'
import { contrast } from './contrast'

// Every text and background pair the site uses. WCAG 2.1 AA asks for 4.5:1 for body text and
// 3:1 for large text (24px, or 18.66px bold) and for interface shapes.
const body: [string, string, string][] = [
  ['navy on blush', c.navy, c.blush],
  ['navy on cream', c.navy, c.cream],
  ['navy on white', c.navy, c.white],
  ['navy on chip', c.navy, c.chip],
  ['navy on petal (active nav, selected stop)', c.navy, c.petal],
  ['cream on navy', c.cream, c.navy],
  ['mist on navy', c.mist, c.navy],
  ['slate on blush', c.slate, c.blush],
  ['slate on cream', c.slate, c.cream],
  ['slate on white', c.slate, c.white],
  ['coral ink on blush', c.coralInk, c.blush],
  ['coral ink on cream', c.coralInk, c.cream],
  ['coral ink on white', c.coralInk, c.white],
  ['white on coral ink (filled chips)', c.white, c.coralInk],
  ['plum on placeholder', c.plum, c.placeholder],
]

const large: [string, string, string][] = [
  ['white on coral (badge numbers, 22px bold and up)', c.white, c.coral],
  ['navy border on cream', c.navy, c.cream],
  ['navy border on blush', c.navy, c.blush],
]

describe('colour contrast', () => {
  it.each(body)('%s meets 4.5:1', (_name, fg, bg) => {
    expect(contrast(fg, bg)).toBeGreaterThanOrEqual(4.5)
  })

  it.each(large)('%s meets 3:1', (_name, fg, bg) => {
    expect(contrast(fg, bg)).toBeGreaterThanOrEqual(3)
  })

  it('shows why the wireframe coral is not used for small text', () => {
    expect(contrast('#FFFFFF', c.coral)).toBeLessThan(4.5)
    expect(contrast('#B84E38', c.blush)).toBeLessThan(4.5)
  })
})
