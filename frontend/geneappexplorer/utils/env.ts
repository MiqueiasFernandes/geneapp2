// Read data from envronment variables

const __get_env = () => useRuntimeConfig().public

export const profile = () => __get_env().PROFILE;
export const is_dev = () => profile() == "DEV";
export const is_prd = () => !is_dev();
export const geneapp_api = () => __get_env().API;
