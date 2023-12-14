
<script setup lang="ts">
import type { FormError, FormSubmitEvent } from '#ui/types'
import { type IProject, type ISample, Command, CMD_Baixar, CMD_Unzip, CMD_Copiar, CMD_Qinput, CMD_Splitx, CMD_Qinput2 } from '~/composables';

const runtimeConfig = useRuntimeConfig()

const toast = useToast()
const LBS = ['SHORT_PAIRED', 'SHORT_SINGLE', 'LONG_SINGLE']
const example_fung: IProject = {
    name: "Project EXPPATOG",
    control: "WILD",
    treatment: "TREATED",
    organism: "Candida albicans",
    online: true, rmats_readLength: 50,
    genome: "https://ftp.ncbi.nlm.nih.gov/genomes/all/GCF/000/182/965/GCF_000182965.3_ASM18296v3/GCF_000182965.3_ASM18296v3_genomic.fna.gz",
    anotattion: "https://ftp.ncbi.nlm.nih.gov/genomes/all/GCF/000/182/965/GCF_000182965.3_ASM18296v3/GCF_000182965.3_ASM18296v3_genomic.gff.gz",
    proteome: "https://ftp.ncbi.nlm.nih.gov/genomes/all/GCF/000/182/965/GCF_000182965.3_ASM18296v3/GCF_000182965.3_ASM18296v3_protein.faa.gz",
    transcriptome: "https://ftp.ncbi.nlm.nih.gov/genomes/all/GCF/000/182/965/GCF_000182965.3_ASM18296v3/GCF_000182965.3_ASM18296v3_rna.fna.gz",
    library: LBS[1],
    threads: 1, ram: 2, disk: 10, fast: false, qvalue: .05, psi: .1,
    samples: [
        // { acession: "SRR2513862", name: "ctrl1", group: 'WILD' },
        // { acession: "SRR2513863", name: "ctrl2", group: 'WILD' },
        // { acession: "SRR2513864", name: "ctrl3", group: 'WILD' },
        // { acession: "SRR2513867", name: "trt1", group: 'TREATED' },
        // { acession: "SRR2513868", name: "trt2", group: 'TREATED' },
        // { acession: "SRR2513869", name: "trt3", group: 'TREATED' }
    ],
    commands: [Command.model()]
}

const example_arab: IProject = Object.assign(Object.assign({}, example_fung), {
    name: "Project Arab", organism: "Arabidopsis",
    genome: 'https://ftp.ncbi.nlm.nih.gov/genomes/all/GCF/000/001/735/GCF_000001735.4_TAIR10.1/GCF_000001735.4_TAIR10.1_genomic.fna.gz',
    anotattion: 'https://ftp.ncbi.nlm.nih.gov/genomes/all/GCF/000/001/735/GCF_000001735.4_TAIR10.1/GCF_000001735.4_TAIR10.1_genomic.gff.gz',
    proteome: 'https://ftp.ncbi.nlm.nih.gov/genomes/all/GCF/000/001/735/GCF_000001735.4_TAIR10.1/GCF_000001735.4_TAIR10.1_protein.faa.gz',
    transcriptome: 'https://ftp.ncbi.nlm.nih.gov/genomes/all/GCF/000/001/735/GCF_000001735.4_TAIR10.1/GCF_000001735.4_TAIR10.1_rna.fna.gz',
    samples: []
})

const example_hm: IProject = Object.assign(Object.assign({}, example_fung), {
    name: "Project Human", organism: "Humano",
    genome: 'https://ftp.ncbi.nlm.nih.gov/genomes/all/GCF/000/001/405/GCF_000001405.40_GRCh38.p14/GCF_000001405.40_GRCh38.p14_genomic.fna.gz',
    anotattion: 'https://ftp.ncbi.nlm.nih.gov/genomes/all/GCF/000/001/405/GCF_000001405.40_GRCh38.p14/GCF_000001405.40_GRCh38.p14_genomic.gff.gz',
    proteome: 'https://ftp.ncbi.nlm.nih.gov/genomes/all/GCF/000/001/405/GCF_000001405.40_GRCh38.p14/GCF_000001405.40_GRCh38.p14_protein.faa.gz',
    transcriptome: 'https://ftp.ncbi.nlm.nih.gov/genomes/all/GCF/000/001/405/GCF_000001405.40_GRCh38.p14/GCF_000001405.40_GRCh38.p14_rna.fna.gz',
    samples: []
})


const project = reactive(Project.model())
const load_project = ref()
const set_example = (x: any) => Object.assign(project, x == 1 ? example_hm : x == 2 ? example_arab : example_fung)
const new_smp = (t: string) => `${t}${project.samples.filter(x => x.group === t).length + 1}`
const terms = reactive({ a: false, b: false, c: false })
const projects = await Project.api.list();
const salvando = ref(false)
const sel = ref(false)
const zip = ref(true);
const isOpen = ref(false)
const pname = ref();
const btn_baixar = ref(false);
const btn_baixar_l = ref(false);
const jobs3 = ref({ total: 0, wait: 0, error: 0, success: 0, ended: 0, info: "", dtime: "" })
const logs3 = ref("")
const show_logs = ref(false)


const btn_baixar4 = ref(false);
const btn_baixar_l4 = ref(false);
const jobs4 = ref({ total: 0, wait: 0, error: 0, success: 0, ended: 0, info: "", dtime: "" })
const logs4 = ref("")
const show_logs4 = ref(false)

const items = reactive([{
    label: '1. Terms and conditions',
    icon: 'i-heroicons-information-circle',
    defaultOpen: true, slot: 'terms'
}, {
    label: '2. Project setup',
    icon: 'i-heroicons-pencil-square',
    disabled: true, slot: 'configure'
}, {
    label: '3. Download data',
    icon: 'i-heroicons-arrow-down-tray',
    disabled: true, slot: 'download'
}, {
    label: '4. Process and integration',
    icon: 'i-heroicons-wrench-screwdriver',
    disabled: true, slot: 'process'
}, {
    label: '5. Results explorer',
    icon: 'i-heroicons-square-3-stack-3d',
    disabled: true, slot: 'results'
}])

function set_prj() {
    const s = Object.assign(project, load_project.value).status;
    terms.a = terms.b = terms.c = true;  ///  1. 
    items[1].disabled = s < 2;           ///  2.
    items[2].disabled = s < 3;           ///  3.
    items[3].disabled = s < 4;           ///  4.
    items[4].disabled = s < 5;           ///  5.
    sel.value = true;

    if (!items[3].disabled) {
        // acompanhar(project.commands.filter(c => c.meta === "step4").map(x => x.id), btn_baixar, btn_baixar_l, hab_prc);
        // stp1_cc.value = 100;
        //return;
        acompanhar(jobs4, logs4,
            project.commands.filter(c => c.meta === "step4").map(x => x.id), btn_baixar4, btn_baixar_l4, hab_prc);
    }

    if (!items[2].disabled) {
        acompanhar(jobs3, logs3,
            project.commands.filter(c => c.meta === "step3").map(x => x.id), btn_baixar, btn_baixar_l, hab_prc);
    }

}

const terms_review = () => {
    if (terms.a && terms.b && terms.c) {
        project.status = 2;
        items[1].disabled = false;
    }
};

const validate = (state: any): FormError[] => {
    const errors = []

    if (!state.name || /^[a-z0-9_ ]+$/i.test(state.name) || state.name < 3 || state.name > 50)
        errors.push({ path: 'name', message: 'Required a valide name' })

    if (!state.control || /^[a-z0-9_]+$/i.test(state.control) || state.control < 3 || state.control > 50)
        errors.push({ path: 'control', message: 'Required a valide control label' })

    if (!state.treatment || /^[a-z0-9_]+$/i.test(state.treatment) || state.treatment < 3 || state.treatment > 50)
        errors.push({ path: 'treatment', message: 'Required a valide treatment label' })

    if (!state.genome || state.genome.length < 4 || state.genome.length > 1000)
        errors.push({ path: 'genome', message: 'Type a valid genome FASTA file url or path' })
    if (!state.anottation || state.genome.length < 4 || state.genome.length > 1000)
        errors.push({ path: 'anottation', message: 'Type a valid genome GFF3 file url or path' })
    if (!state.proteome || state.genome.length < 4 || state.genome.length > 1000)
        errors.push({ path: 'proteome', message: 'Type a valid genome FAA file url or path' })
    if (!state.transcriptome || state.genome.length < 4 || state.genome.length > 1000)
        errors.push({ path: 'transcriptome', message: 'Type a valid genome FNA file url or path' })

    return [] ///errors
}

async function onSubmit(event: FormSubmitEvent<any>) {
    salvando.value = true;
    project.status = 3;
    Project.api.create(project)
        .then(() => {
            items[2].disabled = false;
            btn_baixar.value = true;
            toast.add({
                id: 'save_prj',
                title: `Project [${project.id}]: ${project.name} created`,
                description: `Your project ${project.path} was created now.`,
                icon: 'i-heroicons-rocket-launch',
                color: "emerald", timeout: 10000
            })
        })
        .catch(() => {
            project.status = 2;
            toast.add({
                id: 'error_save_prj',
                title: 'Error',
                description: 'Fail on save the project. Try again',
                icon: 'i-heroicons-exclamation-triangle',
                color: "rose", timeout: 20000
            });
        })
        .finally(() => salvando.value = false)
}

function remover() {
    if (pname.value === project.name) {
        Project.api.delete(project.id || NaN).then(() => {
            alert(`Project [${project.id}] "${project.name}" => ${project.path} was permanentmently deleted from server.`)
            window.location.href = window.location.href;
        })
    }
}

async function acompanhar(jobs: any, logs: any, follow: any[], btn1: { value: any }, btn2: { value: any }, hab: () => void, timex = 1000) {

    if (follow.filter(x => x && x > 0).length < 1) {
        btn1.value = true;
        return;
    }

    btn1.value = !(btn2.value = true);
    var limit = timex > 9999 ? 360 : 3600
    const parar = setInterval(() => {
        limit--;
        Project.api.find(project.id || NaN)
            .then(prj => {

                const cms = prj.commands.filter(c => follow.includes(c.id))
                const total = cms.length;
                const term = cms.reduce((a, b) => a + (b.end ? 1 : 0), 0)
                const ss = cms.reduce((a, b) => a + (b.success ? 1 : 0), 0)
                const run = cms.filter(x => (!x.end) && (!x.err) && (x.status == "running"))

                if (term < total)
                    jobs.value.info = (run.length > 0 ? run.map(x => x.info).join(", ").substring(0, 30) : 'Server busy') + " ...";
                else
                    jobs.value.info = 'finished all jobs.';

                jobs.value.total = total;
                jobs.value.ended = term;
                jobs.value.wait = run.length;
                jobs.value.success = ss;
                jobs.value.error = term - ss;

                const f = Math.min(...cms.map(c => new Date(c.started_at || Date.now()).getTime()))
                const l = Math.max(...cms.map(c => new Date(c.ended_at || Date.now()).getTime()));
                const dt = l - f;
                const mint = dt > 100000;
                jobs.value.dtime = `${Math.round(dt / (mint ? 60000 : 1000))} ${mint ? 'min' : 's'}.`;

                if (total == term || limit < 0) {

                    logs.value = cms.filter(j => j.end && !j.success).map(c => {
                        var l = `Job [${c.id} / tsp(${c.tsp})]: ${c.info}\n`;
                        l += `Status ${c.success ? "OK" : "ERR"}: ${c.status}\n`
                        l += "LOG: \n" + c.log + '\n';
                        l += "OUT: \n" + c.out + '\n';
                        l += "ERR: \n" + c.err + '\n';
                        return l;
                    }).join("\n-------\n\n\n");

                    clearInterval(parar);
                    btn2.value = false;
                    if (total === term)
                        hab();

                } else if (limit == 3500) {
                    clearInterval(parar);
                    acompanhar(jobs, logs, follow, btn1, btn2, hab, 10000)
                } else {
                    btn1.value = !(btn2.value = true);
                }

            }).catch(_ => alert("Invalid project") + (window.location.href = window.location.href));
    }, timex)
}

async function copiar() {
    btn_baixar.value = false;
    const follow: any[] = [];

    const copy = async (a: string, b: string) =>
        new CMD_Copiar(project).from(a).to(b).step(3)
            .enqueue().then(x => {
                follow.push(x.id);
                if (zip.value)
                    new CMD_Unzip(project).file(b).wait(x)
                        .step(3).enqueue().then(x => follow.push(x.id));
            });

    await Promise.all([
        copy(project.anotattion, 'anotattion.gff3'),
        copy(project.transcriptome, 'transcriptome.fna'),
        copy(project.genome, 'genome.fasta'),
        copy(project.proteome, 'proteome.faa'),
        project.samples.map(sample => new CMD_Copiar(project)
            .from(sample.acession)
            .to(sample.name)
            .step(3).enqueue().then(x => follow.push(x.id)))
    ])

    acompanhar(jobs3, logs3, follow, btn_baixar, btn_baixar_l, hab_prc);

}

async function baixar() {
    btn_baixar.value = false;
    const follow: any[] = [];

    const download = async (a: string, b: string) =>
        new CMD_Baixar(project).from(a).to(b).step(3)
            .enqueue().then(x => {
                follow.push(x.id);
                if (zip.value)
                    new CMD_Unzip(project).file(b).wait(x)
                        .step(3).enqueue().then(x => follow.push(x.id));
            });

    await Promise.all([
        download(project.anotattion, 'anotattion.gff3'),
        download(project.transcriptome, 'transcriptome.fna'),
        download(project.genome, 'genome.fasta'),
        download(project.proteome, 'proteome.faa'),
        project.samples.map(sample => new CMD_Baixar(project)
            .from(sample.acession)
            .to(sample.name)
            .sra()
            .step(3).enqueue()
            .then(x => follow.push(x.id)))
    ])

    acompanhar(jobs3, logs3, follow, btn_baixar, btn_baixar_l, hab_prc);

}

function hab_prc() {

    btn_baixar.value = btn_baixar_l.value = false;
    btn_baixar4.value = !(btn_baixar_l4.value = false);

    project.status = 4;
    Project.api.update(project).then(prj => {
        Object.assign(project, prj);
        items[3].disabled = !(items[4].disabled = true);
        toast.add({
            id: 'down_prj',
            title: `Load files step`,
            description: `All files are on server folder now.`,
            icon: 'i-heroicons-arrow-down-on-square-stack',
            color: "emerald", timeout: 10000
        })
    })
}

async function process() {
    btn_baixar4.value = !(btn_baixar_l4.value = true);
    const follow: any[] = [];

    const stp1 = await new CMD_Qinput(project).fill().step(4).enqueue()
    follow.push(stp1.id);
       
    await new CMD_Qinput2(project).fill().step(4).wait(stp1).enqueue().then(
        x => follow.push(x.id)
    )

    // const hold: Promise<ICommand>[] = [];

    // await new CMD_Splitx(project).fill().step(4).enqueue().then(x => {
    //     follow.push(x.id);
    //     for (let I = 1; I <= 5; I++) {
    //         hold.push(new CMD_Qinput(project).fill()
    //             .genome("genome.fasta_pt" + I)
    //             .anotattion("anotattion.gff3_pt" + I).reorg(I * 1000)
    //             .step(4)
    //             .wait(x).enqueue().then(x => { follow.push(x.id); return x }));
    //     }
    // });
    // await Promise.all(hold);

    // await new CMD_Holder(project)
    //     .add(await hold[0])
    //     .add(await hold[1])
    //     .add(await hold[2])
    //     .add(await hold[3])
    //     .add(await hold[4])
    //     .step(4).enqueue().then(x => {
    //         follow.push(x.id);
    //         new CMD_Joinx(project)
    //             .fill().wait(x)
    //             .step(4).enqueue().then(x => follow.push(x.id));
    //     });

    acompanhar(jobs4, logs4, follow, btn_baixar4, btn_baixar_l4, hab_exp);
}

function hab_exp() {

}

</script>
<template>
    <UModal v-model="isOpen">
        <UCard :ui="{ ring: '', divide: 'divide-y divide-gray-100 dark:divide-gray-800' }">
            <template #header>
                <div class="flex items-center justify-between">
                    <h3 class="text-base font-semibold leading-6 text-gray-900 dark:text-white">
                        Remove existing project
                    </h3>
                    <UButton color="gray" variant="ghost" icon="i-heroicons-x-mark-20-solid" class="-my-1"
                        @click="isOpen = false" />
                </div>
            </template>
            <p class="text-slate-600">
                If you want to remove this project type its name bellow:
            </p>
            <p>
                <UInput placeholder="type here" class="my-2" v-model="pname" />
            </p>
            <template #footer>
                <div class="text-right">
                    <UButton class="mx-2" color="rose" @click="remover()">Confirm</UButton>
                    <UButton @click="isOpen = false" color="sky">Cancel</UButton>
                </div>
            </template>
        </UCard>
    </UModal>

    <div v-if="projects.length > 0" class="flex inline mx-32 mt-8">
        <USelectMenu v-model="load_project" :options="projects" class="w-48 mx-2" placeholder="Select an project" searchable
            searchable-placeholder="Search by name or organism" option-attribute="name" by="id" clear-search-on-close
            :search-attributes="['name', 'id', 'organism']" :disabled="sel" />
        <UButton icon="i-heroicons-arrow-down-on-square-stack" @click="set_prj" :disabled="sel || !load_project">
            Load project</UButton>
        <UButton icon="i-heroicons-arrow-top-right-on-square" class="mx-2" :to="`projects/${project.path}/results`"
            target="_blank" v-if="project.path">
            Go to project</UButton>
    </div>
    <p class="text-gray font-mono text-sm pt-4 text-slate-300 text-center">
        {{ project.path }}
    </p>

    <div class="flex justify-center">
        <UAccordion :items="items" class="p-4 mx-12 mt-6 bg-white rounded-lg max-w-4xl">

            <!-- etapa 1 -->
            <template #terms>
                <div class=" px-2">
                    <UCheckbox v-model="terms.a" required @change="terms_review()" :disabled="terms.a">
                        <template #label>
                            <span>
                                <b>Terms of licence: </b>I understand that GeneApp is owned by the UFV & UFMG,
                                and that my use of GeneApp is
                                restricted to non-commercial purposes. I also understand that GeneApp is open-source
                                software, and that the source code is available in a public repository. However, I may not
                                copy, edit, modify, or distribute GeneApp without the express written permission of the
                                owners or authors.
                            </span>
                        </template>
                    </UCheckbox>
                    <UCheckbox v-model="terms.b" class="mt-2" required @change="terms_review()" :disabled="terms.b">
                        <template #label>
                            <span>
                                <b>Terms of dependences:</b> I understand that GeneApp can execute other software as a
                                wrapper. However, each of these softwares has its own specific licenses that must be
                                observed by the user on a case-by-case basis.
                            </span>
                        </template>
                    </UCheckbox>
                    <UCheckbox v-model="terms.c" class="mt-2" required @change="terms_review()" :disabled="terms.c">
                        <template #label>
                            <span>
                                <b>Terms of use:</b> By using GeneApp, you acknowledge that projects created on the server
                                http://bioinfo.icb.ufmg.br/geneapp are publicly visible and will be deleted after 7 days or
                                during scheduled server maintenance. GeneApp uses cookies to track my activity and
                                preferences. I can disable cookies in my browser settings. The email address may be used to
                                consume NCBI and InterPro APIs. GeneApp does not save any personal data about me. GeneApp is
                                still under development. The results of any analysis performed with GeneApp should be
                                validated.
                            </span>
                        </template>
                    </UCheckbox>
                </div>
            </template>

            <!-- etapa 2 -->
            <template #configure>

                <UForm :validate="validate" :state="project" class="space-y-4 py-2 px-8" @submit="onSubmit">

                    <UCard>
                        <UFormGroup label="Project name" name="name">
                            <UInput v-model="project.name" :disabled="project.status !== 2" />
                        </UFormGroup>
                        <UFormGroup label="Organism" name="organism" class="mt-6">
                            <UInput v-model="project.organism" placeholder="ex.: Homo Sapiens" class="italic"
                                :disabled="project.status !== 2" />
                        </UFormGroup>

                        <UDivider label="Input files" class="my-6" />
                        <div class="flex items-center mt-2">
                            <UToggle v-model="project.online" class="mr-2" :disabled="project.status !== 2" />
                            Get from remote url
                        </div>
                        <UFormGroup label="Genome FASTA file" name="genome" class="mt-6">
                            <UInput v-model="project.genome" :disabled="project.status !== 2" />
                        </UFormGroup>
                        <UFormGroup label="Anotattion GFF3 file" name="anotattion" class="mt-6">
                            <UInput v-model="project.anotattion" :disabled="project.status !== 2" />
                        </UFormGroup>
                        <UFormGroup label="Transcripts FNA file" name="transcriptome" class="mt-6">
                            <UInput v-model="project.transcriptome" :disabled="project.status !== 2" />
                        </UFormGroup>
                        <UFormGroup label="Proteome FAA file" name="proteome" class="mt-6">
                            <UInput v-model="project.proteome" :disabled="project.status !== 2" />
                        </UFormGroup>

                        <UDivider label="Contrast group" class="my-6" />
                        <USelect v-model="project.library" :options="LBS" placeholder="Library layout" class="w-48"
                            color="primary" :disabled="project.status !== 2" />
                        <div class="w-full flex justify-around mt-6">

                            <div class="text-center w-1/3 p-2">
                                <UFormGroup label="Label for control" name="control" class="mb-4">
                                    <UInput v-model="project.control"
                                        :disabled="project.status !== 2 || project.samples.filter(x => x.group === project.control).length > 0" />
                                </UFormGroup>

                                <div v-for="sample in project.samples.filter(x => x.group === project.control)"
                                    class="pt-2 mx-4 w-full flex justify-around">
                                    <div class="w-2/3">
                                        <UInput v-model="sample.acession" :placeholder="sample.name"
                                            :disabled="project.status !== 2" />
                                    </div>
                                    <div class="w-1/3">
                                        <UButton icon="i-heroicons-x-mark" color="red" variant="soft"
                                            v-if="project.status === 2"
                                            @click="project.samples = project.samples.filter(x => x !== sample)" />
                                    </div>
                                </div>
                                <UButton icon="i-heroicons-plus" color="emerald" variant="soft" class="m-6"
                                    v-if="project.status === 2"
                                    @click="project.samples.push({ name: new_smp(project.control), group: project.control } as ISample)">
                                    Sample
                                </UButton>
                            </div>

                            <div class="text-center w-1/3 p-2">
                                <UFormGroup label="Label for treatment" name="treatment" class="mb-4">
                                    <UInput v-model="project.treatment"
                                        :disabled="project.status !== 2 || project.samples.filter(x => x.group === project.treatment).length > 0" />
                                </UFormGroup>

                                <div v-for="sample in project.samples.filter(x => x.group === project.treatment)"
                                    class="pt-2 mx-4 w-full flex justify-around">
                                    <div class="w-2/3">
                                        <UInput v-model="sample.acession" :placeholder="sample.name"
                                            :disabled="project.status !== 2" />
                                    </div>
                                    <div class="w-1/3">
                                        <UButton icon="i-heroicons-x-mark" color="red" variant="soft"
                                            v-if="project.status === 2"
                                            @click="project.samples = project.samples.filter(x => x !== sample)" />
                                    </div>
                                </div>
                                <UButton icon="i-heroicons-plus" color="emerald" variant="soft" class="m-6"
                                    v-if="project.status === 2"
                                    @click="project.samples.push({ name: new_smp(project.treatment), group: project.treatment } as ISample)">
                                    Sample
                                </UButton>
                            </div>

                        </div>

                        <UDivider label="Params configuration" class="my-6" />

                        <div class="w-full flex justify-around">
                            <div class="w-1/3 p-2">
                                <UCheckbox v-model="project.fast" name="fast" label="Enable fast mode"
                                    :disabled="project.status !== 2" />

                                <UFormGroup label="Read length" hint="used in rMATS" class="mt-6">
                                    <UInput type="number" min="10" max="1000" v-model="project.rmats_readLength"
                                        :disabled="project.status !== 2" />
                                </UFormGroup>
                                <UFormGroup label="PSI" hint="at least to DAS" class="mt-6">
                                    <UInput type="number" min="0" max="9" step=".0000001" v-model="project.psi"
                                        :disabled="project.status !== 2" />
                                </UFormGroup>
                                <UFormGroup label="Qvalue" hint="FDR adjusted Pvalue" class="mt-6">
                                    <UInput type="number" min="0" max="2" step=".0000000000001" v-model="project.qvalue"
                                        :disabled="project.status !== 2" />
                                </UFormGroup>
                            </div>
                            <div class="text-center w-1/3">
                                <div class=" border-solid border-2 border-indigo-100 rounded-md p-4">
                                    <UFormGroup label="CPU" :hint="`${project.threads}`">
                                        <URange :min="1" :max="runtimeConfig.public.CPU" v-model="project.threads"
                                            :disabled="project.status !== 2" />
                                    </UFormGroup>
                                    <UFormGroup label="RAM" :hint="`${project.ram}`" class="mt-6">
                                        <URange :min="1" :max="runtimeConfig.public.RAM" v-model="project.ram"
                                            :disabled="project.status !== 2" />
                                    </UFormGroup>
                                    <UFormGroup label="Disk" :hint="`${project.disk}`" class="mt-6">
                                        <URange :min="1" :max="runtimeConfig.public.DISK" v-model="project.disk"
                                            :disabled="project.status !== 2" />
                                    </UFormGroup>
                                </div>
                            </div>
                        </div>

                        <template #footer>
                            <div class="flex justify-around">
                                <UButton v-if="sel" icon="i-heroicons-trash" color="red" @click="isOpen = true">
                                    Delete project
                                </UButton>
                                <UButton v-else icon="i-heroicons-trash" color="red" @click="project = Project.model()"
                                    :disabled="project.status !== 2">
                                    Clear from
                                </UButton>
                                <UButton type="submit" icon="i-heroicons-check" :loading="salvando"
                                    :disabled="project.status !== 2">
                                    Save project
                                </UButton>
                                <UButton icon="i-heroicons-bolt" color="emerald" @click="set_example(1)"
                                    :disabled="project.status !== 2">
                                    Load H
                                </UButton>
                                <UButton icon="i-heroicons-bolt" color="emerald" @click="set_example(2)"
                                    :disabled="project.status !== 2">
                                    Load A
                                </UButton>
                                <UButton icon="i-heroicons-bolt" color="emerald" @click="set_example(3)"
                                    :disabled="project.status !== 2">
                                    Load F
                                </UButton>
                            </div>
                        </template>
                    </UCard>
                </UForm>
            </template>

            <!-- etapa 3 -->
            <template #download>
                <div class="px-8">
                    <UAlert v-if="project.online" icon="i-heroicons-information-circle" color="sky" variant="subtle"
                        class="my-6" title="Files will be downloaded from the internet"
                        description="Please make sure that the file is on an allowed server, the URL is simple, and the file is compressed in the .gz format and extension." />

                    <UAlert v-else icon="i-heroicons-information-circle" color="sky" variant="subtle" class="my-6"
                        title="Files will be copied from data/projects/inputs to project folder"
                        description="The system will be copying files from the data/projects/inputs folder to the project folder. Please make sure that each file is in the correct format, not ziped, and has a simple name." />

                    <UCheckbox v-model="zip" :disabled="!btn_baixar" class="my-4">
                        <template #label>
                            <span class="italic">
                                Files were compressed with <code>zip</code>, <code>gzip</code> or <code>tar.gz</code>
                            </span>
                        </template>
                    </UCheckbox>

                    <UButton v-if="project.online" @click="baixar" icon="i-heroicons-arrow-down-tray" class="my-4"
                        :loading="btn_baixar_l" :disabled="!btn_baixar">Download input files</UButton>

                    <UButton v-else @click="copiar" icon="i-heroicons-document-duplicate" :loading="btn_baixar_l"
                        :disabled="!btn_baixar" class="my-4">
                        Copy input Files</UButton>

                    <UMeterGroup :max="jobs3.total" size="md" class="my-4" v-if="jobs3.total > 0">
                        <template #indicator>
                            <div class="flex gap-1.5 justify-between text-sm">
                                <p>
                                    <UBadge color="sky" variant="subtle" class="mr-2">{{ jobs3.dtime }}</UBadge> {{
                                        jobs3.info }}
                                </p>
                                <p class="text-gray-500 dark:text-gray-400">
                                    {{ jobs3.ended }} of {{ jobs3.total }}
                                </p>
                            </div>
                        </template>

                        <UMeter :value="jobs3.success" color="green" label="Sucess" icon="i-heroicons-check" />
                        <UMeter :value="jobs3.error" color="rose" label="Some Error"
                            icon="i-heroicons-exclamation-triangle" />
                        <UMeter :value="jobs3.wait" color="gray" label="Runing" icon="i-heroicons-clock" />
                    </UMeterGroup>



                    <UButton v-if="logs3 !== ''" @click="show_logs = !show_logs" icon="i-heroicons-eye" class="my-4">Show
                        logs</UButton>

                    <UTextarea class="text-sm tracking-tight leading-none break-all" v-if="show_logs" disabled resize
                        color="rose" variant="outline" v-model="logs3" :rows="10" size="md" />

                </div>
            </template>


            <!-- etapa 4 -->
            <template #process>
                <UButton @click="process" icon="i-heroicons-arrow-path-rounded-square" :loading="btn_baixar_l4"
                    :disabled="!btn_baixar4" class="my-4">Build input files</UButton>

                <UMeterGroup :max="jobs4.total" size="md" class="my-4" v-if="jobs4.total > 0">
                    <template #indicator>
                        <div class="flex gap-1.5 justify-between text-sm">
                            <p>
                                <UBadge color="sky" variant="subtle" class="mr-2">{{ jobs4.dtime }}</UBadge> {{ jobs4.info
                                }}
                            </p>
                            <p class="text-gray-500 dark:text-gray-400">
                                {{ jobs4.ended }} of {{ jobs4.total }}
                            </p>
                        </div>
                    </template>

                    <UMeter :value="jobs4.success" color="green" label="Sucess" icon="i-heroicons-check" />
                    <UMeter :value="jobs4.error" color="rose" label="Some Error" icon="i-heroicons-exclamation-triangle" />
                    <UMeter :value="jobs4.wait" color="gray" label="Running" icon="i-heroicons-clock" />
                </UMeterGroup>

                <UButton v-if="logs4 !== ''" @click="show_logs4 = !show_logs4" icon="i-heroicons-eye" class="my-4">Show
                    logs</UButton>

                <UTextarea class="text-sm tracking-tight leading-none break-all" v-if="show_logs4" disabled resize
                    color="rose" variant="outline" v-model="logs4" :rows="10" size="md" />

            </template>
        </UAccordion>
    </div>
</template>


