import Model, { type IModel } from "../../utils/api";
import type { IProject } from "./project";

const API = '/command'

export interface ICommand extends IModel {

    status?: string;
    success?: boolean;
    end?: string;
    created_at?: string;
    ended_at?: string;

    info?: string;
    meta?: string;
    out?: string;
    log?: string;
    err?: string;

    op: number
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
    // arg5?: string | undefined;
    // arg6?: string | undefined;
    // arg7?: string | undefined;
    // arg8?: string | undefined;
    // arg9?: string | undefined;

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
    proteome(file: string) { this.arg3 = file; return this }
    transcriptome(file: string) { this.arg4 = file; return this }

    fill() {
        this.genome('genome.fasta');
        this.anotattion('anotattion.gff3');
        this.proteome('proteome.faa');
        this.transcriptome('transcriptome.fna');
        return this;
    }
}