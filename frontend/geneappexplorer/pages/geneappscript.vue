
<script setup lang="ts">
import type { FormError, FormSubmitEvent } from '#ui/types'
import { Projeto, type IProjeto } from '../composables/models/projeto';
import type { ISample } from '../composables/models/sample';
const runtimeConfig = useRuntimeConfig()

const toast = useToast()
const LBS = ['SHORT_PAIRED', 'SHORT_SINGLE', 'LONG_SINGLE']
const example: IProjeto = {
    name: "Project EXPPATOG",
    control: "WILD",
    treatment: "TREATED",
    organism: "Candida albicans",
    online: true, rmats_readLength: 50,
    genome: "https://ftp.ncbi.nlm.nih.gov/genomes/all/GCF/000/182/965/GCF_000182965.3_ASM18296v3/GCF_000182965.3_ASM18296v3_genomic.fna.gz",
    anotattion: "https://ftp.ncbi.nlm.nih.gov/genomes/all/GCF/000/182/965/GCF_000182965.3_ASM18296v3/GCF_000182965.3_ASM18296v3_genomic.gff.gz",
    proteome: "https://ftp.ncbi.nlm.nih.gov/genomes/all/GCF/000/182/965/GCF_000182965.3_ASM18296v3/GCF_000182965.3_ASM18296v3_protein.faa.gz",
    transcriptome: "https://ftp.ncbi.nlm.nih.gov/genomes/all/GCF/000/182/965/GCF_000182965.3_ASM18296v3/GCF_000182965.3_ASM18296v3_rna.fna.gz",
    library: LBS[0],
    ctrl_samples: [
        { acession: "SRR2513862", name: "ctrl1" },
        { acession: "SRR2513863", name: "ctrl2" },
        { acession: "SRR2513864", name: "ctrl3" }],
    treat_samples: [
        { acession: "SRR2513867", name: "trt1" },
        { acession: "SRR2513868", name: "trt2" },
        { acession: "SRR2513869", name: "trt3" }],
    threads: 1, ram: 2, disk: 10, fast: false, qvalue: .05, psi: .1
}
const step = ref(0)
const terms = ref({ a: true, b: true, c: true })
const projeto = useProjeto();

const lst = ref([] as IProjeto[]) 
Projeto.api.list().then(rs => lst.value = rs);

const items = reactive([{
    label: '1. Terms and conditions',
    icon: 'i-heroicons-information-circle',
    defaultOpen: false, slot: 'terms'
}, {
    label: '2. Project setup',
    icon: 'i-heroicons-pencil-square',
    disabled: false, slot: 'configure'
}, {
    label: '3. Download data',
    icon: 'i-heroicons-arrow-down-tray',
    defaultOpen: true, disabled: false, slot: 'download'
}, {
    label: '4. Process and integration',
    icon: 'i-heroicons-wrench-screwdriver',
    disabled: true, slot: 'process'
}, {
    label: '5. Results explorer',
    icon: 'i-heroicons-square-3-stack-3d',
    disabled: true, slot: 'results'
}])

const terms_review = () => {
    if (terms.value.a && terms.value.b && terms.value.c) {
        step.value = 1;
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
    step.value = 2;
    // apiFetch('/projetos', {
    //     method: 'POST',
    //     body: JSON.stringify(projeto.value)
    // })
    Projeto.api.create(projeto.value)
    .then((nproj) => {
        projeto.value = nproj;
        step.value = 3;
        items[2].disabled = !(items[1].disabled = true);
        toast.add({
            id: 'save_prj',
            title: `Project [${projeto.value.id}]: ${projeto.value.name} created`,
            description: `Your project ${projeto.value.path} was created now.`,
            icon: 'i-heroicons-rocket-launch',
            color: "emerald", timeout: 10000
        })
    })
        .catch(() => {
            step.value = 1;
            toast.add({
                id: 'error_save_prj',
                title: 'Error',
                description: 'Fail on save the project. Try again',
                icon: 'i-heroicons-exclamation-triangle',
                color: "rose", timeout: 20000
            });
        })
}

function baixar() {
    apiFetch('/projetos', {
        method: 'PUT',
        body: JSON.stringify(projeto.value)
    }).then(() => {
        step.value = 3;
        items[2].disabled = !(items[1].disabled = true);
        toast.add({
            id: 'save_prj',
            title: `Project ${projeto.value.name} created`,
            description: 'Your project was created now.',
            icon: 'i-heroicons-rocket-launch',
            color: "emerald", timeout: 10000
        })
    })
}

</script>

<template>
    {{ lst  }}
    {{ projeto }}

    <div class="flex justify-center">
        <UAccordion :items="items" class="p-4 mx-12 mt-8 bg-white rounded-lg max-w-4xl">
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

            <template #configure>

                <UForm :validate="validate" :state="projeto" class="space-y-4 py-2 px-8" @submit="onSubmit">

                    <UCard>
                        <UFormGroup label="Project name" name="name">
                            <UInput v-model="projeto.name" :disabled="step > 1" />
                        </UFormGroup>
                        <UFormGroup label="Organism" name="organism" class="mt-6">
                            <UInput v-model="projeto.organism" placeholder="ex.: Homo Sapiens" class="italic"
                                :disabled="step > 1" />
                        </UFormGroup>

                        <UDivider label="Input files" class="my-6" />
                        <div class="flex items-center mt-2">
                            <UToggle v-model="projeto.online" class="mr-2" :disabled="step > 1" /> Get from remote url
                        </div>
                        <UFormGroup label="Genome FASTA file" name="genome" class="mt-6">
                            <UInput v-model="projeto.genome" :disabled="step > 1" />
                        </UFormGroup>
                        <UFormGroup label="Anotattion GFF3 file" name="anotattion" class="mt-6">
                            <UInput v-model="projeto.anotattion" :disabled="step > 1" />
                        </UFormGroup>
                        <UFormGroup label="Proteome FAA file" name="proteome" class="mt-6">
                            <UInput v-model="projeto.proteome" :disabled="step > 1" />
                        </UFormGroup>
                        <UFormGroup label="Transcripts FNA file" name="transcriptome" class="mt-6">
                            <UInput v-model="projeto.transcriptome" :disabled="step > 1" />
                        </UFormGroup>

                        <UDivider label="Contrast group" class="my-6" />
                        <USelect v-model="projeto.library" :options="LBS" placeholder="Library layout" class="w-48"
                            color="primary" :disabled="step > 1" />
                        <div class="w-full flex justify-around mt-6">
                            <div class="text-center w-1/3 p-2">
                                <UFormGroup label="Label for control" name="control" class="mb-4">
                                    <UInput v-model="projeto.control" :disabled="step > 1" />
                                </UFormGroup>

                                <div v-for="sample in projeto.ctrl_samples" class="pt-2 mx-4 w-full flex justify-around">
                                    <div class="w-2/3">
                                        <UInput v-model="sample.acession" :placeholder="sample.name" :disabled="step > 1" />
                                    </div>
                                    <div class="w-1/3">
                                        <UButton icon="i-heroicons-x-mark" color="red" variant="soft" :disabled="step > 1"
                                            @click="projeto.ctrl_samples = projeto.ctrl_samples.filter(x => x !== sample)" />
                                    </div>
                                </div>
                                <UButton icon="i-heroicons-plus" color="emerald" variant="soft" class="m-6"
                                    :disabled="step > 1"
                                    @click="projeto.ctrl_samples.push({ name: projeto.control + (projeto.ctrl_samples.length + 1) } as ISample)">
                                    Sample
                                </UButton>
                            </div>

                            <div class="text-center w-1/3 p-2">
                                <UFormGroup label="Label for treatment" name="treatment" class="mb-4">
                                    <UInput v-model="projeto.treatment" :disabled="step > 1" />
                                </UFormGroup>

                                <div v-for="sample in projeto.treat_samples" class="pt-2 mx-4 w-full flex justify-around">
                                    <div class="w-2/3">
                                        <UInput v-model="sample.acession" :placeholder="sample.name" :disabled="step > 1" />
                                    </div>
                                    <div class="w-1/3">
                                        <UButton icon="i-heroicons-x-mark" color="red" variant="soft" :disabled="step > 1"
                                            @click="projeto.treat_samples = projeto.treat_samples.filter(x => x !== sample)" />
                                    </div>
                                </div>
                                <UButton icon="i-heroicons-plus" color="emerald" variant="soft" class="m-6"
                                    :disabled="step > 1"
                                    @click="projeto.treat_samples.push({ name: projeto.treatment + (projeto.treat_samples.length + 1) } as ISample)">
                                    Sample
                                </UButton>
                            </div>

                        </div>

                        <UDivider label="Params configuration" class="my-6" />

                        <div class="w-full flex justify-around">
                            <div class="w-1/3 p-2">
                                <UCheckbox v-model="projeto.fast" name="fast" label="Enable fast mode"
                                    :disabled="step > 1" />

                                <UFormGroup label="Read length" hint="used in rMATS" class="mt-6">
                                    <UInput type="number" min="10" max="1000" v-model="projeto.rmats_readLength"
                                        :disabled="step > 1" />
                                </UFormGroup>
                                <UFormGroup label="PSI" hint="at least to DAS" class="mt-6">
                                    <UInput type="number" min="0" max="9" step=".0000001" v-model="projeto.psi"
                                        :disabled="step > 1" />
                                </UFormGroup>
                                <UFormGroup label="Qvalue" hint="FDR adjusted Pvalue" class="mt-6">
                                    <UInput type="number" min="0" max="2" step=".0000000000001" v-model="projeto.qvalue"
                                        :disabled="step > 1" />
                                </UFormGroup>
                            </div>
                            <div class="text-center w-1/3">
                                <div class=" border-solid border-2 border-indigo-100 rounded-md p-4">
                                    <UFormGroup label="CPU" :hint="`${projeto.threads}`">
                                        <URange :min="1" :max="runtimeConfig.public.CPU" v-model="projeto.threads"
                                            :disabled="step > 1" />
                                    </UFormGroup>
                                    <UFormGroup label="RAM" :hint="`${projeto.ram}`" class="mt-6">
                                        <URange :min="1" :max="runtimeConfig.public.RAM" v-model="projeto.ram"
                                            :disabled="step > 1" />
                                    </UFormGroup>
                                    <UFormGroup label="Disk" :hint="`${projeto.disk}`" class="mt-6">
                                        <URange :min="1" :max="runtimeConfig.public.DISK" v-model="projeto.disk"
                                            :disabled="step > 1" />
                                    </UFormGroup>
                                </div>
                            </div>
                        </div>

                        <template #footer>
                            <div class="flex justify-around">
                                <UButton icon="i-heroicons-trash" color="red" @click="projeto = Projeto.model()"
                                    :disabled="step > 1">
                                    Clear from
                                </UButton>
                                <UButton type="submit" icon="i-heroicons-check" :loading="step == 2" :disabled="step > 1">
                                    Save project
                                </UButton>
                                <UButton icon="i-heroicons-bolt" color="emerald" @click="projeto = example"
                                    :disabled="step > 1">
                                    Load example
                                </UButton>
                            </div>
                        </template>
                    </UCard>
                </UForm>
            </template>

            <template as="div" class="my-2 mx-8" #download>



                <UAlert v-if="projeto.online" icon="i-heroicons-information-circle" color="sky" variant="subtle"
                    title="Heads up!" description="infor se baixar tem q ser zipado" />

                <UAlert v-if="projeto.online" icon="i-heroicons-information-circle" color="sky" variant="subtle"
                    title="Heads up!" description="infor se copiar tem q ta na pasta ja descomp" />

                <UButton @click="baixar">Baixar</UButton>

                <UMeter  icon="i-heroicons-server" size="md" indicator label="CPU Load" :value="75.4" class="mt-6"/>

            </template>
        </UAccordion>
    </div>
</template>


