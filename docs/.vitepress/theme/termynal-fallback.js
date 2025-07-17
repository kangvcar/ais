/**
 * Termynal.js 简化版备用实现
 * 在原版加载失败时提供基本的打字动画效果
 */
window.TermynalFallback = class TermynalFallback {
  constructor(container, options = {}) {
    this.container = container;
    this.options = {
      typeDelay: options.typeDelay || 40,
      lineDelay: options.lineDelay || 700,
      cursor: options.cursor || '▋',
      ...options
    };
    
    this.lines = Array.from(container.querySelectorAll('[data-ty]'));
    this.currentLine = 0;
    
    // 隐藏所有行
    this.lines.forEach(line => {
      line.style.opacity = '0';
      line.style.display = 'none';
    });
    
    // 自动开始动画
    setTimeout(() => this.start(), 100);
  }
  
  async start() {
    for (let i = 0; i < this.lines.length; i++) {
      await this.animateLine(this.lines[i]);
      await this.delay(this.options.lineDelay);
    }
  }
  
  async animateLine(line) {
    const isInput = line.hasAttribute('data-ty') && line.getAttribute('data-ty') === 'input';
    const isProgress = line.hasAttribute('data-ty') && line.getAttribute('data-ty') === 'progress';
    
    line.style.display = 'block';
    line.style.opacity = '1';
    
    if (isProgress) {
      // 进度条动画
      line.innerHTML = '';
      const progressChars = '⠋⠙⠹⠸⠼⠴⠦⠧⠇⠏';
      let i = 0;
      const progressInterval = setInterval(() => {
        line.innerHTML = progressChars[i % progressChars.length];
        i++;
      }, 80);
      
      await this.delay(2000);
      clearInterval(progressInterval);
      line.innerHTML = '';
      return;
    }
    
    const text = line.textContent;
    line.innerHTML = '';
    
    if (isInput) {
      // 添加提示符
      const prompt = line.getAttribute('data-ty-prompt') || '$';
      line.innerHTML = `<span style="color: #4CAF50; font-weight: 600;">${prompt} </span>`;
    }
    
    // 打字动画
    for (let i = 0; i < text.length; i++) {
      line.innerHTML += text[i];
      await this.delay(this.options.typeDelay);
    }
  }
  
  delay(ms) {
    return new Promise(resolve => setTimeout(resolve, ms));
  }
}