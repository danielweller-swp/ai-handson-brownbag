<script setup lang="ts">
defineProps<{
  name: string,
  response?: string
}>()
</script>

<template>
  <b>{{ name }}</b>
  <textarea class="response">{{ response ? response : "" }}</textarea>
</template>
<style scoped>
.response {
  height: 100%;
  width: 100%;
}
</style>