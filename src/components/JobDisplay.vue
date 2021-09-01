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
  <router-link :to="{ name: 'JobDetails', params: { id: job.id } }">
    <div class="job-display">
      <span>Status of Job.{{ job.id }}</span>
      <h4>{{ job.status }}</h4>
      <div v-show="active">
        <v-divider class="my-3" />
        <JobConfiguration
          :job="job"
          :build-detail="false"
        />
      </div>
    </div>
  </router-link>
</template>

<script>
import JobConfiguration from '../components/JobConfiguration.vue'

export default {
  components: {
    JobConfiguration
  },
  props: {
    job: {
      type: Object,
      required: true,
    },
    active: {
      type: Boolean,
      default: false,
    },
  }
}
</script>

<style>
.job-display {
  padding: 5%;
  width: 90%;
  cursor: pointer;
  border: 1px solid #39495c;
  margin-bottom: 18px;
}

.job-display:hover {
  transform: scale(1.01);
  box-shadow: 0 3px 12px 0 rgba(0, 0, 0, 0.2);
}
</style>
