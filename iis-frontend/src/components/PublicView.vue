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
  fetchConferences()
  console.log(conferences.value)
})

</script>

<template>
  <v-app-bar>
    <v-app-bar-title>
      Konference
    </v-app-bar-title>
    <v-spacer/>
    <v-btn v-if="isLoggedIn" to="main" prepend-icon="mdi-account">
      Můj účet
    </v-btn>
    <v-btn v-else to="/login">
      Přihlásit se
    </v-btn>
  </v-app-bar>

  <v-progress-linear indeterminate v-if="loading" ></v-progress-linear>

  <div class="d-flex flex-wrap justify-center" style="flex: 1 1 30%">
    <v-card title="Kokotinec" subtitle="Super prezentace">
      <v-card-text>
        Lorem ipsum dolor sit amet, consectetur adipiscing elit. Nulla nec purus euismod, fermentum turpis in, ultricies nunc
      </v-card-text>
      <v-card-actions>
        <v-btn @click="showConferenceDetail(0)">
          Zobrazit
        </v-btn>
      </v-card-actions>
    </v-card>
  </div>
</template>

<style scoped lang="sass">
.v-card
  margin: 20px
  padding: 20px
  max-width: 450px

</style>
