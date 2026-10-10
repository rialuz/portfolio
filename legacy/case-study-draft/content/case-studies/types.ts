export interface CaseStudyImage {
  src: string
  alt: string
}

export interface CaseStudyStage {
  /** Short label for the stage nav. */
  label: string
  title: string
  body: string
  tags: string[]
  image?: CaseStudyImage
  callout?: { label: string; text: string }
  stats?: { value: string; label: string }[]
}

export interface CaseStudy {
  slug: string
  title: string
  summary: string
  /** The first label is highlighted. */
  labels: string[]
  role: string
  team: string
  /** For example 'Mar 2025 to present'. Left out of the page until it is set. */
  timeline?: string
  link?: { href: string; label: string }
  stack: string[]
  heroImage?: CaseStudyImage
  stagesIntro: string
  stages: CaseStudyStage[]
  problem?: string
  learned?: string
  whatsNext?: string
}
