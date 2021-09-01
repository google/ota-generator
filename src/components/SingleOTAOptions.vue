<!--
 Copyright 2021 Google LLC

 Licensed under the Apache License, Version 2.0 (the "License");
 you may not use this file except in compliance with the License.
 You may obtain a copy of the License at

      http://www.apache.org/licenses/LICENSE-2.0

 Unless required by applicable law or agreed to in writing, software
 distributed under the License is distributed on an "AS IS" BASIS,
 WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
 See the License for the specific language governing permissions and
 limitations under the License.
-->

<template>
  <form @submit.prevent="sendForm">
    <FileSelect
      v-if="checkIncremental"
      v-model="incrementalSource"
      label="Select the source file"
      :options="targetDetails"
    />
    <FileSelect
      v-model="targetBuild"
      label="Select a target file"
      :options="targetDetails"
    />
    <OTAOptions
      :targetDetails="targetDetails"
      :targetBuilds="[targetBuild]"
    />
    <v-divider class="my-5" />
    <v-btn
      block
      type="submit"
    >
      Submit
    </v-btn>
  </form>
</template>

<script>
import OTAOptions from '@/components/OTAOptions.vue'
import FileSelect from '@/components/FileSelect.vue'

export default {
  components: {
    OTAOptions,
    FileSelect,
  },
  props: {
    targetDetails: {
      type: Array,
      default: () => [],
    }
  },
  data() {
    return {
    }
  },
  computed: {
    checkIncremental() {
      return this.$store.state.otaConfig.isIncremental
    },
    incrementalSource: {
      get() {
        return this.$store.state.sourceBuilds[0]
      },
      set(target) {
        this.$store.commit('SET_SOURCE', target)
      }
    },
    targetBuild: {
      get() {
        return this.$store.state.targetBuilds[0]
      },
      set(target) {
        this.$store.commit('SET_TARGET', target)
      }
    }
  },
  created() {
    this.$emit('update:handler', this.setIncrementalSource, this.setTargetBuild)
  },
  methods: {
    /**
     * Send the configuration to the backend.
     */
    async sendForm() {
      try {
        let data = await this.$store.state.otaConfig.sendForm(
          this.targetBuild, this.incrementalSource)
        alert(data.msg);
        this.$store.state.otaConfig.reset()
        this.$store.commit('SET_TARGETS', [])
        this.$store.commit('SET_SOURCES', [])
      } catch (err) {
        alert(
          'Job cannot be started properly for the following reasons: ' + err
        )
      }
    },
    setIncrementalSource (build) {
      this.incrementalSource = build
    },
    setTargetBuild (build) {
      this.targetBuild = build
    }
  },
}
</script>