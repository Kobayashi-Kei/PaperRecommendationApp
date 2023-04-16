<script setup lang="ts">
import { ref } from "vue";
import Header from "../components/Header.vue";
import SearchForm from "../components/SearchForm.vue";
import { useRouter } from "vue-router";

const router = useRouter();



// データストアから論文の詳細を取得してTempleteに渡す

const backTo = ():void => {
    router.push('/searchResult');   
}

</script>

<template>
    <Header />
    <SearchForm />

    <!-- データストアからのデータを表示する -->
    <div class="mt-3 mb-3">
        論文の詳細
    </div>
    
    <button 
        class="inline-block bg-indigo-500 hover:bg-indigo-600 active:bg-indigo-700 focus-visible:ring ring-indigo-300 text-white text-sm md:text-base font-semibold text-center rounded outline-none transition duration-100 px-8 py-2 pt"
        v-on:click="backTo"
    >
    Back
    </button>
</template>

<style scoped>
</style>