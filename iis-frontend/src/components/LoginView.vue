<script setup>

import { ref } from 'vue';

const email = ref('');
const password = ref('');

// from  index.js import login
import { login } from '@/router'

const snackbar = ref(false);

async function doLogin() {
  const res = await login(email.value, password.value);

  if (res) {
    console.log('Logged in');
  } else {
    console.log('Failed to log in');
    snackbar.value = true;
  }
}

const emailRules = [
  value => {
    if (/.+@.+\..+/.test(value)) return true

    return 'E-mail must be valid.'
  },
]

</script>

<template>
  <v-container>
    <v-snackbar
      v-model="snackbar"
      color="error"
    variant="tonal">
      Nesprávné přihlašovací údaje
    </v-snackbar>
    <v-card class="w-lg-33 mx-auto my-10" elevation="5">
      <v-card-title>Přihlášení</v-card-title>
      <v-divider></v-divider>
      <v-card-text>
        <v-form>
          <v-text-field
            v-model="email"
            label="Email"
            :rules="emailRules"
          ></v-text-field>
          <v-text-field
            v-model="password"
            label="Heslo"
            type="password"
          ></v-text-field>
          <div class="d-flex">
            <v-btn
              prepend-icon="mdi-login"
              @click="doLogin"
              color="primary"
            >
              Přihlásit
            </v-btn>
            <v-spacer></v-spacer>
            <v-btn
              variant="text"
              to="/register"
            >
              Registrovat
            </v-btn>
          </div>
        </v-form>
      </v-card-text>
    </v-card>
  </v-container>
</template>

<style scoped lang="sass">

</style>
