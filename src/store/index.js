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

import { createStore } from 'vuex'
import { OTAConfiguration, OTAExtraFlags } from '@/services/JobSubmission.js'

export default createStore({
  state: {
    otaConfig: new OTAConfiguration(),
    targetBuilds: [],
    sourceBuilds: []
  },
  mutations: {
    REUSE_CONFIG(state, config) {
      state.otaConfig.verbose = config.verbose
      state.otaConfig.isIncremental = config.isIncremental
      state.otaConfig.partial = config.partial
      state.otaConfig.isPartial = config.isPartial
      state.targetBuilds = [config.target]
      if (config.isIncremental)
        state.sourceBuilds = [config.incremental]
      const extra =
        config.extra.split('--')
          .filter((s) => s!=='')
          .map((s) => s.trimRight())
      extra.forEach( (key) => {
        if (OTAExtraFlags.filter((flags) => flags.key == key)) {
          state.otaConfig[key] = true
        } else {
          state.extra += key
        }
      })
    },
    SET_CONFIG(state, config) {
      state.otaConfig = config
    },
    RESET_CONFIG(state) {
      state.otaConfig = new OTAConfiguration()
    },
    SET_TARGET(state, target) {
      state.targetBuilds = [target]
    },
    SET_SOURCE(state, target) {
      state.sourceBuilds = [target]
    },
    SET_TARGETS(state, targets) {
      state.targetBuilds = targets
    },
    SET_SOURCES(state, targets) {
      state.sourceBuilds = targets
    },
    SET_ISINCREMENTAL(state, isIncremental) {
      state.otaConfig.isIncremental = isIncremental
    }
  },
  actions: {},
  modules: {}
})
