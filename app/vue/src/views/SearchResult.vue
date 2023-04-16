<script setup lang="ts">
import { ref, watch, watchEffect} from "vue";
import axios from 'axios';
import Header from "../components/Header.vue";
import SearchForm from "../components/SearchForm.vue";
import { useRouter } from "vue-router";
import {useRoute} from 'vue-router'

const router = useRouter();
const route = useRoute()

const inputText = ref(route.query.queryText as string);

// console.log(inputText)
interface Paper {
    title: string;
    abst: string;
    listShowAbst: string;
    isShowFullAbst: boolean;
}
const paperListInit: Paper[] = [] 
const paperList = ref(paperListInit);
const isLoading = ref(true);
function resolve() {
    console.log("Delayed for 3 second.");
}

async function getPaperList() {
    isLoading.value = true
    console.log(`getPaperList(): ${inputText.value}`);
    const path = 'http://localhost:5050/search';
    const params = {
        query: inputText.value
    };
    try {
        const res = await axios.post(path, params);
        paperList.value = res.data;
        // Piniaデータストアに格納

        for (let i = 0; i < paperList.value.length; ++i) {
            // console.log(paperList.value[i].abst)
            if (paperList.value[i].abst.length >= 200){
                paperList.value[i].listShowAbst = paperList.value[i].abst.substr(0,200) + " ..."
                paperList.value[i].isShowFullAbst = false
            } else {
                paperList.value[i].listShowAbst = paperList.value[i].abst;
                paperList.value[i].isShowFullAbst = true
            }
        }    
        // なんか計算してる風に1.5秒遅延させる
        // await new Promise(resolve => setTimeout(resolve, 1500))
        isLoading.value = false;
    } catch (error) {
        console.log(error);
        console.log(path)
    }
}
getPaperList();

watch(route, () => {
    inputText.value = route.query.queryText as string;
    getPaperList();
})

// console.log(`asyncの外: ${paperList.value.length}`)

// console.log(paperList);
// console.log(paperList.value)

const linkClick = ():void => {
    router.push('/paperDetail');   
};

const clickReadMore = (index: number):void => {
    paperList.value[index].isShowFullAbst = true
};

const clickFold = (index: number):void => {
    paperList.value[index].isShowFullAbst = false
};



</script>

<template>

    <Header />
    <SearchForm v-bind:inputText="inputText"/>

    <div v-if="isLoading" class="flex justify-center">
        <div class="animate-ping h-2 w-2 bg-blue-600 rounded-full"></div>
        <div class="animate-ping h-2 w-2 bg-blue-600 rounded-full mx-4"></div>
        <div class="animate-ping h-2 w-2 bg-blue-600 rounded-full"></div>
    </div>
    <div v-else v-for="paper, index in paperList" class="pb-4">
        <!-- {{paper }} -->
        <div class="max-w-4xl px-10 py-6 bg-white rounded-lg shadow-md">
            <div class="flex justify-between items-center">
                <!-- <span class="font-light text-gray-600">{{ data.date }}</span> -->
                <span class="font-light text-gray-600">2022</span>
                <!-- <a class="px-2 py-1 bg-gray-600 text-gray-100 font-bold rounded hover:bg-gray-500" href="#">{{ data.tag }}</a> -->
                <a class="px-2 py-1 bg-gray-600 text-gray-100 font-bold rounded hover:bg-gray-500" href="#">arXiv</a>
            </div>
            <div class="mt-2">
                <!-- <a class="text-2xl text-gray-700 fo?nt-bold hover:underline" href="#">{{ data.title }}</a> -->
                <a class="text-2xl text-gray-700 font-bold hover:underline" href="#" @click.prevent.stop="linkClick"
                    >{{ paper.title }}
                </a>
                <!-- <p class="mt-2 text-gray-600">{{ data.body }}</p> -->
                <!-- <p class="mt-2 text-gray-600">
                    The dominant sequence transduction models are based on complex recurrent or convolutional neural networks in an encoder-decoder configuration. The best performing models also connect the encoder and decoder through an attention mechanism. We propose a new simple network architecture, the Transformer, based solely on attention mechanisms, dispensing with recurrence and convolutions entirely. ...
                </p> -->
                <template v-if="!paper.isShowFullAbst">
                    <p class="mt-2 text-gray-600">{{ paper.listShowAbst }}</p>

                    <a @click.prevent.stop="clickReadMore(index)" class="text-blue-500 hover:underline" href="#">Read more</a>
                </template>
                <template v-else>
                    <p class="mt-2 text-gray-600">{{ paper.abst }}</p>

                    <a @click.prevent.stop="clickFold(index)" class="text-blue-500 hover:underline" href="#">fold</a>
                </template>

            </div>
            <div class="flex justify-between items-center mt-4">
                <div>
                    <div class="flex items-center" href="#">
                        <!-- <img class="mx-4 w-10 h-10 object-cover rounded-full hidden sm:block" :src="data.image" alt="avatar"> -->
                        <!-- <img class="mx-4 w-10 h-10 object-cover rounded-full hidden sm:block" :src="data.image" alt="avatar"> -->
                        <!-- <h1 class="text-gray-700 font-bold hover:underline">{{ data.userName }}</h1> -->
                        <h1 class="text-gray-700 text-2xl">Author</h1>
                    </div>
                </div>
            </div>
        </div>
    </div>


</template>

<style scoped>
</style>