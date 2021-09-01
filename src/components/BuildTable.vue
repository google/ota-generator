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
  <TableLite
    :columns="columns"
    :is-re-search="isReSearch"
    :is-loading="isLoading"
    :rows="rows"
    :sortable="sortable"
    :total="tableLength"
    @do-search="doSearch"
  />
</template>

<script>
import TableLite from 'vue3-table-lite'
import FormDate from '../services/FormDate.js'
import { TableSort } from '../services/TableService.js'

export default {
  components: {
    TableLite
  },
  props: {
    builds: {
      type: Array,
      required: true
    }
  },
  data () {
    return {
      rows: null,
      columns: [
        {
          label: "Build Name",
          field: "file_name",
          sortable: true
        },
        {
          label: "Upload Time",
          field: "time",
          sortable: true,
          display: function (row) {
            return FormDate.formDate(row.time)
          }
        },
        {
          label: "Build ID",
          field: "build_id",
          sortable: true
        },
        {
          label: "Build Version",
          field: "build_version",
          sortable: true
        },
        {
          label: "Build Flavor",
          field: "build_flavor",
          sortable: true
        }
      ],
      sortable: {
        order: "time",
        sort: "desc",
      },
      isReSearch: false,
      isLoading: false,
      total: 0
    }
  },
  computed: {
    tableLength() {
      return this.builds.length
    }
  },
  watch: {
    builds: {
      handler: function() {
        this.rows = TableSort(this.builds, this.sortable.order, this.sortable.sort, 0, 10)
      },
      deep: true
    }
  },
  created() {
    this.rows = TableSort(this.builds, this.sortable.order, this.sortable.sort, 0, 10)
  },
  methods: {
    doSearch(offset, limit, order, sort) {
      this.isLoading = true
      this.sortable.order = order
      this.sortable.sort = sort
      this.rows = TableSort(this.builds, order, sort, offset, limit)
      this.isLoading = false
    }
  }
}
</script>