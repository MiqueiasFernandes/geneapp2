import Model, { type IModel } from "../../utils/api";

const API = '/sample'

export interface ISample extends IModel{
    name: string;
    group: string;
    acession: string;
    local_path?: string;
}

export class Sample extends Model<ISample> {
    public static api = new Sample(API);

}