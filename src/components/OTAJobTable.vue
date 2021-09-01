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
    jobs: {
      type: Array,
      required: true
    }
  },
  data () {
    return {
      rows: null,
      columns: [
        {
          label: "Source build",
          field: "incremental_name",
          sortable: true
        },
        {
          label: "Target build",
          field: "target_name",
          sortable: true
        },
        {
          label: "Status",
          field: "status",
          sortable: true,
          display: function (row) {
            return (
              "<a href=/check-job/" + row.id + '>'
              + row.status
              + "</a>"
            );
          }
        },
        {
          label: "Partial",
          field: "isPartial",
          sortable: true
        },
        {
          label: "Start Time",
          field: "start_time",
          sortable: true,
          display: function (row) {
            return FormDate.formDate(row.start_time)
          }
        },
        {
          label: "Finish Time",
          field: "finish_time",
          sortable: true,
          display: function (row) {
            return FormDate.formDate(row.finish_time)
          }
        },
      ],
      sortable: {
        order: "start_time",
        sort: "desc",
      },
      isReSearch: false,
      isLoading: false,
      total: 0
    }
  },
  computed: {
    tableLength() {
      return this.jobs.length
    },
  },
  watch: {
    jobs: {
      handler: function() {
        this.rows = TableSort(this.jobs, this.sortable.order, this.sortable.sort, 0, 10)
      },
      deep: true
    }
  },
  created() {
    this.rows = TableSort(this.jobs, this.sortable.order, this.sortable.sort, 0, 10)
  },
  methods: {
    doSearch(offset, limit, order, sort) {
      this.isLoading = true
      this.sortable.order = order
      this.sortable.sort = sort
      this.rows = TableSort(this.jobs, order, sort, offset, limit)
      this.isLoading = false
    }
  }
}
</script>