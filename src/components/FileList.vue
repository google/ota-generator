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
  <h4> {{ label }} </h4>
  <select
    class="list-box"
    :size="modelValue.length + 1"
    v-bind="$attrs"
    @click="selected=$event.target.value"
  >
    <option
      v-for="build in modelValue"
      :key="build"
      :selected="build === selected"
    >
      {{ build }}
    </option>
  </select>
  <v-row
    class="my-2"
  >
    <v-col
      cols="12"
      md="4"
    >
      <v-btn
        :disabled="!selected"
        block
        @click="deleteSelected"
      >
        Remove selected item
      </v-btn>
    </v-col>
    <v-col
      cols="12"
      md="4"
    >
      <v-btn
        v-if="movable"
        :disabled="!selected"
        block
        @click="moveSelected(-1)"
      >
        &#128316;
      </v-btn>
    </v-col>
    <v-col
      cols="12"
      md="4"
    >
      <v-btn
        v-if="movable"
        :disabled="!selected"
        block
        @click="moveSelected(1)"
      >
        &#128317;
      </v-btn>
    </v-col>
  </v-row>
</template>

<script>
export default {
  props: {
    label: {
      type: String,
      required: true
    },
    modelValue: {
      type: Array,
      required: true
    },
    movable: {
      type: Boolean,
      default: false
    }
  },
  data() {
    return {
      selected: null
    }
  },
  methods: {
    deleteSelected() {
      let deleteIndex = this.modelValue.indexOf(this.selected)
      if (deleteIndex > 0) {
        this.$emit(
          "update:modelValue",
          this.modelValue
            .slice(0, deleteIndex)
            .concat(
              this.modelValue.slice(
                deleteIndex+1,
                this.modelValue.length
              ))
        )
      } else {
        this.$emit(
          "update:modelValue",
          this.modelValue.slice(1, this.modelValue.length)
        )
      }
      this.selected = null
    },
    moveSelected(direction) {
      let selectedIndex = this.modelValue.indexOf(this.selected)
      if (selectedIndex + direction > this.modelValue.length ||
        selectedIndex + direction < 0) {
        return
      }
      let tempArray = Array.from(this.modelValue)
      let temp = this.modelValue[selectedIndex]
      tempArray[selectedIndex] = tempArray[selectedIndex + direction]
      tempArray[selectedIndex + direction] = temp
      this.$emit("update:modelValue", tempArray)
    }
  }
}
</script>

<style scoped>
.list-box {
  width: 100%;
}
</style>