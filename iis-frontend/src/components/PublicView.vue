<script setup>

import {onMounted, ref} from "vue";
import router, {axiosInstance} from "@/router";
import {isLoggedIn} from "@/router";

const conferences = ref([])
const loading = ref(true)

// fetch conferences
async function fetchConferences() {
  loading.value = true;
  try {
    console.log('get');
    const response = await axiosInstance.get('/conferences/all');
    conferences.value = response.data;
  } catch (error) {
    console.error('Error fetching conferences:', error);
  } finally {
    loading.value = false;
  }
}

function showConferenceDetail(id) {
  router.push('/public/conference/' + id)
}

onMounted(() => {
  getEnrichedConferences();
  console.log("Conferences fetched")
})

async function getEnrichedConferences() {
  try {
    const response = await axiosInstance.get('/conferences/all');
    const conferencesData = response.data;

    for (const conference of conferencesData) {
      try {
        const capacityResponse = await axiosInstance.get(`/conferences/${conference.id}/available`);
        conference.freeCapacity = capacityResponse.data.available;
      } catch (error) {
        console.error(`Error fetching capacity for conference ${conference.id}:`, error);
        conference.freeCapacity = 'N/A'; // Default value in case of error
      }
    }

    conferences.value = conferencesData;
    loading.value = false;
    console.log('Conferences fetched:', conferencesData);
  } catch (error) {
    console.error('Error fetching conferences:', error);
    conferences.value = [];
    loading.value = false;
  }
}

</script>

<template>
  <v-app-bar>
    <v-app-bar-title>
      Konference
    </v-app-bar-title>
    <v-spacer/>
    <v-btn v-if="isLoggedIn" to="/main" prepend-icon="mdi-account">
      Můj účet
    </v-btn>
    <v-btn v-else to="/login">
      Přihlásit se
    </v-btn>
  </v-app-bar>

  <v-progress-linear indeterminate v-if="loading" ></v-progress-linear>

  <div class="d-flex flex-wrap justify-center" style="flex: 1 1 30%" v-if="conferences.length > 0">
    <v-card v-for="conference in conferences" :key="conference.id" :title="conference.name" :subtitle=" conference.capacity - conference.freeCapacity + ' volných míst z ' + conference.capacity">
      <v-card-text>
        {{ conference.description }}
      </v-card-text>
      <v-card-actions>
        <v-btn @click="showConferenceDetail(conference.id)">
          Zobrazit
        </v-btn>
      </v-card-actions>
    </v-card>
  </div>
  <div v-else>
    <div class="text-center my-10">
      Zatím nejsou žádné konference
    </div>
  </div>
</template>

<style scoped lang="sass">
.v-card
  margin: 20px
  padding: 20px
  max-width: 450px

</style>
