import Link from 'next/link'
import type { JourneyStop } from '@/content/journey'
import { ChipList } from '@/components/ui/Chip'

const linkClass =
  'inline-flex min-h-11 items-center self-start text-[15px] font-bold text-coral-ink underline underline-offset-4 hover:text-navy'

function Bullets({ items }: { items: string[] }) {
  return (
    <ul className="flex list-none flex-col gap-2 text-[15px] font-medium tracking-wide">
      {items.map((item) => (
        <li key={item} className="flex gap-2.5">
          <span aria-hidden="true" className="mt-2 size-2 flex-none bg-coral" />
          <span>{item}</span>
        </li>
      ))}
    </ul>
  )
}

/** The panel for one stop. Every stop is rendered; the road collapses all but the selected one. */
export function StopDetail({ stop, collapsed }: { stop: JourneyStop; collapsed: boolean }) {
  const grouped = stop.groups.length > 1

  return (
    <article data-stop-panel={stop.id} data-collapsed={collapsed || undefined} className="flex flex-col gap-4">
      <div className="flex flex-wrap items-start justify-between gap-3">
        <div className="flex flex-col gap-0.5">
          <p className="text-sm font-bold text-coral-ink">{stop.period}</p>
          <h3 className="text-[22px] leading-tight font-bold sm:text-[26px]">{stop.title}</h3>
        </div>
        <ChipList items={stop.chips} highlight={1} label="Skills used" />
      </div>

      {stop.intro && <p className="max-w-[760px] font-medium tracking-wide text-slate">{stop.intro}</p>}

      <div className={grouped ? 'grid gap-x-9 gap-y-6 md:grid-cols-2' : 'max-w-[860px]'}>
        {stop.groups.map((group, i) => (
          <div key={group.heading ?? i} className="flex flex-col gap-2">
            {group.heading && <h4 className="font-pixel text-[17px] font-bold text-coral-ink">{group.heading}</h4>}
            <Bullets items={group.bullets} />
            {group.link &&
              (group.link.href.startsWith('http') ? (
                <a href={group.link.href} className={linkClass}>
                  {group.link.label}
                </a>
              ) : (
                <Link href={group.link.href} className={linkClass}>
                  {group.link.label}
                </Link>
              ))}
          </div>
        ))}
      </div>
    </article>
  )
}
