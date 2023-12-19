import Model, { type IModel } from "../../utils/api";
import type { IProject } from "./project";

const API = '/command'

export interface ICommand extends IModel {

    status?: string;
    success?: boolean;
    end?: string;
    created_at?: string;
    started_at?: string;
    ended_at?: string;
    payload?: string;

    info?: string;
    meta?: string;
    out?: string;
    log?: string;
    err?: string;

    op: number;
    tsp?: number;
    lock?: number;
    arg1?: string;
    arg2?: string;
    arg3?: string;
    arg4?: string;
    arg5?: string;
    arg6?: string;
    arg7?: string;
    arg8?: string;
    arg9?: string;

    project_id?: number;

}

export class Command extends Model<ICommand> {
    public static api = new Command(API);

    public static model = (a?: string, b?: string) => ({
        op: 1, arg1: a || 'welcome.txt', payload: b || 'projeto_criado_com_sucesso', status: 'exec'
    } as ICommand)
}

class CMD implements ICommand {

    project_id?: number | undefined;
    id?: number | undefined;

    op: number = 1;
    lock = 0;
    status?: string | undefined;
    info?: string = 'bash command';
    meta?: string = 'step 0';
    payload?: string | undefined;

    arg1?: string | undefined;
    arg2?: string | undefined;
    arg3?: string | undefined;
    arg4?: string | undefined;
    arg5?: string | undefined;
    arg6?: string | undefined;
    arg7?: string | undefined;
    arg8?: string | undefined;
    arg9?: string | undefined;

    constructor(public prj: IProject) {
        this.project_id = prj.id;
    }

    step(x: number) {
        this.meta = 'step' + x;
        return this;
    }

    enqueue(): Promise<ICommand> {
        this.status = 'exec';
        return Command.api.create(this);
    }

    wait(c?: ICommand) { if (c) this.lock = c.tsp || 0; return this }

}

export class CMD_Copiar extends CMD {
    op = 2;
    info = 'Copy input file';
    from(file: string) { this.arg1 = file; return this }
    to(file: string) { this.info += ' ' + (this.arg2 = file); return this }
}

export class CMD_Baixar extends CMD {
    op = 3;
    info = 'Download remote file';
    arg3 = "http";
    from(url: string) { this.arg1 = url; return this }
    to(file: string) { this.info += ' ' + (this.arg2 = file); return this }
    sra() { this.arg3 = 'sra'; this.info = `Dump sample ${this.arg1} to ${this.arg2}`; return this }
}

export class CMD_Unzip extends CMD {
    op = 4;
    info = 'Unzip file';
    file(file: string) { this.info += ' ' + (this.arg1 = file); return this }
}

export class CMD_Qinput extends CMD {
    op = 5;
    info = 'Clean data input files';
    genome(file: string) { this.arg1 = file; return this }
    anotattion(file: string) { this.arg2 = file; return this }
    to_genome(file: string) { this.arg3 = file; return this }
    to_anotation(file: string) { this.arg4 = file; return this }

    fill() {
        this.genome('genome.fasta');
        this.anotattion('anotattion.gff3');
        this.to_genome('genome_clean.fa');
        this.to_anotation('genes.gff3');
        return this;
    }
}

export class CMD_Splitx extends CMD {
    op = 6;
    info = 'Split data input files';
    genome(file: string) { this.arg1 = file; return this }
    anotattion(file: string) { this.arg2 = file; return this }

    fill() {
        this.genome('genome.fasta');
        this.anotattion('anotattion.gff3');
        return this;
    }
}

export class CMD_Joinx extends CMD {
    op = 7;
    info = 'Join data input files';
    genome(file: string) { this.arg1 = file; return this }
    anotattion(file: string) { this.arg2 = file; return this }

    fill() {
        this.genome('genome.fasta');
        this.anotattion('anotattion.gff3');
        return this;
    }
}

export class CMD_Holder extends CMD {
    op = 8;
    info = 'Holder for jobs finish toghether';

    add(c?: ICommand) {
        if (!c) return this;
        const tsp = `${c.tsp}`;
        if (!this.arg1) { this.arg1 = tsp; return this };
        if (!this.arg2) { this.arg2 = tsp; return this };
        if (!this.arg3) { this.arg3 = tsp; return this };
        if (!this.arg4) { this.arg4 = tsp; return this };
        if (!this.arg5) { this.arg5 = tsp; return this };
        if (!this.arg6) { this.arg6 = tsp; return this };
        if (!this.arg7) { this.arg7 = tsp; return this };
        if (!this.arg8) { this.arg8 = tsp; return this };
        if (!this.arg9) { this.arg9 = tsp; return this };
        return this
    }
}

export class CMD_Qinput2 extends CMD {
    op = 9;
    info = 'Generate proteome and transcriptome';
    genome(file: string) { this.arg1 = file; return this }
    anotattion(file: string) { this.arg2 = file; return this }
    novo_gff(file: string) { this.arg3 = file; return this }
    fasta_genes(file: string) { this.arg4 = file; return this }

    fill() {
        this.genome('genome_clean.fa');
        this.anotattion('genes.gff3');
        this.novo_gff('genes.gff3');
        this.fasta_genes('genes.fa');
        return this;
    }
}

export class CMD_Index extends CMD {

    op = 10;
    info = 'Index genomic files';
    arg3 = "0";

    genomic(file: string) { this.arg1 = file; return this }
    idx_name(name: string) { this.arg2 = name; return this }
    is_salmon() { this.arg3 = "1"; return this }

}

export class CMD_QCSample extends CMD {

    op = 11;
    info = 'Quality control for ? fastqc files';
    arg3 = "0";

    constructor(prj: IProject) {
        super(prj);
        this.arg2 = "ILLUMINACLIP:TruSeq3-PE.fa:2:30:10:2:True LEADING:3 TRAILING:3 MINLEN:36"
        this.arg3 = prj.library.includes("PAIRED") ? "1" : "0";
    }

    sample(file: string) { this.arg1 = file; this.info = this.info.replace("?", file); return this }
    args(args: string) { this.arg2 = args; return this }

}

export class CMD_Mapping extends CMD {

    op = 12;
    info = 'Mapping ? sample on @';
    arg4 = "0";

    constructor(prj: IProject) {
        super(prj);
        this.arg3 = "--no-unal"
        this.arg4 = prj.library.includes("PAIRED") ? "1" : "0";
    }

    sample(file: string) { this.arg1 = file; this.info = this.info.replace("?", file); return this }
    index(name: string) { this.arg2 = name; this.info = this.info.replace("@", name); return this }
    args(args: string) { this.arg3 = args; return this }

}

export class CMD_Quantify extends CMD {

    op = 13;
    info = 'Quantify ? sample on @';
    arg4 = "0";

    constructor(prj: IProject) {
        super(prj);
        this.arg3 = "--libType IU"
        this.arg4 = prj.library.includes("PAIRED") ? "1" : "0";
    }

    sample(file: string) { this.arg1 = file; this.info = this.info.replace("?", file); return this }
    index(name: string) { this.arg2 = name; this.info = this.info.replace("@", name); return this }
    args(args: string) { this.arg3 = args; return this }

}

export class CMD_Rmats extends CMD {

    //bam1, bam2, rlen, param = command.arg1, command.arg2, command.arg3, command.arg4
    op = 14;
    info = 'run rMATS';

    fill() {
        const bams1 = this.prj.samples.filter(s => s.group == this.prj.control);
        const bams2 = this.prj.samples.filter(s => s.group == this.prj.treatment);
        this.arg1 = bams1.map(s => `${s.name}.idx_genoma.bam`).join(",");
        this.arg2 = bams2.map(s => `${s.name}.idx_genoma.bam`).join(",");
        this.arg3 = this.prj.rmats_readLength.toString();
        this.arg4 = "-t single";
        return this;
    }

    args(args: string) { this.arg4 = args; return this }

}

export class CMD_T3drnaseq extends CMD {

    op = 15;
    info = 'run 3DRNASeq';

    fill() {
        this.arg1 = this.prj.control;
        this.arg2 = this.prj.treatment;
        this.arg3 = 'deltaPS_cut=0.05 DE_pipeline="glmQL"'
        //RUN,SAMPLE,FACTOR,FOLDER
        this.payload = this.prj.samples.map(s => `${s.acession},${s.name},${s.group}`).join("\n")

        return this;
    }

    args(args: string) { this.arg3 = args; return this }

}

export class CMD_Multiqc extends CMD {

    op = 16;
    info = 'run MultiQC';

}

export class CMD_ASResults extends CMD {

    op = 17;
    info = 'Summarize results';

}

export class CMD_Group extends CMD {

    op = 18;
    info = 'Run ETE3 for AS genes';

}

export class CMD_Interpro extends CMD {

    op = 19;
    info = 'Run Interporscan5 annotattion for AS genes';

}