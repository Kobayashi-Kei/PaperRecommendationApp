<script setup lang="ts">
import { ref } from 'vue';
import axios from 'axios';

const inputText = ref("InputText");
const paperList = ref({});

const getPaperList = (): void => {
    // const path = 'http://localhost:5050/search/'+  inputText.value;
    const path = 'http://localhost:5050/search';
    const params = {
        text: inputText.value
    };
    // const queryParams = new URLSearchParams(params);
    // const urlFull = `${path}?${queryParams}`;
    // axios.post(urlFull)
    axios.post(path, params)
        .then(response => {
            paperList.value = response.data.paperList;
        })
        .catch(error => {
            console.log(error)
            console.log(path)
            // console.log(urlFull)
        })
};

const inputSearchText = ref("こんにちは");
const onFormSubmit = (): void => {
    console.log("Submit")
}

</script>

<template>
    <div>
        <form action="#" v-on:submit.prevent="onFormSubmit">
            <div class="mb-3">
                <label for="inputText" class="form-label">検索する文章を入力してください</label>
                <textarea type="" v-model="inputSearchText" class="form-control" id="inputText"
                    aria-describedby="emailHelp"></textarea>
            </div>
            <button type="submit" class="btn btn-primary">Submit</button>
        </form>
        <button v-on:click="getPaperList">論文を取得する</button>

        <!-- <p>Paper List from backend: {{ paperList }}</p> -->
        <div class="list-group">
            <div v-for="paper in paperList">
                {{paper }}
            </div>
            <a href="#" class="list-group-item list-group-item-action active" aria-current="true">
                The current link item
            </a>
            <a href="#" class="list-group-item list-group-item-action">A second link item</a>
            <a href="#" class="list-group-item list-group-item-action">A third link item</a>
            <a href="#" class="list-group-item list-group-item-action">A fourth link item</a>
            <a href="#" class="list-group-item list-group-item-action disabled" tabindex="-1" aria-disabled="true">A
                disabled link item</a>
        </div>
    </div>

   

</template>

<style scoped>
</style>