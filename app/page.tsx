import { HeroCard } from '@/components/hero/HeroCard'
import { HeroView } from '@/components/hero/HeroView'
import { HeroDialogue } from '@/components/hero-dialogue/HeroDialogue'
import { JourneyRoad } from '@/components/journey/JourneyRoad'
import { ProjectTabs } from '@/components/projects/ProjectTabs'
import { ChipList } from '@/components/ui/Chip'
import { journeyIntro } from '@/content/journey'
import { HobbyIcon } from '@/components/hobbies/HobbyIcon'
import { hobbies } from '@/content/site'
import { skillGroups } from '@/content/skills'

const container = 'mx-auto w-full max-w-[1440px] px-5 lg:px-8'

export default function Home() {
  return (
    <>
      <HeroView
        container={container}
        card={<HeroCard container={container} />}
        dialogue={<HeroDialogue container={container} />}
      />

      <section id="skills" aria-labelledby="skills-heading" className={`${container} flex flex-col gap-5 pt-10 lg:pt-14`}>
        <h2 id="skills-heading" className="text-[26px] leading-tight font-bold lg:text-[34px]">
          Skills
        </h2>
        <div className="grid gap-4 sm:grid-cols-2 lg:gap-5 xl:grid-cols-4">
          {skillGroups.map((group) => (
            <div
              key={group.title}
              className="flex flex-col gap-3 rounded-md border-[3px] border-navy bg-cream p-4 shadow-pixel lg:p-5"
            >
              <h3 className="text-xl font-bold text-coral-ink lg:text-[22px]">{group.title}</h3>
              <ChipList items={group.skills} highlight={group.highlight} size="lg" />
            </div>
          ))}
        </div>
      </section>

      <section id="hobbies" aria-labelledby="hobbies-heading" className={`${container} flex flex-col gap-5 pt-12 lg:pt-14`}>
        <h2 id="hobbies-heading" className="text-[24px] leading-tight font-bold lg:text-3xl">
          {hobbies.heading}
        </h2>
        <ul className="grid list-none gap-4 sm:grid-cols-2 lg:grid-cols-3 lg:gap-5">
          {hobbies.items.map((hobby) => (
            <li key={hobby.text} className="flex items-center gap-4 rounded-md border-[3px] border-navy bg-cream p-4">
              <HobbyIcon name={hobby.icon} />
              <p className="font-medium tracking-wide">{hobby.text}</p>
            </li>
          ))}
        </ul>
      </section>

      <section id="projects" aria-labelledby="projects-heading" className={`${container} pt-12 pb-8 lg:pt-16 lg:pb-10`}>
        <ProjectTabs
          intro={
            <h2 id="projects-heading" className="text-[26px] leading-tight font-bold lg:text-[34px]">
              Projects
            </h2>
          }
        />
      </section>

      <div aria-hidden="true" className="blend blend-blush-to-cream" />
      <section id="experience" aria-labelledby="experience-heading" className="bg-cream pt-8 pb-10 lg:pt-10 lg:pb-12">
        <div className={container}>
          <JourneyRoad
            intro={
              <div className="flex flex-col gap-1.5">
                <h2 id="experience-heading" className="text-[26px] leading-tight font-bold lg:text-[34px]">
                  Experience
                </h2>
                <p className="max-w-[680px] font-medium tracking-wide text-slate">{journeyIntro}</p>
              </div>
            }
          />
        </div>
      </section>
      <div aria-hidden="true" className="blend blend-cream-to-blush" />
    </>
  )
}
