<template>
  <h1>NUXT FRONTEEND GENEAPPEXPLORER</h1>
  <div>
    Genes:
    <ol >
      <li v-for="gene in genes">{{ gene }}</li>
    </ol>
  </div>
</template>
<script setup lang="ts">
const genes = await $fetch('/api/genes')
console.log(genes)
</script>