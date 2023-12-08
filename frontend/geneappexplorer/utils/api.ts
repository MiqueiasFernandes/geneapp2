// GLOBAL GENEAPP FRONTEND CONFIGURATIONS 


export const api = () => {
    const href =String(useRuntimeConfig().public.API)
    return $fetch.create({ baseURL: href })
}

