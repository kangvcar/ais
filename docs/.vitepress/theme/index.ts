import DefaultTheme from 'vitepress/theme'
import './custom.css'
import { h } from 'vue'
import type { Theme } from 'vitepress'

export default {
  extends: DefaultTheme,
  Layout: () => {
    return h(DefaultTheme.Layout, null, {
      // https://vitepress.dev/guide/extending-default-theme#layout-slots
    })
  },
  enhanceApp({ app, router, siteData }) {
    // 在客户端加载 termynal
    if (typeof window !== 'undefined') {
      // 从CDN加载termynal
      const loadTermynal = () => {
        return new Promise((resolve) => {
          if (window.Termynal) {
            resolve(window.Termynal)
            return
          }
          
          const script = document.createElement('script')
          script.src = 'https://cdn.jsdelivr.net/npm/termynal@0.0.4/dist/umd/termynal.js'
          script.onload = () => {
            resolve(window.Termynal)
          }
          document.head.appendChild(script)
        })
      }
      
      loadTermynal().then((Termynal) => {
        // 初始化termynal实例
        const initTermynals = () => {
          const terminals = document.querySelectorAll('[data-termynal]')
          terminals.forEach((terminal) => {
            if (!terminal.classList.contains('termynal-initialized')) {
              new Termynal(terminal)
              terminal.classList.add('termynal-initialized')
            }
          })
        }
        
        // 页面加载完成后初始化
        if (document.readyState === 'loading') {
          document.addEventListener('DOMContentLoaded', initTermynals)
        } else {
          initTermynals()
        }
        
        // 路由变化时重新初始化
        router.onAfterRouteChanged = () => {
          setTimeout(initTermynals, 100)
        }
      })
    }
  }
} satisfies Theme