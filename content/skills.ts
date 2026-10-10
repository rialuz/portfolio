export interface SkillGroup {
  title: string
  /** The first `highlight` skills are filled in on the card. */
  highlight: number
  skills: string[]
}

export const skillGroups: SkillGroup[] = [
  {
    title: 'Frontend',
    highlight: 2,
    skills: [
      'React',
      'Next.js',
      'Vue',
      'Nuxt 3',
      'TypeScript',
      'JavaScript',
      'HTML',
      'CSS',
      'Tailwind CSS',
      'shadcn/Radix UI',
      'Zustand',
      'Pinia',
      'Vite',
      'Webpack',
    ],
  },
  {
    title: 'Backend & data',
    highlight: 1,
    skills: [
      '.NET / C#',
      'ASP.NET Core',
      'EF Core',
      'REST APIs',
      'SignalR',
      'PostgreSQL',
      'MySQL',
      'SQL',
      'Spring Boot',
      'Node.js',
      'Express',
    ],
  },
  {
    title: 'Quality & access',
    highlight: 1,
    skills: ['WCAG 2.1 AA', 'Playwright', 'Cypress', 'Vitest', 'Jest', 'New Relic'],
  },
  {
    title: 'Tools & integrations',
    highlight: 1,
    skills: ['Stripe', 'Twilio', 'OpenAI', 'Anthropic', 'Docker', 'Git/GitLab', 'CI/CD'],
  },
]
