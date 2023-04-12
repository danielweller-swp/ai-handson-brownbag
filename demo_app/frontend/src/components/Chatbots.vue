<script setup lang="ts">
import { ref } from 'vue'
import axios from 'axios'
import { BASE_URL } from '../../api'
import Chatbot from './Chatbot.vue'

const props = defineProps<{
  botNames: string[]
}>()

const initialBotResponse =
  Object.fromEntries(
    props.botNames
    .map(name => [name, ""])
  )

const botResponse = ref(initialBotResponse)

const fetchResponseFromBot = (botName: string, query: string) => {
  botResponse.value[botName] = "Loading..."
  axios
    .get(`${BASE_URL}/bot/${botName}/completion?query=${query}`)
    .then(r => botResponse.value[botName] = r.data)
}

const query = ref("")

const fetchDataFromApi = () =>
  props.botNames.forEach(botName => fetchResponseFromBot(botName, query.value))
</script>

<template>
  <div class="query-div">
    Query:<br/><el-input v-model="query" class="query"/>
    <el-button @click="fetchDataFromApi">Go!</el-button>
  </div>
  <div class="container">
    <div v-for="botName in props.botNames" class="child">
      <Chatbot :name="botName" :response="botResponse[botName]"/>
    </div>
  </div>
</template>
<style scoped>
.container {
  display: flex;
  flex-wrap: wrap;
  padding-bottom: 50px;
}

.child {
  flex: 1;
  width: 500px;
  height: 400px;
  margin-right: 10px;
  padding-right: 10px;
}

.query {
  width: 1000px;
  margin-right: 10px;
}

.query-div {
  margin-bottom: 50px;
}
</style>
