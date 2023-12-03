// GLOBAL GENEAPP FRONTEND CONFIGURATIONS 

const runtimeConfig = useRuntimeConfig()

export const apiFetch = $fetch.create({ baseURL: String(runtimeConfig.public.API) })