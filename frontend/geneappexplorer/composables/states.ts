import { Projeto, type IProjeto } from "./models/projeto";



export const useProjeto = () => useState<IProjeto>(Projeto.model)