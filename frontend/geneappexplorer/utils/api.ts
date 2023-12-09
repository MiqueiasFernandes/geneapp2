// GLOBAL GENEAPP FRONTEND CONFIGURATIONS 

export interface IModel {
    id?: number;
}

export default class Model<T extends IModel> {

    private $fetch = $fetch.create({ baseURL: String(useRuntimeConfig().public.API) })

    constructor(private href: string) { }

    public async list(): Promise<T[]> {
        return await this.$fetch(this.href);
    }

    public async create(obj: T): Promise<T> {
        return await this.$fetch(this.href, {
            method: 'POST',
            body: JSON.stringify(obj)
        }).then(r => Object.assign(obj as any, r) as T)
    }

    public async find(id: number): Promise<T> {
        return await this.$fetch(`${this.href}/${id}`);
    }

    public async update(obj: T): Promise<T> {
        return await this.$fetch(`${this.href}/${obj.id}`, {
            method: 'PUT',
            body: JSON.stringify(obj)
        }).then(r => Object.assign(obj as any, r) as T)
    }

    public async delete(id: number): Promise<void> {
        return await this.$fetch(`${this.href}/${id}`, { method: 'DELETE' });
    }
}