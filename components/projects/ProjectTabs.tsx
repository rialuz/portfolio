'use client'

import Image from 'next/image'
import { useState, type CSSProperties, type ReactNode } from 'react'
import {
  personalProjects,
  statusLabel,
  workProjects,
  type PersonalProject,
  type WorkProject,
} from '@/content/projects'
import { Chip, ChipList } from '@/components/ui/Chip'
import { PixelNumber } from '@/components/ui/PixelNumber'

type Tab = 'work' | 'personal'

const linkClass =
  'inline-flex min-h-11 items-center self-start text-[15px] font-bold text-coral-ink underline underline-offset-4 hover:text-navy'

const badgeBase =
  'flex size-10 flex-none items-center justify-center rounded border-[3px] font-pixel text-lg font-bold lg:size-[58px] lg:text-2xl'

/** A numbered stop with its card: a row with a dashed line down the side on small screens, a column from 1024px. */
function Numbered({ n, last, badge, children }: { n: number; last: boolean; badge: string; children: ReactNode }) {
  return (
    <li className="relative flex gap-3 lg:flex-col lg:items-center lg:gap-3.5">
      <div aria-hidden="true" className="flex flex-none flex-col items-center">
        <span className={`${badgeBase} ${badge}`}>
          <PixelNumber value={n} />
        </span>
        {!last && (
          <span className="w-1.5 flex-auto bg-[repeating-linear-gradient(180deg,var(--color-sand)_0_12px,transparent_12px_20px)] lg:hidden" />
        )}
      </div>
      <div className={`min-w-0 flex-auto lg:w-full ${last ? '' : 'pb-4 lg:pb-0'}`}>{children}</div>
    </li>
  )
}

function WorkCard({ project, featured }: { project: WorkProject; featured: boolean }) {
  return (
    <article
      className={`flex h-full flex-col gap-2.5 rounded-md border-[3px] border-navy p-4 ${
        featured ? 'bg-white shadow-coral' : 'bg-cream shadow-rose'
      }`}
    >
      {project.image && (
        <Image
          src={project.image.src}
          alt={project.image.alt}
          width={640}
          height={400}
          className="aspect-[16/10] h-auto w-full rounded border-2 border-navy object-cover object-top"
        />
      )}
      <h3 className="text-[19px] leading-snug font-bold lg:text-[21px]">{project.title}</h3>
      <p className="text-[13px] font-bold text-coral-ink">{project.role}</p>
      <p className="text-sm font-medium tracking-wide text-slate lg:text-[15px]">{project.summary}</p>
      <ChipList items={project.tags} highlight={1} label="Built with" />
      {project.link && (
        <a href={project.link.href} className={`mt-auto ${linkClass}`}>
          {project.link.label}
        </a>
      )}
    </article>
  )
}

const personalCard: Record<PersonalProject['status'], string> = {
  built: 'border-solid border-navy bg-white shadow-rose',
  next: 'border-solid border-navy bg-cream',
  planned: 'border-dashed border-dash bg-cream',
}

function PersonalCard({ project }: { project: PersonalProject }) {
  const tone = project.status === 'built' ? 'solid' : project.status === 'next' ? 'navy' : 'soft'
  return (
    <article className={`flex h-full flex-col gap-2.5 rounded-md border-[3px] p-4 ${personalCard[project.status]}`}>
      {project.image && (
        <Image
          src={project.image.src}
          alt={project.image.alt}
          width={640}
          height={400}
          className="aspect-[16/10] h-auto w-full rounded border-2 border-navy object-cover object-top"
        />
      )}
      <Chip tone={tone} className="self-start">
        {statusLabel[project.status]}
      </Chip>
      <h3 className="text-[19px] leading-snug font-bold lg:text-[21px]">{project.title}</h3>
      <p className="text-sm font-medium tracking-wide text-slate lg:text-[15px]">{project.summary}</p>
      <ChipList items={project.tags} label="Built with" />
      {project.link && (
        <a href={project.link.href} className={`mt-auto ${linkClass}`}>
          {project.link.label}
          <span className="sr-only">: {project.title}</span>
        </a>
      )}
    </article>
  )
}

const workBadge = (i: number) =>
  i === 0 ? 'border-navy bg-coral text-white shadow-pixel' : 'border-navy bg-navy text-cream shadow-bright'

const personalBadge: Record<PersonalProject['status'], string> = {
  built: 'border-solid border-navy bg-navy text-cream shadow-bright',
  next: 'border-solid border-navy bg-cream text-navy shadow-bright',
  planned: 'border-dashed border-navy bg-cream text-navy',
}

// One column per project from 1024px, so the row is full whether there are three or four.
const listClass = 'relative flex list-none flex-col lg:grid lg:grid-cols-[repeat(var(--n),minmax(0,1fr))] lg:gap-x-5 lg:gap-y-8'
const MAX_COLUMNS = 4
const columns = (n: number) => ({ '--n': Math.min(n, MAX_COLUMNS) }) as CSSProperties

/**
 * Personal projects are shown a page at a time, so the older apps are not all loaded up
 * front. What is coming up and what is already built never share a page.
 */
const PAGE_SIZE = MAX_COLUMNS
const personalPages: { projects: PersonalProject[]; first: number }[] = []
{
  const upcoming = personalProjects.filter((p) => p.status !== 'built')
  const built = personalProjects.filter((p) => p.status === 'built')
  let first = 1
  for (const group of [upcoming, built]) {
    for (let i = 0; i < group.length; i += PAGE_SIZE) {
      const projects = group.slice(i, i + PAGE_SIZE)
      personalPages.push({ projects, first })
      first += projects.length
    }
  }
}

const pagerButton =
  'flex size-11 cursor-pointer items-center justify-center rounded border-[3px] border-navy bg-cream text-navy shadow-pixel-sm hover:bg-petal disabled:cursor-not-allowed disabled:border-dash disabled:bg-chip disabled:text-dash disabled:shadow-none'

/** A pixel chevron pointing left; flipped, it points right. */
function PagerArrow({ flipped = false }: { flipped?: boolean }) {
  return (
    <svg
      width="15"
      height="21"
      viewBox="0 0 5 7"
      shapeRendering="crispEdges"
      aria-hidden="true"
      fill="currentColor"
      className={flipped ? '-scale-x-100' : undefined}
    >
      <path d="M3 0h1v1H3zM2 1h1v1H2zM1 2h1v1H1zM0 3h1v1H0zM1 4h1v1H1zM2 5h1v1H2zM3 6h1v1H3zM4 0h1v1H4zM3 1h1v1H3zM2 2h1v1H2zM1 3h1v1H1zM2 4h1v1H2zM3 5h1v1H3zM4 6h1v1H4z" />
    </svg>
  )
}

function Trail() {
  return (
    <li
      aria-hidden="true"
      className="absolute top-[25px] right-[calc(50%/var(--n))] left-[calc(50%/var(--n))] hidden h-2 bg-[repeating-linear-gradient(90deg,var(--color-sand)_0_18px,transparent_18px_28px)] lg:block"
    />
  )
}

export function ProjectTabs({ intro }: { intro: ReactNode }) {
  const [tab, setTab] = useState<Tab>('work')
  const [page, setPage] = useState(0)

  const tabButton = (value: Tab, label: string) => (
    <button
      type="button"
      aria-pressed={tab === value}
      onClick={() => setTab(value)}
      className={`min-h-11 flex-1 cursor-pointer px-[22px] py-2 text-[15px] font-bold sm:flex-none ${
        tab === value ? 'bg-navy text-cream' : 'bg-cream text-navy hover:bg-petal'
      }`}
    >
      {label}
    </button>
  )

  return (
    <div className="flex flex-col gap-7">
      <div className="flex flex-wrap items-end justify-between gap-4">
        {intro}
        <div
          role="group"
          aria-label="Project type"
          className="js-only flex w-full overflow-hidden rounded-md border-[3px] border-navy shadow-pixel sm:w-auto"
        >
          {tabButton('work', 'Work')}
          {tabButton('personal', 'Personal')}
        </div>
      </div>

      <section aria-label="Work projects" data-collapsed={tab !== 'work' || undefined}>
        <ol className={listClass} style={columns(workProjects.length)}>
          {workProjects.length <= MAX_COLUMNS && <Trail />}
          {workProjects.map((project, i) => (
            <Numbered key={project.slug} n={i + 1} last={i === workProjects.length - 1} badge={workBadge(i)}>
              <WorkCard project={project} featured={i === 0} />
            </Numbered>
          ))}
        </ol>
      </section>

      <section aria-label="Personal projects" data-collapsed={tab !== 'personal' || undefined} className="flex flex-col gap-6">
        {/* One list per page. Without JavaScript nothing is collapsed, so every page shows. */}
        {personalPages.map(({ projects, first }, p) => (
          <ol
            key={p}
            start={first}
            className={listClass}
            style={columns(projects.length)}
            data-collapsed={p !== page || undefined}
          >
            <Trail />
            {projects.map((project, i) => (
              <Numbered
                key={project.slug}
                n={first + i}
                last={i === projects.length - 1}
                badge={personalBadge[project.status]}
              >
                <PersonalCard project={project} />
              </Numbered>
            ))}
          </ol>
        ))}

        {personalPages.length > 1 && (
          <nav aria-label="Personal project pages" className="js-only flex items-center justify-center gap-4">
            <button
              type="button"
              aria-label="Previous projects"
              disabled={page === 0}
              onClick={() => setPage(page - 1)}
              className={pagerButton}
            >
              <PagerArrow />
            </button>
            <p aria-live="polite" className="min-w-24 text-center text-sm font-bold">
              Page {page + 1} of {personalPages.length}
            </p>
            <button
              type="button"
              aria-label="Next projects"
              disabled={page === personalPages.length - 1}
              onClick={() => setPage(page + 1)}
              className={pagerButton}
            >
              <PagerArrow flipped />
            </button>
          </nav>
        )}
      </section>
    </div>
  )
}
