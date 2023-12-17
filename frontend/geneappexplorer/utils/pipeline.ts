import type { ICommand, IProject } from "#imports";
import { CMD_Index } from "~/composables";


export default class Pipeline {

    constructor(private project: IProject) { }

    public async quality_Control(): Promise<ICommand[]> {
        const stp1 = await new CMD_Qinput(this.project).fill().step(4).enqueue();
        const stp2 = await new CMD_Qinput2(this.project).fill().step(4).wait(stp1).enqueue();
        return [stp2, stp1];
    }

    private async index(fasta: string, name: string, is_salamon = false, lock: ICommand): Promise<ICommand> {
        const cmd = new CMD_Index(this.project).genomic(fasta).idx_name(name);
        if (is_salamon) cmd.is_salmon();
        if (lock) cmd.wait(lock);
        return cmd.step(4).enqueue();
    }

    public async index_all(lock: ICommand): Promise<ICommand[]> {
        //indexar genoma  => rmats
        const idx_genoma = await this.index('genome.final.fasta', 'idx_genoma', false, lock);
        //indexar genes => grafico
        const idx_genes = await this.index('genes.fa', 'idx_genes', false, lock);
        //indexar trancritos - hisat => validar anotacao (genes no gff)
        const idx_rnas = await this.index('transcripts.fa', 'idx_rnas', false, lock);
        //indexar trancritos - salmon => t3drnaseq
        const idx_rnas_slm = await this.index('transcripts.fa', 'idx_rnas_slm', true, lock);

        const holder = await new CMD_Holder(this.project)
            .add(idx_genoma)
            .add(idx_genes)
            .add(idx_rnas)
            .add(idx_rnas_slm)
            .enqueue()

        return [holder, idx_genoma, idx_genes, idx_rnas, idx_rnas_slm]
    }



    public process_Sample() {

        /// verificar se a amostra nao ja existe
        /// rodar ela
    }


    public async main(): Promise<ICommand[]> {

        const qc_jobs = await this.quality_Control();
        const ixd_jobs = await this.index_all(qc_jobs[0]);

        return qc_jobs.concat(ixd_jobs)
    }

}


