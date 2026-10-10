export const HERO_KEY = 'hero'

/**
 * Runs before first paint, from app/layout.tsx. If the visitor picked a hero this session, it
 * goes on <html data-hero>, so the page knows before React does and never flashes the other.
 */
export const heroViewScript = `(function(){var h=null;try{h=sessionStorage.getItem('${HERO_KEY}')}catch(e){}if(h==='card'||h==='dialogue'){document.documentElement.dataset.hero=h}})()`
