<script setup>
import { onMounted, ref } from "vue";
import { axiosInstance } from "@/router";

const loading = ref(false);
const users = ref([]);

function fetchUsers() {
    loading.value = true;

    // Retrieve the token from localStorage
    const token = localStorage.getItem('authToken');
    axiosInstance.defaults.headers.common['Authorization'] = `Bearer ${token}`;

    axiosInstance.get('user/all')
        .then(response => {
            users.value = response.data;
        })
        .catch(error => {
            console.error("Error fetching users:", error.response ? error.response.data : error.message);
        })
        .finally(() => {
            loading.value = false;
            console.log(users.value);
        });
}

onMounted(() => {
    fetchUsers();
});
</script>

<template>
  <v-dialog v-model="dialog">
    <v-card>
      <!-- Your dialog content goes here -->
    </v-card>
  </v-dialog>

  <v-container>
    <div class="my-2">
      <v-btn prepend-icon="mdi-plus">Přidat</v-btn>
    </div>
    <v-progress-linear v-if="loading" indeterminate></v-progress-linear>
    <v-list>
      <v-list-item v-for="user in users" :key="user.id">
        <v-card>
          <v-list-item-title>{{ user.name }}</v-list-item-title> <!-- Corrected from conference.name -->
          <v-list-item-subtitle>{{ user.email }}</v-list-item-subtitle> <!-- Added user.email -->
        </v-card>
      </v-list-item>
    </v-list>
  </v-container>
</template>

<style scoped lang="sass">

</style>
