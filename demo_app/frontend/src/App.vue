<script setup lang="ts">
import Chatbots from './components/Chatbots.vue'
import TextAnalysis from './components/TextAnalysis.vue'
import Transcripts from './components/Transcripts.vue'

const generalBotNames = [
  "CamachoBot",
  "AnticapitalistBot",
  "NeoConBot",
  "MundlBot",
  "EmojiBot"  
]

const specializedKnowledgeBotNames = [
  "TrustBot",
  "EmployeeBot",
  "DocumentDbBot"
]

</script>

<template>
  <main>
    <el-tabs>
      <el-tab-pane label="General Chatbots">
        <Chatbots :bot-names="generalBotNames" />
      </el-tab-pane>
      <el-tab-pane label="Specialized Chatbots">
        <Chatbots :bot-names="specializedKnowledgeBotNames" />
      </el-tab-pane>      
      <el-tab-pane label="Text Analysis">
        <TextAnalysis />
      </el-tab-pane>
      <el-tab-pane label="Transcripts">
        <Transcripts />
      </el-tab-pane>
    </el-tabs>
  </main>
</template>
<style scoped>
main {
  width: 100%;
  margin: 0px;
  padding: 0px;
}

.el-tabs {
  width: 1160px;
  height: 1400px;
}

.el-tab-pane {
  width: 100%;
  height: 1400px;
}
</style>
<style>
.el-tabs__item {
  color: grey;
}
</style>