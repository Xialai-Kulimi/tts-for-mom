<template>
  <!-- <HelloWorld /> -->
  <v-container class="d-flex flex-column text-center align-center justify-center" style="height: 100%;">

    <v-card title="文字轉語音" width="500">
      <v-card-text>
        <v-card-subtitle class="text-start">請注意，系統只會保留最新的一萬筆檔案</v-card-subtitle>
        <v-list>
          <template v-for="pair, i in textAndSoundPairs" :key="i">
            <AudioListItem :model-value="pair"></AudioListItem>


          </template>

        </v-list>


        <v-card-actions>
          <v-text-field variant="solo-filled" flat density="compact" hide-details v-model="text" class="mr-4"
            placeholder="請輸入要轉換的文字" @keydown.enter="submit" :loading="loading" :disabled="loading"></v-text-field>
          語速：
          <input type="number" v-model="speed" step="0.1" style="width: 50px;">
          <v-btn @click="submit">送出</v-btn>
        </v-card-actions>
        <v-card-actions>

          <v-checkbox v-model="autoDownload" label="自動下載" hide-details density="compact"></v-checkbox>
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

const textAndSoundPairs = ref<AudioPair[]>([])

const loading = ref(false)

const snackbarList = ref<SnackBar[]>([])


async function submit() {
  if (!text.value) {
    return
  }
  loading.value = true
  const snackbar = await post_api('/sound', { text: text.value, speed: speed.value })
  if (snackbar.status == 'error') {
    snackbarList.value.push(snackbar)

  }
  else {
    textAndSoundPairs.value.push(
      // var audio = new Audio(`/api/download/${fileId}`);
      { text: text.value, fileId: snackbar.data as string }
    )
    if (autoDownload.value) {
      downloadFile(snackbar.data)
    }
    text.value = ''
  }
  loading.value = false



}

</script>
