<script setup>

import {onMounted, ref} from "vue";
import {axiosInstance} from "@/router";

const currentAccount = ref(null)
const loading = ref(false)
const myRooms = ref([])

function getRooms() {
  // get user using axios
  axiosInstance.get('/user/me')
    .then(response => {
      currentAccount.value = response.data
    })
    .catch(error => {
      console.error(error)
    })
    .finally(() => {
      loading.value = false
      console.log(currentAccount.value)
    })

  // filter conferences by user id, then filter rooms by conferences
}

onMounted(() => {

})

</script>

<template>
  <div v-if="myRooms.length === 0" class="mx-auto text-center">
    Ještě neporádáte žádné konference
  </div>
  <v-list v-else>
    <v-list-item v-for="room in myRooms" :key="room.id">
      <v-card>
        <v-list-item-title>{{room.name}}</v-list-item-title>
        <v-list-item-subtitle>{{room.description}}</v-list-item-subtitle>
      </v-card>
    </v-list-item>
  </v-list>
</template>

<style scoped lang="sass">

</style>
