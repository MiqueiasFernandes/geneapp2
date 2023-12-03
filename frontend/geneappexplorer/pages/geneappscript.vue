
<script setup lang="ts">
import type { FormError, FormSubmitEvent } from '#ui/types'
import { Projeto, type IProjeto } from '~/composables/models/projeto';


const salvou = ref(false);
const projeto = useProjeto();
const genes = await apiFetch('/genes') ///await $fetch('http://localhost:8000/api/genes')
console.log(genes)

const projetos = ref(await Projeto.api.list());

const validate = (state: any): FormError[] => {
    const errors = []
    if (!state.nome) errors.push({ path: 'nome', message: 'Insira um nome valido' })
    return errors
}

async function onSubmit(form: FormSubmitEvent<any>) {
    const projeto: IProjeto = form.data;
    apiFetch('/projetos', {
        method: 'POST',
        body: projeto
    }).then(() => (salvou.value = true) && Projeto.api.list().then(ps => projetos.value = ps))
}





</script>


<template>
    Projetos: {{ projetos }}

    <UForm :validate="validate" :state="projeto" class="space-y-4" @submit="onSubmit">
        <UCard class="w-96">
            <template #header>
                Criar novo projeto
            </template>
            <UFormGroup label="Nome" name="nome">
                <UInput v-model="projeto.nome" />
            </UFormGroup>

            <template #footer>
                <UButton type="submit" icon="i-heroicons-check" :disabled="salvou">

                    Salvar
                </UButton>
            </template>
        </UCard>
    </UForm>

    pagina geneappscript

    <div>
        Genes:
        <ol>
            <li v-for="gene in genes">{{ gene }}</li>
        </ol>
    </div>
</template>


