<script setup>

import { ref } from 'vue';
import { register } from '@/router';

const username = ref('');
const email = ref('');
const password = ref('');
const passwordConfirmation = ref('');
const usernameError = ref('');
const emailError = ref('');
const otherError = ref('');

async function doRegister() {
  usernameError.value = '';
  emailError.value = '';
  otherError.value = '';
  const res = await register(username.value, email.value, password.value);

  if (res) {
    console.log('Logged in');
  } else {
    console.log('Failed to log in');

    if (res === 'Username already registered.') {
      usernameError.value = 'This username is already taken.';
    } else if (res === 'Email already registered.') {
      emailError.value = 'This email is already registered.';
    }
  }
}

const emailRules = [
  value => {
    if (/.+@.+\..+/.test(value)) return true

    return 'E-mail must be valid.'
  },
  value => {
    if (value.length > 0) return true

    return 'E-mail is required.'
  }
];

const passwordRules = [
  value => {
    if (value.length > 0) return true

    return 'Password is required.'
  },
  value => {
    if (value.length >= 8) return true

    return 'Password must be at least 8 characters long.'
  }
];

const passwordConfirmationRules = [
  value => {
    if (value === password.value) return true

    return 'Passwords do not match.'
  }
];

const usernameRules = [
  value => {
    if (value.length > 0) return true;
    return 'Username is required.';
  }
];

</script>

<template>
  <v-container>
    <v-card class="w-lg-33 mx-auto my-10" elevation="5">
      <v-card-title>Registrace</v-card-title>
      <!-- separator -->
      <v-divider></v-divider>
      <!-- registration form -->
      <v-card-text>
        <v-form>
          <v-text-field
            v-model="username"
            label="Uživatelské jméno"
            :rules="usernameRules"
            :error-messages="[usernameError]"


          ></v-text-field>
          <!-- separator TODO: add error message under the field
          TODO: turn off notification on website
                      -->
          <v-text-field
            v-model="email"
            label="Email"
            :rules="emailRules"
            :error-messages="[emailError]"
          ></v-text-field>
          <v-text-field
            v-model="password"
            label="Heslo"
            type="password"
            :rules="passwordRules"
          ></v-text-field>
          <v-text-field
            v-model="passwordConfirmation"
            label="Ověření hesla"
            type="password"
            :rules="passwordConfirmationRules"
          ></v-text-field>
          <div class="d-flex">
            <v-btn
              prepend-icon="mdi-account-plus"
              @click="doRegister"
              color="primary"
            >
              Registrovat
            </v-btn>
            <v-spacer></v-spacer>
            <v-btn
              variant="text"
              to="/login"
            >
              Přihlásit se
            </v-btn>
          </div>
        </v-form>
      </v-card-text>
    </v-card>
  </v-container>
</template>

<style scoped lang="sass">

</style>
