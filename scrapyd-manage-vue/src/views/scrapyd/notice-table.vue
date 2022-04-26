<template>
  <div class="app-container">
    <template>
      <el-table v-loading="TableLoading" v-el-table-infinite-scroll="loaddata" :data="noticeData" stripe="true" :height="tableHeight" :header-cell-style="{background:'#eef1f6',color:'#606266'}" :row-style="{height:'10px'}" :cell-style="{padding:'7px'}">
        <el-table-column type="index" label="Id" header-align="center" align="center" width="80" />
        <el-table-column prop="project" label="Project" show-overflow-tooltip="true" header-align="center" align="center" min-width="60" width="120" />
        <el-table-column prop="spider" label="Spider" header-align="center" align="center" min-width="60" width="120" />
        <el-table-column prop="title" label="Title" header-align="center" align="center" min-width="50" />
        <el-table-column prop="content" label="Content" header-align="center" align="center" min-width="100" />
        <el-table-column prop="level" label="Level" show-overflow-tooltip="true" header-align="center" align="center" width="80" />
        <el-table-column prop="from_ip" label="Ip" show-overflow-tooltip="true" header-align="center" align="center" width="150" />
        <el-table-column prop="datetime" label="Datatime" show-overflow-tooltip="true" header-align="center" align="center" width="150" />
        <el-table-column fixed="right" width="150" label="Opthons" header-align="center" align="center">
          <template slot-scope="scope">
            <el-button v-show="!scope.row.read" size="mini" type="success" style="width:80px" @click="updateNoticoStatu(scope.row)">Read OK</el-button>
          </template>
        </el-table-column>
      </el-table>
    </template>
  </div>
</template>

<script>
import { getNoticeData, putNoticeData } from '@/api/scrapyd'

export default {
  data() {
    return {
      tableHeight: `${document.documentElement.clientHeight}`,
      currentPage: 0,
      TableLoading: false,
      noticeData: []
    }
  },
  created() {
    this.loaddata()
  },
  methods: {
    loaddata() {
      getNoticeData({ page: this.currentPage }).then(response => {
        this.noticeData = this.noticeData.concat(response.data)
      })
      this.currentPage += 1
    },
    updateNoticoStatu(row) {
      putNoticeData({ id: row._id }).then(response => {
        row.read = true
      })
    }
  }
}
</script>

<style>
.el-table.header-cell-style {
  background: #eef1f6;
  color: #606266
}

.el-dialog {
    position: absolute;
    top: 50%;
    left: 50%;
    width: 50%;
    margin: 0 !important;
    transform: translate(-50%, -50%);
    max-height: calc(100% - 30px);
    max-width: calc(100% - 30px);
    display: flex;
    flex-direction: column;
}

.el-dialog__body {
    overflow: auto;
}
</style>
