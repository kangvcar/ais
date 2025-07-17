import DefaultTheme from 'vitepress/theme'
import './custom.css'
import { h, onMounted, nextTick } from 'vue'
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
      // 更可靠的初始化方案
      const initializeTermynal = () => {
        // 加载termynal脚本
        const loadScript = () => {
          return new Promise((resolve, reject) => {
            if (window.Termynal) {
              resolve(window.Termynal)
              return
            }
            
            const script = document.createElement('script')
            // 尝试使用更稳定的CDN
            script.src = 'https://unpkg.com/termynal@0.0.4/dist/termynal.js'
            script.async = true
            
            script.onload = () => {
              console.log('Termynal script loaded')
              resolve(window.Termynal)
            }
            
            script.onerror = () => {
              // 备用CDN
              const backupScript = document.createElement('script')
              backupScript.src = 'https://cdn.jsdelivr.net/gh/ines/termynal/termynal.js'
              backupScript.async = true
              backupScript.onload = () => {
                console.log('Termynal script loaded from backup CDN')
                resolve(window.Termynal)
              }
              backupScript.onerror = () => {
                console.log('Using fallback Termynal implementation')
                // 加载本地备用实现
                const fallbackScript = document.createElement('script')
                fallbackScript.src = './termynal-fallback.js'
                fallbackScript.onload = () => {
                  window.Termynal = window.TermynalFallback
                  resolve(window.Termynal)
                }
                fallbackScript.onerror = () => reject(new Error('Failed to load any Termynal implementation'))
                document.head.appendChild(fallbackScript)
              }
              document.head.appendChild(backupScript)
            }
            
            document.head.appendChild(script)
          })
        }
        
        // 初始化所有终端
        const initTerminals = () => {
          const terminals = document.querySelectorAll('[data-termynal]:not([data-termynal-initialized])')
          console.log(`Initializing ${terminals.length} terminals`)
          
          terminals.forEach((terminal, index) => {
            try {
              // 清理已有的内容并重新创建
              const terminalId = `terminal-${Date.now()}-${index}`
              
              // 创建新的Termynal实例
              const termynal = new window.Termynal(terminal, {
                typeDelay: 40,
                lineDelay: 700,
                cursor: '▋'
              })
              
              terminal.setAttribute('data-termynal-initialized', 'true')
              console.log(`Terminal ${index + 1} initialized`)
              
              // 手动启动动画（如果需要）
              if (termynal.start && typeof termynal.start === 'function') {
                termynal.start()
              }
              
            } catch (error) {
              console.error(`Failed to initialize terminal ${index + 1}:`, error)
            }
          })
        }
        
        // 加载并初始化
        loadScript().then(() => {
          // 多次尝试初始化以确保成功
          const tryInit = (attempts = 0) => {
            if (attempts > 5) {
              console.error('Max initialization attempts reached')
              return
            }
            
            const delay = attempts * 200 + 100
            setTimeout(() => {
              const uninitializedTerminals = document.querySelectorAll('[data-termynal]:not([data-termynal-initialized])')
              if (uninitializedTerminals.length > 0) {
                initTerminals()
                // 如果还有未初始化的，继续尝试
                setTimeout(() => {
                  const stillUninit = document.querySelectorAll('[data-termynal]:not([data-termynal-initialized])')
                  if (stillUninit.length > 0) {
                    tryInit(attempts + 1)
                  }
                }, 300)
              }
            }, delay)
          }
          
          tryInit()
        }).catch(error => {
          console.error('Failed to load Termynal:', error)
        })
      }
      
      // 在客户端水合化完成后初始化
      if (document.readyState === 'loading') {
        document.addEventListener('DOMContentLoaded', () => {
          setTimeout(initializeTermynal, 100)
        })
      } else {
        setTimeout(initializeTermynal, 100)
      }
      
      // 路由变化时重新初始化
      router.onAfterRouteChanged = () => {
        setTimeout(initializeTermynal, 200)
      }
    }
  }
} satisfies Theme