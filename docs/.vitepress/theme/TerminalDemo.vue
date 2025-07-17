<template>
  <div class="terminal-demo-container">
    <div 
      ref="terminalRef"
      :id="terminalId"
      data-termynal 
      :data-ty-typeDelay="typeDelay"
      :data-ty-lineDelay="lineDelay"
    >
      <slot />
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted, nextTick } from 'vue'

const props = defineProps({
  terminalId: {
    type: String,
    required: true
  },
  typeDelay: {
    type: Number,
    default: 40
  },
  lineDelay: {
    type: Number,
    default: 700
  }
})

const terminalRef = ref(null)

const initializeTerminal = async () => {
  console.log(`Initializing terminal: ${props.terminalId}`)
  
  if (!terminalRef.value) {
    console.error('Terminal ref not available')
    return
  }
  
  // 等待Termynal加载
  let attempts = 0
  while (typeof window.Termynal === 'undefined' && attempts < 10) {
    console.log(`Waiting for Termynal... attempt ${attempts + 1}`)
    await new Promise(resolve => setTimeout(resolve, 200))
    attempts++
  }
  
  if (typeof window.Termynal === 'undefined') {
    console.error('Termynal not available after waiting')
    return
  }
  
  try {
    console.log('Creating Termynal instance...')
    const termynal = new window.Termynal(terminalRef.value, {
      typeDelay: props.typeDelay,
      lineDelay: props.lineDelay,
      cursor: '▋'
    })
    
    console.log('✅ Terminal initialized successfully:', props.terminalId)
    
    // 手动启动动画
    if (termynal.start && typeof termynal.start === 'function') {
      termynal.start()
    }
    
  } catch (error) {
    console.error('❌ Failed to initialize terminal:', error)
  }
}

onMounted(async () => {
  await nextTick()
  setTimeout(initializeTerminal, 500)
})
</script>

<style scoped>
.terminal-demo-container {
  margin: 2rem 0;
}
</style>