<script setup>
import { ref, onMounted } from 'vue';

const myReservations = ref([]);

</script>

<template>
  <div v-if="myReservations.length === 0" class="mx-auto text-center">
    Ještě neporádáte žádné konference
  </div>
  <v-list v-else>
    <v-list-item v-for="reservation in myReservations" :key="reservation.id">
      <v-card>
        <v-list-item-title>{{reservation.name}}</v-list-item-title>
        <v-list-item-subtitle>{{reservation.description}}</v-list-item-subtitle>
      </v-card>
    </v-list-item>
  </v-list>
</template>

<style scoped lang="sass">

</style>
