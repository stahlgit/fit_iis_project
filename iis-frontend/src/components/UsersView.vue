<script setup>
import { onMounted, ref } from "vue";
import { axiosInstance } from "@/router";

const loading = ref(false);
const users = ref([]);
const selectedUser = ref(null);
const dialog = ref(false);

function fetchUsers() {
    loading.value = true;

    const token = localStorage.getItem('authToken');
    axiosInstance.defaults.headers.common['Authorization'] = `Bearer ${token}`;

    axiosInstance.get('user/all')
        .then(response => {
            users.value = response.data;
        })
        .catch(error => {
            console.error("Error fetching users:", error.response ? error.response.data : error.message);
        })
        .finally(() => {
            loading.value = false;
        });
}

onMounted(() => {
    fetchUsers();
});

function openEditDialog(user) {
    selectedUser.value = { ...user }; // Create a copy of the user data
    dialog.value = true; // Open the dialog
}

function saveUserChanges() {
    if (!selectedUser.value) return;

    const token = localStorage.getItem('authToken');
    axiosInstance.defaults.headers.common['Authorization'] = `Bearer ${token}`;

    axiosInstance.put(`user/${selectedUser.value.id}`, selectedUser.value)
        .then(response => {
            // Update the user list with the modified user
            const index = users.value.findIndex(user => user.id === response.data.id);
            if (index !== -1) {
                users.value[index] = response.data;
            }
            dialog.value = false; // Close the dialog
        })
        .catch(error => {
            console.error("Error updating user:", error.response ? error.response.data : error.message);
        });
}


</script>

<template>
  <v-dialog v-model="dialog" max-width="500px">
    <v-card>
      <v-card-title>Edit User</v-card-title>
      <v-card-text>
        <v-form>
          <v-text-field
            label="Name"
            v-model="selectedUser.name"
            outlined
          ></v-text-field>
          <v-text-field
            label="Email"
            v-model="selectedUser.email"
            outlined
          ></v-text-field>
          <v-select
            label="Role"
            v-model="selectedUser.role"
            :items="['ADMIN', 'REGISTERED', 'GUEST']"
            outlined
          ></v-select>
        </v-form>
      </v-card-text>
      <v-card-actions>
        <v-spacer></v-spacer>
        <v-btn text @click="dialog = false">Cancel</v-btn>
        <v-btn color="primary" text @click="saveUserChanges">Save</v-btn>
      </v-card-actions>
    </v-card>
  </v-dialog>

  <v-container>
    <div class="my-2">
      <v-btn prepend-icon="mdi-plus">Přidat</v-btn>
    </div>
    <v-progress-linear v-if="loading" indeterminate></v-progress-linear>
    <v-list>
      <v-list-item v-for="user in users" :key="user.id">
        <v-card>
          <v-list-item-title>{{ user.name }}</v-list-item-title>
          <v-list-item-subtitle>{{ user.email }}</v-list-item-subtitle>
          <v-list-item-action>
            <v-btn @click="openEditDialog(user)">Edit</v-btn> <!-- Call openEditDialog with the user -->
          </v-list-item-action>
        </v-card>
      </v-list-item>
    </v-list>
  </v-container>
</template>

<style scoped lang="sass">

</style>
