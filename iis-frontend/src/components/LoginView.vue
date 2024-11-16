<script setup>

import { ref } from 'vue';

const email = ref('');
const password = ref('');

async function login() {
  console.log(email.value, password.value);
}

const fieldRules = [
  (v) => !!v || 'Povinné pole'
];

</script>

<template>
  <v-container>
    <v-card class="w-lg-33 mx-auto my-10" elevation="5">
      <v-card-title>Přihlášení</v-card-title>
      <v-divider></v-divider>
      <v-card-text>
        <v-form>
          <v-text-field
            v-model="email"
            label="Email"
          ></v-text-field>
          <v-text-field
            v-model="password"
            label="Heslo"
            type="password"
          ></v-text-field>
          <div class="d-flex">
            <v-btn
              prepend-icon="mdi-login"
              @click="login"
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
