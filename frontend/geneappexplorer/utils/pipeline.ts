import type { ICommand, IProject, ISample } from "#imports";
import { CMD_Mapping, CMD_QCSample, CMD_Quantify, CMD_Rmats, CMD_T3drnaseq } from "~/composables";

export default class Pipeline {

    constructor(
        private project: IProject,
        private args: {
            trimommatic: string,
            hisat2: string,
            salmon: string,
            rmats: string,
            t3drna: string
        }) { }

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
            .add(idx_rnas_slm).step(4)
            .enqueue()

        return [holder, idx_genoma, idx_genes, idx_rnas, idx_rnas_slm]
    }

    public async map_sample(sample: ISample, idx: string, c: ICommand): Promise<ICommand> {
        return new CMD_Mapping(this.project)
            .sample(sample.name).index(idx).args(this.args.hisat2)
            .step(4).wait(c).enqueue();
    }

    public async quant_sample(sample: ISample, idx: string, c: ICommand): Promise<ICommand> {
        return new CMD_Quantify(this.project)
            .sample(sample.name).index(idx).args(this.args.salmon)
            .step(4).wait(c).enqueue();
    }

    public async process_Sample(sample: ISample, lock: ICommand): Promise<ICommand[]> {
        /// as amostra ja devem estar descompatads da origem
        /// pegar args do frontend
        var fq: ICommand;
        if (this.project.online)
            fq = await new CMD_Baixar(this.project)
                .from(sample.acession)
                .to(sample.name)
                .sra().wait(lock)
                .step(4).enqueue()
        else
            fq = await new CMD_Copiar(this.project)
                .from(sample.acession)
                .to(sample.name + '.fq')
                .step(4).wait(lock).enqueue()

        const qcfq = await new CMD_QCSample(this.project)
            .sample(sample.name)
            .args(this.args.trimommatic)
            .step(4).wait(fq).enqueue();

        const map_genom = await this.map_sample(sample, 'idx_genoma', qcfq);
        const map_gene = await this.map_sample(sample, 'idx_genes', this.project.fast ? qcfq : map_genom);
        const map_rna = await this.map_sample(sample, 'idx_rnas', this.project.fast ? qcfq : map_gene);
        const quant = await this.quant_sample(sample, 'idx_rnas_slm', this.project.fast ? qcfq : map_rna);

        const holder = await new CMD_Holder(this.project)
            .add(map_genom)
            .add(map_gene)
            .add(map_rna)
            .add(quant)
            .step(4).enqueue()

        return [holder, fq, qcfq, map_genom, map_gene, map_rna, quant]
    }


    public async main(): Promise<ICommand[]> {

       return [await new CMD_Rmats(this.project)
        .fill().args(this.args.rmats)
        .step(4).enqueue(),
       await new CMD_T3drnaseq(this.project)
        .fill().args(this.args.t3drna)
        .step(4).enqueue()];

        // const qc_jobs = await this.quality_Control();
        // const ixd_jobs = await this.index_all(qc_jobs[0]);
        // var samples_jobs: ICommand[] = []

        // /// mapear e quantificar
        // const holder1 = new CMD_Holder(this.project)
        // const holder2 = new CMD_Holder(this.project)
        // var lock: ICommand = ixd_jobs[0];
        // for (let index = 0; index < this.project.samples.length; index++) {
        //     const sample = this.project.samples[index];
        //     const cmdsmp = await this.process_Sample(sample, lock);
        //     lock = this.project.fast ? ixd_jobs[0] : cmdsmp[0];
        //     if (sample.group == this.project.control)
        //         holder1.add(cmdsmp[0]);
        //     else
        //         holder2.add(cmdsmp[0]);
        //     samples_jobs.push(...cmdsmp);
        // }

        // const holder3 = await new CMD_Holder(this.project)
        //     .add(await holder1.step(4).enqueue())
        //     .add(await holder2.step(4).enqueue())
        //     .step(4).enqueue();

        ///rmats, t3drnaaseq, multiqc, ete3, interproscan

        // const rmats = await new CMD_Rmats(this.project)
        //     .fill().args(this.args.rmats)
        //     .wait(holder3).step(4).enqueue();
        // const t3drnaseq = await new CMD_T3drnaseq(this.project)
        //     .fill().args(this.args.t3drna)
        //     .wait(holder3).step(4).enqueue();

        // /// gerar output

        // return qc_jobs.concat(ixd_jobs).concat(samples_jobs).concat([rmats, t3drnaseq])
    }

}


