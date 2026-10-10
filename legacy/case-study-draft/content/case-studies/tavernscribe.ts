import type { CaseStudy } from './types'

// Still needed from Luz, each one optional so the page simply leaves it out until it is set:
//   timeline    start date, for example 'Mar 2025 to present'
//   heroImage   a session recap on desktop and phone
//   stages[0].image   before and after of the mobile redesign
//   stages[2].image   diagram: browser to S3, upload state in the database
//   stages[3].stats   a Lighthouse or load-time result after the migration
//   learned, whatsNext
// `problem` is the wireframe's draft and needs confirming.

export const tavernscribe: CaseStudy = {
  slug: 'tavernscribe',
  title: 'TavernScribe',
  summary:
    'A subscription product that turns recorded game sessions into AI-generated recaps, newspapers and timelines.',
  labels: ['Work project', 'Gaming', 'Subscription product'],
  role: 'Lead frontend engineer and major backend contributor',
  team: 'LOJI',
  link: { href: 'https://tavernscribe.com', label: 'tavernscribe.com' },
  stack: ['Next.js', 'React', 'TypeScript', 'C# / .NET', 'Stripe', 'AWS S3'],
  stagesIntro: 'Five stages, from the core product to getting found. Jump to any stage.',
  problem:
    'Game groups record long sessions but rarely go back to them. TavernScribe turns those recordings into something the whole party will actually read, and it needed to feel polished enough that people would pay for it.',
  stages: [
    {
      label: 'Core product UI',
      title: 'Core product UI',
      body: 'Built the core interface in Next.js, React and TypeScript, including themes and a full mobile redesign so recaps read well on a phone.',
      tags: ['Next.js', 'Theming', 'Responsive design'],
    },
    {
      label: 'Subscriptions',
      title: 'Subscriptions with Stripe',
      body: 'Built monetization end to end in C#/.NET and React: embedded checkout, a billing portal, signed webhooks, subscriptions, affiliate coupons and promo codes.',
      tags: ['Stripe', '.NET', 'Webhooks'],
      callout: {
        label: 'Key decision',
        text: "Promo codes redeem atomically, so two requests arriving at the same moment can't use the same code twice.",
      },
    },
    {
      label: 'Large uploads',
      title: 'Resumable uploads for long recordings',
      body: 'Session recordings are large, so uploads go straight to S3 and can resume after a dropped connection. Upload state lives in the database, so an upload survives even when requests hit different server instances.',
      tags: ['AWS S3', 'PostgreSQL'],
    },
    {
      label: 'App Router migration',
      title: 'Next.js App Router migration',
      body: 'Led the move to the App Router: the product runs as a single-page app, and the marketing pages are statically generated. I fixed WCAG contrast failures along the way.',
      tags: [],
      stats: [{ value: '1,660 → 442', label: 'lines in the largest page, about 73% smaller' }],
    },
    {
      label: 'Discoverability',
      title: 'Getting found',
      body: "Owned SEO for TavernScribe and LOJI's marketing sites: structured data, sitemaps, per-page keywords, llms.txt files, and Search Console setup and monitoring.",
      tags: ['JSON-LD', 'Sitemaps', 'llms.txt', 'Search Console'],
    },
  ],
}
