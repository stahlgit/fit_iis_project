<script setup>
import { ref, onMounted } from "vue";
import { axiosInstance } from "@/router";

const loading = ref(false);
const currentAccount = ref(null)

const conferences = ref([]);
const createDialog = ref(false);
const newConference = ref({
  name: "",
  description: "",
  genre: "",
  place: "",
  start_time: "",
  end_time: "",
  price: "",
  capacity: "",
});
const showerror = ref(false);
const formattedStartTime = ref("");
const formattedEndTime = ref("");

const isValidMonth = ref(true);
const isValidDay = ref(true);
const isValidHour = ref(true);
const isValidMinute = ref(true);

function formatDateTime(type) {
  showerror.value = false;
  isValidMonth.value = true;
  isValidDay.value = true;
  isValidHour.value = true;
  isValidMinute.value = true;


  const rawValue = type === "start" ? formattedStartTime.value : formattedEndTime.value;

  const numbers = rawValue.replace(/\D/g, "");

  let formatted = "";
  let isValid = true;
  if (numbers.length >= 4) formatted += numbers.slice(0, 4) + "-";
  if (numbers.length >= 6) formatted += numbers.slice(4, 6) + "-";
  if (numbers.length >= 8) formatted += numbers.slice(6, 8) + " ";
  if (numbers.length >= 10) formatted += numbers.slice(8, 10) + ":";
  if (numbers.length >= 12) formatted += numbers.slice(10, 12);

  const yearPart = parseInt(numbers.slice(0, 4), 10);
  const monthPart = parseInt(numbers.slice(4, 6), 10);
  const dayPart = parseInt(numbers.slice(6, 8), 10);
  const hourPart = parseInt(numbers.slice(8, 10), 10);
  const minutePart = parseInt(numbers.slice(10, 12), 10);

  if (monthPart < 1 || monthPart > 12) {
    isValid = false;
    console.error("Invalid month input: Month must be between 01 and 12.");
    showerror.value = true;
    return;
  }

  // Check day validity based on the month
  const daysInMonth = new Date(yearPart, monthPart, 0).getDate(); // Get last day of the month
  if (dayPart < 1 || dayPart > daysInMonth) {
    isValid = false;
    console.error(`Invalid day input: Day must be between 01 and ${daysInMonth}.`);
    showerror.value = true;
    return;
  }

   // Validate hours and minutes
  if (hourPart < 0 || hourPart > 23) { // Change here to allow only up to HH:23
    isValid = false;
    console.error("Invalid time input: Hours must be between 00-23.");
    showerror.value = true;
    return;
  }

  if (minutePart < 0 || minutePart > 59) { // Change here to allow only up to MM:59
    isValid = false;
    console.error("Invalid time input: Minutes must be between 00-59.");
    showerror.value = true;
    return;
  }

  // Assign the formatted value to the appropriate field
  if (type === "start") {
    formattedStartTime.value = formatted;
    newConference.value.start_time = formatted;
  } else {
    formattedEndTime.value = formatted;
    newConference.value.end_time = formatted;
  }
  showerror.value = !isValid;
}

async function fetchConferences() {
  loading.value = true;
  try {
    const response = await axiosInstance.get("conferences/all");
    conferences.value = response.data;
  } catch (error) {
    console.error(error);
  } finally {
    loading.value = false;
  }
}

async function createConference() {
  loading.value = true;
  showerror.value = false;

  try {
    if (!newConference.value.name.trim()) {
      console.error("Missing required fields.");
      showerror.value = true;
      return;
    }

    const response = await axiosInstance.post('/conferences/', {
      name: newConference.value.name,
      description: newConference.value.description,
      genre: newConference.value.genre,
      place: newConference.value.place,
      start_time: newConference.value.start_time,
      end_time: newConference.value.end_time,
      price: newConference.value.price,
      capacity: newConference.value.capacity,
      organizer_id: currentAccount.value.id,
    });    console.log("Conference created:", response.data);
    closeDialogs();
    await fetchConferences();
  } catch (error) {
    console.error("Error creating conference:", error.response?.data || error.message);
    showerror.value = true;
  } finally {
    loading.value = false;
  }
}

function openCreateDialog() {
  createDialog.value = true;
}

function closeDialogs() {
  createDialog.value = false;
  showerror.value = false;
}

async function getAccount(){
  loading.value = true;
  try {
    const userResponse = await axiosInstance.get('/user/me');
    currentAccount.value = userResponse.data;
  } catch (error) {
    console.error("Error fetching account:", error);
  } finally {
    loading.value = false;
  }
}

async function initialize() {
  await Promise.all([fetchConferences(), getAccount()]);
}


onMounted(initialize);
</script>


<template>
  <v-dialog v-model="createDialog" max-width="600px">
    <v-card>
      <v-card-title>Create Conference</v-card-title>
      <v-card-text>
        <v-text-field label="Conference Name" v-model="newConference.name"></v-text-field>
        <v-text-field label="Description" v-model="newConference.description"></v-text-field>
        <v-text-field label="Genre" v-model="newConference.genre"></v-text-field>
        <v-text-field label="Place" v-model="newConference.place"></v-text-field>

        <v-text-field
          v-model="formattedStartTime"
          label="Start Time"
          :placeholder="formattedStartTime.length < 16 ? 'YYYY-MM-DD HH:MM' : ''"
          aria-placeholder="YYYY-MM-DD HH:MM"
          @input="formatDateTime('start')"
          maxlength="16"
        />

        <v-text-field
          v-model="formattedEndTime"
          label="End Time"
          :placeholder="formattedEndTime.length < 16 ? 'YYYY-MM-DD HH:MM' : ''"
          aria-placeholder="YYYY-MM-DD HH:MM"
          @input="formatDateTime('end')"
          maxlength="16"
        />
        <v-banner variant="outlined" icon="mdi-alert" color="error" v-if="showerror">
          Invalid input. Please check:
          <ul>
              <li v-if="!isValidMonth">Month must be between January (01) and December (12).</li>
              <li v-if="!isValidDay">Day must be valid for the selected month.</li>
              <li v-if="!isValidHour">Hours must be between <strong>00</strong> and <strong>23</strong>.</li>
              <li v-if="!isValidMinute">Minutes must be between <strong>00</strong> and <strong>59</strong>.</li>
          </ul>
      </v-banner>

        <v-text-field label="Price" v-model="newConference.price"></v-text-field>
        <v-text-field label="Capacity" v-model="newConference.capacity"></v-text-field>
        <v-banner variant="outlined" icon="mdi-alert" color="error" v-if="showerror">
          Missing required fields. Please check your inputs.
        </v-banner>
      </v-card-text>
      <v-card-actions>
        <v-btn text @click="closeDialogs">Cancel</v-btn>
        <v-btn text @click="createConference">Create</v-btn>
      </v-card-actions>
    </v-card>
  </v-dialog>

  <v-container>
    <div class="my-2">
      <v-btn prepend-icon="mdi-plus" @click="openCreateDialog">Add Conference</v-btn>
    </div>
    <v-progress-linear v-if="loading" indeterminate></v-progress-linear>
    <v-list>
      <v-list-item v-for="conference in conferences" :key="conference.id">
        <v-card>
          <v-list-item-title>{{ conference.name }}</v-list-item-title>
          <v-list-item-subtitle>{{ conference.description }}</v-list-item-subtitle>
        </v-card>
      </v-list-item>
    </v-list>
  </v-container>
</template>


<style scoped lang="sass">

</style>
