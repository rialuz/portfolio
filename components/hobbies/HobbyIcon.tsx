import type { HobbyIconName } from '@/content/site'

// Each icon is a 16x16 pixel drawing: [x, y, width, height, colour].
type Pixel = [number, number, number, number, string]

const NAVY = 'var(--color-navy)'
const CREAM = 'var(--color-cream)'
const CORAL = 'var(--color-coral)'
const PETAL = 'var(--color-petal)'
const DASH = 'var(--color-dash)'

const icons: Record<HobbyIconName, Pixel[]> = {
  book: [
    [1, 3, 14, 11, NAVY],
    [2, 4, 5, 9, CREAM],
    [9, 4, 5, 9, CREAM],
    [7, 4, 2, 9, CORAL],
    [3, 6, 3, 1, DASH],
    [3, 8, 3, 1, DASH],
    [3, 10, 2, 1, DASH],
    [10, 6, 3, 1, DASH],
    [10, 8, 3, 1, DASH],
    [10, 10, 2, 1, DASH],
  ],
  // A controller, mirrored left to right: the d-pad's centre is column 4 and the four face
  // buttons sit in a diamond around column 11.
  gamepad: [
    // body, rounded at the top corners
    [3, 4, 10, 1, NAVY],
    [2, 5, 12, 1, NAVY],
    [1, 6, 14, 4, NAVY],
    // grips
    [1, 10, 5, 2, NAVY],
    [10, 10, 5, 2, NAVY],
    [2, 12, 3, 1, NAVY],
    [11, 12, 3, 1, NAVY],
    // d-pad
    [3, 7, 3, 1, CREAM],
    [4, 6, 1, 3, CREAM],
    // face buttons: top, bottom, left, right
    [11, 6, 1, 1, CORAL],
    [11, 8, 1, 1, CORAL],
    [10, 7, 1, 1, PETAL],
    [12, 7, 1, 1, PETAL],
    // start and select
    [7, 9, 1, 1, DASH],
    [8, 9, 1, 1, DASH],
  ],
  robot: [
    [6, 2, 4, 2, CORAL],
    [5, 4, 6, 5, NAVY],
    [6, 5, 1, 1, CREAM],
    [9, 5, 1, 1, CREAM],
    [3, 7, 2, 1, NAVY],
    [2, 8, 1, 4, NAVY],
    [11, 7, 2, 1, NAVY],
    [13, 8, 1, 4, NAVY],
    [4, 9, 2, 1, NAVY],
    [4, 10, 1, 3, NAVY],
    [10, 9, 2, 1, NAVY],
    [11, 10, 1, 3, NAVY],
  ],
}

export function HobbyIcon({ name }: { name: HobbyIconName }) {
  return (
    <svg width="48" height="48" viewBox="0 0 16 16" shapeRendering="crispEdges" aria-hidden="true" className="flex-none">
      {icons[name].map(([x, y, width, height, fill], i) => (
        <rect key={i} x={x} y={y} width={width} height={height} fill={fill} />
      ))}
    </svg>
  )
}
