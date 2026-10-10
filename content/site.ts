import type { Environment } from '@/lib/seasons'

export const site = {
  name: 'Luz Lopez Marcano',
  shortName: 'Luz',
  title: 'Luz Lopez Marcano | Full-Stack Software Engineer',
  description:
    'I’m Luz Lopez Marcano, a full-stack software engineer who builds reliable, accessible web applications with React, Next.js, Vue, TypeScript and C#/.NET.',
  url: 'https://luz-portfolio.vercel.app',
  email: 'l.lopezmarcano4@gmail.com',
  // The work account, where most of the contributions show. Personal project repositories
  // live on the personal account (rialuz) and are linked from content/projects.ts.
  github: 'https://github.com/loji-luz',
  linkedin: 'https://www.linkedin.com/in/luzlmarcano/',
  resume: '/Luz-Lopez-Marcano-Resume.pdf',
} as const

export const nav = [
  { id: 'top', label: 'About' },
  { id: 'projects', label: 'Projects' },
  { id: 'experience', label: 'Experience' },
  { id: 'contact', label: 'Contact' },
] as const

/**
 * Which hero the home page opens on. Change this one word to switch:
 * 'card' is the text card over the scene (components/hero/HeroCard.tsx),
 * 'dialogue' is the game-style dialogue box with the portrait (components/hero-dialogue/).
 * Visitors can change to the other with the "Interactive dialogue" switch on the hero.
 */
export type HeroStyle = 'card' | 'dialogue'
export const heroStyle: HeroStyle = 'dialogue'

/**
 * Which pixel scene the site opens on follows the calendar, by the visitor's own date. One
 * entry per month, January first: 'candy', the scene the site was built with, or a season:
 * 'halloween', 'valentines', 'easter' or 'summer' (the folders in public/sprites/seasons).
 * A season changes the pixel art only; the site's colours stay the same.
 * Visitors can change it with the Season menu on the hero; their pick lasts for the session.
 */
export const sceneByMonth: readonly Environment[] = [
  'candy', // January: winter
  'valentines', // February
  'easter', // March: spring
  'easter', // April
  'easter', // May
  'summer', // June
  'summer', // July
  'summer', // August
  'halloween', // September: fall
  'halloween', // October
  'halloween', // November
  'candy', // December: winter
]

/** The scene before the visitor's date is known: what the server sends, and what shows without JavaScript. */
export const scene: Environment = 'candy'

/** The Season menu on the hero: its label, and each scene's name in the order of the year. */
export const sceneMenu: { label: string; options: readonly { scene: Environment; name: string }[] } = {
  label: 'Season',
  options: [
    { scene: 'candy', name: 'Candy Land' },
    { scene: 'valentines', name: 'Valentine’s Day' },
    { scene: 'easter', name: 'Easter Garden' },
    { scene: 'summer', name: 'Summer Beach' },
    { scene: 'halloween', name: 'Halloween Night' },
  ],
}

export const hero = {
  name: 'Luz Lopez Marcano',
  role: 'Full-Stack Software Engineer | React, TypeScript & .NET',
  headline: 'I turn complex workflows into intuitive, reliable software.',
  intro: [
    'I’m a full-stack software engineer who enjoys solving complex problems and building applications that make everyday workflows easier.',
    'Since 2022, I’ve worked across federal government, insurance, and gaming projects, building everything from responsive interfaces to backend APIs, integrations, and data-driven systems. I enjoy understanding the bigger picture behind a product, breaking down requirements, and finding practical solutions that balance usability, performance, and maintainability.',
    'My experience spans React, Next.js, Vue, TypeScript, and C#/.NET, along with mentoring developers, establishing engineering standards, and delivering applications from concept to production. Whether I’m simplifying a complicated user flow, designing a new feature, or debugging an issue deep in the backend, I care about building software that’s thoughtful, accessible, and built to last.',
  ],
  bubble: "Hi, I'm Luz!",
} as const

export type HobbyIconName = 'book' | 'gamepad' | 'robot'

export const hobbies: { heading: string; items: { icon: HobbyIconName; text: string }[] } = {
  heading: "When I'm not coding, I'm...",
  items: [
    { icon: 'book', text: 'Reading historical fiction and fantasy novels' },
    { icon: 'gamepad', text: 'Playing video games' },
    { icon: 'robot', text: 'Building side projects, like setting up a PiCrawler robot' },
  ],
}

export const contact = {
  heading: "Let's build something useful.",
  body: "I'm open to full-stack and frontend roles on teams building tools for people.",
} as const
