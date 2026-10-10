import { tavernscribe } from './tavernscribe'
import type { CaseStudy } from './types'

// In reading order: each page links on to the next one.
export const caseStudies: CaseStudy[] = [tavernscribe]

export const getCaseStudy = (slug: string) => caseStudies.find((c) => c.slug === slug)

export type { CaseStudy, CaseStudyStage } from './types'
