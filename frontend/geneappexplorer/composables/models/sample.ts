import Model from "../../utils/model";

const API = '/sample'

export interface ISample {
    id?: number;
    name: string;
    group: string;
    acession: string;
    local_path?: string;
}

export class Sample extends Model<ISample> {
    public static api = new Sample(API);

}