<script>
export default {
  name: "PublicView"
}
</script>

<template>
  <v-app-bar>
    <v-app-bar-title>
      Konference v0.1
    </v-app-bar-title>
    <v-spacer/>
    <v-btn to="/login">
      Přihlásit se
    </v-btn>
  </v-app-bar>

  <div class="d-flex flex-wrap justify-center" style="flex: 1 1 30%">
    <v-card title="Kokotinec" subtitle="Super prezentace">
      <v-card-text>
        Lorem ipsum dolor sit amet, consectetur adipiscing elit. Nulla nec purus euismod, fermentum turpis in, ultricies nunc
      </v-card-text>
      <v-card-actions>
        <v-btn>
          Zobrazit
        </v-btn>
      </v-card-actions>
    </v-card>

    <v-card title="Kokotinec" subtitle="Super prezentace">
      <v-card-text>
        Lorem ipsum dolor sit amet, consectetur adipiscing elit. Nulla nec purus euismod, fermentum turpis in, ultricies nunc
      </v-card-text>
      <v-card-actions>
        <v-btn>
          Zobrazit
        </v-btn>
      </v-card-actions>
    </v-card>

    <v-card title="Kokotinec" subtitle="Super prezentace">
      <v-card-text>
        Lorem ipsum dolor sit amet, consectetur adipiscing elit. Nulla nec purus euismod, fermentum turpis in, ultricies nunc
      </v-card-text>
      <v-card-actions>
        <v-btn>
          Zobrazit
        </v-btn>
      </v-card-actions>
    </v-card>

    <v-card title="Kokotinec" subtitle="Super prezentace">
      <v-card-text>
        Lorem ipsum dolor sit amet, consectetur adipiscing elit. Nulla nec purus euismod, fermentum turpis in, ultricies nunc
      </v-card-text>
      <v-card-actions>
        <v-btn>
          Zobrazit
        </v-btn>
      </v-card-actions>
    </v-card>

    <v-card title="Kokotinec" subtitle="Super prezentace">
      <v-card-text>
        Lorem ipsum dolor sit amet, consectetur adipiscing elit. Nulla nec purus euismod, fermentum turpis in, ultricies nunc
      </v-card-text>
      <v-card-actions>
        <v-btn>
          Zobrazit
        </v-btn>
      </v-card-actions>
    </v-card>
  </div>
</template>

<style scoped lang="sass">
.v-card
  margin: 20px
  padding: 20px
  max-width: 450px

</style>
