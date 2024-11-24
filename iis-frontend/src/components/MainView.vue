<script setup>

import {ref, watchEffect} from 'vue';

const navigationDrawer = ref(false);

import router, { logout} from "@/router";
const userRole = ref(localStorage.getItem('role'));

const routeName = ref('');

watchEffect(() => {
  routeName.value = router.currentRoute.value.name;
});
</script>

<template>
  <v-navigation-drawer v-model="navigationDrawer">
    <!-- -->
    <v-list>
      <v-list-subheader>Uživatel</v-list-subheader>
      <v-list-item link prepend-icon="mdi-ticket" @click="router.push('/main/tickets')">
        Vstupenky
      </v-list-item>
      <v-list-subheader>Pořadatel</v-list-subheader>
      <v-list-item link prepend-icon="mdi-account-group" @click="router.push('/main/conferences')">
        Konference
      </v-list-item>
      <v-list-item link prepend-icon="mdi-office-building" @click="router.push('/main/rooms')">
        Místnosti
      </v-list-item>
      <v-list-item link prepend-icon="mdi-calendar" @click="router.push('/main/reservations')">
        Rezervace
      </v-list-item>
      <v-list-item link prepend-icon="mdi-star" @click="router.push('/main/voting')">
        Hlasování
      </v-list-item>
      <v-list-subheader>Přednášející</v-list-subheader>
      <v-list-item link prepend-icon="mdi-presentation" @click="router.push('/main/presentations')">
        Prezentace
      </v-list-item>
      <template v-if="userRole === 'admin'">
        <v-list-subheader>Admin</v-list-subheader>
        <v-list-item link prepend-icon="mdi-account" @click="router.push('/main/users')">
          Uživatelé
        </v-list-item>
      </template>
    </v-list>
  </v-navigation-drawer>
  <v-app-bar>
    <v-app-bar-nav-icon @click="navigationDrawer = !navigationDrawer">
      <v-icon>mdi-menu</v-icon>
    </v-app-bar-nav-icon>
    <v-app-bar-title>
      {{routeName}}
    </v-app-bar-title>

    <v-spacer/>

    <v-btn prepend-icon="mdi-logout" @click="logout">
      Odhlásit se
    </v-btn>
  </v-app-bar>
  <v-container>
    <router-view/>
  </v-container>
</template>

<style scoped lang="sass">

</style>
