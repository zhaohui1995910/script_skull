<template>
  <div class="app-container">
    <div style="margin-bottom:10px">
      <el-select v-model="SelectForm.project" size="mini" clearable placeholder="Select Projuct" style="width:200px" @change="handleSelectSpider">
        <el-option v-for="item in projectList" :key="item" :label="item" :value="item" />
      </el-select>
      <el-select v-model="SelectForm.spider" size="mini" clearable filterable placeholder="Select Spider" style="width:200px">
        <el-option v-for="item in spiderList" :key="item" :label="item" :value="item" />
      </el-select>
      <el-date-picker v-model="SelectForm.start_time" size="mini" type="datetime" placeholder="Select Jobs Start DateTime" value-format="yyyy-MM-dd HH:mm:ss" />
      <el-date-picker v-model="SelectForm.end_time" size="mini" type="datetime" placeholder="Select Jobs Finsh DateTime" value-format="yyyy-MM-dd HH:mm:ss" />
      <el-button type="primary" icon="el-icon-search" size="mini" @click="handleSelectJobs">Search</el-button>
    </div>
    <template>
      <el-table
        ref="multipleTable"
        :data="tableData"
        :header-cell-style="{background:'#eef1f6',color:'#606266'}"
        :row-style="{height:'10px'}"
        :cell-style="{padding:'5px'}"
        style="width: 100%"
        stripe="true"
      >
        <el-table-column width="50" type="expand" align="center">
          <template slot-scope="props">
            <el-form label-position="left" inline class="demo-table-expand">
              <el-form-item label="start_time"><span>{{ props.row.start_time }}</span></el-form-item>
              <el-form-item label="job"><span>{{ props.row.job }}</span></el-form-item>
              <el-form-item label="pages"><span style="color:#00CC00; font-weight:600">{{ props.row.pages }}</span></el-form-item>
              <el-form-item label="finish_time"><span>{{ props.row.finish_time }}</span></el-form-item>
              <el-form-item label="pending_display"><span>{{ props.row.pending_display }}</span></el-form-item>
              <el-form-item label="items"><span style="color:#00CC00; font-weight:600">{{ props.row.items }}</span></el-form-item>
              <el-form-item label="update_time"><span>{{ props.row.update_time }}</span></el-form-item>
              <el-form-item label="runtime"><span>{{ props.row.runtime }}</span></el-form-item>
              <el-form-item label="Jid"><span>{{ props.row.id }}</span></el-form-item>
              <el-form-item label="Status"><span style="color:#00CC00; font-weight:600">{{ props.row.status }}</span></el-form-item>
              <el-form-item label="Version"><span>{{ props.row.version }}</span></el-form-item>
            </el-form>
          </template>
        </el-table-column>

        <el-table-column type="index" label="Id" width="50" />
        <el-table-column prop="job" label="JName" show-overflow-tooltip header-align="center" align="center" min-width="100" />
        <el-table-column prop="project" label="Project" show-overflow-tooltip header-align="center" align="center" min-width="100" />
        <el-table-column prop="spider" label="Spider" show-overflow-tooltip header-align="center" align="center" min-width="100" />
        <el-table-column prop="pages" label="Pages" show-overflow-tooltip header-align="center" align="center" min-width="60">
          <template slot-scope="scope">
            <span style="color:#00CC00; font-weight:600">{{ scope.row.pages }}</span>
          </template>
        </el-table-column>
        <el-table-column prop="items" label="Items" show-overflow-tooltip header-align="center" align="center" min-width="60">
          <template slot-scope="scope">
            <span style="color:#00CC00; font-weight:600">{{ scope.row.items }}</span>
          </template>
        </el-table-column>

        <el-table-column prop="start_time" label="StartTime" :sort-method="sortStart" :sort-orders="sortOrders" header-align="center" align="center" />
        <el-table-column prop="runtime" label="RunTime" show-overflow-tooltip header-align="center" align="center" />
        <el-table-column fixed="right" width="350" label="Opthons" header-align="center" align="right">
          <template slot-scope="scope">
            <el-button v-show="scope.row.status!='finished'" size="mini" type="primary" style="width:60px" @click="handleFreshJob(scope.$index, scope.row)">Fresh</el-button>
            <el-button size="mini" type="info" style="width:60px" @click="handleStatsAction(scope.$index, scope.row)">Stats</el-button>
            <el-button size="mini" type="success" style="width:60px" @click="handleStartAction(scope.$index, scope.row)">Start</el-button>
            <el-button v-show="scope.row.status!='finished'" size="mini" type="danger" style="width:60px" @click="handleSotpAction(scope.$index, scope.row)">Stop</el-button>
            <el-button v-show="scope.row.status=='finished'" size="mini" type="danger" style="width:60px" @click="handleDeleteJob(scope.$index, scope.row)">Del</el-button>
          </template>
        </el-table-column>
      </el-table>
    </template>
    <el-pagination
      background
      :total="dataTotal"
      :page-sizes="[10, 15, 18, 100]"
      :page-count="1"
      :page-size.sync="pageSize"
      :current-page.sync="currentPage"
      :pager-count="11"
      layout="total, sizes, prev, pager, next"
      style="margin-top:30px;margin-left:30px"
      @current-change="getPageJobs"
    />
    <el-dialog title="Spider-Start" :lock-scroll="false" :modal="true" :visible.sync="runSpidersForm" @close="closeDialog">
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
    <el-dialog class="hustory" title="Job-Info" :modal="true" :visible.sync="statsSpidersForm" @close="closeDialog">
      <template>
        <el-tabs v-model="statsTag" stretch="true" @tab-click="handleClick">
          <el-tab-pane label="Analysis" name="analysis">
            <div class="stats vertical-table">
              <table>
                <tr><th>project</th><td>{{ statsData.Analysis.project }}</td></tr>
                <tr><th>spider</th><td>{{ statsData.Analysis.spider }}</td></tr>
                <tr><th>job</th><td>{{ statsData.Analysis.jobName }}</td></tr>
                <tr><th>first_log_time</th><td>{{ statsData.Analysis.first_log_time }}</td></tr>
                <tr><th>latest_log_time</th><td>{{ statsData.Analysis.latest_log_time }}</td></tr>
                <tr><th>runtime</th><td>{{ statsData.Analysis.runtime }}</td></tr>
                <tr>
                  <th>crawled_pages</th>
                  <td>
                    <strong class="green">{{ statsData.Analysis.crawled_pages }}</strong>
                  </td>
                </tr>
                <tr>
                  <th>scraped_items</th>
                  <td>
                    <strong class="green">{{ statsData.Analysis.scraped_items }}</strong>
                  </td>
                </tr>
                <tr><th>shutdown_reason</th><td id="shutdown_reason">{{ statsData.Analysis.shutdown_reason }}</td></tr>
                <tr><th>finish_reason</th><td id="finish_reason">{{ statsData.Analysis.finish_reason }}</td></tr>
                <tr><th>log_critical_count</th><td id="log_critical_count">{{ statsData.Analysis.log_critical_count }}</td></tr>
                <tr><th>log_error_count</th><td id="log_error_count">{{ statsData.Analysis.log_error_count }}</td></tr>
                <tr><th>log_warning_count</th><td id="log_warning_count">{{ statsData.Analysis.log_warning_count }}</td></tr>
                <tr><th>log_redirect_count</th><td id="log_redirect_count">{{ statsData.Analysis.log_redirect_count }}</td></tr>
                <tr><th>log_retry_count</th><td id="log_retry_count">{{ statsData.Analysis.log_retry_count }}</td></tr>
                <tr><th>log_ignore_count</th><td id="log_ignore_count">{{ statsData.Analysis.log_ignore_count }}</td></tr>
                <tr><th>latest_crawl</th><td id="latest_crawl">{{ statsData.Analysis.latest_crawl }}</td></tr>
                <tr><th>latest_scrape</th><td id="latest_scrape">{{ statsData.Analysis.latest_scrape }}</td></tr>
                <tr><th>latest_item</th><td style="word-break: break-all;">{{ statsData.Analysis.project }}</td></tr>
              </table>
            </div>
          </el-tab-pane>
          <el-tab-pane label="Log" name="second">
            <div class="stats vertical-table">
              <table>
                <tr><th>source</th><td>{{ statsData.crawler.source }}</td></tr>
                <tr><th>last_update_time</th><td>{{ statsData.crawler.last_update_time }}</td></tr>
                <tr><th>downloader/response_bytes</th><td>{{ statsData.crawler.downloader_response_bytes }}</td></tr>
                <tr><th>downloader/response_count</th><td>{{ statsData.crawler.downloader_response_count }}</td></tr>
                <tr><th>downloader/response_status_count/200</th><td>{{ statsData.crawler.downloader_response_status_count_200 }}</td></tr>
                <tr><th>elapsed_time_seconds</th><td>{{ statsData.crawler.elapsed_time_seconds }}</td></tr>
                <tr><th>finish_reason</th><td>{{ statsData.crawler.finish_reason }}</td></tr>
                <tr><th>finish_time</th><td>{{ statsData.crawler.finish_time }}</td></tr>
                <tr><th>item_scraped_count</th><td>{{ statsData.crawler.item_scraped_count }}</td></tr>
                <tr><th>log_count/INFO</th><td>{{ statsData.crawler.log_count_INFO }}</td></tr>
                <tr><th>memusage/max</th><td>{{ statsData.crawler.memusage_max }}</td></tr>
                <tr><th>memusage/startup</th><td>{{ statsData.crawler.memusage_startup }}</td></tr>
                <tr><th>request_depth_max</th><td>{{ statsData.crawler.request_depth_max }}</td></tr>
                <tr><th>response_received_count</th><td>{{ statsData.crawler.response_received_count }}</td></tr>
                <tr><th>scheduler/dequeued</th><td>{{ statsData.crawler.scheduler_dequeued }}</td></tr>
                <tr><th>scheduler/dequeued/memory</th><td>{{ statsData.crawler.scheduler_dequeued_memory }}</td></tr>
                <tr><th>start_time</th><td>{{ statsData.crawler.start_time }}</td></tr>
              </table>
            </div>
          </el-tab-pane>
          <el-tab-pane label="Matplotlib" name="third">
            <line-chart :chart-data="lineChartDataSum" :width="chartwidth" />
            <line-chart :chart-data="lineChartDataMin" :width="chartwidth" />
          </el-tab-pane>
        </el-tabs>
      </template>
    </el-dialog>
  </div>
</template>

<script>
import { jobList, deleteJob, getJob, projectSet, spiderList, runSpider, jobStats, stopSpider } from '@/api/scrapyd'
import LineChart from './components/LineChart'

export default {
  components: {
    LineChart
  },
  data() {
    return {
      dataTotal: 0,
      size: 'mini',
      pageSize: 18,
      maxHeight: window.innerHeight - 220,
      currentPage: 1,
      sortOrders: ['descending', 'ascending', null],
      Action: 'Start',
      tableData: [],
      SelectForm: {
        page: 1,
        project: '',
        spider: '',
        start_time: '',
        end_time: ''
      },
      projectList: ['amazon', 'otto'],
      spiderList: [],
      jobForm: {
        jobId: '',
        is_delete: false
      },
      runSpidersForm: false,
      statsSpidersForm: false,
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
      },
      statsTag: 'analysis',
      chartwidth: '998px',
      lineChartDataSum: {
        expectedData: [100, 120, 161, 134, 105, 160, 165],
        actualData: [120, 82, 91, 154, 162, 140, 145],
        xAxisData: []
      },
      lineChartDataMin: {
        expectedData: [100, 120, 161, 134, 105, 160, 165],
        actualData: [120, 82, 91, 154, 162, 140, 145],
        xAxisData: []
      },
      statsForm: {
        jobid: '',
        project: '',
        port: '',
        spider: '',
        host: '',
        jobName: ''
      },
      statsData: {
        Analysis: {},
        crawler: {}
      },
      stopSpiderForm: {
        server: '',
        port: '',
        project: '',
        job: ''
      }
    }
  },
  created() {
    this.getJobList()
    this.getProjectList()
    this.getSpiderList()
  },
  methods: {
    getJobList() {
      jobList({ page: this.currentPage }).then(response => {
        this.tableData = response.data
        this.dataTotal = response.data_count
      })
    },
    handleDeleteJob(index, row) {
      this.jobForm.jobId = row.id
      this.jobForm.is_delete = true
      deleteJob(this.jobForm).then(response => {
        this.getJobList()
      })
    },
    handleFreshJob(index, row) {
      this.jobForm.jobId = row.id
      this.jobForm.is_delete = false
      getJob(this.jobForm).then(response => {
        this.tableData[index].pages = response.data.pages
        this.tableData[index].items = response.data.items
        this.tableData[index].runtime = response.data.runtime
        this.tableData[index].status = response.data.status
        this.tableData[index].start_time = response.data.start_time
        this.tableData[index].finish_time = response.data.finish_time
        this.tableData[index].update_time = response.data.update_time
      })
    },
    handleSelectJobs() {
      this.SelectForm.page = this.currentPage
      jobList(this.SelectForm).then(response => {
        this.tableData = response.data
        this.dataTotal = response.data_count
      })
    },
    handleSelectSpider() {
      this.spiderList = this.spiderList.filter(data => this.SelectForm.project.includes(data.project))
      this.spiderList = new Set(this.spiderList.map(item => { return item.name }))
    },
    getProjectList() {
      projectSet().then(response => {
        this.projectList = response.data
      })
    },
    getSpiderList() {
      spiderList().then(response => {
        this.spiderList = response.data
      })
    },
    handleStartAction(index, row) {
      this.runSpiderSettingsForm.spider = row.spider
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
    },
    handleStatsAction(index, row) {
      this.statsForm.project = row.project
      this.statsForm.spider = row.spider
      this.statsForm.host = row.server
      this.statsForm.port = row.port
      this.statsForm.jobName = row.job
      this.statsSpidersForm = true
      jobStats(this.statsForm).then(response => {
        if (response.code === 20000) {
          this.statsData.crawler = response.data.crawler
          this.statsData.Analysis = response.data.Analysis
          this.lineChartDataSum.expectedData = response.data.datas[1]
          this.lineChartDataSum.actualData = response.data.datas[3]
          this.lineChartDataSum.xAxisData = response.data.datas[0]
          this.lineChartDataMin.expectedData = response.data.datas[2]
          this.lineChartDataMin.actualData = response.data.datas[4]
          this.lineChartDataMin.xAxisData = response.data.datas[0]
        } else {
          this.statsSpidersForm = false
        }
      })
    },
    handleSotpAction(index, row) {
      this.stopSpiderForm.server = row.server
      this.stopSpiderForm.port = row.port
      this.stopSpiderForm.project = row.project
      this.stopSpiderForm.job = row.job
      stopSpider(this.stopSpiderForm).then(response => {
        const h = this.$createElement
        this.runSpidersForm = false
        this.$notify({
          title: 'job stop ok',
          message: h('i', { style: 'color:teal' }, 'Please fresh look')
        })
      })
    },
    handleClick() {},
    closeDialog() {
      this.runSpidersForm = false
      this.statsSpidersForm = false
    },
    getPageJobs() {
      this.SelectForm.page = this.currentPage
      jobList(this.SelectForm).then(response => {
        this.tableData = response.data
        this.dataTotal = response.data_count
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

.stats {
    width: 100%;
    border-collapse: collapse;
}

.stats tr {
    text-align: center;
    height: 30px;
    border-bottom: 1px solid #ebeef5;
    padding: 0 20px;
    position: relative;
}

.stats th {
    font-weight: 500;
    background: #faf8e9;
}

.stats>tbody>tr {
    font-size: 14px;
    font-weight: 400;
}

.popover {
    position: absolute;
    left: 0;
    top: 0;
}

.stats>tbody tr .hover {
    display: inline-block;
    position: absolute;
    left: 0;
    top: 100%;
    background: red;
}

.stats>tbody tr:nth-child(2n) {
    background: #fafafa;
}

/* .stats>tbody tr:nth-child(2n+1) {} */

.stats>tbody tr:last-child {
    border-bottom: 0;
}

.vertical-table th,
.vertical-table td {
    padding-left: 20px;
    padding-right: 20px;
}

.vertical-table th {
    font-weight: 700;
}

.vertical-table td {
    text-align: left;
}

/* https://stackoverflow.com/questions/49095440/width-fit-content-working-on-chrome-but-not-explorer */
/* https://developer.mozilla.org/en-US/docs/Web/CSS/width#Browser_compatibility */
.vertical-table {
    /* width: fit-content; */
    display: table;
}

.hustory .el-dialog {
  position: absolute;
  top: 50%;
  left: 50%;
  width: 60%;
  margin: 0 !important;
  transform: translate(-50%, -50%);
  max-height: calc(100% - 30px);
  max-width: calc(100% - 30px);
  display: flex;
  flex-direction: column;
}
</style>
