<script setup lang="ts">
import { ref, computed } from 'vue'
import { Radar } from 'vue-chartjs'
import 'chart.js/auto'
import axios from 'axios';
import { BASE_URL } from '../../api'

type TextAnalysis = {
  categorization: {
    "Food": number
    "Science & Technology": number
    "Nature": number
    "Sports": number    
    "Art": number
  },
  keywords: string[]
}

const text = ref("")
const analysis = ref<TextAnalysis>({
  categorization: {
    "Food": 0,
    "Science & Technology": 0,
    "Nature": 0,
    "Art": 0,
    "Sports": 0
  },
  keywords: []  
})

const data = computed(() => ({
  labels: Object.keys(analysis.value.categorization),
  datasets: [{
    label: 'Text Analysis',
    data: Object.values(analysis.value.categorization),
  }]
}))

const options = {
  elements: {
    line: {
      borderWidth: 3
    }
  },
  scales: {
    r: {
      ticks: {
        backdropColor: '#1E1E1E',
      },
      grid: {
        color: '#706d6d'
      },
      angleLines: {
        color: '#706d6d'
      },
      suggestedMin: 0,
      suggestedMax: 100
    }
  }
}

const fetchAnalysis = () => {
  axios
    .post(`${BASE_URL}/text/analysis`, { text: text.value })
    .then(r => analysis.value = r.data)
}
</script>

<template>
  <div class="container">
    <div class="child">
      <textarea class="text-input" v-model="text"></textarea>
      <br/>
      <el-button @click="fetchAnalysis">Analyse</el-button>
    </div>
    <div class="child">
      <Radar :data="data" :options="options"/>
      <div v-for="keyword in analysis.keywords" class="keyword">{{ keyword }}</div>
    </div>
  </div>
</template>
<style scoped>
.text-input {
  height: 700px;
  width: 500px;
}

.container {
  display: flex;
  flex-wrap: wrap;
}

.child {
  flex: 1;
  width: 500px;
  height: 500px;
  margin-right: 10px;
  padding-right: 10px;
}

.keyword {
  display: block;
  border: 1px solid yellowgreen;
  border-radius: 5px;
  padding: 5px;
  margin: 5px;
  text-align: center;
}
</style>