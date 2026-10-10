import { expect, type Locator } from '@playwright/test'

/**
 * Waits until React has hydrated this element, so a click or key press meant for it is not
 * lost. The header and the page hydrate separately, so the header being ready says nothing
 * about the page. React puts a __reactProps key on each DOM node it has taken over.
 */
export async function hydrated(target: Locator) {
  await expect
    .poll(() => target.first().evaluate((el) => Object.keys(el).some((key) => key.startsWith('__reactProps'))))
    .toBe(true)
}
