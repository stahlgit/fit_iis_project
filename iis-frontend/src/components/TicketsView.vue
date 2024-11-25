<script setup>
import { ref, onMounted } from 'vue';
import {axiosInstance} from "@/router";

const myReservations = ref([]);
const enrichedReservations = ref([]);

// todo show pending reservations and confirmed tickets

async function getReservations() {
  try {
    let me = {}
    const response = await axiosInstance.get('/user/me');
    me = response.data;
    console.log(me);
    const response2 = await axiosInstance.get('/reservation/user/' + me.id);
    myReservations.value = response2.data;
    console.log(myReservations.value);
  } catch (error) {
    console.error(error);
  }

  for (let reservation of myReservations.value) {
    try {
      const response = await axiosInstance.get('/conferences/' + reservation.conference_id);
      enrichedReservations.value.push({
        ...reservation,
        conference: response.data
      });
    } catch (error) {
      console.error(error);
    }
  }
  console.log(enrichedReservations.value);
  console.log(myReservations.value);
}

async function cancelReservation(id) {
  try {
    await axiosInstance.delete('/reservation/' + id);
    enrichedReservations.value = [];
    await getReservations();
  } catch (error) {
    console.error(error);
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

  enrichedReservations.value = [];
  await getReservations();
}

onMounted(() => {
  getReservations();
});
</script>

<template>
  <div v-if="enrichedReservations.length === 0" class="mx-auto text-center">
    Ještě nemáte žádné lístky
    <v-btn class="mx-2" to="/public">Koupit</v-btn>
  </div>
  <div v-else>
    <v-btn to="/public" class="mx-2 my-4">Koupit další</v-btn>
    <v-list>
      <v-list-item class="my-2" v-for="reservation in enrichedReservations" :key="reservation.id">
        <v-card>
          <div class="d-flex">
            <div>
              <v-list-item-title>{{reservation.conference.name}}</v-list-item-title>
              <v-list-item-subtitle>{{reservation.number_of_tickets}} vstupenky</v-list-item-subtitle>
            </div>
            <v-spacer/>
            <div>
              <v-chip>
                <div v-if="reservation.approved === true">
                  <v-icon>mdi-ticket</v-icon>
                  Vstupenky vydány
                </div>
                <div v-else-if="reservation.paid === true">
                  <v-icon>mdi-check</v-icon>
                  Zaplaceno
                </div>
                <div v-else>
                  <v-icon>mdi-timer-sand</v-icon>
                  Čeká na zaplacení
                </div>
                <v-btn :disabled="reservation.paid" class="ml-4" variant="text" @click="cancelReservation(reservation.id)">Zrušit</v-btn>
                <v-btn :disabled="reservation.paid" variant="text" @click="payReservation(reservation.id)">Zaplatit</v-btn>
              </v-chip>
            </div>
          </div>
        </v-card>
      </v-list-item>
    </v-list>
  </div>
</template>

<style scoped lang="sass">

</style>
