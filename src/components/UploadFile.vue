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
  <div>
    <BaseFile
      label="Upload a target file"
      @file-select="UploadHandler"
    />
    <br>
    <progress
      v-if="uploadPercentage > 0"
      max="100"
      :value.prop="uploadPercentage"
    />
  </div>
</template>

<script>
import BaseFile from '@/components/BaseFile.vue'
import ApiService from '../services/ApiService.js'

export default {
  components: {
    BaseFile,
  },
  data() {
    return {
      files: '',
      uploadPercentage: 0,
    }
  },
  methods: {
    async UploadHandler(files) {
      this.file = files[0]
      console.log(this.file.name)
      try {
        let response = await ApiService.uploadTarget(this.file, (event) => {
          this.uploadPercentage = Math.round((100 * event.loaded) / event.total)
        })
        console.log(response)
        this.$emit('file-uploaded')
      } catch (err) {
        console.log(err)
      }
    },
  },
}
</script>

<style scoped>
progress {
  width: 100%;
  height: 40px;
}
</style>