import Model, { type IModel } from "~/utils/api";
import type { ISample } from "./sample";
import type { ICommand } from "./command";

const API = '/project'

export interface IProject extends IModel {

    name: string;
    control: string;
    treatment: string;
    path?: string;
    organism: string;
    created_at?: string;
    status?: number;

    genome: string;
    online: boolean;
    anotattion: string;
    proteome: string;
    transcriptome: string;
    library: string;

    samples: ISample[];
    commands: ICommand[];

    threads: number;
    ram: number;
    disk: number;
    fast: boolean; /// true: modo_rapido
    qvalue: number;
    psi: number;

    // hisat2_build: string;
    // salmon_index: string;
    // hisat2: string;
    // fastq_dump: string;
    // Trimmomatic: string;
    // fastqc: string;
    // salmon_quant: string;
    // samtools_view: string;
    // bamtools_sort: string;
    // bamCoverage: string;
    rmats_readLength: number;

}

export class Project extends Model<IProject> {

    public static api = new Project(API);

    public static model = () => ({
        name: 'Geneapp Project',
        control: 'Control', treatment: 'Treatment',
        online: true,
        samples: [] as ISample[], commands: [] as ICommand[],
        threads: 1, ram: 1, disk: 5, psi: .1, qvalue: .05
    } as IProject)

}