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
  <label class="file-select ma-5">
    <div
      class="select-button"
      @dragover="dragover"
      @dragleave="dragleave"
      @drop="drop"
    >
      <span v-if="label">{{ !fileName ? label : '' }}</span>
      <span v-else>Select File</span>
      <div v-if="fileName"> File selected: {{ fileName }}</div>
    </div>
    <input
      ref="file"
      type="file"
      accept=".zip"
      @change="handleFileChange"
    >
  </label>
</template>

<script>
export default {
  props: {
    label: {
      type: String,
      default: '',
    },
  },
  data() {
    return {
      fileName: '',
    }
  },
  methods: {
    handleFileChange(event) {
      this.$emit('file-select', this.$refs.file.files)
      this.fileName = this.$refs.file.files[0].name
    },
    dragover(event) {
      event.preventDefault()
      if (!event.currentTarget.classList.contains('file-hover')) {
        event.currentTarget.classList.add('file-hover')
      }
    },
    dragleave(event) {
      event.currentTarget.classList.remove('file-hover')
    },
    drop(event) {
      event.preventDefault()
      this.$refs.file.files = event.dataTransfer.files
      this.handleFileChange(event)
      event.currentTarget.classList.remove('file-hover')
    },
  },
}
</script>

<style scoped>
.file-select > .select-button {
  padding: 3rem;
  border-radius: 0.3rem;
  border: 4px dashed #eaebec;
  text-align: center;
  font-weight: bold;
  cursor: pointer;
}

.file-select > input[type='file'] {
  display: none;
}

.file-hover {
  background-color: #95e995;
}
</style>