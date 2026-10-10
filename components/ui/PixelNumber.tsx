// Numbers for the badges, drawn on a 5x7 pixel grid rather than set in the pixel font, whose
// 2 and 5 were hard to tell apart at badge size. Drawn as SVG so every pixel has a crisp edge
// at any scale.

const DIGITS: Record<string, string[]> = {
  '0': ['.###.', '#...#', '#..##', '#.#.#', '##..#', '#...#', '.###.'],
  '1': ['..#..', '.##..', '..#..', '..#..', '..#..', '..#..', '.###.'],
  '2': ['.###.', '#...#', '....#', '...#.', '..#..', '.#...', '#####'],
  '3': ['####.', '....#', '....#', '.###.', '....#', '....#', '####.'],
  '4': ['...#.', '..##.', '.#.#.', '#..#.', '#####', '...#.', '...#.'],
  '5': ['#####', '#....', '####.', '....#', '....#', '#...#', '.###.'],
  '6': ['.###.', '#....', '#....', '####.', '#...#', '#...#', '.###.'],
  '7': ['#####', '....#', '...#.', '..#..', '..#..', '..#..', '..#..'],
  '8': ['.###.', '#...#', '#...#', '.###.', '#...#', '#...#', '.###.'],
  '9': ['.###.', '#...#', '#...#', '.####', '....#', '....#', '.###.'],
}

const WIDTH = 5
const HEIGHT = 7
const GAP = 1

/**
 * A number in pixel digits, in the current text colour. Decorative: whatever it sits in
 * carries the number as text or in its label. Size it with a height class that is a
 * multiple of 7px, so each pixel is a whole number of screen pixels.
 */
export function PixelNumber({ value, className = 'h-[21px] lg:h-7' }: { value: number; className?: string }) {
  const digits = String(value).split('')
  const width = digits.length * WIDTH + (digits.length - 1) * GAP

  return (
    <svg
      viewBox={`0 0 ${width} ${HEIGHT}`}
      shapeRendering="crispEdges"
      aria-hidden="true"
      fill="currentColor"
      className={`w-auto flex-none ${className}`}
      style={{ aspectRatio: `${width} / ${HEIGHT}` }}
    >
      {digits.flatMap((digit, d) =>
        DIGITS[digit].flatMap((row, y) =>
          row.split('').map((cell, x) =>
            cell === '#' ? <rect key={`${d}-${x}-${y}`} x={d * (WIDTH + GAP) + x} y={y} width="1" height="1" /> : null,
          ),
        ),
      )}
    </svg>
  )
}
