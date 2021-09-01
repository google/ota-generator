/**
 * Copyright 2021 Google LLC
 *
 * Licensed under the Apache License, Version 2.0 (the "License");
 * you may not use this file except in compliance with the License.
 * You may obtain a copy of the License at
 *
 *      http://www.apache.org/licenses/LICENSE-2.0
 *
 * Unless required by applicable law or agreed to in writing, software
 * distributed under the License is distributed on an "AS IS" BASIS,
 * WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
 * See the License for the specific language governing permissions and
 * limitations under the License.
 */

import axios from 'axios'

const baseURL = process.env.NODE_ENV === 'production' ? '' : 'http://localhost:5000';

console.log(`Build mode: ${process.env.NODE_ENV}, API base url ${baseURL}`);

const apiClient = axios.create({
  baseURL,
  withCredentials: false,
  headers: {
    Accept: 'application/json',
    'Content-Type': 'application/json'
  }
});

export default {
  getDownloadURLForJob(job) {
    return `${baseURL}/download/${job.output}`;
  },
  getJobs() {
    return apiClient.get("/check")
  },
  getJobById(id) {
    return apiClient.get("/check/" + id)
  },
  async getBuildList() {
    let resp = await apiClient.get("/file");
    return resp.data || [];
  },
  async reconstructBuildList() {
    let resp = await apiClient.get("/reconstruct_build_list");
    return resp.data;
  },
  uploadTarget(file, onUploadProgress) {
    let formData = new FormData()
    formData.append('file', file)
    return apiClient.post("/file/" + file.name,
      formData,
      {
        onUploadProgress
      })
  },
  async postInput(input, id) {
    try {
      let resp = await apiClient.post(
        '/run/' + id, JSON.stringify(input));
      return resp.data;
    } catch (error) {
      if (error.response.data) {
        return error.response.data;
      } else {
        throw error;
      }
    }
  }
}