import AxeBuilder from '@axe-core/playwright'
import { expect, test, type Page } from '@playwright/test'
import { hydrated } from './hydrated'

// The Season menu on the hero: candy land, or a season. Only the pixel art changes. The site
// opens on the calendar's scene for the visitor's date, so every test here fixes the date:
// mid January, which is candy land, unless it says otherwise.

const menu = (page: Page) => page.getByLabel('Season')
const image = (page: Page, selector: string) =>
  page.locator(selector).first().evaluate((el) => getComputedStyle(el).backgroundImage)
const groundColour = (page: Page) =>
  page.evaluate(() => getComputedStyle(document.documentElement).getPropertyValue('--color-ground').trim())

async function open(page: Page) {
  await page.goto('/')
  await hydrated(page.locator('.hero-view'))
}

test.beforeEach(async ({ page }) => {
  await page.clock.setFixedTime(new Date('2026-01-15T12:00:00'))
})

test.describe('the calendar', () => {
  const days = [
    ['2026-02-14', 'valentines'],
    ['2026-04-05', 'easter'],
    ['2026-07-04', 'summer'],
    ['2026-10-31', 'halloween'],
    ['2026-12-25', 'candy'],
  ] as const

  for (const [day, scene] of days) {
    test(`on ${day} the site opens on ${scene}`, async ({ page }) => {
      await page.clock.setFixedTime(new Date(`${day}T12:00:00`))
      await page.goto('/')
      // set by the script in the head, so the art is right on the first paint
      await expect(page.locator('html')).toHaveAttribute('data-scene', scene)
      await hydrated(page.locator('.hero-view'))
      await expect(menu(page)).toHaveValue(scene)
    })
  }

  test('a pick from the menu outlasts the calendar for the session', async ({ page }) => {
    await page.clock.setFixedTime(new Date('2026-10-31T12:00:00'))
    await open(page)
    await expect(menu(page)).toHaveValue('halloween')
    await menu(page).selectOption('summer')
    await page.reload()
    await expect(page.locator('html')).toHaveAttribute('data-scene', 'summer')
  })
})

test.describe('season menu', () => {
  test('a season changes the painting, the road, the ground, the dialogue frame and her outfit, and nothing else', async ({ page }) => {
    await open(page)
    await expect(menu(page)).toHaveValue('candy')
    const candyGround = await groundColour(page)
    expect(await image(page, '.hero-bg')).toContain('/sprites/bg-hero.png')

    await menu(page).selectOption('summer')
    await expect(page.locator('html')).toHaveAttribute('data-scene', 'summer')
    expect(await image(page, '.hero-bg')).toContain('/sprites/seasons/summer/bg-hero.png')
    expect(await image(page, '.road-tile')).toContain('/sprites/seasons/summer/tile-road-')
    expect(await image(page, '.road-flag')).toContain('/sprites/seasons/summer/prop-flag.png')
    expect(await groundColour(page)).not.toBe(candyGround)
    if ((await page.locator('.dialogue').count()) > 0) {
      const frame = await page.locator('.dialogue').evaluate((el) => getComputedStyle(el).borderImageSource)
      expect(frame).toContain('/sprites/seasons/summer/ui-dialogue-frame.png')
    }
    // the season's own pieces are in the scene and on the road
    await expect(page.locator('.hero-scene .scene-piece').first()).toBeAttached()
    await expect(page.locator('.road-critter')).toHaveCount(1)
    // she is in the season's outfit, here and in the dialogue box's portrait
    expect(await image(page, '.hero-luz .sprite')).toContain('/sprites/seasons/summer/luz-')
    if ((await page.locator('.dialogue-portrait').count()) > 0) {
      expect(await image(page, '.dialogue-portrait')).toContain('/sprites/seasons/summer/luz-portrait.png')
    }
    // and so are the site's own colours
    expect(await page.evaluate(() => getComputedStyle(document.body).color)).toBe('rgb(35, 48, 77)')

    await menu(page).selectOption('candy')
    expect(await image(page, '.hero-bg')).toContain('/sprites/bg-hero.png')
    expect(await groundColour(page)).toBe(candyGround)
    await expect(page.locator('.scene-piece')).toHaveCount(0)
    await expect(page.locator('.road-critter')).toHaveCount(0)
  })

  test('the choice lasts through a reload and is there before the page wakes up', async ({ page }) => {
    await open(page)
    await menu(page).selectOption('halloween')
    await page.reload()
    // set by the script in the head, so the art is right on the first paint
    await expect(page.locator('html')).toHaveAttribute('data-scene', 'halloween')
    expect(await image(page, '.hero-bg')).toContain('/sprites/seasons/halloween/bg-hero.png')
    await hydrated(page.locator('.hero-view'))
    await expect(menu(page)).toHaveValue('halloween')
    await expect(page.locator('.hero-scene .scene-piece').first()).toBeAttached()
  })

  test('the menu is one framed control: the focus ring goes round the frame, not the value', async ({ page }) => {
    await open(page)
    await menu(page).focus()
    await page.keyboard.press('Tab')
    await page.keyboard.press('Shift+Tab')
    await expect(menu(page)).toBeFocused()
    expect(await menu(page).evaluate((el) => getComputedStyle(el).outlineStyle)).toBe('none')
    const frame = page.locator('.scene-menu')
    expect(await frame.evaluate((el) => getComputedStyle(el).outlineStyle)).toBe('solid')
  })

  test('with animation off the moving pieces hold still', async ({ page }) => {
    await page.emulateMedia({ reducedMotion: 'reduce' })
    await open(page)
    await menu(page).selectOption('easter')
    const pieces = page.locator('.hero-scene .scene-piece')
    await expect(pieces.first()).toBeAttached()
    for (const piece of await pieces.all()) {
      expect(await piece.evaluate((el) => getComputedStyle(el).animationName)).toBe('none')
    }
  })

  for (const season of ['halloween', 'valentines', 'easter', 'summer']) {
    test(`no axe violations in ${season}`, async ({ page }) => {
      await open(page)
      await menu(page).selectOption(season)
      await expect(page.locator('html')).toHaveAttribute('data-scene', season)
      const results = await new AxeBuilder({ page }).withTags(['wcag2a', 'wcag2aa', 'wcag21a', 'wcag21aa']).analyze()
      expect(results.violations).toEqual([])
    })
  }
})
