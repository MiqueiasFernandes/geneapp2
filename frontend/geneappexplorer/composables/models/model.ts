export default class Model<T> {

    constructor(public href: string) { }

    public async list(): Promise<T[]> {
        return await apiFetch(this.href);
    }

    public async create(obj: T): Promise<T> {
        return await apiFetch(this.href, {
            method: 'POST',
            body: JSON.stringify(obj)
        }).then(r => Object.assign(obj as any, r) as T)
    }

    public async get(id: number): Promise<T> {
        return await apiFetch(`${this.href}/${id}`);
    }

    public async update(obj: T): Promise<T> {
        return await apiFetch(this.href, {
            method: 'PUT',
            body: JSON.stringify(obj)
        }).then(r => Object.assign(obj as any, r) as T)
    }

    public async delete(id: number): Promise<void> {
        return await apiFetch(`${this.href}/${id}`, { method: 'DELETE' });
    }
}