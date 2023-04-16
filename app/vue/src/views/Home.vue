<script setup lang="ts">
import Header from "../components/Header.vue"
import SearchForm from "../components/SearchForm.vue"



</script>

<template>
    <Header />
    <section class="flex flex-col lg:flex-row justify-between gap-6 sm:gap-10 md:gap-16">
      <!-- content - start -->
      <div class="xl:w-5/12 flex flex-col justify-center items-center lg:items-start sm:text-center lg:text-left lg:py-12 xl:py-24">
        <h1 class="text-black-800 text-4xl sm:text-5xl md:text-6xl font-bold mb-8 md:mb-12">Paper Recommendation System </h1>

        <p class="lg:w-4/5 text-gray-500 xl:text-lg leading-relaxed mb-8 md:mb-12">研究のアプローチや要旨を入力してください。関連する論文を推薦します。</p>
        <SearchForm v-bind:input-text="''"/>
      </div>
      <!-- content - end -->

      <!-- image - start -->
      <div class="xl:w-5/12 h-48 lg:h-auto bg-gray-100 overflow-hidden shadow-lg rounded-lg">
        <img src="https://images.unsplash.com/photo-1620206343767-7da98185edd4?auto=format&q=75&fit=crop&w=1000" loading="lazy" alt="Photo by Fakurian Design" class="w-full h-full object-cover object-center" />
      </div>
      <!-- image - end -->
    </section>


</template>

<style scoped>
</style>