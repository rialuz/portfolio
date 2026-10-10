import { contact, site } from '@/content/site'

const outline =
  'inline-flex min-h-11 items-center justify-center rounded border-[3px] border-navy bg-cream px-[22px] py-2.5 font-bold text-navy no-underline shadow-pixel-sm hover:bg-petal'

/** Contact and the closing line. On every page, so the header's Contact link always has a target. */
export function Footer() {
  return (
    <footer id="contact" className="bg-blush">
      <div className="mx-auto flex max-w-[1440px] flex-wrap items-center justify-between gap-5 px-5 py-11 lg:px-8">
        <div className="flex flex-col gap-1.5">
          <h2 className="text-[22px] leading-tight font-bold sm:text-[28px]">{contact.heading}</h2>
          <p className="text-[15px] font-medium tracking-wide text-slate sm:text-[17px]">{contact.body}</p>
        </div>
        <div className="flex w-full flex-col gap-3 sm:w-auto sm:flex-row sm:flex-wrap">
          <a
            href={`mailto:${site.email}`}
            className="inline-flex min-h-11 items-center justify-center rounded border-[3px] border-navy bg-navy px-[22px] py-2.5 font-bold text-cream no-underline shadow-pixel-sm hover:bg-slate"
          >
            Email me
          </a>
          <a href={site.github} className={outline}>
            GitHub
          </a>
          <a href={site.linkedin} className={outline}>
            LinkedIn
          </a>
        </div>
      </div>
      <p className="mx-auto max-w-[1440px] px-5 pb-6 text-sm font-medium tracking-wide text-slate lg:px-8">
        © {new Date().getFullYear()} {site.name}. Built with Next.js and a lot of pixels.
      </p>
    </footer>
  )
}
