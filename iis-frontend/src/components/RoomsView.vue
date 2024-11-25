<script setup>

import {onMounted, ref} from "vue";
import {axiosInstance} from "@/router";
import {getUserConferences} from "@/services/utils";

const currentAccount = ref(null)
const loading = ref(false)
const conferencesWithRooms = ref([])
const createDialog = ref(false);
const updateDialog = ref(false);
const selectedRoom = ref({ name: '', capacity: null, conference_id: null });
const newRoom = ref({ name: '', capacity: null});
const showerror = ref(false);
const isAdmin = ref(false);


async function getUserRooms(conferences) {
  const conferenceRoomMap = [];

  for (const conference of conferences) {
    try {
      const response = await axiosInstance.get('/room/all');
      const filteredRooms = response.data.filter(room => room.conference_id === conference.id);
      conferenceRoomMap.push({ conference, rooms: filteredRooms });
    } catch (error) {
      console.error(error);
      return [];
    }
  }
  return conferenceRoomMap;
}

async function getUser() {
  loading.value = true;
  let conferences = []; // Declare conferences variable at the top

  try {
    const userResponse = await axiosInstance.get('/user/me');
    currentAccount.value = userResponse.data;

    isAdmin.value = currentAccount.value.role === 'admin';

    if (isAdmin.value) {
      const response = await axiosInstance.get('/conferences/all');
      conferences = response.data; // Assign data to the conferences variable
    } else {
      conferences = await getUserConferences(currentAccount.value.id);
    }

    conferencesWithRooms.value = await getUserRooms(conferences);

  } catch (error) {
    console.error("Error fetching user data:", error);
  } finally {
    loading.value = false; // Set loading to false after fetching data
  }
}


function openCreateDialog() {
  createDialog.value = true;
}

function openUpdateDialog(room) {
  if (room) {
    selectedRoom.value = room;
    updateDialog.value = true;
  } else {
    console.error("Attempted to open update dialog without a room.");
  }
}

function closeDialogs() {
  createDialog.value = false;
  updateDialog.value = false;
  selectedRoom.value = null;
}

async function createRoom() {
  loading.value = true;

  try {
    if (!newRoom.value.name || !newRoom.value.capacity || !newRoom.value.conference_id) {
      console.error("Missing required fields.");
      showerror.value = true;
      return;
    }
    const response = await axiosInstance.post('/room/', {
      name: newRoom.value.name,
      capacity: newRoom.value.capacity,
      conference_id: newRoom.value.conference_id,
    });

    console.log('Room created:', response.data);
    closeDialogs();
    await getUser();
  } catch (error) {
    console.error("Error creating room:", error);
    showerror.value = true;
  } finally {
    loading.value = false;
  }
}

async function updateRoom() {
  loading.value = true;

  try {
    const response = await axiosInstance.put(`/room/${selectedRoom.value.id}`, {
      name: selectedRoom.value.name,
      capacity: selectedRoom.value.capacity,
      conference_id: newRoom.value.conference_id,
    });

    console.log('Room updated:', response.data);
    closeDialogs();
    await getUser();
  } catch (error) {
    console.error("Error updating room:", error);
  } finally {
    loading.value = false;
  }
}


onMounted(() => {
  getUser();
})

</script>

<template>
<v-dialog v-model="createDialog" max-width="600px">
  <v-card>
    <v-card-title>Create Room</v-card-title>
    <v-card-text>
      <v-text-field label="Room Name" v-model="newRoom.name"></v-text-field>
      <v-text-field label="Capacity" v-model="newRoom.capacity"></v-text-field>
      <v-select
        v-model="newRoom.conference_id"
        :items="conferencesWithRooms.map(item => ({ id: item.conference.id, name: item.conference.name }))"
        item-title="name"
        item-value="id"
        label="Select Conference"
      ></v-select>
      <v-banner variant="outlined" icon="mdi-close" color="error" v-if="showerror">
        Nepodařilo se vytvořit místnost.
      </v-banner>
    </v-card-text>
    <v-card-actions>
      <v-btn text @click="closeDialogs">Cancel</v-btn>
      <v-btn text @click="createRoom">Create</v-btn>
    </v-card-actions>
  </v-card>
</v-dialog>


  <v-dialog v-model="updateDialog" max-width="600px">
    <v-card v-if="selectedRoom">
      <v-card-title>Update Room</v-card-title>
      <v-card-text>
        <v-text-field label="Room Name" v-model="selectedRoom.name"></v-text-field>
        <v-text-field label="Capacity" v-model="selectedRoom.capacity"></v-text-field>
        <v-select
          v-model="newRoom.conference_id"
          :items="conferencesWithRooms.map(item => ({ id: item.conference.id, name: item.conference.name }))"
          item-title="name"
          item-value="id"
          label="Select Conference"
        ></v-select>
      </v-card-text>
      <v-card-actions>
        <v-btn text @click="closeDialogs">Cancel</v-btn>
        <v-btn text @click="updateRoom">Update</v-btn>
      </v-card-actions>
    </v-card>
  </v-dialog>


  <v-container>
    <div class="my-2">
      <v-btn prepend-icon="mdi-plus" @click="openCreateDialog">Přidat</v-btn>
    </div>
    <v-progress-linear v-if="loading" indeterminate></v-progress-linear>
    <template v-for="item in conferencesWithRooms" :key="item.conference.id">
      <v-list-item>
        <v-list-item-title class="font-weight-bold">{{ item.conference.name }}</v-list-item-title>
      </v-list-item>
      <v-list class="ml-4">
        <template v-if="item.rooms.length === 0">
          <v-list-item>
            <v-list-item-title>Zatím žádné místnosti</v-list-item-title>
          </v-list-item>
        </template>
        <template v-else>
          <v-list-item v-for="room in item.rooms" :key="room.id">
            <v-card class="mx-2">
              <v-list-item-title @click="openUpdateDialog(room)">{{ room.name }}</v-list-item-title>
              <v-list-item-subtitle>{{ room.description }}</v-list-item-subtitle>
            </v-card>
          </v-list-item>
        </template>
      </v-list>
    </template>
  </v-container>
</template>

<style scoped lang="sass">

</style>
