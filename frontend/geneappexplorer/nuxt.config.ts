// https://nuxt.com/docs/api/configuration/nuxt-config
export default defineNuxtConfig({
  devtools: { enabled: true },
  ssr: false,
  routeRules: {
    // Generated at build time for SEO purpose
    '/': { prerender: true }
  },
  modules: ['@nuxt/ui'],
  runtimeConfig: {
    public: {
      DEV: true,
      PRD: false,
      API: 'http://localhost:8000/api'
    }
  }
})
