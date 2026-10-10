import { hero } from '@/content/site'

/**
 * How the description is cut into dialogue pages. 'sentence' gives short pages that fit the
 * box, like a game; 'paragraph' shows each paragraph of hero.intro whole.
 */
const PAGE_BY: 'sentence' | 'paragraph' = 'sentence'

// A sentence ends at ". " before a capital, so "Next.js," and "C#/.NET," are left alone.
const sentences = (paragraph: string) => paragraph.split(/(?<=[.!?])\s+(?=[A-Z])/)

/** The dialogue, in order. The first page is the headline; the rest is the description. */
export const pages: readonly string[] = [
  hero.headline,
  ...(PAGE_BY === 'sentence' ? hero.intro.flatMap(sentences) : hero.intro),
]
