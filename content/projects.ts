export interface WorkProject {
  slug: string
  title: string
  role: string
  summary: string
  /** The first tag is the one the card highlights. */
  tags: string[]
  /** Screenshot in public/, for example '/projects/tavernscribe.png'. Leave out until one is ready. */
  image?: { src: string; alt: string }
  /** The live product, when it is public. */
  link?: { href: string; label: string }
}

export type PersonalStatus = 'built' | 'next' | 'planned'

export interface PersonalProject {
  slug: string
  title: string
  status: PersonalStatus
  summary: string
  tags: string[]
  image?: { src: string; alt: string }
  link?: { href: string; label: string }
}

export const workProjects: WorkProject[] = [
  {
    slug: 'tavernscribe',
    title: 'TavernScribe',
    role: 'Software engineer',
    summary:
      'Built the core product UI, Stripe subscription billing, and resumable uploads for a platform that turns recorded game sessions into AI-generated recaps, newspapers, and timelines.',
    tags: ['Next.js', 'TypeScript', '.NET', 'Stripe'],
    image: {
      src: '/projects/tavernscribe.webp',
      alt: 'The TavernScribe homepage: Stop running your game across twelve tabs.',
    },
    link: { href: 'https://tavernscribe.com', label: 'tavernscribe.com' },
  },
  {
    slug: 'fipp-coaching-logs',
    title: 'FIPP Coaching Logs',
    role: 'Main developer',
    summary:
      'Led development of an accessible, multi-organization platform that replaced manual Excel workflows with centralized coaching, scoring, and reporting tools.',
    tags: ['React', '.NET 10', 'WCAG'],
  },
  {
    slug: 'power-dialer',
    title: 'Call center Power Dialer',
    role: 'Feature lead',
    summary:
      'Led the power dialer for an insurance call center, building Twilio answering-machine detection, voicemail drop, and a softphone window that stays in sync with the app.',
    tags: ['Nuxt 3', 'SignalR', 'Twilio'],
  },
  {
    slug: 'supply-chain-risk',
    title: 'Supply-chain risk tool',
    role: 'Primary frontend developer',
    summary:
      'Built the frontend for a federal SBIR tool that tracks supply-chain risk, including an editable parts inventory table, risk-over-time charts, supplier maps, and a drag-and-drop simulation builder.',
    tags: ['Next.js', 'Mapbox GL', 'ECharts'],
  },
]

// Personal project repositories live on the personal account, not the work one in content/site.ts.
const github = (repo: string) => ({ href: `https://github.com/rialuz/${repo}`, label: 'View on GitHub' })

// In the order shown: what is built first, newest first, then what is coming up.
export const personalProjects: PersonalProject[] = [
  {
    slug: 'little-quest',
    title: 'Little Quest',
    status: 'built',
    summary:
      'A focus timer that turns study sessions into quests. Finished sessions earn XP, and each level unlocks something new for the pixel character you make.',
    tags: ['Next.js', 'TypeScript', '.NET 10', 'EF Core', 'PSQL'],
    image: {
      src: '/projects/little-quest.png',
      alt: 'Little Quest during a focus session: a pixel character reading in a sunset meadow, beside the level bar and the timer',
    },
    link: { href: 'https://little-quest-rho.vercel.app/', label: 'Try it live' },
  },
  {
    slug: 'todo-app',
    title: 'To Do App',
    status: 'built',
    summary:
      'A full-stack to-do list built to learn Node.js and Remult, with role-based access: admins have full CRUD on tasks, and other users can read them and mark them complete.',
    tags: ['Vue.js', 'Node.js', 'Express', 'Remult', 'PSQL'],
    image: { src: '/projects/todo-app.png', alt: 'The To Do App task list' },
    link: github('todo-app'),
  },
  {
    slug: 'medspot',
    title: 'MedSpot',
    status: 'built',
    summary: 'A full-stack patient management system built with React, Java with Spring Boot, PostgreSQL, and JUnit.',
    tags: ['React.js', 'Java', 'Spring Boot', 'JUnit', 'PSQL'],
    image: { src: '/projects/medspot.png', alt: 'The MedSpot patient management screen' },
    link: github('medspot'),
  },
  {
    slug: 'rock-paper-scissors',
    title: 'Rock, Paper, Scissor, SHOOT!',
    status: 'built',
    summary: 'Play a game of Rock, Paper, Scissor against a computer with this cute, aesthetic UI!',
    tags: ['Vue.js', 'JavaScript'],
    image: { src: '/projects/rock-paper-scissors.png', alt: 'The Rock, Paper, Scissor game screen' },
    link: github('rock-paper-scissor'),
  },
  {
    slug: 'snake-game',
    title: 'Snake Game',
    status: 'built',
    summary: 'Have fun eating food and growing your Pacman snake!',
    tags: ['Java', 'JFrame'],
    image: { src: '/projects/snake-game.png', alt: 'The Snake Game board' },
    link: github('snake-game'),
  },
  {
    slug: 'ripple',
    title: 'Ripple',
    status: 'planned',
    summary: 'A planner that compares paying down debt against building savings, side by side.',
    tags: ['FinTech', 'React'],
  },
  // Pathway is parked until there is something to show. Uncomment it to put it back.
  // {
  //   slug: 'pathway',
  //   title: 'Pathway',
  //   status: 'next',
  //   summary: 'A benefits screener that shows which programs someone may qualify for, and why.',
  //   tags: ['CivicTech', 'Next.js', 'Vitest'],
  // },
]

export const statusLabel: Record<PersonalStatus, string> = {
  built: 'Built',
  next: 'Up next',
  planned: 'Planned',
}
