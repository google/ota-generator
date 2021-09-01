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
  <ul v-if="job">
    <li> <strong> Start Time: </strong> {{ formDate(job.start_time) }}</li>
    <li v-if="job.finish_time > 0">
      <strong> Finish Time: </strong> {{ formDate(job.finish_time) }}
    </li>
    <li v-if="job.isIncremental">
      <strong> Incremental source: </strong> {{ job.incremental_name }}
    </li>
    <li v-if="job.isIncremental && buildDetail">
      <strong> Incremental source version: </strong> {{ job.incremental_build_version }}
    </li>
    <li> <strong> Target source: </strong> {{ job.target_name }}</li>
    <li v-if="buildDetail">
      <strong> Target source version: </strong> {{ job.target_build_version }}
    </li>
    <li v-if="job.isPartial">
      <strong> Partial: </strong> {{ job.partial }}
    </li>
  </ul>
</template>

<script>
import FormDate from '../services/FormDate.js'

export default {
  props: {
    job: {
      type: Object,
      required: true,
      default: null,
    },
    buildDetail: {
      type: Boolean,
      default: false,
    },
  },
  methods: {
    formDate(unixTime) {
      return FormDate.formDate(unixTime)
    },
  },
}
</script>

<style scoped>
ul > li {
  list-style: none;
  text-align: center;
}
</style>