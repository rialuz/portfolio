import { seasonIds, seasons, seasonSpriteUrl } from '@/lib/seasons'

/**
 * The rules that put a season on screen, written from the season data so a new season needs
 * no CSS of its own. For the scene on <html data-scene> they set the sky and ground colours,
 * point every replaced sprite at the season's file, and dress the dialogue box.
 */
export function SceneStyles() {
  const css = seasonIds
    .map((id) => {
      const at = `html[data-scene='${id}']`
      const season = seasons[id]
      return [
        `${at}{--color-sky:${season.sky};--color-ground:${season.ground}}`,
        `${at} .sprite{background-image:var(--sheet-${id},var(--sheet))}`,
        `${at} .dialogue{border-image-source:url(${seasonSpriteUrl(id, 'ui-dialogue-frame')})}`,
        `${at} .dialogue-name{border-image-source:url(${seasonSpriteUrl(id, 'ui-nameplate')});background-color:${season.plate}}`,
      ].join('')
    })
    .join('')

  return <style dangerouslySetInnerHTML={{ __html: css }} />
}
