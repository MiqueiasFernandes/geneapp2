<script setup lang="ts">
const runtimeConfig = useRuntimeConfig()

</script>


<template>


{{ runtimeConfig.public }}

  <h1>NUXT FRONTEEND GENEAPP</h1>

  <header>
    <nav>
      <ul>
        <li><NuxtLink to="/about">About</NuxtLink></li>
        <li><NuxtLink to="/geneappscript">geneappscript</NuxtLink></li>
        <li><NuxtLink to="/geneappservice">geneappservice</NuxtLink></li>
        <li><NuxtLink to="/geneappexplorer">geneappexplorer</NuxtLink></li>
      </ul>
    </nav>
  </header>

  <UContainer>
  <NuxtPage />
</UContainer>
</template>