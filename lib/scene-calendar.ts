import { sceneByMonth } from '@/content/site'
import type { Environment } from './seasons'

/** The scene the calendar gives for a date: `sceneByMonth` in content/site.ts, by its month. */
export function sceneOn(date: Date): Environment {
  return sceneByMonth[date.getMonth()]
}
