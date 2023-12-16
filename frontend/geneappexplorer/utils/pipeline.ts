import type { ICommand, IProject } from "#imports";


export default class Pipeline {

    constructor(private project: IProject) {}

    public async quality_Control(): Promise<number[]> {

        const stp1 = await new CMD_Qinput(this.project).fill().step(4).enqueue();
        const stp2 = await new CMD_Qinput2(this.project).fill().step(4).wait(stp1).enqueue();

        //indexar genoma
        //indexar genes
        //indexar trancritos - hisat
        //indexar trancritos - salmon

        return [stp1.id || NaN, stp2.id || NaN].filter(x => !isNaN(x));
    }

    public process_Sample() {

        /// verificar se a amostra nao ja existe
        /// rodar ela
    }

}


