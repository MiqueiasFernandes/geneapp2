import Model from "./model";
import type { ISample } from "./sample";

const API = '/projetos'

export interface IProjeto {

    id?: number;
    name: string;
    control: string;
    treatment: string;
    path?: string;
    organism: string;
    created_at?: string;

    genome: string;
    online: boolean;
    anotattion: string;
    proteome: string;
    transcriptome: string;
    ctrl_samples: ISample[];
    treat_samples: ISample[];
    library: string;

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

export class Projeto extends Model<IProjeto> {
    public static api = new Projeto(API);
    public static model = () => ({
        name: 'Geneapp Project',
        control: 'Control', treatment: 'Treatment',
        online: true,
        treat_samples: [] as ISample[], ctrl_samples: [] as ISample[],
        threads: 1, ram: 1, disk: 5, psi: .1, qvalue: .05
    } as IProjeto)
}