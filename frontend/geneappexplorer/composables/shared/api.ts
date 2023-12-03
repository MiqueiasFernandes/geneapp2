// GLOBAL GENEAPP FRONTEND CONFIGURATIONS 

const runtimeConfig = useRuntimeConfig()

export const DEV = true
export const PRD = !DEV
export const API = DEV ? 'http://localhost:8000/api' : '/api'
export const apiFetch = $fetch.create({ baseURL: API })