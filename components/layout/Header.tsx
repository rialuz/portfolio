import Link from 'next/link'
import { site } from '@/content/site'
import { MobileMenu } from './MobileMenu'
import { MotionSwitch } from './MotionSwitch'
import { NavLinks } from './NavLinks'

function PixelHeart() {
  return (
    <svg width="28" height="24" viewBox="0 0 7 6" shapeRendering="crispEdges" aria-hidden="true">
      <path fill="#E07A5F" d="M1 0h2v1H1zM4 0h2v1H4zM0 1h7v2H0zM1 3h5v1H1zM2 4h3v1H2zM3 5h1v1H3z" />
      <path fill="#FFF7EE" d="M1 1h1v1H1z" />
    </svg>
  )
}

export function Header() {
  return (
    <header className="sticky top-0 z-30 border-b-[3px] border-navy bg-cream">
      <div className="relative mx-auto flex max-w-[1440px] items-center justify-between gap-3 px-5 py-3 lg:px-8">
        <Link
          href="/#top"
          aria-label={`${site.shortName}, home`}
          className="flex items-center gap-2.5 font-pixel text-[26px] leading-none font-bold no-underline"
        >
          <PixelHeart />
          {site.shortName}
        </Link>

        <nav aria-label="Main" className="hidden items-center gap-x-2 lg:flex">
          <NavLinks />
          <a
            href={site.resume}
            className="ml-2 inline-flex min-h-11 items-center rounded border-[3px] border-navy bg-cream px-[18px] py-1.5 font-bold no-underline shadow-pixel-sm hover:bg-petal"
          >
            Resume
          </a>
          <MotionSwitch />
        </nav>

        <MobileMenu />
      </div>
    </header>
  )
}
