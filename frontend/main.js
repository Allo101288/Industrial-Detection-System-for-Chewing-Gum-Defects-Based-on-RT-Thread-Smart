import App from './App'

// #ifndef VUE3
import Vue from 'vue'
import './uni.promisify.adaptor'
import { PiniaVuePlugin, createPinia } from 'pinia'

Vue.config.productionTip = false
App.mpType = 'app'

// 创建 Pinia 实例
const pinia = createPinia()
// 安装 Pinia 插件
Vue.use(PiniaVuePlugin)

const app = new Vue({
  ...App,
  pinia  // 挂载 Pinia
})
app.$mount()
// #endif

// #ifdef VUE3
import { createSSRApp } from 'vue'
import { createPinia } from 'pinia'

export function createApp() {
  const app = createSSRApp(App)
  // 创建 Pinia 实例
  const pinia = createPinia()
  // 使用 Pinia
  app.use(pinia)
  
  return {
    app,
    pinia  // 如果需要服务器端渲染可以返回 pinia
  }
}
// #endif