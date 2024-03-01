<template>
  <!-- <HelloWorld /> -->
  <v-container class="d-flex flex-column text-center align-center justify-center" style="height: 100%;">

    <v-card title="文字轉語音" width="500">
      <v-card-text>
        <v-card-subtitle class="text-start">請注意，系統只會保留最新的一萬筆檔案</v-card-subtitle>
        <v-list>
          <template v-for="pair, i in textAndSoundPairs" :key="i">
            <v-dialog width="500">
              <template v-slot:activator="{ props }">

                <v-list-item v-bind="props" :title="pair.text" class="text-start">
                  <template v-slot:append>
                    <v-btn download variant="tonal" color="success" :href="`/api/download/${pair.fileId}`">下載</v-btn>
                  </template>
                </v-list-item>

              </template>

              <v-card>
                <v-card-text>
                  {{ pair.text }}
                </v-card-text>
              </v-card>
            </v-dialog>


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
import { ref } from 'vue';
import { post_api } from '@/utils/api';
import { SnackBar } from '@/utils/model'

const text = ref('')
const speed = ref(2.0)

const autoDownload = ref(false)

const textAndSoundPairs = ref<{
  text: string,
  fileId: string,
}[]>([])

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
      { text: text.value, fileId: snackbar.data as string }
    )
    if (autoDownload.value) {
      const link = document.createElement('a')
      link.href = `/download/${snackbar.data}`;

      link.download = `${snackbar.data}.mp3`
      document.body.appendChild(link)
      link.click()
      document.body.removeChild(link)
    }
  }
  loading.value = false
  text.value = ''


}

</script>
