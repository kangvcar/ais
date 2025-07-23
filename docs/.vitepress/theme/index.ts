import DefaultTheme from 'vitepress/theme'
import './custom.css'
import './style.css'
import { h, onMounted, nextTick } from 'vue'
import type { Theme } from 'vitepress'
import TerminalDemo from './TerminalDemo.vue'

export default {
  extends: DefaultTheme,
  Layout: () => {
    return h(DefaultTheme.Layout, null, {
      // https://vitepress.dev/guide/extending-default-theme#layout-slots
    })
  },
  enhanceApp({ app, router, siteData }) {
    // 注册TerminalDemo组件
    app.component('TerminalDemo', TerminalDemo)
    
    // 使用内嵌termynal实现
    if (typeof window !== 'undefined') {
      // 动态加载内嵌termynal脚本
      const loadInlineTermynal = () => {
        if (window.initInlineTermynals) {
          return Promise.resolve()
        }
        
        return new Promise((resolve) => {
          const script = document.createElement('script')
          script.src = '/ais/inline-termynal.js'
          script.onload = () => {
            console.log('Inline termynal loaded')
            resolve()
          }
          script.onerror = () => {
            console.error('Failed to load inline termynal')
            resolve() // 继续执行，不阻塞
          }
          document.head.appendChild(script)
        })
      }
      
      const initTerminals = () => {
        if (typeof window.initInlineTermynals === 'function') {
          window.initInlineTermynals()
        } else {
          console.log('initInlineTermynals not available, retrying...')
          setTimeout(initTerminals, 200)
        }
      }
      
      // 加载并初始化
      loadInlineTermynal().then(() => {
        setTimeout(initTerminals, 100)
        
        // 路由变化时重新初始化
        router.onAfterRouteChanged = () => {
          setTimeout(initTerminals, 200)
        }
        
        // 兜底重试
        setTimeout(initTerminals, 1000)
      })
    }
  }
} satisfies Theme