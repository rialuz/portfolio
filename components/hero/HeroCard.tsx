import Link from 'next/link'
import { HeroScene } from '@/components/hero/HeroScene'
import { hero } from '@/content/site'

/**
 * The hero as a text card over the scene: the plain version, shown when the visitor turns the
 * dialogue off, or first if heroStyle in content/site.ts is 'card'.
 */
export function HeroCard({ container }: { container: string }) {
  return (
    <section id="top" aria-labelledby="hero-heading" className="hero">
      <HeroScene />
      {/* The card starts under the hero's controls, until the window is wide enough to pass beside them. */}
      <div className={`hero-content ${container} pt-[68px] 2xl:pt-6`}>
        <div
          id="about"
          className="flex flex-col gap-3.5 rounded-md border-[3px] border-navy bg-cream p-[18px] shadow-pixel-lg lg:max-w-[680px] lg:p-[30px] xl:max-w-[800px]"
        >
          <div className="flex flex-col gap-0.5">
            <p className="text-lg font-bold">{hero.name}</p>
            <p className="text-[15px] font-bold text-coral-ink lg:text-base">{hero.role}</p>
          </div>
          <h1 id="hero-heading" className="text-[26px] leading-[1.2] font-bold tracking-[-0.3px] lg:text-4xl lg:leading-[1.15]">
            {hero.headline}
          </h1>
          {hero.intro.map((paragraph) => (
            <p key={paragraph} className="text-[15px] font-medium tracking-wide text-slate lg:text-base">
              {paragraph}
            </p>
          ))}
          <div className="flex flex-wrap gap-3 pt-1">
            <Link
              href="/#projects"
              className="inline-flex min-h-11 flex-1 items-center justify-center rounded border-[3px] border-navy bg-navy px-3 py-2.5 font-bold whitespace-nowrap text-cream no-underline hover:bg-slate sm:flex-none sm:px-[22px]"
            >
              View projects
            </Link>
            <Link
              href="/#contact"
              className="inline-flex min-h-11 flex-1 items-center justify-center rounded border-[3px] border-navy bg-cream px-3 py-2.5 font-bold whitespace-nowrap text-navy no-underline hover:bg-petal sm:flex-none sm:px-[22px]"
            >
              Get in touch
            </Link>
          </div>
        </div>
      </div>
    </section>
  )
}
