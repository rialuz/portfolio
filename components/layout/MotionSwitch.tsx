'use client'

import { Switch } from '@/components/ui/Switch'
import { setMotion, useMotion } from '@/lib/motion'

/**
 * Turns animation on or off for the session. It starts on the system setting, so without it
 * a visitor whose system has animation off would never know the site moves.
 */
export function MotionSwitch() {
  return <Switch label="Animation" on={useMotion()} onChange={setMotion} className="px-2" />
}
