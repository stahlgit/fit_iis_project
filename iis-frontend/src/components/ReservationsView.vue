<script setup>
import { ref, onMounted } from 'vue';
import {axiosInstance} from "@/router";
import { getUserConferences } from '@/services/utils';

const currentAccount = ref(null)
const loading = ref(false)
const myReservations = ref([])


async function getUserReservations(conferences){
  const conferenceReservations = [];
  for(const conference of conferences){
    try{
      const response = await axiosInstance.get('/reservation/all');
      const filteredReservations = response.data.filter(reservation => reservation.conference_id === conference.id);
      conferenceReservations.push({conference, reservations: filteredReservations});
      console.log(conferenceReservations);
    }
    catch(error){
      console.error(error);
    }
  }
  return conferenceReservations;
}

async function getMyReservations(){
  loading.value = true;
  try{
    const userResponse = await axiosInstance.get('/user/me');
    currentAccount.value = userResponse.data;

    const conferences = await getUserConferences(currentAccount.value.id);
    console.log(conferences.value);

    myReservations.value = await getUserReservations(conferences);

  }
  catch(error){
    console.error("Error fetching user data:", error);
  }
  finally{
    loading.value = false;
    console.log(currentAccount.value);

  }
}

onMounted(()=>{
  getMyReservations();
})
</script>

<template>
  <div v-if="myReservations.length === 0" class="mx-auto text-center">
    Ještě neporádáte žádné konference
  </div>
  <v-list v-else>
    <template v-for="item in myReservations" :key="item.conference.id">
      <v-list-item>
        <v-list-item-title class="font-weight-bold">{{ item.conference.name }}</v-list-item-title> <!-- Display Conference Name -->
      </v-list-item>
      <v-list class="ml-4"> <!-- Indent the list of rooms -->
        <v-list-item v-for="reservation in item.reservations" :key="reservation.id">
          <v-card class="mx-2"> <!-- Add some margin to the card -->
            <v-list-item-title>number of tickets: {{ reservation.number_of_tickets }}</v-list-item-title> <!-- Display Room Name -->
            <v-list-item-subtitle>paid: {{ reservation.paid }}</v-list-item-subtitle> <!-- Display Room Description -->
          </v-card>
        </v-list-item>
      </v-list>
    </template>
  </v-list>
</template>

<style scoped lang="sass">

</style>
