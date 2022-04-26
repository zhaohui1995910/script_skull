<template>
  <div class="app-container">
    <div>
      <el-select v-model="SelectForm.project" size="mini" clearable placeholder="Select Projuct" style="width:200px" @change="handleProjectOption">
        <el-option v-for="item in projectOption" :key="item" :label="item" :value="item" />
      </el-select>
      <el-select v-model="SelectForm.spider" size="mini" clearable filterable placeholder="Select Spider" style="width:200px" @change="handleSpiderOption">
        <el-option v-for="item in spiderOption" :key="item" :label="item" :value="item" />
      </el-select>
      <!-- <el-date-picker v-model="SelectForm.startDateTime" type="datetime" placeholder="Select Jobs Start DateTime" default-time="12:00:00" />
      <el-date-picker v-model="SelectForm.finishDateTime" type="datetime" placeholder="Select Jobs Finsh DateTime" default-time="12:00:00" /> -->
      <!-- <el-button type="primary" icon="el-icon-search" size="mini">搜索</el-button> -->
    </div>
    <template>
      <el-table ref="multipleTable" :data="filterSpider.slice((currentPage-1)*pageSize, currentPage*pageSize)" :header-cell-style="{background:'#eef1f6',color:'#606266'}" :row-style="{height:'10px'}" :cell-style="{padding:'5px'}" style="width: 100%;margin-top:10px" stripe="true">
        <el-table-column type="index" label="Id" header-align="center" align="center" width="80" />
        <el-table-column prop="name" label="Spider" show-overflow-tooltip="true" header-align="center" align="center" min-width="60" />
        <el-table-column prop="project" label="Project" header-align="center" align="center" min-width="60" />
        <el-table-column prop="server" label="Host" header-align="center" align="center" min-width="50" />
        <el-table-column prop="desc" label="Description" show-overflow-tooltip="true" header-align="center" align="center" min-width="100" />
        <el-table-column prop="version" label="Version" show-overflow-tooltip="true" header-align="center" align="center" width="100" />
        <el-table-column fixed="right" width="260" label="Opthons" header-align="center" align="center">
          <template slot-scope="scope">
            <el-button size="mini" type="info" @click="handleSpiderHistory(scope.$index, scope.row)">History</el-button>
            <el-button size="mini" type="success" style="width:60px" @click="handleAction(scope.$index, scope.row)">Start</el-button>
          </template>
        </el-table-column>
      </el-table>
    </template>
    <el-pagination
      v-show="filterSpider.length>20"
      background
      :total="filterSpider.length"
      :page-sizes="[10, 15, 18, 100]"
      :page-size.sync="pageSize"
      :current-page.sync="currentPage"
      :pager-count="5"
      layout="total, sizes, prev, pager, next"
      style="margin-top:30px;margin-left:30px"
    />
    <el-dialog class="hustory" title="Spider-History" :lock-scroll="false" :modal="true" :visible.sync="spidersHistoryForm">
      <el-table :data="spiderHistoryList.slice((currentPage-1)*pageSize, currentPage*pageSize)" style="width: 100%;margin-top:10px" stripe="true">
        <el-table-column type="index" label="Id" header-align="center" align="center" width="35" />
        <el-table-column prop="job" label="JName" header-align="center" align="center" />
        <el-table-column prop="status" label="Status" header-align="center" align="center" />
        <el-table-column prop="pages" label="Pages" header-align="center" align="center" />
        <el-table-column prop="items" label="Items" header-align="center" align="center" />
        <el-table-column prop="start_time" label="StartTime" header-align="center" align="center" />
        <el-table-column prop="runtime" label="RunTime" header-align="center" align="center" />
        <el-table-column fixed="right" label="Opthons" header-align="center" align="center">
          <template slot-scope="scope">
            <el-button size="mini" type="info" @click="handlerJobLogs(scope.$index, scope.row)">Log</el-button>
          </template>
        </el-table-column>
      </el-table>
      <el-pagination
        v-show="spiderHistoryList.length>20"
        background
        :total="spiderHistoryList.length"
        :page-sizes="[10, 15, 20, 100]"
        :page-size.sync="pageSize"
        :current-page.sync="historyCurrentPage"
        :pager-count="5"
        layout="total, sizes, prev, pager, next"
        style="margin-top:30px;margin-left:30px"
      />
    </el-dialog>

    <el-dialog class="hustory" title="Log" :visible.sync="LogForm">
      <div><pre>{{ logInfoData }}</pre></div>
    </el-dialog>

    <el-dialog title="Spider-Start" :lock-scroll="false" :modal="true" :visible.sync="runSpidersForm">
      <el-button type="success" style="margin-left:20px" @click="runSpiderAlert">START</el-button>
      <div>
        <h6>Jonid：</h6>
        <el-input v-model="runSpiderSettingsForm.jobid" placeholder="选填jobid参数" :rows="1" style="width:300px;margin-left:10px" size="mini" />
      </div>
      <div>
        <h6>USER_AGENT: </h6>
        <el-input v-model="runSpiderSettingsForm.settings.USER_AGENT" placeholder="选填USER_AGENT参数" :rows="1" style="width:300px;margin-left:10px" size="mini" />
      </div>
      <div>
        <h6>ROBOTSTXT_OBEY: </h6>
        <el-input v-model="runSpiderSettingsForm.settings.ROBOTSTXT_OBEY" placeholder="选填ROBOTSTXT_OBEY参数" :rows="1" style="width:300px;margin-left:10px" size="mini" />
      </div>
      <div>
        <h6>COOKIES_ENABLED: </h6>
        <el-input v-model="runSpiderSettingsForm.settings.COOKIES_ENABLED" placeholder="选填COOKIES_ENABLED参数(bool)" :rows="1" style="width:300px;margin-left:10px" size="mini" />
      </div>
      <div>
        <h6>CONCURRENT_REQUESTS: </h6>
        <el-input v-model="runSpiderSettingsForm.settings.CONCURRENT_REQUESTS" placeholder="选填CONCURRENT_REQUESTS参数(int)" :rows="1" style="width:300px;margin-left:10px" size="mini" />
      </div>
      <div>
        <h6>DOWNLOAD_DELAY: </h6>
        <el-input v-model="runSpiderSettingsForm.settings.DOWNLOAD_DELAY" placeholder="选填DOWNLOAD_DELAY参数(int)" :rows="1" style="width:300px;margin-left:10px" size="mini" />
      </div>
      <div>
        <h6>additional: </h6>
        <el-input v-model="runSpiderSettingsForm.settings.additional" placeholder="选填jobid参数" type="textarea" :rows="2" style="width:300px;margin-left:10px" size="mini" />
      </div>
    </el-dialog>

  </div>
</template>

<script>
import { spiderList, jobList, LogInfo, runSpider } from '@/api/scrapyd'

export default {
  data() {
    return {
      projectInfoList: [],
      projectOption: [],
      filterSpider: [],
      spiderOption: [],
      currentPage: 0,
      historyCurrentPage: 0,
      pageSize: 18,
      spiderListdata: [],
      projectList: [],
      spiderList: [],
      SelectForm: {
        project: '',
        spider: '',
        startDateTime: '',
        finishDateTime: ''
      },
      runSpidersForm: false,
      spidersHistoryForm: false,
      jobsListForm: {
        project: '',
        spider: '',
        version: '',
        start_time: '',
        end_time: ''
      },
      spiderHistoryList: [],
      LogForm: false,
      logInfoData: '',
      jobLogInfoForm: {
        host: '',
        port: '',
        project: '',
        spider: '',
        logName: ''
      },
      runSpiderSettingsForm: {
        spider: '',
        project: '',
        version: '',
        server: '',
        port: '',
        jobid: '',
        settings: {
          USER_AGENT: '',
          ROBOTSTXT_OBEY: '',
          COOKIES_ENABLED: '',
          CONCURRENT_REQUESTS: '',
          DOWNLOAD_DELAY: '',
          additional: ''
        }
      }
    }
  },
  created() {
    spiderList().then(response => {
      this.spiderListdata = response.data
      this.filterSpider = response.data
      this.projectOption = response.projectOption
      this.spiderOption = response.spiderOption
    })
  },
  methods: {
    handleProjectOption() {
      this.filterSpider = this.spiderListdata.filter(data => !this.SelectForm.project || data.project === this.SelectForm.project)
      this.spiderOption = new Set(this.filterSpider.map(item => { return item.name }))
    },
    handleSpiderOption() {
      this.filterSpider = this.spiderListdata.filter(data => !this.SelectForm.spider || this.SelectForm.project === data.project && this.SelectForm.spider === data.name)
    },
    handleSpiderHistory(index, row) {
      this.jobsListForm.project = row.project
      this.jobsListForm.spider = row.name
      this.jobsListForm.version = row.version
      jobList(this.jobsListForm).then(response => {
        if (response.code === 20000) {
          this.spiderHistoryList = response.data
          this.spidersHistoryForm = true
        }
      })
    },
    handlerJobLogs(index, row) {
      this.logInfoData = ''
      this.jobLogInfoForm.host = row.server
      this.jobLogInfoForm.port = row.port
      this.jobLogInfoForm.project = row.project
      this.jobLogInfoForm.spider = row.spider
      this.jobLogInfoForm.logName = row.job + '.json'
      this.LogForm = true
      LogInfo(this.jobLogInfoForm).then(response => {
        if (response.code === 20000) {
          this.logInfoData = response.data
        }
      })
    },
    handleAction(index, row) {
      this.runSpiderSettingsForm.spider = row.name
      this.runSpiderSettingsForm.project = row.project
      this.runSpiderSettingsForm.version = row.version
      this.runSpiderSettingsForm.server = row.server
      this.runSpiderSettingsForm.port = row.port
      this.runSpidersForm = true
    },
    runSpiderAlert() {
      runSpider(this.runSpiderSettingsForm).then(response => {
        if (response.code === 20000) {
          const h = this.$createElement
          this.runSpidersForm = false
          this.$notify({
            title: '爬虫启动成功',
            message: h('i', { style: 'color:teal' }, '请到Jobs模块查看爬虫工作记录')
          })
        }
      })
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

.hustory .el-dialog {
  position: absolute;
  top: 50%;
  left: 50%;
  width: 70%;
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
