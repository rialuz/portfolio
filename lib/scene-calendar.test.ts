import { describe, expect, it } from 'vitest'
import { scene, sceneByMonth, sceneMenu } from '@/content/site'
import { sceneOn } from './scene-calendar'
import { isEnvironment, seasonIds } from './seasons'

describe('the scene calendar', () => {
  it('has a scene for every month', () => {
    expect(sceneByMonth).toHaveLength(12)
    expect(sceneByMonth.every(isEnvironment)).toBe(true)
    expect(isEnvironment(scene)).toBe(true)
  })

  it.each([
    ['2026-01-15', 'candy'],
    ['2026-02-01', 'valentines'],
    ['2026-02-28', 'valentines'],
    ['2026-03-01', 'easter'],
    ['2026-05-31', 'easter'],
    ['2026-06-01', 'summer'],
    ['2026-08-31', 'summer'],
    ['2026-09-01', 'halloween'],
    ['2026-10-09', 'halloween'],
    ['2026-11-30', 'halloween'],
    ['2026-12-01', 'candy'],
    ['2026-12-25', 'candy'],
  ])('on %s the site opens on %s', (day, expected) => {
    // noon, local time: the visitor's own date decides, wherever they are
    expect(sceneOn(new Date(`${day}T12:00:00`))).toBe(expected)
  })
})

describe('the Season menu', () => {
  it('names every scene once', () => {
    expect(sceneMenu.options.map((option) => option.scene).sort()).toEqual(['candy', ...seasonIds].sort())
    expect(sceneMenu.options.every((option) => option.name.trim().length > 0)).toBe(true)
    expect(sceneMenu.label.trim().length).toBeGreaterThan(0)
  })

  it('lists the scenes in the order of the year, as the calendar meets them', () => {
    const met = sceneByMonth.filter((id, month) => sceneByMonth.indexOf(id) === month)
    expect(sceneMenu.options.map((option) => option.scene)).toEqual(met)
  })
})
