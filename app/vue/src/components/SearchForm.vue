<script setup lang="ts">
import { ref } from "vue";
import { useRouter } from "vue-router";
import { defineProps } from "vue";

const router = useRouter();

interface Props {
    inputText: string;
}
const props = defineProps<Props>();

const query = ref(props.inputText);
const tmpStr = ref("aaaaa");
const clickSearchBottun = (): void =>{
    console.log("clicked search");
    router.push({path: '/searchResult', query:{queryText:query.value}});   
    // router.push({path: '/searchResult'});   
};
</script>

<template>
    <form class="w-full md:max-w-md flex gap-2 pb-3">
        <textarea 
            placeholder="The aim of this research is to build a model for recommending papers that can explain the reasons for the recommendation. We propose a method based on Abstract Classification and the Paper Embedding Transfomer model." 
            class="w-full flex-1 bg-gray-50 text-gray-800 placeholder-gray-500 border focus:ring ring-indigo-300 rounded outline-none transition duration-100 px-3 py-2"
            v-model="query"
        ></textarea>
    </form>
    <button 
        class="inline-block bg-indigo-500 hover:bg-indigo-600 active:bg-indigo-700 focus-visible:ring ring-indigo-300 text-white text-sm md:text-base font-semibold text-center rounded outline-none transition duration-100 px-8 py-2 pt"
        v-on:click="clickSearchBottun"
    >
    Search
    </button>
</template>

<style scoped>
</style>