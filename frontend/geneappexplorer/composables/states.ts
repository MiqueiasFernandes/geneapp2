import type { IProjeto } from "./models/projeto";


export const useProjeto = () => useState<IProjeto>(() => ({} as IProjeto))