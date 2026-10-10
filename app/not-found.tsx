import Link from 'next/link'
import { Sprite } from '@/components/sprite/Sprite'

export default function NotFound() {
  return (
    <div className="mx-auto flex max-w-[1440px] flex-col items-center gap-4 px-5 py-20 text-center">
      <Sprite sheet="luz-emote-wow" scale={2} />
      <h1 className="text-3xl font-bold">This road doesn&apos;t go anywhere.</h1>
      <p className="font-medium tracking-wide text-slate">The page you were looking for isn&apos;t here.</p>
      <Link
        href="/"
        className="inline-flex min-h-11 items-center rounded border-[3px] border-navy bg-navy px-[22px] py-2.5 font-bold text-cream no-underline"
      >
        Back to the start
      </Link>
    </div>
  )
}
