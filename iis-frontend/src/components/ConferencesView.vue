<script setup>
import {onMounted, ref} from "vue";
import {axiosInstance} from "@/router";

const loading = ref(false)
const conferences = ref([])

 function fetchConferences() {
   loading.value = true
   axiosInstance.get('conferences/all')
     .then(response => {
       conferences.value = response.data
     })
     .catch(error => {
       console.error(error)
     })
     .finally(() => {
       loading.value = false
       console.log(conferences.value)
     })
 }

 onMounted(() => {
   fetchConferences()
 })
</script>

<template>

  <v-dialog v-model="dialog">
    <v-card>

    </v-card>
  </v-dialog>

  <v-container>
    <div class="my-2">
      <v-btn prepend-icon="mdi-plus">Přidat</v-btn>
    </div>
    <v-progress-linear v-if="loading" indeterminate></v-progress-linear>
      <v-list>
          <v-list-item v-for="conference in conferences" :key="conference.id">
            <v-card>
              <v-list-item-title>{{conference.name}}</v-list-item-title>
              <v-list-item-subtitle>{{conference.description}}</v-list-item-subtitle>
            </v-card>
          </v-list-item>
      </v-list>
  </v-container>
</template>

<style scoped lang="sass">

</style>
