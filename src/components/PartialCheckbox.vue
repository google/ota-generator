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
  <v-btn
    block
    type="button"
    class="my-5"
    @click="revertAllSelection"
  >
    {{ selectAllText[selectAll] }}
  </v-btn>
  <v-row class="mb-5">
    <v-col
      v-for="label in labels"
      :key="label"
      cols="12"
      md="4"
    >
      <label
        v-if="label"
        class="checkbox"
      >
        <input
          type="checkbox"
          :value="label"
          :checked="partitionSelected.get(label)"
          @change="updateSelected($event.target.value)"
        >
        {{ label }}
      </label>
    </v-col>
  </v-row>
</template>

<script>
export default {
  props: {
    labels: {
      type: Array,
      default: new Array(),
    },
    modelValue: {
      type: Array,
      required: true
    },
  },
  data() {
    return {
      selectAll: 1,
      selectAllText: ['Select All', 'Unselect All'],
      partitionSelected: new Map()
    }
  },
  watch: {
    partitionSelected: {
      handler: function() {
        let list = []
        for (let [key, value] of this.partitionSelected) {
          if (value) {
            list.push(key)
          }
        }
        this.$emit('update:modelValue', list)
      },
      deep: true
    }
  },
  mounted() {
    // Set the default value to be true once mounted if nothing has been selected
    if (this.modelValue.length === 0) {
      for (let key of this.labels) {
        this.partitionSelected.set(key, true)
      }
    } else {
      for (let key of this.labels) {
        this.partitionSelected.set(key, false)
      }
      for (let key of this.modelValue) {
        this.partitionSelected.set(key, true)
      }
    }
    this.$emit('update:modelValue', this.modelValue)
  },
  methods: {
    updateSelected(newSelect) {
      this.partitionSelected.set(newSelect, !this.partitionSelected.get(newSelect))
    },
    revertAllSelection() {
      this.selectAll = 1 - this.selectAll
      for (let key of this.partitionSelected.keys()) {
        this.partitionSelected.set(key, Boolean(this.selectAll))
      }
    },
  }
}
</script>

<style scoped>
ul > li {
  display: inline-block;
  list-style-type: none;
  margin-left: 5%;
  margin-right: 5%;
  top: 0px;
  height: 50px;
}

.checkbox {
  display: block;
  position: relative;
  padding-left: 35px;
  margin-bottom: 12px;
  cursor: pointer;
  -webkit-user-select: none;
  -moz-user-select: none;
  -ms-user-select: none;
  user-select: none;
  transition: all 0.2s ease;
}
</style>