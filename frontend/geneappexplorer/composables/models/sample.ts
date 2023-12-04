import Model from "./model";

const API = '/samples'

export interface ISample {
    id?: number;
    name: string;
    local_path?: string;
    acession: string;
}

export class Sample extends Model<ISample> {
    public static api = new Sample(API);

}