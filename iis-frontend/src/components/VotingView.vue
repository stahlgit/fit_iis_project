<script setup>
// get all conferences
import {onMounted, ref} from "vue";

const conferences = ref([])

onMounted(() => {
  fetchConferences()
})

function fetchConferences() {
  conferences.value = [
    {name: 'Conference 1', description: 'Description 1'},
    {name: 'Conference 2', description: 'Description 2'},
    {name: 'Conference 3', description: 'Description 3'},
  ]
}
</script>

<template>

</template>

<style scoped lang="sass">

</style>
