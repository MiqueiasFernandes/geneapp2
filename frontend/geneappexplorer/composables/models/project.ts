import Model, { type IModel } from "~/utils/api";
import type { ISample } from "./sample";
import type { ICommand } from "./command";
import { parse, stringify } from 'yaml'

const API = '/project'
export const LBS = ['SHORT_PAIRED', 'SHORT_SINGLE', 'LONG_SINGLE']

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

    public static from_yaml(data: string): IProject {

        const parsed = parse(data);
        const inputs = parsed["Input Files"];
        const contrast = parsed["Contrast group"];
        const configs = parsed["Params configuration"];

        const prj = {} as IProject;

        prj.name = parsed.Project?.Name;
        prj.organism = parsed.Project?.Organism;

        if (inputs) {
            prj.online = inputs.remote
            prj.genome = inputs.Genome
            prj.anotattion = inputs.Anotattion
            prj.transcriptome = inputs.Transcriptome
            prj.proteome = inputs.Proteome
        }

        if (contrast) {
            prj.library = contrast["Library layout"]
            prj.control = contrast.Control?.label
            prj.treatment = contrast.Treatment?.label
            prj.samples = []
            const ctrls: string[] = contrast.Control?.samples || []
            const tts: string[] = contrast.Treatment?.samples || []
            prj.samples.push(...ctrls.map((x: any, i) => ({ name: prj.control + (i + 1), acession: x.acession, group: prj.control } as ISample)))
            prj.samples.push(...tts.map((x: any, i) => ({ name: prj.treatment + (i + 1), acession: x.acession, group: prj.treatment } as ISample)))
        }

        if (configs) {
            prj.fast = configs["Fast mode"];
            prj.rmats_readLength = configs["rMATS read lengt"];
            prj.psi = configs.PSI;
            prj.qvalue = configs.Qvalue;
        }

        return prj
    }

    public static to_yaml(prj: IProject) {

        var obj: any = { Project: { Name: prj.name, Organism: prj.organism } };
        obj["Input Files"] = { remote: prj.online }
        obj["Input Files"].Genome = prj.genome;
        obj["Input Files"].Anotattion = prj.anotattion;
        obj["Input Files"].Transcriptome = prj.transcriptome
        obj["Input Files"].Proteome = prj.proteome

        obj["Contrast group"] = { "Library layout": prj.library }
        obj["Contrast group"].Control = { label: prj.control, samples: prj.samples.filter(x => x.group == prj.control).map(x => ({ acession: x.acession })) }
        obj["Contrast group"].Treatment = { label: prj.treatment, samples: prj.samples.filter(x => x.group == prj.treatment).map(x => ({ acession: x.acession })) }

        obj["Params configuration"] = {
            "Fast mode": prj.fast, "PSI": prj.psi, "Qvalue": prj.qvalue,
            "rMATS read lengt": prj.rmats_readLength,
        }
        return stringify(obj)
    }

}

export const Project_FUNGI: IProject = {
    name: "Project Fungi",
    control: "WILD",
    treatment: "TREATED",
    organism: "Candida albicans",
    online: false, //true, 
    rmats_readLength: 50,
    genome: "genome.fasta", //"https://ftp.ncbi.nlm.nih.gov/genomes/all/GCF/000/182/965/GCF_000182965.3_ASM18296v3/GCF_000182965.3_ASM18296v3_genomic.fna.gz",
    anotattion: "anotattion.gff3", //"https://ftp.ncbi.nlm.nih.gov/genomes/all/GCF/000/182/965/GCF_000182965.3_ASM18296v3/GCF_000182965.3_ASM18296v3_genomic.gff.gz",
    proteome: "proteome.faa", //"https://ftp.ncbi.nlm.nih.gov/genomes/all/GCF/000/182/965/GCF_000182965.3_ASM18296v3/GCF_000182965.3_ASM18296v3_protein.faa.gz",
    transcriptome: "transcriptome.fna", //"https://ftp.ncbi.nlm.nih.gov/genomes/all/GCF/000/182/965/GCF_000182965.3_ASM18296v3/GCF_000182965.3_ASM18296v3_rna.fna.gz",
    library: LBS[1],
    threads: 1, ram: 2, disk: 10, fast: false, qvalue: .05, psi: .1,
    samples: [
        { acession: "SRR2513862", name: "wild1", group: 'WILD' },
        { acession: "SRR2513863", name: "wild2", group: 'WILD' },
        { acession: "SRR2513864", name: "wild3", group: 'WILD' },
        { acession: "SRR2513867", name: "treated1", group: 'TREATED' },
        { acession: "SRR2513868", name: "treated2", group: 'TREATED' },
        { acession: "SRR2513869", name: "treated3", group: 'TREATED' }
    ],
    commands: [Command.model()]
}

export const Project_ARABDOPSIS: IProject = Object.assign(Object.assign({}, Project_FUNGI), {
    name: "Project Arabidopsis", organism: "Arabidopsis",
    genome: 'https://ftp.ncbi.nlm.nih.gov/genomes/all/GCF/000/001/735/GCF_000001735.4_TAIR10.1/GCF_000001735.4_TAIR10.1_genomic.fna.gz',
    anotattion: 'https://ftp.ncbi.nlm.nih.gov/genomes/all/GCF/000/001/735/GCF_000001735.4_TAIR10.1/GCF_000001735.4_TAIR10.1_genomic.gff.gz',
    proteome: 'https://ftp.ncbi.nlm.nih.gov/genomes/all/GCF/000/001/735/GCF_000001735.4_TAIR10.1/GCF_000001735.4_TAIR10.1_protein.faa.gz',
    transcriptome: 'https://ftp.ncbi.nlm.nih.gov/genomes/all/GCF/000/001/735/GCF_000001735.4_TAIR10.1/GCF_000001735.4_TAIR10.1_rna.fna.gz',
    samples: []
})

export const Project_HUMAN: IProject = Object.assign(Object.assign({}, Project_FUNGI), {
    name: "Project Human", organism: "Humano",
    genome: 'https://ftp.ncbi.nlm.nih.gov/genomes/all/GCF/000/001/405/GCF_000001405.40_GRCh38.p14/GCF_000001405.40_GRCh38.p14_genomic.fna.gz',
    anotattion: 'https://ftp.ncbi.nlm.nih.gov/genomes/all/GCF/000/001/405/GCF_000001405.40_GRCh38.p14/GCF_000001405.40_GRCh38.p14_genomic.gff.gz',
    proteome: 'https://ftp.ncbi.nlm.nih.gov/genomes/all/GCF/000/001/405/GCF_000001405.40_GRCh38.p14/GCF_000001405.40_GRCh38.p14_protein.faa.gz',
    transcriptome: 'https://ftp.ncbi.nlm.nih.gov/genomes/all/GCF/000/001/405/GCF_000001405.40_GRCh38.p14/GCF_000001405.40_GRCh38.p14_rna.fna.gz',
    samples: []
})
