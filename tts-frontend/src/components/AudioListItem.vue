<template>
    <v-dialog width="500" v-if="modelValue">
        <template v-slot:activator="{ props }">

            <v-list-item v-bind="props" :title="modelValue.text" class="text-start">
                <template v-slot:append v-if="audio">
                    <!-- <audio controls>
                      <source :src="`/api/download/${pair.fileId}`" type="audio/mpeg">
                    </audio> -->
                    <v-fade-transition>

                        <v-btn icon="mdi-stop" variant="text" @click.stop="stop" v-show="isPlaying"></v-btn>
                    </v-fade-transition>

                    <v-progress-circular :model-value="progress">
                        <v-btn icon="mdi-play" variant="text" @click.stop="play" v-show="!isPlaying"></v-btn>
                        <v-btn icon="mdi-pause" variant="text" @click.stop="pause" v-show="isPlaying"></v-btn>
                    </v-progress-circular>

                    <v-btn variant="text" icon="mdi-download" @click.stop="downloadFile(modelValue.fileId)"></v-btn>
                </template>
            </v-list-item>

        </template>

        <v-card :text="modelValue.text">
            <!-- <v-card-text>
                  {{  }}
                </v-card-text> -->
        </v-card>
    </v-dialog>
</template>
<script setup lang="ts">
import { PropType } from 'vue';
import { downloadFile } from '@/utils/utils'
import { AudioPair } from '@/utils/model';
import { ref } from 'vue';
import { onMounted } from 'vue';

const audio = ref<HTMLAudioElement>()
const isPlaying = ref(false)

const props = defineProps({
    modelValue: {
        type: Object as PropType<AudioPair>
    }
})

const progress = ref(0)

function loadAudio() {
    if (props.modelValue) {
        audio.value = new Audio(`/api/download/${props.modelValue.fileId}`)
    }
    setInterval(() => {
        if (audio.value) {
            progress.value = ((audio.value.currentTime / audio.value.duration)) * 100
        }
    }, 100)
}

function stop() {
    isPlaying.value = false
    if (audio.value) {
        audio.value.pause()
        audio.value.currentTime = 0
    }
}

function play() {
    if (audio.value) {

        isPlaying.value = true
        audio.value.play()
        audio.value.onended = stop
    }
}


function pause() {
    if (audio.value) {
        isPlaying.value = false
        audio.value.pause()
    }

}

onMounted(loadAudio)

</script>