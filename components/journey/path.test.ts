import { describe, expect, it } from 'vitest'
import { fadedStop, journey } from '@/content/journey'
import {
  advance,
  buildPath,
  facingAt,
  keyTarget,
  positionAt,
  roadSize,
  roadTiles,
  segmentsBetween,
  WALK_SPEED,
} from './path'

const stops = journey.map((s) => ({ x: s.tile.col, y: s.tile.row }))
const path = buildPath(stops)
const index = (id: string) => journey.findIndex((s) => s.id === id)

describe('path model', () => {
  it('runs level, turns, climbs or drops, turns, and runs level between stops', () => {
    expect(segmentsBetween(path, index('catalyte'), index('bloomberg'))).toEqual([
      { facing: 'right', length: 1.5 },
      { facing: 'up', length: 3 },
      { facing: 'right', length: 1.5 },
    ])
    expect(segmentsBetween(path, index('bloomberg'), index('junior'))).toEqual([
      { facing: 'right', length: 1.5 },
      { facing: 'down', length: 3 },
      { facing: 'right', length: 1.5 },
    ])
  })

  it('reverses the order and the facings when walking back', () => {
    expect(segmentsBetween(path, index('lead'), index('junior'))).toEqual([
      { facing: 'left', length: 1.5 },
      { facing: 'down', length: 3 },
      { facing: 'left', length: 1.5 },
    ])
  })

  it('gives the stretches between any two stops, each with one facing', () => {
    for (let from = 0; from < stops.length; from++) {
      for (let to = 0; to < stops.length; to++) {
        const steps = segmentsBetween(path, from, to)
        const walked = steps.reduce((sum, s) => sum + s.length, 0)
        expect(walked).toBeCloseTo(Math.abs(path.stopDistances[to] - path.stopDistances[from]))
        expect(steps).toHaveLength(Math.abs(to - from) * 3)
        if (from !== to) {
          const sideways = to > from ? 'right' : 'left'
          expect(steps[0].facing).toBe(sideways)
          expect(steps[steps.length - 1].facing).toBe(sideways)
        }
      }
    }
  })

  it('places each stop at its own distance along the road', () => {
    journey.forEach((stop, i) => {
      const p = positionAt(path, path.stopDistances[i])
      expect(p.x).toBeCloseTo(stop.tile.col)
      expect(p.y).toBeCloseTo(stop.tile.row)
    })
  })

  it('faces the direction of travel, and the stretch ahead on a turn', () => {
    const turn = 1.5 // first turn after the apprentice stop
    expect(facingAt(path, 1, 1)).toBe('right')
    expect(facingAt(path, 1, -1)).toBe('left')
    expect(facingAt(path, turn, 1)).toBe('up')
    expect(facingAt(path, turn, -1)).toBe('left')
    expect(facingAt(path, turn + 1, 1)).toBe('up')
    expect(facingAt(path, turn + 1, -1)).toBe('down')
  })

  it('never leaves the road', () => {
    for (let d = 0; d <= path.length; d += 0.05) {
      const p = positionAt(path, d)
      const onRow = Number.isInteger(p.y)
      const onTurnColumn = Number.isInteger(p.x)
      expect(onRow || onTurnColumn).toBe(true)
    }
  })
})

describe('walking', () => {
  it('moves at a constant speed and stops on the target', () => {
    expect(advance(0, 6, 1)).toBe(WALK_SPEED)
    expect(advance(5, 6, 1)).toBe(6)
    expect(advance(6, 0, 0.5)).toBe(6 - WALK_SPEED / 2)
    expect(advance(2, 2, 1)).toBe(2)
  })

  it('carries on along the road when a new target is chosen mid-walk', () => {
    const lead = path.stopDistances[index('lead')]
    const next = path.stopDistances[index('next')]
    const start = path.stopDistances[index('catalyte')]

    // Far enough towards the next stop to be on the way down, then turn around for the first one.
    let d = advance(lead, next, 0.75)
    expect(d).toBeGreaterThan(lead)
    expect(facingAt(path, d, 1)).toBe('down')

    const before = d
    d = advance(d, start, 0.1)
    expect(d).toBeLessThan(before)
    expect(before - d).toBeCloseTo(WALK_SPEED * 0.1)
    expect(facingAt(path, d, -1)).toBe('up')

    // She walks the whole road back, never cutting across.
    let steps = 0
    while (d !== start && steps < 1000) {
      const p = positionAt(path, d)
      expect(Number.isInteger(p.x) || Number.isInteger(p.y)).toBe(true)
      d = advance(d, start, 1 / 60)
      steps++
    }
    expect(d).toBe(start)
  })
})

describe('keyboard', () => {
  const count = journey.length

  it('walks to the next and previous stop', () => {
    expect(keyTarget('ArrowRight', 2, count)).toBe(3)
    expect(keyTarget('ArrowLeft', 2, count)).toBe(1)
  })

  it('jumps to the first and last stop', () => {
    expect(keyTarget('Home', 3, count)).toBe(0)
    expect(keyTarget('End', 1, count)).toBe(count - 1)
  })

  it('does nothing past either end, so the page can still scroll', () => {
    expect(keyTarget('ArrowLeft', 0, count)).toBeNull()
    expect(keyTarget('ArrowRight', count - 1, count)).toBeNull()
    expect(keyTarget('Home', 0, count)).toBeNull()
    expect(keyTarget('End', count - 1, count)).toBeNull()
  })

  const rows = journey.map((s) => s.tile.row)

  it('walks up a climb and down a drop, preferring the stop further along', () => {
    // Stops alternate low, high, low, high, low.
    expect(keyTarget('ArrowUp', 0, count, rows)).toBe(1)
    expect(keyTarget('ArrowDown', 1, count, rows)).toBe(2)
    expect(keyTarget('ArrowUp', 2, count, rows)).toBe(3)
    expect(keyTarget('ArrowDown', 3, count, rows)).toBe(4)
    // The last stop has no stop ahead, so Up goes back up to the one before.
    expect(keyTarget('ArrowUp', 4, count, rows)).toBe(3)
  })

  it('leaves Up and Down to the page when there is no climb or drop to take', () => {
    expect(keyTarget('ArrowDown', 0, count, rows)).toBeNull()
    expect(keyTarget('ArrowUp', 1, count, rows)).toBeNull()
    expect(keyTarget('ArrowDown', 4, count, rows)).toBeNull()
  })

  it('leaves every other key alone', () => {
    for (const key of ['PageDown', ' ', 'Tab', 'a']) {
      expect(keyTarget(key, 2, count, rows)).toBeNull()
    }
  })

  it('steps from the target, so two quick presses go two stops', () => {
    const first = keyTarget('ArrowLeft', 3, count)!
    expect(keyTarget('ArrowLeft', first, count)).toBe(1)
  })
})

describe('road tiles', () => {
  const tiles = roadTiles(stops, index(fadedStop) - 1)
  const at = (col: number, row: number) => tiles.find((t) => t.col === col && t.row === row)

  it('puts every tile on a whole grid cell, with no doubles', () => {
    const seen = new Set<string>()
    for (const t of tiles) {
      expect(Number.isInteger(t.col) && Number.isInteger(t.row)).toBe(true)
      const key = `${t.col},${t.row}`
      expect(seen.has(key)).toBe(false)
      seen.add(key)
    }
    expect(roadSize(tiles)).toEqual({ cols: 14, rows: 4 })
  })

  it('has two turns between each pair of stops, rotated to join the right sides', () => {
    const corners = tiles.filter((t) => t.kind === 'corner')
    expect(corners).toHaveLength((stops.length - 1) * 2)
    expect(at(2, 3)).toMatchObject({ kind: 'corner', turns: 0 }) // in from the left, out the top
    expect(at(2, 0)).toMatchObject({ kind: 'corner', turns: 2 }) // in from the bottom, out the right
    expect(at(5, 0)).toMatchObject({ kind: 'corner', turns: 3 }) // in from the left, out the bottom
    expect(at(5, 3)).toMatchObject({ kind: 'corner', turns: 1 }) // in from the top, out the right
  })

  it('turns the straight tile on vertical stretches', () => {
    expect(at(1, 3)).toMatchObject({ kind: 'straight', turns: 0 })
    expect(at(2, 1)).toMatchObject({ kind: 'straight', turns: 1 })
    expect(at(2, 2)).toMatchObject({ kind: 'straight', turns: 1 })
  })

  it('fades the stretch leading to the last stop, from its first turn', () => {
    expect(at(10, 0)?.faded).toBe(false)
    for (const [col, row] of [[11, 0], [11, 1], [11, 2], [11, 3], [12, 3], [13, 3]]) {
      expect(at(col, row)?.faded, `tile ${col},${row}`).toBe(true)
    }
    expect(tiles.filter((t) => t.faded)).toHaveLength(6)
  })
})
