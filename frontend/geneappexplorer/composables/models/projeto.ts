import Model from "./model";

const API = '/projetos'

export interface IProjeto {
    id: number;
    nome: string;
    path: string;
    created_at: string;
}

export class Projeto extends Model<IProjeto> {
    public static api = new Projeto(API);

}