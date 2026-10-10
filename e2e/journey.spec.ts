import AxeBuilder from '@axe-core/playwright'
import { expect, test, type Page } from '@playwright/test'
import { hydrated } from './hydrated'

// The opening scene follows the calendar. These tests are about other things, so they all
// run on a January day, in candy land, whatever today is.
test.beforeEach(async ({ page }) => {
  await page.clock.setFixedTime(new Date('2026-01-15T12:00:00'))
})

const road = (page: Page) => page.getByRole('group', { name: 'Experience road' })
const stop = (page: Page, name: RegExp) => road(page).getByRole('button', { name })
const panel = (page: Page, id: string) => page.locator(`[data-stop-panel="${id}"]`)
const walker = (page: Page) => page.locator('.road-walker')

/**
 * Open a page and wait until React has hydrated: the nav marks its current section in an
 * effect, and the road, which hydrates after the header, is checked on its own.
 */
async function open(page: Page, path = '/') {
  await page.goto(path)
  await expect(page.locator('header [aria-current="true"]').first()).toBeAttached()
  if ((await road(page).count()) > 0) await hydrated(road(page))
}

test.describe('experience road', () => {
  test('loads on the current role', async ({ page }) => {
    await open(page)
    await expect(stop(page, /Stop 4 of 5: Frontend Team Lead, 2025 to now/)).toHaveAttribute('aria-pressed', 'true')
    await expect(panel(page, 'lead')).toBeVisible()
    await expect(panel(page, 'junior')).toBeHidden()
  })

  test('Right Arrow walks from lead to next and the panel updates', async ({ page }) => {
    await open(page)
    await stop(page, /Stop 4 of 5/).focus()
    await page.keyboard.press('ArrowRight')

    await expect(stop(page, /Stop 5 of 5/)).toHaveAttribute('aria-pressed', 'true')
    await expect(walker(page)).toHaveAttribute('data-phase', 'walk')
    await expect(panel(page, 'next')).toBeVisible({ timeout: 8000 })
    await expect(panel(page, 'lead')).toBeHidden()
    await expect(page.getByRole('status')).toHaveText("Stop 5 of 5: Where I'm headed, Next")
    await expect(page).toHaveURL(/#experience-next$/)
    // Focus stays where the visitor left it.
    await expect(stop(page, /Stop 4 of 5/)).toBeFocused()
  })

  test('Up and Down walk the climbs and drops', async ({ page }) => {
    await open(page)
    await stop(page, /Stop 4 of 5/).focus()
    await page.keyboard.press('ArrowDown')
    await expect(stop(page, /Stop 5 of 5/)).toHaveAttribute('aria-pressed', 'true')
    await expect(panel(page, 'next')).toBeVisible({ timeout: 8000 })
    await page.keyboard.press('ArrowUp')
    await expect(stop(page, /Stop 4 of 5/)).toHaveAttribute('aria-pressed', 'true')
  })

  test('Home and End walk to the first and last stop', async ({ page }) => {
    await open(page)
    await stop(page, /Stop 4 of 5/).focus()
    await page.keyboard.press('End')
    await expect(panel(page, 'next')).toBeVisible({ timeout: 8000 })
    await page.keyboard.press('Home')
    await expect(stop(page, /Stop 1 of 5/)).toHaveAttribute('aria-pressed', 'true')
    await expect(panel(page, 'catalyte')).toBeVisible({ timeout: 15000 })
  })

  test('arrow keys outside the road still scroll the page', async ({ page }) => {
    await open(page)
    // A header link: the hero dialogue's choices use the arrow keys themselves.
    await page.locator('header').getByRole('link', { name: 'Projects' }).first().focus()
    await page.keyboard.press('ArrowDown')
    await page.keyboard.press('ArrowUp')
    await page.keyboard.press('ArrowDown')
    await page.keyboard.press('ArrowRight')
    await expect.poll(() => page.evaluate(() => window.scrollY)).toBeGreaterThan(0)
    await expect(stop(page, /Stop 4 of 5/)).toHaveAttribute('aria-pressed', 'true')
  })

  test('Left and Right walk the road without focusing a stop, once it is on screen', async ({ page }) => {
    await open(page)
    await road(page).scrollIntoViewIfNeeded()
    await expect(road(page).locator(':focus')).toHaveCount(0)

    await page.keyboard.press('ArrowRight')
    await expect(stop(page, /Stop 5 of 5/)).toHaveAttribute('aria-pressed', 'true')
    await page.keyboard.press('ArrowLeft')
    await expect(stop(page, /Stop 4 of 5/)).toHaveAttribute('aria-pressed', 'true')

    // Up and Down belong to page scrolling until the road has focus.
    await page.keyboard.press('ArrowDown')
    await expect(stop(page, /Stop 4 of 5/)).toHaveAttribute('aria-pressed', 'true')
  })

  test('Right Arrow on the last stop is left to the browser', async ({ page }) => {
    await open(page, '/#experience-next')
    await stop(page, /Stop 5 of 5/).focus()
    const prevented = await page.evaluate(
      () =>
        new Promise<boolean>((resolve) => {
          window.addEventListener('keydown', (e) => setTimeout(() => resolve(e.defaultPrevented)), { once: true })
          document.activeElement?.dispatchEvent(new KeyboardEvent('keydown', { key: 'ArrowRight', bubbles: true, cancelable: true }))
        }),
    )
    expect(prevented).toBe(false)
  })

  test('a click on a stop walks there', async ({ page }) => {
    await open(page)
    await stop(page, /Stop 3 of 5/).click()
    await expect(walker(page)).toHaveAttribute('data-phase', 'walk')
    await expect(panel(page, 'junior')).toBeVisible({ timeout: 8000 })
    await expect(walker(page)).toHaveAttribute('data-phase', 'rest')
  })

  test('a new target mid-walk is followed along the road', async ({ page }) => {
    await open(page)
    await stop(page, /Stop 1 of 5/).click()
    await page.waitForTimeout(600)
    await stop(page, /Stop 5 of 5/).click()
    await expect(panel(page, 'next')).toBeVisible({ timeout: 10000 })
    await expect(panel(page, 'catalyte')).toBeHidden()
  })

  test('the URL hash selects a stop on load', async ({ page }) => {
    await open(page, '/#experience-bloomberg')
    await expect(stop(page, /Stop 2 of 5/)).toHaveAttribute('aria-pressed', 'true')
    await expect(panel(page, 'bloomberg')).toBeVisible()
    await expect(walker(page)).toHaveAttribute('data-phase', 'rest')
  })
})

test.describe('reduced motion', () => {
  test.use({ reducedMotion: 'reduce' })

  test('no sprite animates and she changes stop without walking', async ({ page }) => {
    await open(page)
    await expect(page.locator('html')).toHaveAttribute('data-motion', 'off')
    const running = await page.evaluate(() => document.getAnimations().filter((a) => a.playState === 'running').length)
    expect(running).toBe(0)

    await stop(page, /Stop 1 of 5/).click()
    await expect(walker(page)).toHaveAttribute('data-phase', 'rest')
    await expect(panel(page, 'catalyte')).toBeVisible()
  })

  test('the header switch turns motion back on', async ({ page }) => {
    await open(page)
    const toggle = page.getByRole('switch', { name: 'Animation' })
    await expect(toggle).toHaveAttribute('aria-checked', 'false')
    await toggle.click()
    await expect(toggle).toHaveAttribute('aria-checked', 'true')
    await expect(page.locator('html')).toHaveAttribute('data-motion', 'on')
    await stop(page, /Stop 3 of 5/).click()
    await expect(walker(page)).toHaveAttribute('data-phase', 'walk')
  })
})

test.describe('small screens', () => {
  test.use({ viewport: { width: 390, height: 844 } })

  test('the stops are a list and tapping one selects it without walking', async ({ page }) => {
    await open(page)
    await expect(page.locator('.road')).toBeHidden()
    const list = page.getByRole('list', { name: 'Experience road' })
    await list.getByRole('button', { name: /Stop 2 of 5/ }).click()
    await expect(panel(page, 'bloomberg')).toBeVisible()
    const overflow = await page.evaluate(() => document.documentElement.scrollWidth - window.innerWidth)
    expect(overflow).toBeLessThanOrEqual(0)
  })
})

test.describe('projects', () => {
  test('tabs switch between work and personal', async ({ page }) => {
    await open(page)
    await expect(page.getByRole('heading', { level: 3, name: 'TavernScribe' })).toBeVisible()
    await page.getByRole('button', { name: 'Personal' }).click()
    await expect(page.getByRole('heading', { name: 'Pathway' })).toBeVisible()
    await expect(page.getByRole('heading', { level: 3, name: 'TavernScribe' })).toBeHidden()
  })

  test('personal projects page through with the arrows, older apps last', async ({ page }) => {
    await open(page)
    await page.getByRole('button', { name: 'Personal' }).click()
    const previous = page.getByRole('button', { name: 'Previous projects' })
    const next = page.getByRole('button', { name: 'Next projects' })
    await expect(previous).toBeDisabled()
    await expect(page.getByRole('heading', { level: 3, name: 'Pathway' })).toBeVisible()
    await expect(page.getByRole('heading', { level: 3, name: 'Snake Game' })).toBeHidden()

    await next.click()
    await expect(page.getByText('Page 2 of 2')).toBeVisible()
    await expect(page.getByRole('heading', { level: 3, name: 'Snake Game' })).toBeVisible()
    await expect(page.getByRole('heading', { level: 3, name: 'Pathway' })).toBeHidden()
    await expect(next).toBeDisabled()

    await previous.click()
    await expect(page.getByRole('heading', { level: 3, name: 'Pathway' })).toBeVisible()
  })

  test('TavernScribe links to the live product, from the card and the experience panel', async ({ page }) => {
    await open(page)
    const links = page.getByRole('link', { name: 'tavernscribe.com' })
    await expect(links).toHaveCount(2)
    for (const link of await links.all()) {
      await expect(link).toHaveAttribute('href', 'https://tavernscribe.com')
    }
    await expect(page.getByRole('link', { name: /case study/i })).toHaveCount(0)
  })
})

test.describe('accessibility', () => {
  for (const path of ['/']) {
    test(`no axe violations on ${path}`, async ({ page }) => {
      await page.goto(path)
      const results = await new AxeBuilder({ page }).withTags(['wcag2a', 'wcag2aa', 'wcag21a', 'wcag21aa']).analyze()
      expect(results.violations).toEqual([])
    })
  }
})

test.describe('without JavaScript', () => {
  test.use({ javaScriptEnabled: false })

  test('every stop and every project can still be read', async ({ page }) => {
    await page.goto('/')
    for (const id of ['catalyte', 'bloomberg', 'junior', 'lead', 'next']) {
      await expect(panel(page, id)).toBeVisible()
    }
    await expect(page.getByRole('heading', { level: 3, name: 'TavernScribe' })).toBeVisible()
    await expect(page.getByRole('heading', { name: 'Pathway' })).toBeVisible()
  })
})
