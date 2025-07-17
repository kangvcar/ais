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
    // 在客户端加载官方 termynal
    if (typeof window !== 'undefined') {
      // 从官方GitHub加载termynal.js
      const loadTermynal = () => {
        return new Promise((resolve, reject) => {
          if (window.Termynal) {
            resolve(window.Termynal)
            return
          }
          
          const script = document.createElement('script')
          script.src = 'https://cdn.jsdelivr.net/gh/ines/termynal/termynal.js'
          script.onload = () => {
            resolve(window.Termynal)
          }
          script.onerror = () => {
            reject(new Error('Failed to load Termynal'))
          }
          document.head.appendChild(script)
        })
      }
      
      loadTermynal().then((Termynal) => {
        // 初始化termynal实例 - 使用官方方法
        const initTermynals = () => {
          const terminals = document.querySelectorAll('[data-termynal]')
          terminals.forEach((terminal) => {
            if (!terminal.hasAttribute('data-termynal-initialized')) {
              new Termynal(terminal, {
                typeDelay: 40,
                lineDelay: 700,
                cursor: '▋',
                noInit: false
              })
              terminal.setAttribute('data-termynal-initialized', 'true')
            }
          })
        }
        
        // 页面加载完成后初始化
        if (document.readyState === 'loading') {
          document.addEventListener('DOMContentLoaded', initTermynals)
        } else {
          setTimeout(initTermynals, 100)
        }
        
        // 路由变化时重新初始化
        router.onAfterRouteChanged = () => {
          setTimeout(initTermynals, 200)
        }
      }).catch((error) => {
        console.error('Termynal loading failed:', error)
      })
    }
  }
} satisfies Theme