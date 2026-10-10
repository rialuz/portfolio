import { sceneByMonth } from '@/content/site'
import { seasonIds } from './seasons'

export const SCENE_KEY = 'scene'

/**
 * Runs before first paint, from app/layout.tsx, and puts the scene on <html data-scene>, so
 * the right art is there from the first paint: the scene the visitor picked this session,
 * otherwise the calendar's scene for their own date (sceneByMonth in content/site.ts).
 */
export const sceneScript = `(function(){var s=null;try{s=sessionStorage.getItem('${SCENE_KEY}')}catch(e){}if(${JSON.stringify(['candy', ...seasonIds])}.indexOf(s)<0){s=${JSON.stringify(sceneByMonth)}[new Date().getMonth()]}document.documentElement.dataset.scene=s})()`
