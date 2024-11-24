<script setup>
import { ref, onMounted } from 'vue';

const myTickets = ref([]);


</script>

<template>
  <div v-if="myTickets.length === 0" class="mx-auto text-center">
    Ještě nemáte žádné lístky
    <v-btn class="mx-2" to="/public">Koupit</v-btn>
  </div>
  <div v-else>
    <v-btn class="mx-2 my-4">Koupit další</v-btn>
    <v-list>
      <v-list-item v-for="ticket in myTickets" :key="ticket.id">
        <v-card>
          <v-list-item-title>{{ticket.name}}</v-list-item-title>
          <v-list-item-subtitle>{{ticket.description}}</v-list-item-subtitle>
        </v-card>
      </v-list-item>
    </v-list>
  </div>
</template>

<style scoped lang="sass">

</style>
