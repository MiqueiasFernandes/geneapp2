<script setup lang="ts">
import { profile } from './utils/env';


const paginas = [
  { nome: 'Guide', href: '/guide' },
  { nome: 'GeneappScript', href: '/geneappscript' },
  { nome: 'GeneappService', href: '/geneappservice' },
  { nome: 'GeneappExplorer', href: '/geneappexplorer' },
  { nome: 'About', href: '/about' },
]

console.log(`

               ....  FRONTEND  .....   ${profile()}
      ██████╗ ███████╗███╗   ██╗███████╗ █████╗ ██████╗ ██████╗ 
     ██╔════╝ ██╔════╝████╗  ██║██╔════╝██╔══██╗██╔══██╗██╔══██╗
     ██║  ███╗█████╗  ██╔██╗ ██║█████╗  ███████║██████╔╝██████╔╝
     ██║   ██║██╔══╝  ██║╚██╗██║██╔══╝  ██╔══██║██╔═══╝ ██╔═══╝ 
     ╚██████╔╝███████╗██║ ╚████║███████╗██║  ██║██║     ██║     
      ╚═════╝ ╚══════╝╚═╝  ╚═══╝╚══════╝╚═╝  ╚═╝╚═╝     ╚═╝     
                   version 2.0 2023 mikeias.net   

`)

</script>


<template>
  <nav class="bg-gray-800 fixed w-full shadow z-10">
    <div class="max-w-7xl mx-auto px-2 sm:px-6 lg:px-8">
      <div class="relative flex items-center justify-between h-14">
        <div class="flex-1 flex items-center justify-center sm:items-stretch sm:justify-start">
          <div class="flex-shrink-0 flex items-center">
            <UButton square to="/" icon="i-heroicons-beaker-solid" color="black" variant="ghost"
              class="text-white transition ease-in-out delay-150 hover:scale-110 duration-300"></UButton>
          </div>

          <div class="hidden sm:block sm:ml-6">
            <div class="flex space-x-4">
              <ULink :to="pagina.href" v-for="pagina in paginas" class="px-3 py-2 rounded-md text-sm font-medium"
                active-class="bg-primary text-white" inactive-class="text-gray-300 hover:bg-gray-700 hover:text-white"> {{
                  pagina.nome }} </ULink>
            </div>
          </div>
          <div class="w-full right-0 flex items-center justify-end">
            <UBadge color="amber" variant="solid" label="DEV" v-if="is_dev()" />
          </div>
        </div>
      </div>
    </div>
  </nav>

  <div class="bg-gray-100 pt-16">
    <UContainer>
      <NuxtPage />
    </UContainer>
  </div>


  <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1440 320" class="bg-gray-800 fill-gray-100">
    <path fill-opacity="1"
      d="M0,128L34.3,154.7C68.6,181,137,235,206,234.7C274.3,235,343,181,411,186.7C480,192,549,256,617,282.7C685.7,309,754,299,823,250.7C891.4,203,960,117,1029,101.3C1097.1,85,1166,139,1234,154.7C1302.9,171,1371,149,1406,138.7L1440,128L1440,0L1405.7,0C1371.4,0,1303,0,1234,0C1165.7,0,1097,0,1029,0C960,0,891,0,823,0C754.3,0,686,0,617,0C548.6,0,480,0,411,0C342.9,0,274,0,206,0C137.1,0,69,0,34,0L0,0Z">
    </path>
  </svg>

  <div class="bg-gray-800 text-white">
    <div class="-mt-0 mb-20 w-100 text-right md:-mt-16">
      <span class="bg-slate-50 rounded-full p-4 mx-16 text-slate-500 font-bold">
        Versão 2.0
      </span>
    </div>
    <div class="px-4 py-4 flex justify-center">
      <span class="text-lg font-extrabold">
        Direitos registrados a UFMG & UFV - permitido uso apenas não comercial - para fins de pesquisa
      </span>
    </div>
    <div class="px-4 py-4 flex justify-center">
      <span class="text-sm font-extrabold">
        Desenvolvido para o capitulo III da tese de doutorado de MF submetida ao PPG Bioinformatica ICB/UFMG
      </span>
    </div>
  </div>

  <UNotifications />
</template>