<script setup>
import { ref, onMounted, toRaw } from 'vue';
import { axiosInstance } from "@/router";
import { getUserConferences } from "@/services/utils";


const myPresentations = ref([]);
const conferencePresentations = ref([]);
const loading = ref(true);
const showerror = ref(false);

const conferenceMap = ref({});
const userMap = ref({});

const createDialog = ref(false);
const updateDialog = ref(false);

const newPresentation = ref({ conference_id: null, proposal: '', status: '' });
const selectedPresentation = ref({ conference_id: null, proposal: '', status: '' , id: null});


async function getUser(userId) {
  if (userMap.value[userId]) {
    // If user is already cached, return the cached value
    return userMap.value[userId];
  }
  try {
    const response = await axiosInstance.get(`/user/${userId}`);
    const user = response.data;
    userMap.value[user.id] = user.name; // Cache the username
    return user.name;
  } catch (error) {
    console.error(`Error fetching user with ID ${userId}:`, error);
    return "Unknown User"; // Fallback in case of error
  }
}

async function getConferences() {
  try {
    const response = await axiosInstance.get('/conferences/all');
    const conferences = response.data;

    conferences.forEach(conference => {
      conferenceMap.value[conference.id] = conference.name; // Map conference_id to name
    });
  } catch (error) {
    console.error('Error fetching conferences:', error);
  }
}


async function getPresentations() {
  const userId = Number(localStorage.getItem('userId'));
    conferencePresentations.value = []; // Clear previous data
  try {
    const response = await axiosInstance.get('/given_presentation/all');
    myPresentations.value = response.data.filter(presentation => presentation.user_id === userId);


    // Get presentations for approval
    const conferences = await getUserConferences(userId); // Ensure this is awaited if it's async
    for (const conference of conferences) { // Use 'of' instead of 'in'
      try {
        const filteredPresentations = response.data.filter(presentation => presentation.conference_id === conference.id);
        for(const presentation of filteredPresentations) {
          if (!userMap.value[presentation.user_id]) {
          await getUser(presentation.user_id);
        }
      }
        conferencePresentations.value.push({ conference, presentations: filteredPresentations });
      } catch (error) {
        console.error(error);
      }
    }
  } catch (error) {
    console.error('Error fetching presentations:', error);
  } finally {
    loading.value = false;
  }
}

function openCreateDialog() {
  createDialog.value = true;
}

function closeDialogs() {
  createDialog.value = false;
  updateDialog.value = false;
  selectedPresentation.value = null;
}



function openUpdateDialog(presentation) {
  if (presentation) {
    selectedPresentation.value = { ...presentation };
    updateDialog.value = true;
  } else {
    console.error("Attempted to open update dialog without a room.");
  }
}

async function createPresention(){
  loading.value = true;
  showerror.value = false;

  if(!newPresentation.value.conference_id || !newPresentation.value.proposal){
    showerror.value = true;
    loading.value = false;
    return;
  }

  try{
    const response = await axiosInstance.post('/given_presentation', {
      user_id: localStorage.getItem('userId'),
      conference_id: newPresentation.value.conference_id,
      proposal: newPresentation.value.proposal,
      status: 'pending'
    });
    closeDialogs();
    await getPresentations();
  }
  catch(error){
    console.error('Error creating presentation:', error);
    showerror.value = true;
  }
  finally{
    loading.value = false;
  }
}

async function updatePresentation() {
  loading.value = true;
  showerror.value = false;

  const rawPresentation = toRaw(selectedPresentation.value);

  const { id, conference_id, proposal, status } = rawPresentation;

  // Validate data
  if (!id || !conference_id || !proposal || !status) {
    console.error("Invalid presentation data:", { id, conference_id, proposal, status });
    showerror.value = true;
    loading.value = false;
    return;
  }

  try {
    const response = await axiosInstance.patch(`/given_presentation/${id}`, {
      user_id: Number(localStorage.getItem('userId')),
      conference_id,
      proposal,
      status,
    });

    closeDialogs();
    await getPresentations();
  } catch (error) {
    console.error("Error updating presentation:", error);
    showerror.value = true;
  } finally {
    loading.value = false;
  }
}

async function deletePresentation(presentation) {
  loading.value = true;

  try {
    const response = await axiosInstance.delete(`/given_presentation/${presentation.id}`)
    getPresentations();
  } catch (error) {
    console.error("Error deleting presentation:", error);
    showerror.value = true;
  } finally {
    loading.value = false;
  }
}

async function handlePresentationAction(presentation, action) {
  loading.value = true;
  try {
    await axiosInstance.patch(`/given_presentation/${presentation.id}`, {
      user_id: presentation.user_id,
      conference_id: presentation.conference_id,
      proposal: presentation.proposal,
      status: action,
    });
    await getPresentations();
  } catch (error) {
    console.error(`Error ${action} presentation:`, error);
    showerror.value = true;
  } finally {
    loading.value = false;
  }
}


onMounted(() => {
  loading.value = true;
  getPresentations();
  getConferences();
});
</script>

<template>
  <v-dialog v-model="createDialog" max-width="600px">
    <v-card>
      <v-card-title>Vytvoření prezentace</v-card-title>
      <v-card-text>
        <v-select
          v-model="newPresentation.conference_id"
          :items="Object.entries(conferenceMap).map(([id, name]) => ({ id: Number(id), name }))"
          item-title="name"
          item-value="id"
          label="Select Conference"
      ></v-select>
      <v-text-field label="Návrh" v-model="newPresentation.proposal"></v-text-field>
      </v-card-text>
      <v-card-actions>
      <v-btn text @click="closeDialogs">Zavřít</v-btn>
      <v-btn text @click="createPresention">Vytvořit</v-btn>
    </v-card-actions>
    </v-card>
  </v-dialog>

  <v-dialog v-model="updateDialog" max-width="600px" v-if="selectedPresentation">
    <v-card>
      <v-card-title>Upravení prezentace</v-card-title>
      <v-card-text>
        <v-select
          v-model="selectedPresentation.conference_id"
          :items="Object.entries(conferenceMap).map(([id, name]) => ({ id: Number(id), name }))"
          item-title="name"
          item-value="id"
          label="Select Conference"
      ></v-select>
      <v-text-field label="Návrh" v-model="selectedPresentation.proposal"></v-text-field>
      </v-card-text>
      <v-card-actions>
        <v-btn text @click="closeDialogs">Zavřít</v-btn>
        <v-btn text @click="updatePresentation(selectedPresentation)">Upravit</v-btn>
    </v-card-actions>
    </v-card>
  </v-dialog>

  <div class="my-2">
    <v-btn prepend-icon="mdi-plus" @click="openCreateDialog">Přidat</v-btn>

  </div>
  <v-progress-linear v-if="loading" indeterminate></v-progress-linear>

  <h2 class="mt-5">Vaše prezentace</h2>
  <div v-if="myPresentations.length === 0" class="mx-auto text-center">
    Ještě nemáte žádné prezentace
  </div>

  <v-list v-else>
    <v-list-item v-for="presentation in myPresentations" :key="presentation.id"> <!-- Corrected variable -->
      <v-card>
        <v-list-item-title>{{ conferenceMap[presentation.conference_id] }}</v-list-item-title>
        <v-list-item-subtitle>{{ presentation.proposal }}</v-list-item-subtitle>
        <v-card-actions>
          <v-btn @click="openUpdateDialog(presentation)">Upravit</v-btn>
          <v-btn @click="deletePresentation(presentation)">Smazat</v-btn>
        </v-card-actions>
      </v-card>
    </v-list-item>
  </v-list>

  <h2 class="mt-5">Prezentace k schválení</h2>
  <div v-if="conferencePresentations.length === 0" class="mx-auto text-center">
    Žádné prezentace k schválení
  </div>

  <v-list v-else>
    <div v-if="conferencePresentations.length === 0">
      žádné prezentace k schválení
    </div>
    <template v-else>
      <template v-for="item in conferencePresentations" :key="item.conference.id">
        <v-list-item>
          <v-list-item-title class="font-weight-bold">{{ item.conference.name }}</v-list-item-title>
        </v-list-item>
        <v-list class="ml-4">
          <div v-if="item.presentations.length === 0">
            <p class="ml-4">všechny prezentace byly schváleny </p>
          </div>
          <v-list-item v-for="presentation in item.presentations" :key="presentation.id">
            <div v-if="presentation.status === 'pending'">
              <v-card class="mx-2">
                <v-list-item-title>{{ userMap[presentation.user_id] || "Fetching user..." }}</v-list-item-title>
                <v-list-item-subtitle>{{ presentation.proposal }}</v-list-item-subtitle>
                <v-card-actions>
                  <v-btn color="green" @click="handlePresentationAction(presentation, 'accepted')">Schválit</v-btn>
                  <v-btn color="red" @click="handlePresentationAction(presentation, 'declined')">Odmítnout</v-btn>
                </v-card-actions>
              </v-card>
            </div>
            <div v-else>
              všechny prezentace byly schváleny
            </div>
          </v-list-item>
        </v-list>
      </template>
    </template>
  </v-list>
</template>

<style scoped lang="sass">

</style>
