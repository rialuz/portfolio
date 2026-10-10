import { expect, test, type Page } from '@playwright/test'
import { hydrated } from './hydrated'

// The opening scene follows the calendar. These tests are about other things, so they all
// run on a January day, in candy land, whatever today is.
test.beforeEach(async ({ page }) => {
  await page.clock.setFixedTime(new Date('2026-01-15T12:00:00'))
})

// The switch on the hero: on is the game dialogue, off is the plain text card.

const toggle = (page: Page) => page.getByRole('switch', { name: 'Interactive dialogue' })
const dialogue = (page: Page) => page.locator('.dialogue')

test.describe('hero switch', () => {
  test('swaps the dialogue for the plain card and back, and stays put', async ({ page }) => {
    await page.goto('/')
    await hydrated(page.locator('.hero-view'))
    const startsOn = (await dialogue(page).count()) > 0
    await expect(toggle(page)).toHaveAttribute('aria-checked', String(startsOn))
    const at = await toggle(page).boundingBox()

    await toggle(page).click()
    await expect(toggle(page)).toHaveAttribute('aria-checked', String(!startsOn))
    await expect(dialogue(page)).toHaveCount(startsOn ? 0 : 1)
    await expect(page.getByRole('heading', { level: 1 })).toHaveCount(1)
    await expect(page.getByRole('heading', { level: 1 })).toBeVisible()
    await expect(page.locator('#about')).toBeVisible()
    await expect(page.getByRole('link', { name: 'View projects' })).toBeVisible()
    // It has not moved, so a second click undoes the first.
    expect(await toggle(page).boundingBox()).toEqual(at)

    await toggle(page).click()
    await expect(dialogue(page)).toHaveCount(startsOn ? 1 : 0)
  })

  test('with the dialogue off, every paragraph shows and Space scrolls the page', async ({ page }) => {
    await page.goto('/')
    await hydrated(page.locator('.hero-view'))
    if ((await dialogue(page).count()) > 0) await toggle(page).click()
    await expect(dialogue(page)).toHaveCount(0)
    for (const p of await page.locator('#about p').all()) await expect(p).toBeVisible()

    await page.locator('body').click({ position: { x: 5, y: 300 } })
    await page.keyboard.press('Space')
    await expect.poll(() => page.evaluate(() => window.scrollY)).toBeGreaterThan(0)
  })

  test('the choice lasts through a reload', async ({ page }) => {
    await page.goto('/')
    await hydrated(page.locator('.hero-view'))
    const startsOn = (await dialogue(page).count()) > 0
    await toggle(page).click()
    await expect(dialogue(page)).toHaveCount(startsOn ? 0 : 1)

    await page.reload()
    await hydrated(page.locator('.hero-view'))
    await expect(toggle(page)).toHaveAttribute('aria-checked', String(!startsOn))
    await expect(dialogue(page)).toHaveCount(startsOn ? 0 : 1)
    await expect(page.getByRole('heading', { level: 1 })).toBeVisible()
  })

  // From laptops up the dialogue lies over the scene: the painting is where it is under the
  // text card, with the box across its foot. 1536 by 864 is a size where both heroes are the
  // height of the window, so nothing at all may move.
  test.describe('on a laptop', () => {
    test.use({ viewport: { width: 1536, height: 864 } })

    test('switching heroes does not move the painting, and the dialogue lies over it', async ({ page }) => {
      await page.goto('/')
      await hydrated(page.locator('.hero-view'))
      if ((await dialogue(page).count()) === 0) await toggle(page).click()
      await expect(dialogue(page)).toHaveCount(1)
      const painting = page.locator('.hero-bg').first()
      const under = (await painting.boundingBox())!
      const box = (await dialogue(page).boundingBox())!
      // the whole box is inside the painting
      expect(box.y).toBeGreaterThan(under.y)
      expect(box.y + box.height).toBeLessThan(under.y + under.height)

      // she stands on the scene's ground beside her portrait, clear of the box
      const luz = (await page.locator('.hero-luz .sprite').boundingBox())!
      const portrait = (await page.locator('.dialogue-portrait').boundingBox())!
      await expect(page.locator('.hero-luz')).toBeVisible()
      expect(luz.x + luz.width * (12 / 64)).toBeGreaterThanOrEqual(portrait.x + portrait.width)

      await toggle(page).click()
      await expect(dialogue(page)).toHaveCount(0)
      expect(await painting.boundingBox()).toEqual(under)
    })
  })
})
