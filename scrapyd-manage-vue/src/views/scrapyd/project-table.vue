<template>
  <div class="app-container">
    <el-select v-model="projectSelect" size="mini" clearable placeholder="请选择" @change="handleProjectInfoList">
      <el-option v-for="item in projectOption" :key="item" :label="item" :value="item" />
    </el-select>

    <el-table
      v-loading="projectLoading"
      :data="ProjectList"
      :header-cell-style="{background:'#eef1f6',color:'#606266'}"
      :row-style="{height:'10px'}"
      :cell-style="{padding:'5px'}"
      style="width: 100%;margin-top:10px"
    >
      <el-table-column width="50" type="expand" align="center">
        <template slot-scope="props">
          <span>{{ props.row.desc }}</span>
          <span>{{ props.row.domain }}</span>
          <!-- <el-form label-position="left" inline class="demo-table-expand">
            <el-form-item label="Product introduced: ">
              <div>{{ props.row.introduced }}</div>
            </el-form-item>

            <el-form-item label="Spider List: ">
              <p :v-for="props.row.spiders">{{ props.row.introduced }}</p>
            </el-form-item>

          </el-form> -->

        </template>
      </el-table-column>
      <el-table-column label="ProjectName" prop="name" />
      <el-table-column label="Desc" prop="desc" show-overflow-tooltip />
      <el-table-column label="CreateTime" prop="create_time" />
      <el-table-column align="Opthons" label="Opthons" width="300px">
        <template slot-scope="scope">
          <el-button size="mini" type="primary" @click="handleEdit(scope.$index, scope.row)">Edit</el-button>
          <el-button size="mini" type="success" @click="handleSpider(scope.$index, scope.row)">Versionr</el-button>
          <el-button size="mini" type="success" @click="handleSpider(scope.$index, scope.row)">Spider</el-button>
        </template>
      </el-table-column>
    </el-table>

    <el-dialog title="Spider-Start" :lock-scroll="false" :modal="true" :visible.sync="spidersListForm">
      <div>
        <el-select v-model="spiderSelect" clearable placeholder="请选择" @change="spiderSelectinfo">
          <el-option v-for="item in SpiderList" :key="item.label" :label="item.name" :value="item.name" />
        </el-select>
        <el-button type="success" round style="margin-left:20px" @click="runSpiderAlert">Run Spider</el-button>
        <el-button type="primary" round style="margin-left:20px" @click="updateSpiderAlert">Update Spider</el-button>
      </div>
      <div>
        <h6>Description：</h6>
        <el-input v-model="spiderDescription" type="textarea" :rows="2" boolean="true" size="mini" style="width:500px;margin-left:10px" />
      </div>
      <div>
        <h6>ProJect：</h6>
        <el-input v-model="currentProjectInfo.project" :rows="1" :disabled="true" style="width:300px;margin-left:10px" size="mini" />
      </div>
      <div>
        <h6>Version：</h6>
        <el-input v-model="currentProjectInfo.version" :rows="1" :disabled="true" style="width:300px;margin-left:10px" size="mini" />
      </div>
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

    <el-dialog title="Porject-Edit" :visible.sync="projectEditForm" width="700px">
      <div>
        <h6>ProjectName：</h6>
        <el-input v-model="EditProjectInfo.project" type="textarea" :rows="1" boolean="true" :disabled="true" size="mini" style="width:500px;margin-left:10px" />
      </div>
      <div>
        <h6>Description：</h6>
        <el-input v-model="EditProjectInfo.desc" type="textarea" :rows="2" boolean="true" size="mini" style="width:500px;margin-left:10px" />
      </div>
      <div>
        <h6>Domains：</h6>
        <el-input v-model="EditProjectInfo.domains" type="textarea" :rows="1" boolean="true" size="mini" style="width:500px;margin-left:10px" />
      </div>
      <div>
        <h6>Server：</h6>
        <el-input v-model="EditProjectInfo.server" type="textarea" :rows="1" boolean="true" :disabled="true" size="mini" style="width:500px;margin-left:10px" />
      </div>
      <div>
        <h6>HostName：</h6>
        <el-input v-model="EditProjectInfo.hostname" type="textarea" :rows="1" boolean="true" :disabled="true" size="mini" style="width:500px;margin-left:10px" />
      </div>
      <div>
        <h6>Version：</h6>
        <el-input v-model="EditProjectInfo.version" type="textarea" :rows="1" boolean="true" :disabled="true" size="mini" style="width:500px;margin-left:10px" />
      </div>
      <el-button size="mini" type="success" style="margin-left:30px;margin-top:30px" @click="handleUpdate">Update</el-button>
      <el-button size="mini" type="danger" style="margin-left:60px;margin-top:30px" @click="handleDelete">Delete</el-button>
    </el-dialog>

  </div>
</template>

<script>
import { projectList, projectSpiderList, updateProject, updateSpider, activateProjectSpider, runSpider } from '@/api/scrapyd'

export default {
  data() {
    return {
      ProjectInfoList: [],
      ProjectList: [],
      projectLoading: false,
      projectSelect: '',
      projectOption: '',
      spidersListForm: false,
      currentProjectInfo: {
        project: '',
        host: '',
        port: '',
        version: ''
      },
      currentSpiderForm: {
        project: '',
        host: '',
        version: '',
        spider: '',
        desc: ''
      },
      SpiderList: [],
      spiderSelect: '',
      spiderDescription: '',
      EditProjectInfo: {
        project: '',
        desc: '',
        domains: '',
        server: '',
        port: '',
        hostname: '',
        version: '',
        is_delete: ''
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
      },
      projectEditForm: false,
      currentPage: 1,
      pageSize: 15
    }
  },
  created() {
    this.getProjectList()
  },
  methods: {
    handleSpider(index, row) {
      this.spiderSelect = ''
      this.spiderDescription = ''
      this.spidersListForm = true
      // 更新currentProjectInfo
      this.currentProjectInfo.project = row.name
      this.currentProjectInfo.host = row.server
      this.currentProjectInfo.version = row.version
      this.currentProjectInfo.port = row.port
      // 获取爬虫列表，点击spider按钮，先获取爬虫列表 若为空，则更新爬虫列表再获取。
      projectSpiderList(this.currentProjectInfo).then(response => {
        if (response.data.length === 0) {
          activateProjectSpider(this.currentProjectInfo).then(response => {
            if (response.code === 20000) {
              projectSpiderList(this.currentProjectInfo).then(response => {
                this.SpiderList = response.data
                this.spidersListForm = true
              })
            }
          })
        } else {
          this.SpiderList = response.data
          this.spidersListForm = true
        }
      })
    },
    handleEdit(index, row) {
      this.EditProjectInfo.project = row.name
      this.EditProjectInfo.desc = row.desc
      this.EditProjectInfo.domains = row.domain
      this.EditProjectInfo.server = row.server
      this.EditProjectInfo.port = row.port
      this.EditProjectInfo.hostname = row.hostName
      this.EditProjectInfo.version = row.version
      this.projectEditForm = true
    },
    handleDelete() {
      this.EditProjectInfo.is_delete = 1
      updateProject(this.EditProjectInfo).then(response => {
        if (response.code === 20000) {
          console.log(response.code)
          this.ProjectInfoList.forEach((item, index) => {
            if (item.name === this.EditProjectInfo.project && item.version === this.EditProjectInfo.version) {
              console.log('detail')
              console.log(item.name)
              item.is_delete = true
            }
          })
        }
      })
      this.projectEditForm = false
    },
    handleUpdate() {
      updateProject(this.EditProjectInfo).then(response => {
        if (response.code === 20000) {
          this.ProjectInfoList.forEach((item, index) => {
            if (item.name === this.EditProjectInfo.project && item.version === this.EditProjectInfo.version) {
              item.desc = this.EditProjectInfo.desc
              item.domain = this.EditProjectInfo.domains
            }
          })
        }
      })
      this.projectEditForm = false
    },
    spiderSelectinfo(spiderName) {
      let spiderinfo
      this.SpiderList.forEach(function(item, index) {
        if (item.name === spiderName) {
          spiderinfo = item.desc
        }
      })
      this.spiderDescription = spiderinfo
    },
    runSpiderAlert() {
      this.runSpiderSettingsForm.spider = this.spiderSelect
      this.runSpiderSettingsForm.project = this.currentProjectInfo.project
      this.runSpiderSettingsForm.version = this.currentProjectInfo.version
      this.runSpiderSettingsForm.server = this.currentProjectInfo.host
      this.runSpiderSettingsForm.port = this.currentProjectInfo.port
      runSpider(this.runSpiderSettingsForm).then(response => {
        if (response.code === 20000) {
          const h = this.$createElement
          this.$notify({
            title: '爬虫启动成功',
            message: h('i', { style: 'color:teal' }, '请到Jobs模块查看爬虫工作记录')
          })
        }
      })
    },
    updateSpiderAlert() {
      this.currentSpiderForm.project = this.currentProjectInfo.project
      this.currentSpiderForm.version = this.currentProjectInfo.version
      this.currentSpiderForm.host = this.currentProjectInfo.host
      this.currentSpiderForm.desc = this.spiderDescription
      this.currentSpiderForm.spider = this.spiderSelect
      updateSpider(this.currentSpiderForm).then(response => {
        if (response.code === 20000) {
          this.$message('爬虫简介更新成功')
          projectSpiderList(this.currentProjectInfo).then(response => {
            this.SpiderList = response.data
          })
        }
      })
    },
    getProjectList() {
      this.projectLoading = true
      projectList({ page: this.currentPage, project: this.projectSelect }).then(response => {
        this.ProjectInfoList = response.data.projects
        this.ProjectList = response.data.projects
        this.projectCount = response.data.total
        // this.projectOption = new Set(response.data.map(item => { return item.name }))
      })
      setTimeout(() => { this.projectLoading = false }, 600)
    },
    handleProjectInfoList() {
      this.getProjectList()
    }
  }
}
</script>

<style>
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
