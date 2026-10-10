# portfolio

Pixel-art portfolio built with Next.js (App Router, static export), TypeScript and Tailwind.

Deployed using Vercel here [Luz Portfolio](https://luz-portfolio.vercel.app/)

## Commands

| Command | What it does |
| --- | --- |
| `npm run dev` | Start the site at http://localhost:3000 |
| `npm run build` | Build the static site into `out/` |
| `npm test` | Unit tests: the road's path model, keyboard handling and colour contrast |
| `npm run test:e2e` | Playwright: walking the road, reduced motion, small screens, axe checks |
| `npm run lint` / `npm run type-check` | ESLint and TypeScript |

## Where things live

| Folder | What is in it |
| --- | --- |
| `content/` | All the copy: site details, skills, projects, the Experience stops, case studies |
| `lib/sprites.ts` | Sprite manifest: frame size, frame count and timing for every strip |
| `components/journey/` | The Experience road: path model, walking, the detail panel |
| `components/hero/` | The hero scene |
| `public/sprites/` | The sprite PNGs |
| `pixel-assets/` | Tools and working files the sprites were made with |
