export default class Model<T> {

    constructor(private href: string) { }

    public async list(): Promise<T[]> {
        return await apiFetch(this.href);
    }

}