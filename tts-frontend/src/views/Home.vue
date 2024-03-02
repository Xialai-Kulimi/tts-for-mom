<template>
  <!-- <HelloWorld /> -->
  <v-container class="d-flex flex-column text-center align-center justify-center" style="height: 100%;">

    <v-card title="文字轉語音" max-width="100vw" width="500">
      <v-card-text>
        <v-card-subtitle class="text-start">請注意，系統只會保留最新的一萬筆檔案</v-card-subtitle>
        <v-list>
          <template v-for="pair, i in textAndSoundPairs" :key="i">
            <AudioListItem :model-value="pair"></AudioListItem>


          </template>

        </v-list>

        <v-card-actions>
          <v-textarea variant="solo-filled" flat density="compact" hide-details v-model="text" class="mr-4" auto-grow
            rows="1" placeholder="請輸入要轉換的文字" :loading="loading" :disabled="loading"></v-textarea>
          語速：
          <input type="number" v-model="speed" step="0.1" style="width: 50px;" :disabled="loading">
          <v-btn @click="submit" :disabled="loading">送出</v-btn>
        </v-card-actions>
        <v-card-actions>
          <v-checkbox v-model="autoDownload" label="自動下載" hide-details density="compact" :disabled="loading"></v-checkbox>
          <v-tooltip text="自動根據換行分割成不同語音檔案">
            <template v-slot:activator="{ props }">
              <v-checkbox v-bind="props" v-model="split" label="批次轉換" hide-details density="compact"
                :disabled="loading"></v-checkbox>


            </template>
          </v-tooltip>
        </v-card-actions>
      </v-card-text>
    </v-card>
    <div class="text-center text-caption text-grey mt-4">Made by Kulimi.</div>

  </v-container>
  <template v-for="snackbar, i in snackbarList" :key="i">
    <v-snackbar :model-value="true" :color="snackbar.status">{{ snackbar.message }}
    </v-snackbar>
  </template>
</template>

<script lang="ts" setup>
import AudioListItem from '@/components/AudioListItem.vue';

import { ref } from 'vue';
import { post_api } from '@/utils/api';
import { SnackBar, AudioPair } from '@/utils/model'
import { downloadFile } from '@/utils/utils'

const text = ref('')
const speed = ref(2.0)

const autoDownload = ref(false)
const split = ref(false)

const textAndSoundPairs = ref<AudioPair[]>([])

const loading = ref(false)

const snackbarList = ref<SnackBar[]>([])

function handleResponse(pair: AudioPair) {
  textAndSoundPairs.value.push(
    { text: pair.text, fileId: pair.fileId }
  )
  if (autoDownload.value) {
    downloadFile(pair.fileId)
  }
}

async function submit() {
  if (!text.value) {
    return
  }
  loading.value = true
  const snackbar = await post_api('/sound', { text: text.value, speed: speed.value, split: split.value })
  if (snackbar.status == 'error') {
    snackbarList.value.push(snackbar)

  }
  else {
    if (Array.isArray(snackbar.data)) {
      for (let i = 0; i < snackbar.data.length; i++) {
        const pair = snackbar.data[i];
        handleResponse(pair)
      }
    }
    else {
      handleResponse(snackbar.data)
    }
    text.value = ''
  }
  loading.value = false



}

</script>
