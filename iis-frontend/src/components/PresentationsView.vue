<script setup>
import { ref, onMounted } from 'vue';
import {axiosInstance} from "@/router";
import {getUserConferences} from "@/services/utils";

const myPresentations = ref([]);
const conferencePresentations = ref([]);
const loading = ref(true);

async function getPresentations() {
  const userId = localStorage.getItem('userId');
  try {
    const response = await axiosInstance.get('/given_presentation/all');
    myPresentations.value = response.data.filter(presentation => presentation.user_id === userId);

    // get presentations for approval
    const conferences = getUserConferences(userId);
    for(const conference in conferences){
      try{
        const response = await axiosInstance.get('/given_presentation/all');
        const filteredPresentations = response.data.filter(presentation => presentation.conference_id === conference.id);
        conferencePresentations.value.push({conference, presentations: filteredPresentations});
      }
      catch(error){
        console.error(error);
      }
    }
  } catch (error) {
    console.error('Error fetching presentations:', error);
  } finally {
    loading.value = false;
    console.log(myPresentations.value);
    console.log(conferencePresentations.value);
  }
}

onMounted(() => {
  getPresentations();
})
</script>

<template>
  <div class="my-2">
    <v-btn prepend-icon="mdi-plus">Přidat</v-btn>
  </div>
  <v-progress-linear v-if="loading" indeterminate></v-progress-linear>
  <h2 class="mt-5">Vaše prezentace</h2>
  <div v-if="myPresentations.length === 0" class="mx-auto text-center">
    Ještě nemáte žádné prezentace
  </div>
  <v-list v-else>
    <v-list-item v-for="presentation in presentations" :key="presentation.id">
      <v-card>
        <v-list-item-title>{{presentation.name}}</v-list-item-title>
        <v-list-item-subtitle>{{presentation.description}}</v-list-item-subtitle>
        <v-card-actions>
          <v-btn>Upravit</v-btn>
          <v-btn>Smazat</v-btn>
        </v-card-actions>
      </v-card>
    </v-list-item>
  </v-list>
  <h2 class="mt-5">Prezentace k schválení</h2>
  <div v-if="conferencePresentations.length === 0" class="mx-auto text-center">
    Žádné prezentace k schválení
  </div>
  <v-list v-else>
    <template v-for="item in conferencePresentations" :key="item.conference.id">
      <v-list-item>
        <v-list-item-title class="font-weight-bold">{{ item.conference.name }}</v-list-item-title>
      </v-list-item>
      <v-list class="ml-4">
        <v-list-item v-for="presentation in item.presentations" :key="presentation.id">
          <v-card class="mx-2">
            <v-list-item-title>{{ presentation.name }}</v-list-item-title>
            <v-list-item-subtitle>{{ presentation.description }}</v-list-item-subtitle>
            <v-card-actions>
              <v-btn>Schválit</v-btn>
              <v-btn>Odmítnout</v-btn>
            </v-card-actions>
          </v-card>
        </v-list-item>
      </v-list>
    </template>
  </v-list>
</template>

<style scoped lang="sass">

</style>
