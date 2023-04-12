<script setup lang="ts">
import { computed, ref, onMounted } from 'vue'
import axios from 'axios'
import fileDownload from 'js-file-download'
import moment from 'moment'
import { BASE_URL } from '../../api'

type Word = {
    word: string
    startTime: string
    endTime: string
}

const words = ref<Word[]>([])
const transcriptText = computed(() => {
    return words.value.map(w => w.word).join(" ")
})
const transcriptLoading = ref(false)

const fetchWordsFromApi = () => {
    transcriptLoading.value = true

    axios
        .get(`${BASE_URL}/transcripts/words`)
        .then(r => {
            words.value = r.data
            transcriptLoading.value = false
        })
}


const selectedWords = ref<Word[]>([])
const getSelectedWords = (selectionEvent: any) => {
    if (!selectionEvent.anchorNode) {
        return []
    } else {
        const { startCharIx, endCharIx } = 
        selectionEvent.anchorOffset < selectionEvent.extentOffset ? 
            {
                startCharIx: selectionEvent.anchorOffset,
                endCharIx: selectionEvent.extentOffset
            } :
            {
                startCharIx: selectionEvent.extentOffset,
                endCharIx: selectionEvent.anchorOffset
            }

        const selectedWords : Word[] = []
        let currentCharIx = 0

        for (let i = 0; i < words.value.length; i++) {
            if (startCharIx <= currentCharIx && currentCharIx <= endCharIx) {
                selectedWords.push(words.value[i])
            }

            currentCharIx += words.value[i].word.length + 1
        }

        return selectedWords
    }
}
const getSoundBite = (e: any) => {
    console.log(selectedWords.value)

    const req = {
        words: selectedWords.value
    }

    axios
        .post(`${BASE_URL}/transcripts/excerpt`, req,
        {
            responseType: 'arraybuffer'
        })
        .then(r => fileDownload(r.data, "excerpt.mp3"))
}

const possibleSelectionChange = (e: any) => {
    const s = window.getSelection()
    selectedWords.value = getSelectedWords(s)
}

const secondStringToNumber = (seconds: string) => parseInt(seconds.substring(0, seconds.length))

const formatSeconds = (seconds: string) => moment.utc(secondStringToNumber(seconds)*1000).format('HH:mm:ss')

const wordsInTranscriptSelected = computed(() => selectedWords.value.length !== 0)

const selectedWordsTimeText = computed(() => {
    if (!wordsInTranscriptSelected.value) {
        return ""
    } else {
        const startTime = selectedWords.value[0].startTime
        const endTime = selectedWords.value[selectedWords.value.length-1].endTime
        return `${formatSeconds(startTime)} - ${formatSeconds(endTime)}`
    }
})

document.body.addEventListener('mouseup', possibleSelectionChange)
document.body.addEventListener('click', possibleSelectionChange)


const summary = ref("")
const summaryLoading = ref(false)

const fetchSummaryFromApi = () => {
  summaryLoading.value = true  
  axios
        .get(`${BASE_URL}/transcripts/summary`)
        .then(r => {
            summary.value = r.data
            summaryLoading.value = false
        })
}

const images=ref<string[]>([])
const imagesLoading = ref(false)

// https://docs.google.com/document/d/11WlzjBT0xRpQhP9tFMtxzd0q6ANIdHPUBkMV-YB043U/edit#heading=h.ippmydsv0wuh
const artStyles = [
  "digital art",
  "vector art",
  "low poly art",
]

const fetchImagesFromApi = () => {
  images.value = []
  imagesLoading.value = true
  artStyles.forEach(style => 
  axios
        .get(`${BASE_URL}/transcripts/image/${style}`)
        .then(r => {
            images.value.push(r.data)
            if (images.value.length == 3) {
              imagesLoading.value = false
            }
        })  
  )
  
}

onMounted(fetchWordsFromApi)
</script>

<template>
        <div class="transcript content-container">
            <h3>Transcript</h3>
            <span v-if="transcriptLoading"><i>Loading...</i></span>
            <span v-if="!transcriptLoading">{{  transcriptText }}</span>
        </div>
        <p>{{ selectedWordsTimeText }}</p>
        <el-button class="button" :disabled="!wordsInTranscriptSelected" @click="getSoundBite">Sound Bite</el-button>
        <div class="summary content-container">
            <h3>Summary</h3>
            <span v-if="summary == '' && !summaryLoading"><el-button @click="fetchSummaryFromApi">Get</el-button></span>
            <span v-if="summaryLoading"><i>Loading...</i></span>
            <span v-if="!summaryLoading">{{  summary }}</span>
        </div>
        <div class="images content-container">
            <el-button @click="fetchImagesFromApi">Get</el-button><br/>
            <span v-if="imagesLoading"><i>Loading...</i></span>
            <div class="image" v-for="image in images"><img :src="image"/></div>
        </div>
</template>
<style scoped>
.summary {
  height: 200px;
  overflow: auto;
  margin-top: 10px;
  margin-bottom: 10px;
}
.transcript {
  margin-top: 10px;
  margin-bottom: 10px;
  height: 610px;
  overflow: auto;
}
.images {
  margin-top: 10px;
  height: 300px;
  display: flex;
}
.image {
  margin-left: 20px;
  margin-right: 20px;
}

.content-container {
  border: 1px solid lightyellow;
  border-radius: 5px;
  padding: 10px;
  text-align: justify;
}
</style>
