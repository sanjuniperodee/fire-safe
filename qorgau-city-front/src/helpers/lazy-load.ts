import { type DirectiveBinding } from 'vue'

const lazyLoad = {
  mounted(el: HTMLImageElement, binding: DirectiveBinding) {
    const options = {
      root: null,
      rootMargin: '0px',
      threshold: 0.1
    }

    const observer = new IntersectionObserver((entries, observer) => {
      entries.forEach((entry) => {
        if (entry.isIntersecting) {
          el.src = binding.value
          observer.unobserve(el)
        }
      })
    }, options)

    observer.observe(el)
  }
}

export default lazyLoad
