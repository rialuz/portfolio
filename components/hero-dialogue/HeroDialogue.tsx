'use client'

import Link from 'next/link'
import type { CSSProperties, KeyboardEvent, MouseEvent, ReactNode } from 'react'
import { HeroScene } from '@/components/hero/HeroScene'
import { Sprite } from '@/components/sprite/Sprite'
import { hero, site } from '@/content/site'
import { sprites } from '@/lib/sprites'
import { pages } from './pages'
import { useDialogue } from './useDialogue'

const portrait = sprites['luz-portrait']

/** One choice: a framed button, as in a game's list of replies. */
const choiceClass =
  'dialogue-choice flex min-h-11 w-full cursor-pointer items-center gap-2.5 rounded border-[3px] border-navy bg-white px-3 py-1.5 text-left font-pixel text-[15px] font-bold text-navy no-underline shadow-pixel-sm lg:text-[17px]'

function ChoiceLabel({ children, hint }: { children: ReactNode; hint?: string }) {
  return (
    <>
      <Sprite sheet="ui-pointer" className="dialogue-pointer" />
      <span className="flex-auto">{children}</span>
      {hint && <kbd className="rounded border-2 border-navy bg-white px-1.5 font-sans text-xs font-bold">{hint}</kbd>}
    </>
  )
}

/**
 * The hero as a game dialogue: the scene, and over its foot a candy-framed box where Luz says
 * the description a page at a time, her portrait beside it. From laptops up the scene is the
 * whole hero, as it is under the text card, so switching between the two moves nothing in the
 * painting; on phones there is no room for that and the box follows a strip of the scene.
 * Shown while the hero's
 * "Interactive dialogue" switch is on, which is how the page opens if heroStyle in
 * content/site.ts is 'dialogue'. The styles are the "Hero, dialogue version" block in
 * app/globals.css.
 *
 * Every page is in the HTML, so it reads whole without JavaScript and to screen readers:
 * the typed-out letters are decoration over a hidden copy of the full text.
 */
export function HeroDialogue({ container }: { container: string }) {
  const { page, typed, typing, last, boxRef, advance, restart } = useDialogue(pages)

  // A click anywhere on the box continues, except on a choice, which does its own thing.
  const onBoxClick = (event: MouseEvent) => {
    if (!(event.target as Element).closest('a, button')) advance()
  }

  // Arrow keys move between the choices, as they would in a game menu. The grid is two
  // columns wide from tablets up and one column on phones.
  const onChoiceKey = (event: KeyboardEvent<HTMLUListElement>) => {
    if (!['ArrowLeft', 'ArrowRight', 'ArrowUp', 'ArrowDown'].includes(event.key)) return
    const choices = [...event.currentTarget.querySelectorAll<HTMLElement>('a, button')]
    const at = choices.indexOf(document.activeElement as HTMLElement)
    if (at < 0) return
    const columns = choices.length > 1 && choices[1].offsetTop === choices[0].offsetTop ? 2 : 1
    const step = { ArrowLeft: -1, ArrowRight: 1, ArrowUp: -columns, ArrowDown: columns }[event.key] ?? 0
    const next = choices[at + step]
    if (next) {
      next.focus()
      event.preventDefault()
    }
  }

  return (
    <section
      id="top"
      aria-labelledby="hero-heading"
      className="hero hero-d"
      style={{ '--pw': portrait.w, '--ph': portrait.h } as CSSProperties}
    >
      <div className="hero-d-stage">
        <HeroScene flag={false} bubble={false} />
      </div>

      <div className="hero-d-ground">
        <div className={`hero-d-panel ${container}`}>
          <div id="about" ref={boxRef} role="group" aria-label="About me" className="dialogue" onClick={onBoxClick}>
            <p className="dialogue-name font-pixel font-bold">{hero.name}</p>

            <div className="dialogue-body flex flex-col gap-2">
              <p className="text-sm font-bold text-coral-ink lg:text-[15px]">{hero.role}</p>

              <div className="relative">
                <div className="dialogue-pages" aria-live="polite">
                  {pages.map((text, i) => {
                    const current = i === page
                    const shown = current ? typed : text.length
                    const Tag = i === 0 ? 'h1' : 'p'
                    return (
                      <Tag
                        key={text}
                        id={i === 0 ? 'hero-heading' : undefined}
                        data-hidden={!current || undefined}
                        className={
                          i === 0
                            ? 'dialogue-page text-[24px] leading-[1.2] font-bold tracking-[-0.3px] lg:text-[32px]'
                            : 'dialogue-page text-[15px] font-medium tracking-wide text-slate lg:text-[17px]'
                        }
                      >
                        <span className="sr-only">{text}</span>
                        <span aria-hidden="true">
                          {text.slice(0, shown)}
                          <span className="invisible">{text.slice(shown)}</span>
                        </span>
                      </Tag>
                    )
                  })}
                </div>
                {!typing && !last && <Sprite sheet="ui-continue" className="dialogue-continue js-only" />}
              </div>

              {/* The replies. The first is the one Space picks, so it starts out highlighted. */}
              <ul aria-label="Your reply" className="dialogue-choices mt-1 grid list-none gap-2 sm:grid-cols-2" onKeyDown={onChoiceKey}>
                <li className="js-only">
                  {last && !typing ? (
                    <button type="button" data-default className={choiceClass} onClick={restart}>
                      <ChoiceLabel>Read that again</ChoiceLabel>
                    </button>
                  ) : (
                    <button type="button" data-default className={choiceClass} onClick={advance}>
                      <ChoiceLabel hint="Space">{typing ? 'Skip ahead' : 'Tell me more'}</ChoiceLabel>
                    </button>
                  )}
                </li>
                <li>
                  <Link href="/#projects" className={choiceClass}>
                    <ChoiceLabel>View projects</ChoiceLabel>
                  </Link>
                </li>
                <li>
                  <Link href="/#contact" className={choiceClass}>
                    <ChoiceLabel>Get in touch</ChoiceLabel>
                  </Link>
                </li>
                <li>
                  <a href={site.resume} className={choiceClass}>
                    <ChoiceLabel>See my resume</ChoiceLabel>
                  </a>
                </li>
              </ul>
            </div>
          </div>

          <Sprite sheet="luz-portrait" className="dialogue-portrait" />
        </div>
      </div>
      <div aria-hidden="true" className="blend hero-d-blend" />
    </section>
  )
}
