<script setup>
// url props
import router, {authentiatedAxiosInstance, axiosInstance, isLoggedIn} from "@/router";
import {onMounted, ref} from "vue";

const props = defineProps({
  id: String
})

const dialog = ref(false)

const conference = ref({})
const me = ref({})
const showGuestReservationConfirmation = ref(false);
const showUserReservationConfirmation = ref(false);

const newReservation = ref({
  "number_of_tickets": 0,
  "status": "string",
  "paid": true,
  "user_id": 0,
  "conference_id": 0,
  })

const username = ref("");
const mail = ref("");

async function getMyDetails() {
  try {
    const response = await authentiatedAxiosInstance.get(`/user/me`);
    me.value = response.data;

  } catch (error) {
    console.error('Error fetching user data:', error);
  }
}

async function getEnrichedConference(id) {
  try {
    const response = await axiosInstance.get(`/conferences/${id}`);
    conference.value = response.data;
    const response2 = await axiosInstance.get(`/conferences/${id}/available`);
    conference.value.freeCapacity = response2.data.available;
  } catch (error) {
    console.error('Error fetching conference:', error);
  }
}

async function doReservation() {
  console.log('doReservation')
  // for guest users
  if (!isLoggedIn()) {
    console.log('not logged in')
    // create user
    // create reservation
    try {
      const response = await authentiatedAxiosInstance.post(`/reservation`, {
        "number_of_tickets": newReservation.value.number_of_tickets,
        "paid": false,
        "conference_id": props.id,
        "email": me.value.email
      });
      console.log(response.data);
      newReservation.value = response.data;
      showGuestReservationConfirmation.value = true;
    } catch (error) {
      console.error('Error creating reservation:', error);
    }
  }

  // for logged in users
  else {
    console.log('logged in')
    // create reservation
    try {
      const response = await authentiatedAxiosInstance.post(`/reservation`, {
        "number_of_tickets": newReservation.value.number_of_tickets,
        "paid": false,
        "conference_id": props.id,
        "user_id": me.value.id
      });
      console.log(response.data);
      newReservation.value = response.data;
      showUserReservationConfirmation.value = true;
    } catch (error) {
      console.error('Error creating reservation:', error);
    }

  }
}

onMounted(() => {
  getEnrichedConference(props.id);
  getMyDetails();
  console.log("Conference fetched")
})
</script>

<template>
  <v-dialog v-model="dialog" max-width="600px">
    <v-card title="Rezervace vstupenek">
      <v-card-text>
        <div class="d-flex">
          <v-text-field disabled v-model="newReservation.number_of_tickets" label="Počet vstupenek"></v-text-field>
          <v-btn-group>
            <v-btn icon @click="newReservation.number_of_tickets > 0 ? newReservation.number_of_tickets-- : null">
              <v-icon>mdi-minus</v-icon>
            </v-btn>
            <v-btn icon @click="newReservation.number_of_tickets < conference.freeCapacity ? newReservation.number_of_tickets++ : null">
              <v-icon>mdi-plus</v-icon>
            </v-btn>
          </v-btn-group>
        </div>
        <div v-if="!isLoggedIn">
          <v-text-field label="Jméno" v-model="username"/>
          <v-text-field label="E-mail" v-model="mail"/>
        </div>
        <div>
          <v-banner>
            Jste přihlášen jako <v-kbd>{{me.name}}</v-kbd> s emailem <v-kbd>{{me.email}}</v-kbd>.
          </v-banner>
          <v-banner icon="mdi-check" color="success" v-show="showGuestReservationConfirmation">
            Děkujeme za rezervaci vstupenek na konferenci.<br> Na email {{me.email}} vám byla zaslána potvrzovací zpráva.
          </v-banner>
          <v-banner icon="mdi-check" color="success" v-show="showUserReservationConfirmation">
            Děkujeme za rezervaci vstupenek na konferenci.<br> Rezervaci najdete ve svém účtu.
          </v-banner>
        </div>
      </v-card-text>
      <v-card-actions>
        <v-spacer></v-spacer>
        <v-btn @click="dialog = false">
          Zavřít
        </v-btn>
        <v-btn :disabled="showGuestReservationConfirmation || showUserReservationConfirmation" color="blue darken-1" @click="() => { doReservation(); }">
          Odeslat
        </v-btn>
      </v-card-actions>
    </v-card>
  </v-dialog>
  <v-container>
    <v-app-bar>
      <v-app-bar-nav-icon icon="mdi-arrow-left" @click="router.go(-1)"></v-app-bar-nav-icon>
      <v-app-bar-title>
        {{conference.name}}
      </v-app-bar-title>
    </v-app-bar>
    <div class="d-flex ga-4 my-4">
      <v-chip prepend-icon="mdi-map-marker">
        {{conference.place}}
      </v-chip>
      <v-chip prepend-icon="mdi-account-group">
        {{conference.freeCapacity}} volných míst
      </v-chip>
      <v-chip prepend-icon="mdi-presentation">
        {{conference.genre}}
      </v-chip>
    </div>
    <h3>{{conference.description}}</h3>

    <v-btn class="my-10" @click="dialog = true">Rezervovat</v-btn>

  </v-container>
</template>

<style scoped lang="sass">

</style>
