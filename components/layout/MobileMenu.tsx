'use client'

import { useRef } from 'react'
import { site } from '@/content/site'
import { MotionSwitch } from './MotionSwitch'
import { NavLinks } from './NavLinks'

/** The small-screen menu. A details element, so it opens without JavaScript too. */
export function MobileMenu() {
  const ref = useRef<HTMLDetailsElement>(null)
  const close = () => ref.current?.removeAttribute('open')

  return (
    <details ref={ref} className="lg:hidden">
      <summary
        aria-label="Menu"
        className="flex size-11 cursor-pointer list-none flex-col items-center justify-center gap-1 rounded border-[3px] border-navy bg-cream shadow-pixel-sm"
      >
        <span className="block h-0.5 w-[18px] bg-navy" />
        <span className="block h-0.5 w-[18px] bg-navy" />
        <span className="block h-0.5 w-[18px] bg-navy" />
      </summary>
      <nav
        aria-label="Main"
        className="absolute inset-x-0 top-full flex flex-col gap-1 border-b-[3px] border-navy bg-cream px-5 py-4"
      >
        <NavLinks stacked onNavigate={close} />
        <a
          href={site.resume}
          className="mt-1 inline-flex min-h-11 items-center justify-center rounded border-[3px] border-navy bg-cream px-4 font-bold no-underline shadow-pixel-sm"
        >
          Resume
        </a>
        <MotionSwitch />
      </nav>
    </details>
  )
}
