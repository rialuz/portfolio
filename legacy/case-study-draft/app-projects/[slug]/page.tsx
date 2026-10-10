import type { Metadata } from 'next'
import Image from 'next/image'
import Link from 'next/link'
import { notFound } from 'next/navigation'
import { Chip, ChipList } from '@/components/ui/Chip'
import { PixelNumber } from '@/components/ui/PixelNumber'
import { caseStudies, getCaseStudy } from '@/content/case-studies'

type Props = { params: Promise<{ slug: string }> }

export const dynamicParams = false

export function generateStaticParams() {
  return caseStudies.map((c) => ({ slug: c.slug }))
}

export async function generateMetadata({ params }: Props): Promise<Metadata> {
  const study = getCaseStudy((await params).slug)
  if (!study) return {}
  return {
    title: `${study.title} case study`,
    description: study.summary,
    alternates: { canonical: `/projects/${study.slug}` },
    openGraph: { title: `${study.title} case study`, description: study.summary, url: `/projects/${study.slug}` },
  }
}

const container = 'mx-auto w-full max-w-[1440px] px-5 lg:px-8'
const backLink =
  'inline-flex min-h-11 items-center rounded border-[3px] border-navy bg-cream px-[18px] py-2.5 font-bold no-underline shadow-pixel-sm hover:bg-petal'
const numberBadge = 'flex size-10 flex-none items-center justify-center rounded font-pixel text-lg font-bold lg:size-[58px] lg:text-2xl'

function Fact({ label, children }: { label: string; children: React.ReactNode }) {
  return (
    <div className="flex flex-col">
      <dt className="text-[13px] font-bold text-coral-ink">{label}</dt>
      <dd>{children}</dd>
    </div>
  )
}

export default async function CaseStudyPage({ params }: Props) {
  const study = getCaseStudy((await params).slug)
  if (!study) notFound()

  const next = caseStudies[caseStudies.findIndex((c) => c.slug === study.slug) + 1]
  const lastStage = study.stages.length - 1

  return (
    <article>
      <div className={`${container} pt-5`}>
        <Link href="/#projects" className={backLink}>
          ← All projects
        </Link>
      </div>

      <header className={`${container} flex flex-wrap items-center gap-10 pt-6 pb-12`}>
        <div className="flex min-w-0 flex-[1_1_460px] flex-col gap-4">
          <ul aria-label="Project type" className="flex list-none flex-wrap gap-1.5">
            {study.labels.map((label, i) => (
              <li key={label} className="flex">
                <Chip tone={i === 0 ? 'solid' : 'soft'} size="md">
                  {label}
                </Chip>
              </li>
            ))}
          </ul>
          <h1 className="text-4xl leading-[1.1] font-bold lg:text-[52px]">{study.title}</h1>
          <p className="text-lg text-slate lg:text-xl">{study.summary}</p>
          <dl className="grid gap-3.5 rounded-md border-[3px] border-navy bg-cream p-[18px] shadow-[5px_5px_0_var(--color-navy)] sm:grid-cols-2">
            <Fact label="My role">{study.role}</Fact>
            <Fact label="Team">{study.team}</Fact>
            {study.timeline && <Fact label="Timeline">{study.timeline}</Fact>}
            {study.link && (
              <Fact label="Links">
                <a href={study.link.href} className="font-bold underline underline-offset-4">
                  {study.link.label}
                </a>
              </Fact>
            )}
          </dl>
          <ChipList items={study.stack} highlight={1} size="md" label="Stack" />
        </div>
        {study.heroImage && (
          <Image
            src={study.heroImage.src}
            alt={study.heroImage.alt}
            width={1120}
            height={760}
            priority
            className="h-auto min-w-0 flex-[1_1_460px] rounded-md border-[3px] border-navy shadow-[6px_6px_0_var(--color-rose)]"
          />
        )}
      </header>

      <section aria-labelledby="stages-heading" className="bg-cream py-12">
        <div className={`${container} flex flex-col gap-6`}>
          <div className="flex flex-col gap-1.5">
            <h2 id="stages-heading" className="text-2xl font-bold lg:text-3xl">
              How the build progressed
            </h2>
            <p className="text-slate">{study.stagesIntro}</p>
          </div>
          <nav aria-label="Project stages">
            <ol className="relative grid list-none grid-cols-2 gap-3 sm:grid-cols-5">
              <li
                aria-hidden="true"
                className="absolute top-[25px] right-[10%] left-[10%] hidden h-2 bg-[repeating-linear-gradient(90deg,var(--color-sand)_0_18px,transparent_18px_28px)] lg:block"
              />
              {study.stages.map((stage, i) => (
                <li key={stage.label} className="relative">
                  <a
                    href={`#stage-${i + 1}`}
                    className="flex min-h-11 items-center gap-2.5 rounded p-1 no-underline sm:flex-col sm:text-center"
                  >
                    <span
                      className={`${numberBadge} border-[3px] border-navy ${
                        i === lastStage ? 'bg-coral text-white shadow-pixel' : 'bg-navy text-cream shadow-bright'
                      }`}
                    >
                      <PixelNumber value={i + 1} />
                    </span>
                    <span className="font-bold">{stage.label}</span>
                  </a>
                </li>
              ))}
            </ol>
          </nav>
        </div>
      </section>

      {study.problem && (
        <section aria-labelledby="problem-heading" className={`${container} flex flex-col gap-3 pt-14 pb-6`}>
          <h2 id="problem-heading" className="text-2xl font-bold lg:text-3xl">
            The problem
          </h2>
          <p className="max-w-[760px]">{study.problem}</p>
        </section>
      )}

      <section aria-label="Stages" className={`${container} pt-6 pb-14`}>
        <ol className="flex list-none flex-col">
          {study.stages.map((stage, i) => (
            <li key={stage.label} id={`stage-${i + 1}`} className="flex gap-3 lg:gap-6">
              <div aria-hidden="true" className="flex flex-none flex-col items-center">
                <span className={`${numberBadge} ${i === lastStage ? 'bg-coral text-white' : 'bg-navy text-cream'}`}>
                  <PixelNumber value={i + 1} />
                </span>
                {i !== lastStage && (
                  <span className="min-h-6 w-2 flex-auto bg-[repeating-linear-gradient(180deg,var(--color-sand)_0_16px,transparent_16px_26px)]" />
                )}
              </div>
              <div className={`flex min-w-0 flex-auto flex-wrap gap-6 ${i !== lastStage ? 'pb-8' : ''}`}>
                <div className="flex min-w-0 flex-[1_1_420px] flex-col gap-3">
                  <h3 className="text-xl font-bold lg:text-2xl">{stage.title}</h3>
                  <p className="max-w-[760px] text-slate">{stage.body}</p>
                  {stage.callout && (
                    <div className="flex max-w-[760px] flex-col gap-1 rounded-md border-[3px] border-navy bg-cream p-4 shadow-[4px_4px_0_var(--color-coral)]">
                      <p className="text-[13px] font-bold text-coral-ink">{stage.callout.label}</p>
                      <p>{stage.callout.text}</p>
                    </div>
                  )}
                  {stage.stats && (
                    <dl className="flex flex-wrap gap-4">
                      {stage.stats.map((stat) => (
                        <div
                          key={stat.label}
                          className="flex flex-[0_1_280px] flex-col-reverse gap-0.5 rounded-md border-[3px] border-navy bg-cream p-4 shadow-pixel"
                        >
                          <dt className="text-[15px]">{stat.label}</dt>
                          <dd className="font-pixel text-[30px] leading-tight font-bold text-coral-ink lg:text-[34px]">
                            {stat.value}
                          </dd>
                        </div>
                      ))}
                    </dl>
                  )}
                  <ChipList items={stage.tags} label="Built with" />
                </div>
                {stage.image && (
                  <Image
                    src={stage.image.src}
                    alt={stage.image.alt}
                    width={720}
                    height={400}
                    className="h-auto min-w-0 flex-[1_1_360px] self-start rounded border-2 border-navy"
                  />
                )}
              </div>
            </li>
          ))}
        </ol>
      </section>

      {(study.learned || study.whatsNext) && (
        <section aria-label="Reflection" className="bg-cream py-12">
          <div className={`${container} flex flex-wrap gap-8`}>
            {study.learned && (
              <div className="flex min-w-0 flex-[1_1_460px] flex-col gap-2.5">
                <h2 className="text-2xl font-bold lg:text-[28px]">What I learned</h2>
                <p>{study.learned}</p>
              </div>
            )}
            {study.whatsNext && (
              <div className="flex min-w-0 flex-[1_1_460px] flex-col gap-2.5">
                <h2 className="text-2xl font-bold lg:text-[28px]">What&apos;s next for {study.title}</h2>
                <p>{study.whatsNext}</p>
              </div>
            )}
          </div>
        </section>
      )}

      <nav aria-label="Case studies" className={`${container} flex flex-wrap justify-between gap-4 pt-10 pb-14`}>
        <Link href="/#projects" className={backLink}>
          ← All projects
        </Link>
        {next && (
          <Link
            href={`/projects/${next.slug}`}
            className="inline-flex min-h-11 items-center rounded border-[3px] border-navy bg-navy px-5 py-2.5 font-bold text-cream no-underline hover:bg-slate"
          >
            Next: {next.title} →
          </Link>
        )}
      </nav>
    </article>
  )
}
