import '@/assets/nullstyle.scss'
import '@/assets/fontstyle.scss'
import '@mdi/font/css/materialdesignicons.css'
import '@fortawesome/fontawesome-free/css/all.css'
import DateFnsAdapter from '@date-io/date-fns'
import enUS from 'date-fns/locale/en-US'
import ruRu from 'date-fns/locale/ru'
import { createApp } from 'vue'
import { createPinia } from 'pinia'
import piniaPluginPersistedstate from 'pinia-plugin-persistedstate'

//@ts-ignore
import App from './App.vue'
import router from './router'

import 'vuetify/styles'
import { createVuetify } from 'vuetify'
import * as components from 'vuetify/components'
//@ts-ignore
import { aliases, mdi } from 'vuetify/lib/iconsets/mdi'
import * as directives from 'vuetify/directives'
import { createI18n } from 'vue-i18n'
import enLocale from './locales/en.json'
import ruLocale from './locales/ru.json'
import kzLocale from './locales/kz.json'
import lazyLoad from '@/helpers/lazy-load'

const i18n = createI18n({
  legacy: false,
  locale: 'ru',
  fallbackLocale: 'ru',
  messages: {
    en: enLocale,
    ru: ruLocale,
    kz: kzLocale
  }
})

const vuetify = createVuetify({
  components,
  directives,
  locale: {
    // @ts-expect-error
    t: (key, ...params) => i18n.global.t(key, params)
  },
  date: {
    adapter: DateFnsAdapter,
    locale: {
      en: enUS,
      ru: ruRu
    }
  },
  icons: {
    defaultSet: 'mdi',
    aliases,
    sets: {
      mdi
    }
  }
})

const app = createApp(App)

const pinia = createPinia()
pinia.use(piniaPluginPersistedstate)
app.use(pinia)
app.use(i18n)
app.use(router)
app.use(vuetify)
app.directive('lazy', lazyLoad)

app.mount('#app')
