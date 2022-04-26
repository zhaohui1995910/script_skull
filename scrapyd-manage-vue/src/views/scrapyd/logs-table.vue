<template>
  <div class="app-container">
    <div style="width: 20%; float: left">
      <el-table :data="serverTable" highlight-current-row style="width: 90%" @row-click="handleServerClick">
        <el-table-column label="Servers" show-overflow-tooltip header-align="left" align="left" min-width="100">
          <template slot-scope="scope">
            <label :title="scope.row">
              <a>{{ scope.row.host }}</a>
            </label>
          </template>
        </el-table-column>
      </el-table>
    </div>
    <div style="width: 20%; float: left">
      <el-table :data="projectTable" highlight-current-row style="width: 90%" @row-click="handleProjectClick">
        <el-table-column label="Projects" show-overflow-tooltip header-align="left" align="left" min-width="100">
          <template slot-scope="scope">
            <label :title="scope.row">
              <a>{{ scope.row }}</a>
            </label>
          </template>
        </el-table-column>
      </el-table>
    </div>
    <div style="width: 30%; float: left">
      <template>
        <el-table highlight-current-row :data="spiderTable" style="width: 90%" @row-click="handleSpiderClick">
          <el-table-column label="Spiders" show-overflow-tooltip header-align="left" align="left" min-width="100">
            <template slot-scope="scope">
              <label :title="scope.row">
                <a>{{ scope.row }}</a>
              </label>
            </template>
          </el-table-column>
        </el-table>
      </template>
    </div>
    <div style="width: 30%; float: left">
      <template>
        <el-table :data="logTable" stripe="true" @row-click="handerLogClick">
          <el-table-column prop="logName" label="Logs" show-overflow-tooltip header-align="left" align="left" min-width="100" />
        </el-table>
      </template>
    </div>

    <el-dialog title="Log" :visible.sync="LogForm">
      <div><pre>{{ logInfoData }}</pre></div>
    </el-dialog>
  </div>
</template>

<script>
import { projectList, spiderList, serverList, LogList, LogInfo } from '@/api/scrapyd'

export default {
  data() {
    return {
      serverTable: [],
      projectTableList: [],
      projectTable: [],
      spiderTableList: [],
      spiderTable: [],
      logTable: [],
      currentServer: '',
      currentProject: '',
      currentSpider: '',
      currentLog: '',
      filterPorject: [],
      filterSpider: [],
      logInfoData: '',
      LogForm: false,
      spiderForm: {
        host: this.currentServer,
        port: '6800',
        project: this.currentProject,
        spider: this.currentSpider,
        logName: this.currentLog
      }
    }
  },
  created() {
    this.getServerList()
    this.getProjectList()
    this.getSpiderList()
  },
  methods: {
    getServerList() {
      serverList().then(response => {
        this.serverTable = response.data
      })
    },
    getProjectList() {
      projectList().then(response => {
        this.projectTableList = response.data
      })
    },
    getSpiderList() {
      spiderList().then(response => {
        this.spiderTableList = response.data
      })
    },
    getLogList() {
      LogList(this.spiderForm).then(response => {
        this.logTable = response.data
      })
    },
    getLogData() {
      LogInfo(this.spiderForm).then(response => {
        this.logInfoData = response.data
      })
    },
    handleServerClick(row, column, event) {
      this.spiderForm.host = row.host
      this.spiderForm.port = row.port
      this.filterPorject = this.projectTableList.filter(data => row.host === data.server)
      this.projectTable = new Set(this.filterPorject.map(item => { return item.name }))
    },
    handleProjectClick(row, column, event) {
      this.spiderForm.project = row
      this.filterSpider = this.spiderTableList.filter(data => row === data.project)
      this.spiderTable = new Set(this.filterSpider.map(item => { return item.name }))
    },
    handleSpiderClick(spider, column, event) {
      this.spiderForm.spider = spider
      this.getLogList()
    },
    handerLogClick(row, column, event) {
      this.spiderForm.logName = row.logName
      this.getLogData()
      this.LogForm = true
    }
  }
}
</script>

<style>

  .demo-table-expand {font-size: 0;}
  .demo-table-expand label {
    color: #99a9bf;
    width: 150px;
  }
  .demo-table-expand .el-form-item {
    margin-bottom: 0;
    margin-right: 0;
    width: 33%;
  }
  .demo-table-expand .el-form-item label{text-align: right;}
  .demo-table-expand .el-form-item .el-form-item__content{
    margin-left: 30px;
    text-align: left;
    width: 200px;
  }

  #help {margin-top: 8px;}
  #help li {margin-bottom: 8px;}
  #message {
    display: none;
    margin-left: 10px;
    margin-top: 8px;
    padding-top: 8px;
    width: 700px;
  }
  #cmd {
    background-color: #e3e3e3;
    cursor: not-allowed;
    opacity: 1;
  }
  #help li span{
    background: #fff;
    border: solid 1px #e1e4e5;
    color: #E74C3C;
    font-size: 90%;
    max-width: 100%;
    padding: 2px 5px;
    white-space: nowrap;
  }
  .el-select {width: 300px}
  .el-switch__core {
    background: #e3e3e3;
    border: 1px solid #e3e3e3;
  }

  #settings_arguments .el-form-item__label {color: #409EFF;}
  #time_task .el-form-item__label {color: #feb324;}
  #time_task .main_settings .el-form-item__label {color: #67c23a;}

  #multinodes .link {margin-left: 200px;}
  #multinodes .key {width: 188px;}

.el-dialog {
    position: absolute;
    top: 50%;
    left: 50%;
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
