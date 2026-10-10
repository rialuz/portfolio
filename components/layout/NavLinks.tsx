'use client'

import Link from 'next/link'
import { usePathname } from 'next/navigation'
import { useEffect, useState } from 'react'
import { nav } from '@/content/site'

/** Section links. On the home page the one for the section in view is marked as current. */
export function NavLinks({ stacked = false, onNavigate }: { stacked?: boolean; onNavigate?: () => void }) {
  const home = usePathname() === '/'
  const [active, setActive] = useState<string>('top')

  useEffect(() => {
    if (!home) return
    const onScroll = () => {
      let current: string = nav[0].id
      for (const { id } of nav) {
        const el = document.getElementById(id)
        if (el && el.getBoundingClientRect().top < 160) current = id
      }
      setActive(current)
    }
    onScroll()
    window.addEventListener('scroll', onScroll, { passive: true })
    return () => window.removeEventListener('scroll', onScroll)
  }, [home])

  return (
    <>
      {nav.map(({ id, label }) => {
        const current = home && active === id
        return (
          <Link
            key={id}
            href={`/#${id}`}
            aria-current={current ? 'true' : undefined}
            onClick={onNavigate}
            className={`inline-flex min-h-11 items-center rounded border-[3px] px-4 py-1.5 no-underline ${
              stacked ? 'w-full' : ''
            } ${current ? 'border-navy bg-petal font-bold shadow-pixel-sm' : 'border-transparent font-medium hover:border-navy'}`}
          >
            {label}
          </Link>
        )
      })}
    </>
  )
}
