'use client'

import type { ReactNode } from 'react'

/**
 * An on/off switch in the site's pixel style. It needs JavaScript, so it is hidden without it.
 * Padding and any frame come from className.
 */
export function Switch({
  label,
  on,
  onChange,
  className = '',
}: {
  label: ReactNode
  on: boolean
  onChange: (on: boolean) => void
  className?: string
}) {
  return (
    <button
      type="button"
      role="switch"
      aria-checked={on}
      onClick={() => onChange(!on)}
      className={`js-only inline-flex min-h-11 cursor-pointer items-center gap-2 rounded text-sm font-bold ${className}`}
    >
      <span>{label}</span>
      <span
        aria-hidden="true"
        className={`relative h-6 w-11 flex-none rounded-sm border-[3px] border-navy ${on ? 'bg-coral' : 'bg-chip'}`}
      >
        <span className={`absolute top-0 size-[18px] bg-navy ${on ? 'right-0' : 'left-0'}`} />
      </span>
      <span aria-hidden="true" className="w-6 text-left">
        {on ? 'On' : 'Off'}
      </span>
    </button>
  )
}
