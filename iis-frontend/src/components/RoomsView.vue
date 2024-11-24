<script setup>

import {onMounted, ref} from "vue";
import {axiosInstance} from "@/router";
import {getUserConferences} from "@/services/utils";

const currentAccount = ref(null)
const loading = ref(false)
const conferencesWithRooms = ref([])


async function getUserRooms(conferences) {
  const conferenceRoomMap = []; // Array to hold conferences with their rooms
  for (const conference of conferences) {
    try {
      const response = await axiosInstance.get('/room/all'); // Fetch all rooms
      const filteredRooms = response.data.filter(room => room.conference_id === conference.id); // Filter rooms for this conference
      conferenceRoomMap.push({ conference, rooms: filteredRooms }); // Push an object with conference and its rooms
    } catch (error) {
      console.error(error);
    }
  }
  return conferenceRoomMap; // Return the structured data
}

async function getUser(){
    loading.value = true;
    try {
      const userResponse = await axiosInstance.get('/user/me');
      currentAccount.value = userResponse.data;

      const conferences = await getUserConferences(currentAccount.value.id);
      console.log(conferences.value);


      conferencesWithRooms.value = await getUserRooms(conferences);

    } catch (error) {
      console.error("Error fetching user data:", error);
    } finally {
      loading.value = false; // Set loading to false after fetching data
      console.log(currentAccount.value);
    }
}

onMounted(() => {
  getUser();
})

</script>

<template>
  <div v-if="loading">Loading...</div>
  <div v-else-if="conferencesWithRooms.length === 0" class="mx-auto text-center">
    Ještě neporádáte žádné konference
  </div>
  <v-list v-else>
    <template v-for="item in conferencesWithRooms" :key="item.conference.id">
      <v-list-item>
        <v-list-item-title class="font-weight-bold">{{ item.conference.name }}</v-list-item-title> <!-- Display Conference Name -->
      </v-list-item>
      <v-list class="ml-4"> <!-- Indent the list of rooms -->
        <v-list-item v-for="room in item.rooms" :key="room.id">
          <v-card class="mx-2"> <!-- Add some margin to the card -->
            <v-list-item-title>{{ room.name }}</v-list-item-title> <!-- Display Room Name -->
            <v-list-item-subtitle>{{ room.description }}</v-list-item-subtitle> <!-- Display Room Description -->
          </v-card>
        </v-list-item>
      </v-list>
    </template>
  </v-list>
</template>

<style scoped lang="sass">

</style>
