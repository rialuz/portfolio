<script setup lang="ts">
import {ref} from 'vue'
import experienceData from '../data/workexperience.json'
import { onMounted, nextTick } from 'vue';
import { onBeforeUnmount } from 'vue';

const data = ref(experienceData.experience);

const regex = /(\b(https?|ftp|file):\/\/[-A-Z0-9+&@#\/%?=~_|!:,.;]*[-A-Z0-9+&@#\/%=~_|])/ig;

    for(const experience of data.value){
    console.log(data.value);
    let summary = experience.description;
    const arr = summary.split(". ");

    experience.summary = arr;

  
    const url = experience.description.match(regex);
    console.log(url);
  }

  const innerWidth = ref(window.innerWidth);

  onMounted( async () => {
   await nextTick(() => {
      window.addEventListener('resize',onResize);
    })
  })

  onBeforeUnmount(() => {
    window.removeEventListener('resize', onResize);
  })

  const onResize = () => {
    innerWidth.value = window.innerWidth;
  }


</script>

<template>
  <div id="experience" class="experience-section">
    <h1 >Experience</h1>
<v-sheet
 color="#ede8f5"
 elevation="1" 
 rounded="lg"
 class="v-sheet"
  >
    
    <div :class="(innerWidth < 675) ? 'mx-auto' :'d-flex flex-row'">
    <v-tabs
      v-model="data[0].id"
      :items="data"
      color="#3d52a0"
      height="60" 
      slider-color="#7091e6"
      :direction="(innerWidth < 675) ? 'horizontal' : 'vertical'"
    >
      <template v-slot:tab="{ item }">
        <v-tab
          :text="item.company"
          :value="item.company"
          class="text-none"
          color="#3d52a0"
        ></v-tab>
      </template>

      <template v-slot:item="{ item }">
        <v-tabs-window-item
          
          :value="item.company"
            >
          <div class="experience-details">
            <h3>{{ item.title }} @ {{ item.company }}</h3>
            <h4>{{ item.startDate }} - {{ item.endDate }}</h4>
          </div>

          <div class="experience-summary">
            <ul v-for="text of item.summary">
              <li>{{ text }}</li><a v-if="text.includes('Selected')" href="https://www.catalyte.io/alumni-stories/luz/">https://www.catalyte.io/alumni-stories/luz/</a>
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

.v-sheet {
  color: #3d52a0 !important;
}

.experience-section {
  margin: 0 auto;
  width: 80vw;
  color: #3d52a0;
}

/* .window-item {
  width: 55vw;
  margin: 0 auto;
  padding: 0 30px;
} */

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