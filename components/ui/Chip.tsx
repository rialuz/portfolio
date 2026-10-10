import type { ReactNode } from 'react'

type Tone = 'soft' | 'solid' | 'navy'
type Size = 'sm' | 'md' | 'lg'

const tones: Record<Tone, string> = {
  soft: 'border-chip-line bg-chip text-navy',
  solid: 'border-coral-ink bg-coral-ink text-white',
  navy: 'border-navy bg-navy text-cream',
}

const sizes: Record<Size, string> = {
  sm: 'px-2.5 py-[3px] text-xs',
  md: 'px-3 py-1 text-[13px]',
  lg: 'px-3.5 py-1.5 text-[15px]',
}

export function Chip({
  children,
  tone = 'soft',
  size = 'sm',
  className = '',
}: {
  children: ReactNode
  tone?: Tone
  size?: Size
  className?: string
}) {
  return (
    <span
      className={`inline-flex items-center rounded-full border font-bold ${tones[tone]} ${sizes[size]} ${className}`}
    >
      {children}
    </span>
  )
}

/** A wrapping row of chips. The first `highlight` chips are filled. */
export function ChipList({
  items,
  highlight = 0,
  size = 'sm',
  label,
}: {
  items: readonly string[]
  highlight?: number
  size?: Size
  label?: string
}) {
  if (items.length === 0) return null
  return (
    <ul aria-label={label} className={`flex list-none flex-wrap ${size === 'lg' ? 'gap-2' : 'gap-1.5'}`}>
      {items.map((item, i) => (
        <li key={item} className="flex">
          <Chip tone={i < highlight ? 'solid' : 'soft'} size={size}>
            {item}
          </Chip>
        </li>
      ))}
    </ul>
  )
}
