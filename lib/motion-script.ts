export const MOTION_KEY = 'motion'
export const MOTION_QUERY = '(prefers-reduced-motion: reduce)'

/**
 * Runs before first paint, from app/layout.tsx. Marks the page as having JavaScript and sets
 * <html data-motion>: the visitor's choice for this session if they made one, otherwise the
 * system setting.
 */
export const motionScript = `(function(){var d=document.documentElement;d.classList.add('js');var m=null;try{m=sessionStorage.getItem('${MOTION_KEY}')}catch(e){}if(m!=='on'&&m!=='off'){m=window.matchMedia('${MOTION_QUERY}').matches?'off':'on'}d.dataset.motion=m})()`
