import { existsSync, readdirSync, readFileSync } from 'node:fs'
import { join } from 'node:path'
import { describe, expect, it } from 'vitest'
import { characterPieces, interfacePieces, replaced, seasonIds, seasons, seasonSpriteUrl } from './seasons'
import { sprites, type SpriteName } from './sprites'

const root = join(__dirname, '..', 'public')

/** Width and height of a PNG, read from its header. */
function size(path: string): [number, number] {
  const header = readFileSync(path)
  return [header.readUInt32BE(16), header.readUInt32BE(20)]
}

describe('seasonal kits', () => {
  it('has the four seasons', () => {
    expect(seasonIds).toEqual(['halloween', 'valentines', 'easter', 'summer'])
  })

  describe.each(seasonIds)('%s', (id) => {
    const season = seasons[id]
    const folder = join(root, 'sprites', 'seasons', id)

    it('has its own copy of every replaced piece, the size of the candy one', () => {
      for (const name of replaced) {
        const sheet = sprites[name as SpriteName]
        expect(sheet, name).toBeDefined()
        expect(size(join(folder, `${name}.png`)), name).toEqual([sheet.w * sheet.frames, sheet.h])
        expect(size(join(folder, `${name}.png`)), name).toEqual(size(join(root, 'sprites', `${name}.png`)))
      }
    })

    it('has its own dialogue frame and name plate, the size of the candy ones', () => {
      expect(interfacePieces).toEqual(['ui-dialogue-frame', 'ui-nameplate'])
      for (const name of interfacePieces) {
        expect(size(join(folder, `${name}.png`)), name).toEqual(size(join(root, 'sprites', `${name}.png`)))
      }
      expect(season.plate).toMatch(/^#[0-9a-f]{6}$/)
    })

    it('has Luz in its own outfit: every strip, still and the portrait, at the kit sizes', () => {
      expect(characterPieces).toContain('luz-idle')
      expect(characterPieces).toContain('luz-portrait')
      for (const name of characterPieces) {
        const sheet = sprites[name as SpriteName]
        expect(sheet, name).toBeDefined()
        expect(size(join(folder, `${name}.png`)), name).toEqual([sheet.w * sheet.frames, sheet.h])
      }
    })

    it('has every piece it lists, at the size it gives', () => {
      for (const [name, sheet] of Object.entries(season.sprites)) {
        expect(size(join(folder, `${name}.png`)), name).toEqual([sheet.w * sheet.frames, sheet.h])
        expect(sheet.frames > 1 ? sheet.duration > 0 : sheet.duration === 0, name).toBe(true)
      }
    })

    it('has a foreground layer exactly when it says so', () => {
      expect(existsSync(join(folder, 'fg-hero.png'))).toBe(season.foreground)
      if (season.foreground) expect(size(join(folder, 'fg-hero.png'))).toEqual([344, 192])
    })

    it('holds no file the data does not know about', () => {
      const known = new Set([
        ...replaced,
        ...interfacePieces,
        ...characterPieces,
        ...Object.keys(season.sprites),
        ...(season.foreground ? ['fg-hero'] : []),
      ])
      const files = readdirSync(folder).map((file) => file.replace(/\.png$/, ''))
      expect(files.filter((file) => !known.has(file))).toEqual([])
    })

    it('places only pieces that exist', () => {
      const own = Object.keys(season.sprites)
      for (const piece of season.ambient) {
        expect(own, piece.sheet).toContain(piece.sheet)
        if (piece.motion === 'drift') expect(piece.seconds, piece.sheet).toBeGreaterThan(0)
        if (piece.motion === 'stride' || piece.motion === 'patrol') expect(piece.x2, piece.sheet).toBeGreaterThan(piece.x)
      }
      for (const name of season.roadWalkers) expect(own, name).toContain(name)
      expect(season.clouds.map((cloud) => cloud.sheet)).toEqual(['bg-cloud-1', 'bg-cloud-2', 'bg-cloud-3'])
    })

    it('gives its sky and ground as colours', () => {
      expect(season.sky).toMatch(/^#[0-9a-f]{6}$/)
      expect(season.ground).toMatch(/^#[0-9a-f]{6}$/)
    })
  })

  it('reads a sprite from the season when the season has it, else from the candy kit', () => {
    expect(seasonSpriteUrl('candy', 'bg-hero')).toBe('/sprites/bg-hero.png')
    expect(seasonSpriteUrl('summer', 'bg-hero')).toBe('/sprites/seasons/summer/bg-hero.png')
    expect(seasonSpriteUrl('summer', 'fx-crab')).toBe('/sprites/seasons/summer/fx-crab.png')
    expect(seasonSpriteUrl('summer', 'fg-hero')).toBe('/sprites/seasons/summer/fg-hero.png')
    expect(seasonSpriteUrl('easter', 'fg-hero')).toBe('/sprites/fg-hero.png')
    expect(seasonSpriteUrl('halloween', 'luz-idle')).toBe('/sprites/seasons/halloween/luz-idle.png')
    expect(seasonSpriteUrl('candy', 'luz-idle')).toBe('/sprites/luz-idle.png')
    expect(seasonSpriteUrl('halloween', 'luz-celebrate')).toBe('/sprites/luz-celebrate.png')
  })
})
