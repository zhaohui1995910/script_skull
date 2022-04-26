<template>
  <div class="app-container">
    <el-table
      :loading="tableLoading"
      :data="projectList"
      :header-cell-style="{background:'#eef1f6',color:'#606266'}"
    >
      <el-table-column type="index" width="50" label=" " />
      <el-table-column label="ProjectName" prop="name" />
      <el-table-column label="Desc" prop="desc" show-overflow-tooltip />
      <el-table-column label="LastVersion" prop="last_version" />
      <el-table-column label="CreateTime" header-align="center" prop="create_time" />
      <el-table-column align="center" header-align="center" label="Opthons" width="300px">
        <template slot-scope="scope">
          <el-button size="mini" type="success" @click="handleVersion(scope.$index, scope.row)">Version</el-button>
        </template>
      </el-table-column>
    </el-table>

    <el-dialog title="Porject Version" :visible.sync="projectVersionDialog" width="60%">
      <el-table
        :data="projectVersionList"
        :default-sort="{prop: 'code', order: 'descending'}"
      >
        <el-table-column type="index" width="50" label=" " />
        <el-table-column label="ProjectName" prop="name" />
        <el-table-column label="Version" prop="code" sortable show-overflow-tooltip />
        <el-table-column label="CreateTime" header-align="center" prop="create_datetime" />
        <el-table-column align="center" header-align="center" label="Opthons" width="300px">
          <template slot-scope="scope">
            <el-button size="mini" type="primary" @click="handleSpider(scope.$index, scope.row)">Spider</el-button>
          </template>
        </el-table-column>
      </el-table>
    </el-dialog>

    <el-dialog title="Spider" :visible.sync="spiderDialog" width="60%">
      <el-table
        :loading="projectSpiderDialog"
        :data="currentSpiderList"
        :header-cell-style="{background:'#eef1f6',color:'#606266'}"
      >
        <el-table-column width="50" type="expand" align="center">
          <template>
            <div>
              <h6>USER_AGENT: </h6>
              <el-input v-model="spiderForm.settings.USER_AGENT" placeholder="选填USER_AGENT参数" :rows="1" style="width:300px;margin-left:10px" size="mini" />
            </div>
            <div>
              <h6>COOKIES_ENABLED: </h6>
              <el-input v-model="spiderForm.settings.COOKIES_ENABLED" placeholder="选填COOKIES_ENABLED参数(bool)" :rows="1" style="width:300px;margin-left:10px" size="mini" />
            </div>
            <div>
              <h6>CONCURRENT_REQUESTS: </h6>
              <el-input v-model="spiderForm.settings.CONCURRENT_REQUESTS" placeholder="选填CONCURRENT_REQUESTS参数(int)" :rows="1" style="width:300px;margin-left:10px" size="mini" />
            </div>
            <div>
              <h6>DOWNLOAD_DELAY: </h6>
              <el-input v-model="spiderForm.settings.DOWNLOAD_DELAY" placeholder="选填DOWNLOAD_DELAY参数(int)" :rows="1" style="width:300px;margin-left:10px" size="mini" />
            </div>
            <div>
              <h6>additional: </h6>
              <el-input v-model="spiderForm.settings.additional" placeholder="选填jobid参数" type="textarea" :rows="2" style="width:300px;margin-left:10px" size="mini" />
            </div>
          </template>
        </el-table-column>
        <el-table-column type="index" width="50" label=" " />
        <el-table-column label="Name" prop="name" />
        <el-table-column label="CreateDatetime" prop="create_datetime" show-overflow-tooltip />
        <el-table-column align="center" header-align="center" label="Opthons" width="300px">
          <template slot-scope="scope">
            <el-button size="mini" type="success" @click="handleRun(scope.$index, scope.row)">Run</el-button>
          </template>
        </el-table-column>
      </el-table>
    </el-dialog>
  </div>
</template>

<script>
import { projectList, spiderList, runSpider } from '@/api/scrapyd'

export default {
  data() {
    return {
      projectList: [],
      projectVersionList: [],
      tableLoading: false,
      projectVersionDialog: false,
      currentProjectList: [],
      spiderDialog: false,
      spiderForm: {
        id: '',
        version: '',
        settings: {
          CUSTOM_USER_AGENT: '',
          USER_AGENT: '',
          ROBOTSTXT_OBEY: '',
          COOKIES_ENABLED: '',
          CONCURRENT_REQUESTS: '',
          DOWNLOAD_DELAY: '',
          additional: ''
        }
      },
      currentSpiderList: [],
      projectSpiderDialog: false
    }
  },
  created() {
    this.getProjectList()
  },
  methods: {
    handleVersion(index, row) {
      this.projectVersionDialog = true
      this.projectVersionList = []
      row.versions.forEach((v, index) => {
        var item = {
          id: row.id,
          name: row.name,
          code: v.code,
          server_id: row.server_id,
          create_datetime: v.create_datetime
        }
        this.projectVersionList.push(item)
      })
    },
    handleSpider(index, row) {
      this.spiderDialog = true
      this.projectSpiderDialog = true
      spiderList({ page: 1, project: row.id, version: row.code }).then(response => {
        this.currentSpiderList = response.data.spiders
      })
      setTimeout(() => { this.tableLoading = false }, 600)
    },
    handleRun(index, row) {
      this.spiderForm.id = row.id
      this.spiderForm.version = row.version
      runSpider(this.spiderForm).then(response => {
        if (response.code === 200) {
          this.$message.success('爬虫启动成功')
          this.projectSpiderDialog = false
        }
      })
    },
    getProjectList() {
      this.tableLoading = true
      projectList({ page: 1 }).then(response => {
        this.projectList = response.data.projects
      })
      setTimeout(() => { this.tableLoading = false }, 600)
    }
  }
}
</script>

<style>
</style>
