<script setup lang="ts">
import {ref} from 'vue'
import experienceData from '../data/workexperience.json'

const data = ref(experienceData.experience)

    for(const experience of data.value){
    console.log(data.value)
    let summary = experience.description;
    const arr = summary.split(". ");

    experience.summary = arr;
  }

</script>

<template>
  <div id="experience" class="experience-section">
    <h1 >Experience</h1>
<v-sheet
 color="rgb(38, 34, 77)"
 elevation="1" 
 rounded="lg"
  >
    
    <div class="d-flex flex-row">
    <v-tabs
      v-model="data[0].id"
      :items="data"
      
      height="60" 
      slider-color="rgb(59, 55, 105)"
      direction="vertical"
    >
      <template v-slot:tab="{ item }">
        <v-tab
          :text="item.company"
          :value="item.company"
          class="text-none"
        ></v-tab>
      </template>

      <template v-slot:item="{ item }">
        <v-tabs-window-item
        
          :value="item.company"
           class="window-item"
            >
          <div class="experience-details">
            <h3>{{ item.title }} @ {{ item.company }}</h3>
            <h4>{{ item.startDate }} - {{ item.endDate }}</h4>
          </div>

          <div class="experience-summary">
            <ul v-for="text of item.summary">
              <li>{{ text }}</li>
            </ul>
          </div>
          
    
        </v-tabs-window-item>
      </template>
    </v-tabs>
  </div>
  </v-sheet>
  </div>
  
</template>

<style scoped>

.experience-section {
  margin: 0 auto;
  width: 80vw;
}

.window-item {
  width: 55vw;
  /* margin-right: 20px; */
  margin: 0 auto;
  padding: 0 30px;
}

.experience-summary {
  margin-top: 20px;
  padding-left: 30px;
  margin-right: 10px;
  margin-bottom: 20px;
  
}

@media screen and (width <= 875px) {

  .experience-details {
    margin-right: 20px;
    padding-right: 20px;
  }
  .experience-summary {
  margin-right: 20px;
  padding-right: 20px;
}
}

</style>