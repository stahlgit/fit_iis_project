<script setup>
// url props
import router from "@/router";
import {ref} from "vue";

defineProps({
  id: String
})

const dialog = ref(false)

const conference = ref({"name":"Nazev konference","description":"Popis Konference","genre":"Zanr","place":"Misto","start_time":"2024-11-20T22:39:44.555000","end_time":"2024-11-20T22:39:44.555000","price":0.0,"capacity":0,"id":1})
</script>

<template>
  <v-dialog v-model="dialog" max-width="600px">
    <v-card title="Rezervace vstupenek">
      <v-card-text>
        <v-text-field title="počet vstupenek"/>
      </v-card-text>
      <v-card-actions>
        <v-spacer></v-spacer>
        <v-btn color="blue darken-1" text @click="dialog = false">
          Zavřít
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
        {{conference.capacity}}
      </v-chip>
      <v-chip prepend-icon="mdi-account-group">
        {{conference.genre}}
      </v-chip>
    </div>
    <h3>{{conference.description}}</h3>

    <v-btn class="my-10" @click="dialog = true">Rezervovat</v-btn>

  </v-container>
</template>

<style scoped lang="sass">

</style>
