<script setup>
import { ref, onMounted } from 'vue';
import {axiosInstance} from "@/router";
import { getUserConferences } from '@/services/utils';

const currentAccount = ref(null)
const loadingMyReservations = ref(false)
const loadingReservationsToApprove = ref(false)
const myReservations = ref([])
const reservationsToApprove = ref([])

async function getUserData(id) {
  try {
    const response = await axiosInstance.get('/user/' + id);
    const user = response.data;
    return user;
  } catch (error) {
    console.error('Error fetching user data:', error);
  }
}

async function getUserReservations(conferences){
  const conferenceReservations = [];
  for (const conference of conferences){
    try {
      const response = await axiosInstance.get('/reservation/all');
      const filteredReservations = response.data.filter(reservation => reservation.conference_id === conference.id);
      for (const reservation of filteredReservations){
        const user = await getUserData(reservation.user_id);
        reservation.user = user;
      }
      conferenceReservations.push({conference, reservations: filteredReservations});
    }
    catch(error){
      console.error(error);
    }
  }
  return conferenceReservations;
}

async function getMyReservations(){
  loadingMyReservations.value = true;
  try{
    const userResponse = await axiosInstance.get('/user/me');
    currentAccount.value = userResponse.data;

    const allresponse = await axiosInstance.get('/reservation/all');
    const allReservations = allresponse.data;

    const userReservations = allReservations.filter(reservation => reservation.user_id === currentAccount.value.id);

    const conferencesResponse = await axiosInstance.get('/conferences/all');
    const conferences = conferencesResponse.data;

    myReservations.value = conferences.map(conference => {
      const conferenceReservations = userReservations.filter(reservation => reservation.conference_id === conference.id);
      return {
        conference,
        reservations: conferenceReservations,
      };
    }).filter(item => item.reservations.length > 0);
  }
  catch(error){
    console.error("Error fetching user data:", error);
  }
  finally{
    loadingMyReservations.value = false;
  }
}

async function getReservationsToApprove() {
  loadingReservationsToApprove.value = true;
  try {
    // get all conferences
    const response = await axiosInstance.get('/conferences/all');
    const currentUserId = localStorage.getItem('userId');
    const conferences = response.data.filter(conference => conference.organizer_id == currentUserId);
    reservationsToApprove.value = await getUserReservations(conferences);
  } catch (error) {
    console.error('Error fetching conferences:', error);
  } finally {
    loadingReservationsToApprove.value = false;
  }
}

async function payReservation(reservationId){
  try {
    const response = await axiosInstance.get(`/reservation/${reservationId}`);
    const reservation = response.data;
    reservation.paid = true;
    await axiosInstance.put(`/reservation/${reservationId}`, reservation);
  }
  catch(error){
    console.error('Error paying reservation:', error);
  }

  await loadData();
}

async function approveReservation(reservationId){
  try {
    const response = await axiosInstance.get(`/reservation/${reservationId}`);
    const reservation = response.data;
    reservation.approved = true;
    await axiosInstance.put(`/reservation/${reservationId}`, reservation);
  }
  catch(error){
    console.error('Error approving reservation:', error);
  }

  await loadData();
}

async function deleteReservation(reservationId){
  alert('Opravdu si přejete smazat rezervaci?');
  try {
    await axiosInstance.delete(`/reservation/${reservationId}`);
  }
  catch(error){
    console.error('Error deleting reservation:', error);
  }

  await loadData();
}

async function loadData(){
  await getMyReservations();
  await getReservationsToApprove();
}

onMounted(()=>{
  loadData();
})
</script>

<template>
  <h2>Moje rezervace</h2>
  <v-progress-linear indeterminate v-if="loadingMyReservations"/>
  <div v-else-if="myReservations.length === 0" class="mx-auto text-center">
    Ještě nemáte žádné rezervace
  </div>
  <v-list v-else>
    <template v-for="item in myReservations" :key="item.conference.id">
      <v-list-item>
        <v-list-item-title class="font-weight-bold">{{ item.conference.name }}</v-list-item-title> <!-- Display Conference Name -->
      </v-list-item>
      <v-list class="ml-4"> <!-- Indent the list of rooms -->
        <v-list-item v-if="item.reservations.length === 0">
          <v-list-item-title>Zatím žádné rezervace</v-list-item-title>
        </v-list-item>
        <v-list-item v-for="reservation in item.reservations" :key="reservation.id">
          <v-card class="mx-2"> <!-- Add some margin to the card -->
            <v-list-item-title>Počet vstupenek: {{ reservation.number_of_tickets }}</v-list-item-title> <!-- Display Room Name -->
            <v-list-item-subtitle style="color: lightgreen" v-if="reservation.paid">Zaplaceno</v-list-item-subtitle> <!-- Display Room Description -->
            <v-list-item-subtitle style="color: lightcoral" v-else>Nezaplaceno</v-list-item-subtitle> <!-- Display Room Description -->
            <v-list-item-subtitle style="color: lightgreen" v-if="reservation.approved">Vstupenky vydány</v-list-item-subtitle> <!-- Display Room Description -->
            <v-list-item-subtitle style="color: lightsalmon" v-else>Vstupenky k dispozici</v-list-item-subtitle> <!-- Display Room Description -->
            <v-card-actions>
              <v-btn @click="payReservation(reservation.id)" :disabled="reservation.paid" variant="outlined" color="success">{{!reservation.paid ? "Zaplatit" : "Zaplaceno"}}</v-btn>
              <v-btn @click="deleteReservation(reservation.id)" :disabled="reservation.paid" variant="outlined" color="error">{{!reservation.paid ? "Zrušit" : "Nelze zrušit"}}</v-btn>
            </v-card-actions>
          </v-card>
        </v-list-item>
      </v-list>
    </template>
  </v-list>

  <h2 class="mt-5">Rezervace ke schválení</h2>
  <v-progress-linear v-if="loadingReservationsToApprove" indeterminate/>
  <div v-else-if="reservationsToApprove.length === 0" class="mx-auto text-center">
    Ještě neporádáte žádné konference
  </div>
  <v-list v-else>
    <template v-for="item in reservationsToApprove" :key="item.conference.id">
      <v-list-item>
        <v-list-item-title class="font-weight-bold">{{ item.conference.name }}</v-list-item-title> <!-- Display Conference Name -->
      </v-list-item>
      <v-list class="ml-4"> <!-- Indent the list of rooms -->
        <v-list-item v-if="item.reservations.length === 0">
          Zatím žádné rezervace
        </v-list-item>
        <v-list-item v-for="reservation in item.reservations" :key="reservation.id">
          <v-card class="mx-2"> <!-- Add some margin to the card -->
            <v-list-item-title>{{reservation.user.name}} </v-list-item-title> <!-- Display Room Name -->
            <v-list-item-subtitle>Počet vstupenek: {{ reservation.number_of_tickets }}</v-list-item-subtitle>
            <v-list-item-subtitle style="color: lightgreen" v-if="reservation.paid">Zaplaceno</v-list-item-subtitle> <!-- Display Room Description -->
            <v-list-item-subtitle style="color: lightcoral" v-else>Nezaplaceno</v-list-item-subtitle> <!-- Display Room Description -->
            <v-card-actions>
              <v-btn @click="payReservation(reservation.id)" :disabled="reservation.paid" variant="outlined" color="success">{{!reservation.paid ? "Označit jako zaplacené" : "Zaplaceno"}}</v-btn>
              <v-btn @click="approveReservation(reservation.id)" :disabled="reservation.approved" variant="outlined" color="warning">{{!reservation.approved ? "Vydat vstupenky" : "Vstupenky vydány"}}</v-btn>
              <v-btn @click="deleteReservation(reservation.id)" variant="outlined" color="error">Smazat</v-btn>
            </v-card-actions>
          </v-card>
        </v-list-item>
      </v-list>
    </template>
  </v-list>
</template>

<style scoped lang="sass">
</style>
