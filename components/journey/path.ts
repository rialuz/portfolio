// Path model for the Experience road. Pure functions, no React, so they can be unit tested.
//
// The road is one line through the stops. Between two stops on different rows it runs level,
// turns, climbs or drops, turns, and runs level again, so every segment is horizontal or
// vertical and needs exactly one facing. Because it is a single line, the character's position
// is just a distance along it: walking to any stop is moving that one number.

export interface Point {
  x: number
  y: number
}

export type Facing = 'left' | 'right' | 'up' | 'down'

export interface Segment {
  from: Point
  to: Point
  /** Distance from the first stop to the start of this segment, in tiles. */
  start: number
  length: number
  /** Facing when travelling from the first stop towards the last. */
  facing: Facing
}

export interface Path {
  segments: Segment[]
  /** Distance of each stop from the first stop, in tiles. */
  stopDistances: number[]
  length: number
}

/** Tiles per second. At 32px a tile this is 96px per second, matching the 0.8s walk cycle. */
export const WALK_SPEED = 3

const OPPOSITE: Record<Facing, Facing> = { left: 'right', right: 'left', up: 'down', down: 'up' }

function facingBetween(a: Point, b: Point): Facing {
  if (a.y === b.y) return b.x > a.x ? 'right' : 'left'
  return b.y > a.y ? 'down' : 'up'
}

/** The points the road passes through between two neighbouring stops, ending on the second. */
export function legPoints(a: Point, b: Point): Point[] {
  if (a.y === b.y || a.x === b.x) return [b]
  const turn = (a.x + b.x) / 2
  return [{ x: turn, y: a.y }, { x: turn, y: b.y }, b]
}

export function buildPath(stops: Point[]): Path {
  const segments: Segment[] = []
  const stopDistances = [0]
  let distance = 0
  for (let i = 0; i < stops.length - 1; i++) {
    let from = stops[i]
    for (const to of legPoints(stops[i], stops[i + 1])) {
      const length = Math.abs(to.x - from.x) + Math.abs(to.y - from.y)
      segments.push({ from, to, start: distance, length, facing: facingBetween(from, to) })
      distance += length
      from = to
    }
    stopDistances.push(distance)
  }
  return { segments, stopDistances, length: distance }
}

/**
 * The segment at a distance along the road. On a turn, where two segments meet, `direction`
 * picks the one ahead: 1 when heading for the last stop, -1 when heading for the first.
 */
export function segmentAt(path: Path, distance: number, direction: 1 | -1 = 1): Segment {
  const d = Math.min(Math.max(distance, 0), path.length)
  const { segments } = path
  if (direction === 1) {
    return segments.find((s) => d < s.start + s.length) ?? segments[segments.length - 1]
  }
  for (let i = segments.length - 1; i >= 0; i--) {
    if (d > segments[i].start) return segments[i]
  }
  return segments[0]
}

export function positionAt(path: Path, distance: number): Point {
  const d = Math.min(Math.max(distance, 0), path.length)
  const s = segmentAt(path, d)
  const t = s.length === 0 ? 0 : (d - s.start) / s.length
  return { x: s.from.x + (s.to.x - s.from.x) * t, y: s.from.y + (s.to.y - s.from.y) * t }
}

/** Which way the character faces at a distance along the road, given her direction of travel. */
export function facingAt(path: Path, distance: number, direction: 1 | -1): Facing {
  const facing = segmentAt(path, distance, direction).facing
  return direction === 1 ? facing : OPPOSITE[facing]
}

export interface WalkStep {
  facing: Facing
  length: number
}

/** The stretches walked between two stops, in order, each with its facing. */
export function segmentsBetween(path: Path, fromStop: number, toStop: number): WalkStep[] {
  const a = path.stopDistances[fromStop]
  const b = path.stopDistances[toStop]
  const lo = Math.min(a, b)
  const hi = Math.max(a, b)
  const steps = path.segments
    .filter((s) => s.start >= lo && s.start + s.length <= hi)
    .map((s) => ({ facing: s.facing, length: s.length }))
  if (b >= a) return steps
  return steps.reverse().map((s) => ({ facing: OPPOSITE[s.facing], length: s.length }))
}

/** Move a distance towards a target distance for `seconds`, without overshooting. */
export function advance(distance: number, target: number, seconds: number, speed = WALK_SPEED): number {
  const step = speed * seconds
  if (Math.abs(target - distance) <= step) return target
  return distance + Math.sign(target - distance) * step
}

/**
 * The stop a key press walks to, or null when the key does nothing here: an unhandled key, or
 * a move past either end of the road, or Up or Down with no climb or drop to take. The caller lets the browser keep its default action
 * (scrolling) whenever this is null.
 */
export function keyTarget(key: string, target: number, stopCount: number, rows?: number[]): number | null {
  let next: number
  switch (key) {
    // Up and Down walk to a neighbouring stop that is higher or lower on the page. Both
    // neighbours can qualify, so the one further along the road wins.
    case 'ArrowUp':
    case 'ArrowDown': {
      if (!rows) return null
      const wanted = (i: number) =>
        i >= 0 && i < stopCount && (key === 'ArrowUp' ? rows[i] < rows[target] : rows[i] > rows[target])
      if (wanted(target + 1)) next = target + 1
      else if (wanted(target - 1)) next = target - 1
      else return null
      break
    }
    case 'ArrowRight':
      next = target + 1
      break
    case 'ArrowLeft':
      next = target - 1
      break
    case 'Home':
      next = 0
      break
    case 'End':
      next = stopCount - 1
      break
    default:
      return null
  }
  if (next < 0 || next >= stopCount || next === target) return null
  return next
}

export type TileKind = 'straight' | 'corner'

export interface RoadTile {
  col: number
  row: number
  kind: TileKind
  /** Clockwise quarter turns. The straight tile runs left to right; the corner joins left and top. */
  turns: 0 | 1 | 2 | 3
  faded: boolean
}

const near = (a: number, b: number) => Math.abs(a - b) < 1e-6

type Side = 'left' | 'top' | 'right' | 'bottom'

function sideTowards(from: Point, to: Point): Side {
  if (from.y === to.y) return to.x > from.x ? 'right' : 'left'
  return to.y > from.y ? 'bottom' : 'top'
}

// One corner tile covers all four turns by rotating it.
const CORNER_TURNS: Record<string, 0 | 1 | 2 | 3> = {
  'left+top': 0,
  'right+top': 1,
  'bottom+right': 2,
  'bottom+left': 3,
}

/**
 * The tiles that draw the road. It runs in from the left edge to the first stop and out to
 * the right edge after the last one. From the first turn after `fadeFromStop` the tiles are
 * marked faded, which is the stretch leading to the stop after it.
 */
export function roadTiles(stops: Point[], fadeFromStop = stops.length): RoadTile[] {
  const first = stops[0]
  const last = stops[stops.length - 1]
  const points: { p: Point; faded: boolean }[] = [
    { p: { x: Math.floor(first.x) - 0.5, y: first.y }, faded: false },
    { p: first, faded: false },
  ]
  for (let i = 0; i < stops.length - 1; i++) {
    const leg = legPoints(stops[i], stops[i + 1])
    // Everything from the first turn of the leg onwards is faded: `faded` describes the
    // stretch that ends at each point, so the level run up to the turn stays solid.
    leg.forEach((p, n) => points.push({ p, faded: i >= fadeFromStop && n > 0 }))
  }
  const fadedEnd = fadeFromStop < stops.length - 1
  points.push({ p: { x: Math.ceil(last.x) + 0.5, y: last.y }, faded: fadedEnd })

  const tiles: RoadTile[] = []
  for (let i = 1; i < points.length; i++) {
    const a = points[i - 1].p
    const b = points[i].p
    const faded = points[i].faded
    const horizontal = a.y === b.y
    const lo = horizontal ? Math.min(a.x, b.x) : Math.min(a.y, b.y)
    const hi = horizontal ? Math.max(a.x, b.x) : Math.max(a.y, b.y)
    for (let n = Math.ceil(lo - 1e-6); n <= Math.floor(hi + 1e-6); n++) {
      // A whole-number end of a stretch is a turn; the corner tile below covers it.
      if (near(n, lo) || near(n, hi)) continue
      tiles.push(
        horizontal
          ? { col: n, row: a.y, kind: 'straight', turns: 0, faded }
          : { col: a.x, row: n, kind: 'straight', turns: 1, faded },
      )
    }
    const c = points[i + 1]
    if (c && horizontal !== (b.y === c.p.y)) {
      const sides = [sideTowards(b, a), sideTowards(b, c.p)].sort().join('+')
      tiles.push({ col: b.x, row: b.y, kind: 'corner', turns: CORNER_TURNS[sides], faded: c.faded })
    }
  }
  return tiles
}

/** Columns and rows the road occupies. */
export function roadSize(tiles: RoadTile[]): { cols: number; rows: number } {
  return {
    cols: Math.max(...tiles.map((t) => t.col)) + 1,
    rows: Math.max(...tiles.map((t) => t.row)) + 1,
  }
}
