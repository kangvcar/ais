/**
 * 内嵌版本的Termynal - 直接在页面中实现打字动画
 * 避免外部依赖和加载问题
 */
class InlineTermynal {
  constructor(container, options = {}) {
    this.container = container
    this.options = {
      typeDelay: options.typeDelay || 20,
      lineDelay: options.lineDelay || 700,
      cursor: options.cursor || '▋',
      ...options
    }
    
    this.lines = []
    this.currentLine = 0
    this.isRunning = false
    
    this.init()
  }
  
  init() {
    // 解析所有data-ty元素
    const elements = this.container.querySelectorAll('[data-ty]')
    elements.forEach((el, index) => {
      const type = el.getAttribute('data-ty') || 'output'
      const text = el.textContent || ''
      const prompt = el.getAttribute('data-ty-prompt')
      const delay = parseInt(el.getAttribute('data-ty-delay')) || null
      
      this.lines.push({
        element: el,
        type: type,
        text: text,
        prompt: prompt,
        delay: delay,
        originalContent: el.innerHTML
      })
      
      // 隐藏原始内容
      el.style.display = 'none'
    })
    
    // 开始动画
    setTimeout(() => this.start(), 100)
  }
  
  async start() {
    if (this.isRunning) return
    this.isRunning = true
    
    console.log(`Starting inline terminal animation with ${this.lines.length} lines`)
    
    for (let i = 0; i < this.lines.length; i++) {
      await this.animateLine(this.lines[i])
      if (i < this.lines.length - 1) {
        await this.delay(this.options.lineDelay)
      }
    }
    
    this.isRunning = false
  }
  
  async animateLine(line) {
    const { element, type, text, prompt } = line
    
    // 显示元素
    element.style.display = 'block'
    element.innerHTML = ''
    
    if (type === 'progress') {
      return this.animateProgress(element)
    }
    
    if (type === 'input') {
      // 添加提示符
      const promptText = prompt || '$'
      const promptSpan = document.createElement('span')
      promptSpan.style.color = '#4CAF50'
      promptSpan.style.fontWeight = '600'
      promptSpan.style.marginRight = '7px'
      promptSpan.textContent = promptText + ' '
      element.appendChild(promptSpan)
    }
    
    // 打字动画 - 支持表情符号
    const chars = Array.from(text) // 使用Array.from正确分割表情符号
    for (let i = 0; i < chars.length; i++) {
      const char = chars[i]
      element.appendChild(document.createTextNode(char))
      await this.delay(this.options.typeDelay)
    }
  }
  
  async animateProgress(element) {
    const frames = ['⠋', '⠙', '⠹', '⠸', '⠼', '⠴', '⠦', '⠧', '⠇', '⠏']
    let frameIndex = 0
    
    const animate = () => {
      element.textContent = frames[frameIndex]
      frameIndex = (frameIndex + 1) % frames.length
    }
    
    const interval = setInterval(animate, 80)
    await this.delay(2000)
    clearInterval(interval)
    
    element.textContent = ''
  }
  
  delay(ms) {
    return new Promise(resolve => setTimeout(resolve, ms))
  }
}

// 自动初始化函数
function initInlineTermynals() {
  console.log('Initializing inline termynals...')
  const terminals = document.querySelectorAll('[data-termynal]:not([data-inline-initialized])')
  
  terminals.forEach((terminal, index) => {
    console.log(`Initializing inline terminal #${index + 1}`)
    new InlineTermynal(terminal)
    terminal.setAttribute('data-inline-initialized', 'true')
  })
}

// 导出到全局
window.InlineTermynal = InlineTermynal
window.initInlineTermynals = initInlineTermynals