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

    public static model = () => ({
        op: 1, arg1: 'welcome.txt', arg2: 'projeto_criado_com_sucesso', status: 'exec'
    } as ICommand)
}

class CMD implements ICommand {

    project_id?: number | undefined;
    id?: number | undefined;

    op: number = 1;
    lock?: number | undefined;
    status?: string | undefined;
    info?: string = 'bash command';
    meta?: string = 'step 0';

    // success?: boolean | undefined;
    // end?: string | undefined;
    // out?: string | undefined;
    // log?: string | undefined;
    // err?: string | undefined;
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

    wait(id: number) { this.lock = id; return this }

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
    info = 'Quality control data input files';
    genome(file: string) { this.arg1 = file; return this }
    anotattion(file: string) { this.arg2 = file; return this }
    transcriptome(file: string) { this.arg3 = file; return this }
    proteome(file: string) { this.arg4 = file; return this }

    fill() {
        this.genome('genome.fasta');
        this.anotattion('anotattion.gff3');
        this.proteome('proteome.faa');
        this.transcriptome('transcriptome.fna');
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

    add(x: number) {
        const tsp = `${x}`;
        if(!this.arg1)  {this.arg1 = tsp; return this};
        if(!this.arg2)  {this.arg2 = tsp; return this};
        if(!this.arg3)  {this.arg3 = tsp; return this};
        if(!this.arg4)  {this.arg4 = tsp; return this};
        if(!this.arg5)  {this.arg5 = tsp; return this};
        if(!this.arg6)  {this.arg6 = tsp; return this};
        return this
    }
}