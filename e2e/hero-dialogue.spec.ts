import { expect, test, type Page } from '@playwright/test'
import { hydrated } from './hydrated'

// The opening scene follows the calendar. These tests are about other things, so they all
// run on a January day, in candy land, whatever today is.
test.beforeEach(async ({ page }) => {
  await page.clock.setFixedTime(new Date('2026-01-15T12:00:00'))
})

// These run only while the page opens on the dialogue: heroStyle in content/site.ts is 'dialogue'.

const lines = (page: Page) => page.locator('.dialogue-page')
const currentLine = (page: Page) => page.locator('.dialogue-page:not([data-hidden])')

async function open(page: Page) {
  await page.goto('/')
  test.skip((await page.locator('.dialogue').count()) === 0, "heroStyle is 'card'")
}

test.describe('hero dialogue', () => {
  test('starts on the headline, with the choices in reach', async ({ page }) => {
    await open(page)
    await hydrated(page.locator('.hero-view'))
    await expect(currentLine(page)).toHaveCount(1)
    await expect(page.getByRole('heading', { level: 1 })).toBeVisible()
    await expect(page.getByRole('link', { name: 'View projects' })).toBeVisible()
    await expect(page.getByRole('link', { name: 'Get in touch' })).toBeVisible()
  })

  test('Space walks through every line, then goes back to scrolling the page', async ({ page }) => {
    await open(page)
    await hydrated(page.locator('.hero-view'))
    const count = await lines(page).count()

    await page.keyboard.press('Space')
    await expect(lines(page).nth(1)).not.toHaveAttribute('data-hidden')
    expect(await page.evaluate(() => window.scrollY)).toBe(0)

    // Each line takes at most two presses: one to finish typing, one to move on.
    for (let i = 0; i < count * 2; i++) {
      await page.keyboard.press('Space')
      await page.waitForTimeout(60)
    }
    await expect(lines(page).last()).not.toHaveAttribute('data-hidden')
    await expect(page.getByRole('button', { name: 'Read that again' })).toBeVisible()

    await page.keyboard.press('Space')
    await expect.poll(() => page.evaluate(() => window.scrollY)).toBeGreaterThan(0)
  })

  test('the choices work with the mouse: tell me more, then read that again', async ({ page }) => {
    await open(page)
    await hydrated(page.locator('.hero-view'))
    const count = await lines(page).count()

    await page.getByRole('button', { name: /Tell me more|Skip ahead/ }).click()
    await expect(lines(page).nth(1)).not.toHaveAttribute('data-hidden')

    for (let i = 0; i < count * 2; i++) {
      const more = page.getByRole('button', { name: /Tell me more|Skip ahead/ })
      if ((await more.count()) === 0) break
      await more.click()
    }
    await page.getByRole('button', { name: 'Read that again' }).click()
    await expect(lines(page).first()).not.toHaveAttribute('data-hidden')
  })
})

test.describe('hero dialogue choices', () => {
  test('the four replies are a list, and one of them is lit at a time', async ({ page }) => {
    await open(page)
    await hydrated(page.locator('.hero-view'))
    const choices = page.getByRole('list', { name: 'Your reply' }).locator('a, button')
    await expect(choices).toHaveCount(4)
    const lit = () =>
      choices.evaluateAll((all) =>
        all.filter((el) => getComputedStyle(el.querySelector('.dialogue-pointer')!).visibility === 'visible').map((el) => el.textContent),
      )

    // Nothing hovered or focused: the reply Space picks.
    await page.mouse.move(5, 5)
    expect(await lit()).toHaveLength(1)
    expect((await lit())[0]).toMatch(/Tell me more|Skip ahead/)

    await page.getByRole('link', { name: 'Get in touch' }).hover()
    expect(await lit()).toEqual(['Get in touch'])
  })

  test('arrow keys move between the replies', async ({ page }) => {
    await open(page)
    await hydrated(page.locator('.hero-view'))
    await page.setViewportSize({ width: 1280, height: 800 })
    await page.mouse.move(5, 5)
    await page.getByRole('button', { name: /Tell me more|Skip ahead/ }).focus()

    await page.keyboard.press('ArrowRight')
    await expect(page.getByRole('link', { name: 'View projects' })).toBeFocused()
    await page.keyboard.press('ArrowDown')
    await expect(page.getByRole('link', { name: 'See my resume' })).toBeFocused()
    await page.keyboard.press('ArrowLeft')
    await expect(page.getByRole('link', { name: 'Get in touch' })).toBeFocused()
    await page.keyboard.press('ArrowUp')
    await expect(page.getByRole('button', { name: /Tell me more|Skip ahead/ })).toBeFocused()
    expect(await page.evaluate(() => window.scrollY)).toBe(0)
  })
})

test.describe('hero dialogue without JavaScript', () => {
  test.use({ javaScriptEnabled: false })

  test('every line can be read at once', async ({ page }) => {
    await open(page)
    const count = await lines(page).count()
    for (let i = 0; i < count; i++) await expect(lines(page).nth(i)).toBeVisible()
    await expect(page.getByRole('link', { name: 'View projects' })).toBeVisible()
  })
})
