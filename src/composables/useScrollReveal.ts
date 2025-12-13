import { onMounted, onUnmounted } from 'vue'

export function useScrollReveal(selector: string, options = {}) {
  let observer: IntersectionObserver

  const defaultOptions = {
    threshold: 0.1,
    rootMargin: '0px 0px -100px 0px',
    ...options
  }

  onMounted(() => {
    observer = new IntersectionObserver((entries) => {
      entries.forEach((entry) => {
        if (entry.isIntersecting) {
          entry.target.classList.add('revealed')
          observer.unobserve(entry.target)
        }
      })
    }, defaultOptions)

    const elements = document.querySelectorAll(selector)
    elements.forEach((el) => {
      el.classList.add('reveal')
      observer.observe(el)
    })
  })

  onUnmounted(() => {
    if (observer) {
      observer.disconnect()
    }
  })
}

