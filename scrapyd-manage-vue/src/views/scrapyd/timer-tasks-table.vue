<template>
  <div class="app-container">
    <el-table
      v-loading="tableLoading"
      :data="taskInfoList.filter(data => !projectSelect || data.project === projectSelect)"
      :header-cell-style="{background:'#eef1f6',color:'#606266'}"
      :row-style="{height:'10px'}"
      :cell-style="{padding:'5px'}"
      style="width: 100%"
    >
      <el-table-column width="50" type="expand" align="center">
        <template slot-scope="props">
          <el-form label-position="left" inline class="demo-table-expand">
            <el-form-item label="create_time"><span>{{ props.row.create_time }}</span></el-form-item>
            <el-form-item label="year"><span>{{ props.row.timer.year }}</span></el-form-item>
            <el-form-item label="start_date"><span>{{ props.row.timer.start_time }}</span></el-form-item>

            <el-form-item label="update_time"><span>{{ props.row.update_time }}</span></el-form-item>
            <el-form-item label="month"><span>{{ props.row.timer.month }}</span></el-form-item>
            <el-form-item label="end_date"><span>{{ props.row.timer.end_time }}</span></el-form-item>

            <el-form-item label="version"><span>{{ props.row.version }}</span></el-form-item>
            <el-form-item label="day"><span>{{ props.row.timer.day }}</span></el-form-item>
            <el-form-item label="timezone"><span>{{ props.row.timer.timezone }}</span></el-form-item>

            <el-form-item label="taskID"><span>{{ props.row.id }}</span></el-form-item>
            <el-form-item label="week"><span>{{ props.row.timer.week }}</span></el-form-item>
            <el-form-item label="jitter"><span>{{ props.row.timer.jitter }}</span></el-form-item>

            <el-form-item label="day_of_week"><span>{{ props.row.timer.day_of_week }}</span></el-form-item>
            <el-form-item label="misfire_grace_time"><span>{{ props.row.timer.misfire_grace_time }}</span>
            </el-form-item>

            <el-form-item />
            <el-form-item label="hour"><span>{{ props.row.timer.hour }}</span></el-form-item>
            <el-form-item label="coalesce"><span>{{ props.row.timer.coalesce }}</span></el-form-item>

            <el-form-item />
            <el-form-item label="minute"><span>{{ props.row.timer.minute }}</span></el-form-item>
            <el-form-item label="max_instances"><span>{{ props.row.timer.max_instances }}</span></el-form-item>

            <el-form-item />
            <el-form-item label="second"><span>{{ props.row.timer.second }}</span></el-form-item>
            <el-form-item />

            <el-form-item label="selected_nodes"><span>{{ props.row.server }}</span></el-form-item>

            <el-form-item class="demo-table-expand task-sttings" label="settings_arguments" style="width: 50%">
              <json-viewer v-if="props.row.settings" :value="JSON.parse(props.row.settings)" :expand-depth="1" />
            </el-form-item>
          </el-form>
        </template>
      </el-table-column>
      <el-table-column type="index" align="left" label="TID" width="50" />
      <el-table-column prop="name" label="Name" width="180" />
      <el-table-column prop="desc" label="Desc" show-overflow-tooltip />
      <el-table-column prop="project" label="Project" width="160" />
      <el-table-column prop="spider" label="Spider" align="center" />
      <el-table-column label="Status" align="center" width="100">
        <template slot-scope="scope">
          <label v-show="scope.row.status == true" :title="scope.row.status">
            <a class="state safe" @click="handleStatusClick(scope.row.status, scope.row.id)">{{ scope.row.status }}</a>
          </label>
          <label v-show="scope.row.status == false" :title="scope.row.status">
            <a class="state normal" @click="handleStatusClick(scope.row.status, scope.row.id)">
              {{ scope.row.status }}</a>
          </label>
        </template>
      </el-table-column>
      <el-table-column prop="p_time" label="PRTime" align="center" width="180" />
      <el-table-column prop="n_time" label="NRTime" align="center" width="180" />
      <el-table-column prop="t_count" label="TRCount" width="80" />
      <el-table-column fixed="right" width="300" label="Opthons" header-align="center" align="right">
        <template slot="header">
          <el-button type="primary" style="margin-left:10px" size="mini" @click="AddTask">Add Task</el-button>
        </template>
        <template slot-scope="scope">
          <el-button size="mini" type="info" @click="handleHistory(scope.$index, scope.row)">History</el-button>
          <el-button size="mini" type="primary" @click="handleEdit(scope.$index, scope.row)">Edit</el-button>
          <el-button size="mini" type="danger" @click="handleDelete(scope.$index, scope.row)">Delete</el-button>
        </template>
      </el-table-column>
    </el-table>

    <el-dialog title="Spider-Task" :visible.sync="spiderTaskForm" style="">
      <el-form id="form" ref="form" :model="form" label-width="200px" size="mini">
        <el-form-item label="server">
          <el-select
            id="node"
            v-model="form.server"
            placeholder="Select a node"
            @visible-change="loadServer"
            @change="loadProjects"
          >
            <el-option
              v-for="SCRAPYD_SERVER in SCRAPYD_SERVERS"
              :key="SCRAPYD_SERVER.id"
              :label="SCRAPYD_SERVER.host+':'+SCRAPYD_SERVER.port"
              :value="SCRAPYD_SERVER"
            />
          </el-select>
        </el-form-item>

        <el-form-item label="project" prop="selectedProject">
          <el-select
            id="projects"
            v-model="form.project"
            placeholder="Select a project"
            no-data-text="No projects found"
            @change="loadVersions"
          >
            <el-option v-for="project in projects" :key="project.name" :label="project.name" :value="project" />
          </el-select>
        </el-form-item>

        <el-form-item label="version" prop="selectedVersion">
          <el-select
            id="versions"
            v-model="form.version"
            placeholder="Select a version"
            no-data-text="Select a project first..."
            @change="loadSpiders"
          >
            <el-option v-for="version in versions" :key="version.code" :label="version.code" :value="version" />
          </el-select>
        </el-form-item>

        <el-form-item label="spider" prop="selectedSpider">
          <el-select
            id="spiders"
            v-model="form.spider"
            placeholder="Select a spider"
            no-data-text="Select a version first..."
          >
            <el-option v-for="spider in spiders" :key="spider.name" :label="spider.name" :value="spider" />
          </el-select>
        </el-form-item>

        <el-form-item label="name">
          <el-input v-model="form.name" :rows="1" placeholder="task Name" style="width:300px" size="mini" />
        </el-form-item>

        <el-form-item label="desc">
          <el-input v-model="form.desc" :rows="2" placeholder="task desc" style="width:300px" size="mini" />
        </el-form-item>

        <el-form-item label="settings & arguments">
          <el-switch v-model="form.expandSettingsArguments" />
        </el-form-item>

        <div v-show="form.expandSettingsArguments" id="settings_arguments">

          <el-form-item label="USER_AGENT">
            <el-col :span="9">
              <el-select v-model="form.settings.USER_AGENT" placeholder="the default User-Agent for crawling" clearable>
                <el-option :label="form.settings.CUSTOM_USER_AGENT" value="custom" />
                <el-option label="Mozilla/5.0 Windows NT Chrome..." value="Chrome" />
                <el-option label="Mozilla/5.0 iPhone Safari..." value="iPhone" />
                <el-option label="Mozilla/5.0 iPad Safari..." value="iPad" />
                <el-option label="Mozilla/5.0 Linux; Android..." value="Android" />
              </el-select>
            </el-col>
          </el-form-item>

          <el-form-item label="ROBOTSTXT_OBEY">
            <el-col :span="9">
              <el-select
                v-model="form.settings.ROBOTSTXT_OBEY"
                placeholder="whether to respect robots.txt policies"
                clearable
              >
                <el-option label="True" value="True" />
                <el-option label="False" value="False" />
              </el-select>
            </el-col>
          </el-form-item>

          <el-form-item label="COOKIES_ENABLED">
            <el-col :span="9">
              <el-select
                v-model="form.settings.COOKIES_ENABLED"
                placeholder="whether to enable cookies middleware"
                clearable
              >
                <el-option label="True" value="True" />
                <el-option label="False" value="False" />
              </el-select>
            </el-col>
          </el-form-item>

          <el-form-item label="CONCURRENT_REQUESTS">
            <el-col :span="9">
              <el-input v-model="form.settings.CONCURRENT_REQUESTS" placeholder="defaults to 16 in Scrapy" clearable />
            </el-col>
          </el-form-item>

          <el-form-item label="DOWNLOAD_DELAY">
            <el-col :span="9">
              <el-input v-model="form.settings.DOWNLOAD_DELAY" placeholder="defaults to 0 in Scrapy" clearable />
            </el-col>
          </el-form-item>

          <el-form-item label="additional">
            <el-col :span="9">
              <el-input
                v-model="form.settings.additional"
                placeholder="key=value  换行分隔"
                type="textarea"
                clearable
                style="width:400px"
              />
            </el-col>
          </el-form-item>
        </div>

        <el-form-item label="timer task">
          <el-switch v-model="form.expandTimerTask" active-color="#67c23a" />
        </el-form-item>

        <div v-show="form.expandTimerTask" id="time_task">

          <el-form-item v-show="form.expandTimerTaskMoreSettings" label="year (*)">
            <el-col :span="9">
              <el-input
                v-model="form.timer.year"
                placeholder="4-digit year, e.g. 2019, defaults to * for any year"
                clearable
              />
            </el-col>
          </el-form-item>
          <el-form-item v-show="form.expandTimerTaskMoreSettings" label="month (*)">
            <el-col :span="9">
              <el-input v-model="form.timer.month" placeholder="month (1-12); 1,6-8 equals to 1,6,7,8" clearable />
            </el-col>
          </el-form-item>
          <el-form-item class="main_settings" label="day (*)">
            <el-col :span="9">
              <el-input
                v-model="form.timer.day"
                placeholder="day (1-31); CAN BE 1st mon OR last sun OF THE MONTH"
                clearable
              />
            </el-col>
          </el-form-item>
          <el-form-item v-show="form.expandTimerTaskMoreSettings" label="week (*)">
            <el-col :span="9">
              <el-input v-model="form.timer.week" placeholder="ISO week (1-53)" clearable />
            </el-col>
          </el-form-item>

          <el-form-item class="main_settings" label="day_of_week (*)">
            <el-col :span="9">
              <el-select v-model="form.timer.day_of_week" placeholder="multiple select or leave blank for *">
                <el-option
                  v-for="item in day_of_week_options"
                  :key="item.value"
                  :label="item.label"
                  :value="item.value"
                />
              </el-select>
            </el-col>
          </el-form-item>
          <el-form-item class="main_settings" label="hour (*)">
            <el-col :span="9">
              <el-input
                v-model="form.timer.hour"
                placeholder="hour (0-23); 9,17,8-20/4 equals to 8,9,12,16,17,20"
                clearable
              />
            </el-col>
          </el-form-item>
          <el-form-item class="main_settings" label="minute (0)">
            <el-col :span="9">
              <el-input
                v-model="form.timer.minute"
                placeholder="minute (0-59); defaults to 0, type */10 to fire every 10 minutes"
                clearable
              />
            </el-col>
          </el-form-item>
          <el-form-item v-show="form.expandTimerTaskMoreSettings" label="second (0)">
            <el-col :span="9">
              <el-input v-model="form.timer.second" placeholder="second (0-59); defaults to 0" clearable />
            </el-col>
          </el-form-item>

          <el-form-item v-show="form.expandTimerTaskMoreSettings" label="start_date">
            <el-date-picker
              v-model="form.timer.start_date"
              type="datetime"
              placeholder="optional (inclusive)"
              default-time="12:00:00"
              value-format="yyyy-MM-dd HH:mm:ss"
            />
          </el-form-item>
          <el-form-item v-show="form.expandTimerTaskMoreSettings" label="end_date">
            <el-date-picker
              v-model="form.timer.end_date"
              type="datetime"
              placeholder="optional (inclusive)"
              value-format="yyyy-MM-dd HH:mm:ss"
            />
          </el-form-item>
          <el-form-item v-show="form.expandTimerTaskMoreSettings" label="timezone">
            <el-col :span="9">
              <el-input
                v-model="form.timer.timezone"
                :placeholder="`defaults to ` + form._timezone + `, (via: from tzlocal import get_localzone)`"
                clearable
              />
            </el-col>
          </el-form-item>
          <el-form-item v-show="form.expandTimerTaskMoreSettings" label="jitter (0)">
            <el-col :span="9">
              <el-input
                v-model="form.timer.jitter"
                placeholder="execute task by random delay of [-N, +N] secs, defaults to 0."
                clearable
              />
            </el-col>
          </el-form-item>

          <el-form-item v-show="form.expandTimerTaskMoreSettings" label="misfire_grace_time (600)">
            <el-col :span="9">
              <el-input
                v-model="form.timer.misfire_grace_time"
                placeholder="max tolerance of delay for misfired task, defaults to 600 secs."
                clearable
              />
            </el-col>
          </el-form-item>
          <el-form-item v-show="form.expandTimerTaskMoreSettings" label="coalesce">
            <el-col :span="9">
              <el-select v-model="form.timer.coalesce">
                <el-option label="True: default, recommended" value="True" />
                <el-option label="False: may run more than once in succession" value="False" />
              </el-select>
            </el-col>
          </el-form-item>
          <el-form-item v-show="form.expandTimerTaskMoreSettings" label="max_instances (1)">
            <el-col :span="9">
              <el-input
                v-model="form.timer.max_instances"
                placeholder="max concurrently running instances of this task, defaults to 1."
                clearable
              />
            </el-col>
          </el-form-item>

          <el-form-item class="main_settings" label="show more timer settings">
            <el-switch v-model="form.expandTimerTaskMoreSettings" active-color="#feb324" />
          </el-form-item>
        </div>

      </el-form>

      <el-button v-show="Addbutton" type="success" style="margin-left:200px" @click="handleAddTask">创建</el-button>
      <el-button v-show="Updatebutton" type="success" style="margin-left:200px" @click="handleUpdateTask">更新</el-button>
      <el-button type="danger" style="margin-left:50px" @click="spiderTaskForm=false">取消</el-button>
    </el-dialog>

    <el-dialog class="hustory" title="Tasks-History" :lock-scroll="false" :modal="true" :visible.sync="taskHistoryForm">
      <el-table
        :data="taskHistoryList.slice((historyCurrentPage-1)*pageSize, historyCurrentPage*pageSize)"
        style="width: 100%;margin-top:10px"
        stripe="true"
      >
        <el-table-column type="index" label="Id" header-align="center" align="center" width="35" />
        <el-table-column prop="job" label="JName" show-overflow-tooltip header-align="center" align="center" />
        <el-table-column prop="status" label="Status" header-align="center" align="center" />
        <el-table-column prop="pages" label="Pages" header-align="center" align="center" />
        <el-table-column prop="items" label="Items" header-align="center" align="center" />
        <el-table-column prop="start_time" label="StartTime" header-align="center" min-width="100px" align="center" />
        <el-table-column prop="runtime" label="RunTime" header-align="center" align="center" />
        <el-table-column fixed="right" label="Opthons" header-align="center" align="center">
          <template slot-scope="scope">
            <el-button size="mini" type="info" @click="handlerJobLogs(scope.$index, scope.row)">Log</el-button>
          </template>
        </el-table-column>
      </el-table>
      <el-pagination
        v-show="taskHistoryList.length>20"
        background
        :total="taskHistoryList.length"
        :page-sizes="[10, 15, 18, 100]"
        :page-size.sync="pageSize"
        :current-page.sync="historyCurrentPage"
        :pager-count="5"
        layout="total, sizes, prev, pager, next"
        style="margin-top:30px;margin-left:30px"
      />
    </el-dialog>
    <el-dialog title="Log" :visible.sync="LogForm">
      <div>
        <pre>{{ logInfoData }}</pre>
      </div>
    </el-dialog>
  </div>
</template>

<script>
import 'vue-json-viewer/style.css'
import JsonViewer from 'vue-json-viewer'
import {
  taskList,
  updateTask,
  addTask,
  projectList,
  statusTask,
  deleteTask,
  jobList,
  LogInfo,
  serverList,
  spiderList
} from '@/api/scrapyd'

export default {
  name: 'TimerTasks',
  components: {
    JsonViewer
  },
  data() {
    return {
      tableLoading: false,
      Updatebutton: null,
      Addbutton: null,
      projectOption: [],
      projectSelect: '',
      taskInfoList: [],
      status_css: {
        true: 'state safe',
        false: 'state normal'
      },
      spiderTaskForm: false,
      SCRAPYD_SERVERS: [],
      projects: [],
      versions: [],
      spiders: [],
      taskHistoryList: [],
      pageSize: 18,
      historyCurrentPage: 0,
      day_of_week_options: [
        { value: '0-6', label: '*' },
        { value: 'mon-fri', label: 'Monday-Friday' },
        { value: 'mon', label: 'Monday' },
        { value: 'tue', label: 'Tuesday' },
        { value: 'wed', label: 'Wednesday' },
        { value: 'thu', label: 'Thursday' },
        { value: 'fri', label: 'Friday' },
        { value: 'sat', label: 'Saturday' },
        { value: 'sun', label: 'Sunday' }
      ],
      form: {
        server: '',
        port: '',
        project: '',
        version: '',
        spider: '',
        taskId: '',
        settings: {
          CUSTOM_USER_AGENT: '',
          USER_AGENT: '',
          ROBOTSTXT_OBEY: '',
          COOKIES_ENABLED: '',
          CONCURRENT_REQUESTS: '',
          DOWNLOAD_DELAY: '',
          additional: ''
        },
        timer: {
          year: '*',
          month: '*',
          day: '*',
          week: '*',
          day_of_week: '0-6',
          hour: '*',
          minute: '0',
          second: '0',
          start_date: null,
          end_date: null,

          timezone: 'Asia/Shanghai',
          jitter: 0,
          misfire_grace_time: 600,
          coalesce: 'True',
          max_instances: 1
        },
        trigger: 'cron',
        name: '',
        desc: '',
        expandSettingsArguments: false,
        expandTimerTask: true,
        expandTimerTaskMoreSettings: false
      },
      currnetServerLabel: '',
      taskHistoryForm: false,
      taskHistoryDataList: [{
        id: '1',
        status: 'ok',
        statusCode: '200',
        runTime: '2020-07-07 12:30:30',
        nextTime: '2020-07-08 08:12:38'
      }, {
        id: '2',
        status: 'ok',
        statusCode: '200',
        runTime: '2020-07-07 12:30:30',
        nextTime: '2020-07-08 08:12:38'
      }],
      project_list: [],
      filterProject: '',
      filterVersion: '',
      filterSpider: '',
      loadSpiderListForm: {
        host: '',
        project: '',
        version: ''
      },
      statusForm: {
        taskId: '',
        status: '',
        taskName: ''
      },
      historyForm: {
        taskId: ''
      },
      LogForm: false,
      logInfoData: '',
      jobLogInfoForm: {
        host: '',
        port: '',
        project: '',
        spider: '',
        logName: ''
      }
    }
  },
  created() {
    this.getTaskInfoList()
  },
  methods: {
    handleEdit(index, row) {
      console.log('handleEdit')
      this.Updatebutton = true
      this.Addbutton = false
      this.spiderTaskForm = true
      this.form.server = row.server
      this.form.port = row.port
      this.form.project = row.project
      this.form.version = row.version
      this.form.spider = row.spider
      this.form.name = row.name
      this.form.taskId = row.id
      this.form.settings = row.settings
      this.form.timer = row.timer
      projectList().then(response => {
        this.project_list = response.data
      })
    },
    handleDelete(index, row) {
      this.tableLoading = true
      deleteTask({ task_id: row.id }).then(response => {
        this.getTaskInfoList()
        this.tableLoading = false
      })
    },
    handleHistory(index, row) {
      this.historyForm.taskId = row.id
      jobList(this.historyForm).then(response => {
        if (response.code === 20000) {
          this.taskHistoryList = response.data
          this.taskHistoryForm = true
        }
      })
    },
    handleHistoryTaskStats() {
      console.log('handleHistoryTaskStats')
    },
    handleHistoryDeleteDelete() {
      console.log('handleHistoryDeleteDelete')
    },
    handleUpdateTask() {
      updateTask(this.form).then(response => {
        if (response.code === 20000) {
          this.spiderTaskForm = false
          this.getTaskInfoList()
        }
      })
    },
    handleAddTask() {
      var formData = {
        spider_id: this.form.spider.id,
        name: this.form.name,
        desc: this.form.desc,
        trigger: this.form.trigger,
        timer: this.form.timer,
        settings: this.form.settings
      }
      addTask(formData).then(response => {
        if (response.code === 200) {
          this.spiderTaskForm = false
          this.getTaskInfoList()
        }
      })
    },
    AddTask() {
      this.Addbutton = true
      this.Updatebutton = false
      this.spiderTaskForm = true
      this.form.server = ''
      this.form.project = ''
      this.form.version = ''
      this.form.spider = ''
      this.form.name = ''
      this.form.timer = {
        year: '*',
        month: '*',
        day: '*',
        week: '*',
        day_of_week: '*',
        hour: '*',
        minute: '0',
        second: '0',
        start_date: null,
        end_date: null,

        timezone: 'Asia/Shanghai',
        jitter: 0,
        misfire_grace_time: 600,
        coalesce: 'True',
        max_instances: 1
      }
      this.form.settings = {
        CUSTOM_USER_AGENT: '',
        USER_AGENT: '',
        ROBOTSTXT_OBEY: '',
        COOKIES_ENABLED: '',
        CONCURRENT_REQUESTS: '',
        DOWNLOAD_DELAY: '',
        additional: ''
      }
    },
    getTaskInfoList() {
      this.tableLoading = true
      taskList().then(response => {
        this.taskInfoList = response.data
        this.tableLoading = false
      })
    },
    loadServer() {
      serverList().then(response => {
        this.SCRAPYD_SERVERS = response.data
      })
    },
    loadProjects() {
      projectList({ spider_id: this.form.server.id }).then(response => {
        this.projects = response.data.projects
      })
    },
    loadVersions(value) {
      this.versions = value.versions
    },
    loadSpiders() {
      this.loadSpiderListForm.project = this.form.project.id
      this.loadSpiderListForm.version = this.form.version.code
      spiderList(this.loadSpiderListForm).then(response => {
        this.spiders = response.data.spiders
      })
    },
    handleStatusClick(status, taskId) {
      this.statusForm.taskId = taskId
      this.statusForm.status = status
      statusTask(this.statusForm).then(response => {
        this.getTaskInfoList()
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
    }
  }
}
</script>

<style>
.demo-table-expand {
  font-size: 0;
}

.demo-table-expand label {
  color: #99a9bf;
  width: 150px;
}

.demo-table-expand .el-form-item {
  margin-bottom: 0;
  margin-right: 0;
  width: 33%;
}

.demo-table-expand .el-form-item label {
  text-align: right;
}

.demo-table-expand .el-form-item .el-form-item__content {
  margin-left: 30px;
  text-align: left;
  width: 200px;
}

.demo-table-expand .task-sttings .el-form-item__content {
  margin-left: 30px;
  text-align: left;
  width: 80%;
}

#help {
  margin-top: 8px;
}

#help li {
  margin-bottom: 8px;
}

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

#help li span {
  background: #fff;
  border: solid 1px #e1e4e5;
  color: #E74C3C;
  font-size: 90%;
  max-width: 100%;
  padding: 2px 5px;
  white-space: nowrap;
}

.el-select {
  width: 300px
}

.el-switch__core {
  background: #e3e3e3;
  border: 1px solid #e3e3e3;
}

#settings_arguments .el-form-item__label {
  color: #409EFF;
}

#time_task .el-form-item__label {
  color: #feb324;
}

#time_task .main_settings .el-form-item__label {
  color: #67c23a;
}

#multinodes .link {
  margin-left: 200px;
}

#multinodes .key {
  width: 188px;
}

.state,
.button {
  border-radius: 3px;
  padding: 3px 10px;
  opacity: 1;
  color: #fff;
  transition: all 0.1s ease-out;
}

.state:hover,
.button:hover {
  opacity: 0.7;
  color: #fff;
}

.button {
  font-size: 20px;
  font-weight: 400;
  margin-right: 8px;
  padding: 5px 20px;
}

.button.big {
  padding-top: 12px;
  padding-bottom: 12px;
}

.button.narrow {
  padding-left: 10px;
  padding-right: 10px;
}

.state.normal, .button.normal {
  background: #ff6633;
}

.state.safe, .button.safe {
  background: #67c23a;
}

.state.delete, .button.delete {
  background: #909399;
}

.state.warning, .button.warning {
  background: #feb324;
}

.state.danger, .button.danger {
  background: #fd6b6e;
}

.state.multinode, .button.multinode {
  background: #7E57C2;
}

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
