import type { SpriteName } from '@/lib/sprites'

export type StopId = 'catalyte' | 'bloomberg' | 'junior' | 'lead' | 'next'
export type StopKind = 'done' | 'current' | 'future'

export interface StopGroup {
  heading?: string
  bullets: string[]
  link?: { href: string; label: string }
}

export interface JourneyStop {
  id: StopId
  /** Short label under the stop on the road. */
  label: string
  /** Short date under the label. */
  when: string
  kind: StopKind
  /**
   * Position on the road grid, in 32px tiles. Whole numbers are tile centres, so a stop at
   * x.5 sits on the seam between two tiles and the corner between two stops lands on a tile.
   */
  tile: { col: number; row: number }
  /** Strip the character loops while she rests at this stop. */
  emote: SpriteName
  /** Speech bubble that pops in when she arrives. */
  bubble: SpriteName
  /** Heading and date line of the detail panel. */
  title: string
  period: string
  /** One line for the mobile list. */
  summary?: string
  chips: string[]
  intro?: string
  groups: StopGroup[]
}

export const journeyIntro =
  'My path from apprentice in 2022 to where I am now. Pick a stop on the road to see what I built there.'

/** The page loads on this stop. */
export const initialStop: StopId = 'lead'

/** The road is drawn faded from the last turn before this stop onwards. */
export const fadedStop: StopId = 'next'

const HIGH = 0
const LOW = 3

export const journey: JourneyStop[] = [
  {
    id: 'catalyte',
    label: 'Apprentice',
    when: 'Sep 2022',
    kind: 'done',
    tile: { col: 0.5, row: LOW },
    emote: 'luz-emote-student',
    bubble: 'emote-wow',
    title: 'Software Engineering Apprenticeship, Catalyte',
    period: 'Sep 2022',
    chips: ['React', 'Java', 'Spring Boot', 'PostgreSQL', 'Jest', 'JUnit'],
    groups: [
      {
        bullets: [
          'Built a full-stack e-commerce application with an agile scrum team of eight, using React, Java with Spring Boot and Spring Security, and Jest.',
          'Independently designed and built a full-stack management system using React, Java with Spring Boot, PostgreSQL, Jest, and JUnit.',
          'Selected for an interview video about my path into software development, published on the company site.',
        ],
      },
    ],
  },
  {
    id: 'bloomberg',
    label: 'Software Engineer',
    when: '2023 to 2024',
    kind: 'done',
    tile: { col: 3.5, row: HIGH },
    emote: 'luz-emote-grin',
    bubble: 'emote-grin',
    title: 'Software Engineer, Bloomberg Industry Group',
    period: 'Jan 2023 to Feb 2024',
    summary: 'Moved two repositories to a micro-frontend architecture.',
    chips: ['single-spa', 'Micro-frontends', 'Feature flags'],
    groups: [
      {
        bullets: [
          'Led the migration and deployment of two repositories to a single-spa micro-frontend architecture, improving site performance and maintainability.',
          'Shipped front-end features behind feature toggles for phased rollouts, working with QA, the tech lead, and product management to release on deadline.',
        ],
      },
    ],
  },
  {
    id: 'junior',
    label: 'Junior Frontend Dev',
    when: '2024',
    kind: 'done',
    tile: { col: 6.5, row: LOW },
    emote: 'luz-emote-cheer',
    bubble: 'emote-cheer',
    title: 'Junior Frontend Developer, LOJI',
    period: 'Aug 2024 to Jan 2025',
    summary: 'Primary frontend developer on a federal supply-chain risk tool.',
    chips: ['Next.js', 'TypeScript', 'Mapbox GL', 'ECharts'],
    groups: [
      {
        bullets: [
          'Primary frontend developer on a federal SBIR supply-chain risk tool: built the parts inventory table (editable columns, saved filters, server-side pagination), risk-over-time charts, and supplier maps (Next.js, TypeScript, Mapbox GL, ECharts).',
          'Built a multi-step simulation builder with a drag-and-drop node editor on a Mapbox map and animated timeline playback.',
        ],
      },
    ],
  },
  {
    id: 'lead',
    label: 'Frontend Team Lead',
    when: '2025 to now',
    kind: 'current',
    tile: { col: 9.5, row: HIGH },
    emote: 'luz-emote-happy',
    bubble: 'emote-happy',
    title: 'Frontend Team Lead, LOJI',
    period: 'Jan 2025 to present',
    summary: 'Lead two junior developers and build full-stack features across three products.',
    chips: ['Mentoring', 'Next.js', '.NET', 'Nuxt 3', 'Stripe', 'Twilio', 'WCAG'],
    groups: [
      {
        heading: 'Leading the team',
        bullets: [
          'Manage and mentor 2 junior developers; introduced code standards, a PR template, and QA practices that made code reviews and releases more consistent.',
          'Work with clients to turn business requirements into technical solutions, present new features, and write the user guides that go with them.',
          'Owned SEO and discoverability across TavernScribe and LOJI’s product marketing sites: JSON-LD structured data, sitemaps, per-page keywords, llms.txt files, and Google Search Console setup and monitoring.',
        ],
      },
      {
        heading: 'TavernScribe',
        bullets: [
          'Work across the stack on a subscription product that turns recorded game sessions into AI-generated recaps, newspapers, and timelines: built the core UI in Next.js, React, and TypeScript, with themes and a mobile redesign, and contributed heavily to the C#/.NET backend.',
          'Built Stripe monetization end to end in C#/.NET and React: embedded checkout, billing portal, signed webhooks, subscriptions, affiliate coupons, and promo codes with atomic redemption.',
          'Built resumable direct-to-S3 uploads for large session recordings, storing upload state in the database so uploads survive across multiple server instances.',
          'Led a Next.js App Router migration (single-page app for the product, static generation for marketing), cut the largest page from 1,660 to 442 lines, and fixed WCAG contrast failures.',
        ],
        link: { href: 'https://tavernscribe.com', label: 'tavernscribe.com' },
      },
      {
        heading: 'Insurance Call Center Platform',
        bullets: [
          'Led the Power Dialer: Twilio answering-machine detection, voicemail drop, conference bridging, and a standalone softphone window synced to the app (Nuxt 3, Vue, SignalR, .NET).',
          'Built carrier quoting and underwriting integrations and workflow handlers for automated client journeys; tracked down a call-outcome race condition and fixed it with atomic database updates.',
        ],
      },
      {
        heading: 'FIPP Coaching Logs',
        bullets: [
          'Main developer on a multi-organization React and .NET 10 web app that replaced the client’s Excel coaching workbooks; ported their fidelity-scoring logic to a backend engine and shipped it to production.',
          'Brought a slow, manual workflow into one app where teams create workbooks, assign them to coaches, log data, audit entries, and manage their users and organizations.',
          'Led WCAG 2.1 AA accessibility compliance for the app, including screen reader and zoom support; built multi-org roles, license enforcement, and a cross-tab idle timeout.',
        ],
      },
    ],
  },
  {
    id: 'next',
    label: "Where I'm headed",
    when: 'Next',
    kind: 'future',
    tile: { col: 12.5, row: LOW },
    emote: 'luz-emote-starry',
    bubble: 'emote-starry',
    title: 'Product teams building tools that help people',
    period: 'Next stop',
    chips: [],
    intro:
      'I want to bring what I’ve learned shipping accessible apps and building payments, data, and real-time features across the stack to a team whose product makes everyday systems easier to use.',
    groups: [],
  },
]

/** The name a screen reader hears for a stop, and the line announced on arrival. */
export function stopName(index: number): string {
  const stop = journey[index]
  return `Stop ${index + 1} of ${journey.length}: ${stop.label}, ${stop.when}`
}
