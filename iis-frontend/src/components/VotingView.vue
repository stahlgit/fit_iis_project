<script setup>
// get all conferences
import {onMounted, ref} from "vue";
import {getUserConferences} from "@/services/utils";
import {axiosInstance} from "@/router";

const attendedConferences = ref([])

onMounted(() => {
  fetchConferences()
})

async function fetchConferences() {
  const userId =  localStorage.getItem('userId')
  let userReservations = []
  try {
    const response = await axiosInstance.get(`/reservation/user/${userId}`)
    userReservations = response.data.filter((obj1, i, arr) => arr.findIndex(obj2 => (obj2.conference_id === obj1.conference_id)) === i)
    for (let reservation of userReservations) {
      const response1 = await axiosInstance.get(`/conferences/${reservation.conference_id}`)
      const conference = response1.data
      conference.lectures = []
      const response2 = await axiosInstance.get(`/lecture/conference/${conference.id}`)
      conference.lectures = response2.data
      attendedConferences.value.push(conference)
    }
  } catch (error) {
    console.error('Error fetching conferences:', error)
  }
}

function showRatingDialog(id) {
  ratingDialog.value = true
  ratingId.value = id
}

async function rateLecture() {
  try {
    const response = await axiosInstance.post(`/voting/`, {
      "rating": rating.value,
      "lecture_id": ratingId.value,
      "user_id": localStorage.getItem('userId')
    })
    ratingDialog.value = false
    snackbar.value = true
  } catch (error) {
    console.error('Error rating lecture:', error)
  }
}

const ratingDialog = ref(false)
const rating = ref(0)
const ratingId = ref(0)
const snackbar = ref(false)

</script>

<template>
  <v-snackbar v-model="snackbar" color="success" top>Děkujeme za hodnocení přednášky</v-snackbar>
  <v-dialog v-model="ratingDialog" >
    <v-card>
      <v-card-title>Zadejte hodnocení</v-card-title>
      <v-card-text>
        <v-rating v-model="rating"></v-rating>
      </v-card-text>
      <v-card-actions>
        <v-btn @click="ratingDialog = false">Zrušit</v-btn>
        <v-btn @click="rateLecture">Odeslat</v-btn>
      </v-card-actions>
    </v-card>
  </v-dialog>
  <v-list>
    <v-list-item v-for="conference in attendedConferences" :key="conference.id">
      <v-list-item-title>{{conference.name}}</v-list-item-title>
      <v-list>
        <v-list-item v-for="lecture in conference.lectures" :key="lecture.id">
          <div class="d-flex">
            <div>
              <v-list-item-title>{{lecture.name}}</v-list-item-title>
              <v-list-item-subtitle>{{lecture.description}}</v-list-item-subtitle>
            </div>
            <v-spacer></v-spacer>
            <div>
              <v-btn @click="showRatingDialog(lecture.id)" variant="text">Hodnotit</v-btn>
            </div>
          </div>
        </v-list-item>
      </v-list>
    </v-list-item>
  </v-list>
</template>

<style scoped lang="sass">

</style>
