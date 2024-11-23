<script setup>
import { ref, onMounted } from 'vue';

const myPresentations = ref([]);

function getPresentations() {

}

</script>

<template>
  <div class="my-2">
    <v-btn prepend-icon="mdi-plus">Přidat</v-btn>
  </div>
  <v-progress-linear v-if="loading" indeterminate></v-progress-linear>
  <div v-if="myPresentations.length === 0" class="mx-auto text-center">
    Ještě nemáte žádné prezentace
  </div>
  <v-list v-else>
    <v-list-item v-for="presentation in presentations" :key="presentation.id">
      <v-card>
        <v-list-item-title>{{presentation.name}}</v-list-item-title>
        <v-list-item-subtitle>{{presentation.description}}</v-list-item-subtitle>
      </v-card>
    </v-list-item>
  </v-list></template>

<style scoped lang="sass">

</style>
