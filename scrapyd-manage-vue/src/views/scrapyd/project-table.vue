<template>
  <div class="app-container">
    <el-table
      v-loading="tableLoading"
      :data="projectList"
      :header-cell-style="{background:'#eef1f6',color:'#606266'}"
    >
      <el-table-column width="80" type="expand" align="center">
        <template slot-scope="scope">
          <el-input
            v-model="scope.row.desc"
            type="textarea"
            :rows="2"
            style="width: 300px"
            @change="handleEditProject(scope.$index, scope.row)"
          />
        </template>
      </el-table-column>
      <el-table-column label="ProjectName" prop="name" />
      <el-table-column label="Desc" prop="desc" show-overflow-tooltip />
      <el-table-column label="LastVersion" prop="last_version" />
      <el-table-column label="CreateTime" header-align="center" prop="create_time" />
      <el-table-column align="center" header-align="center" width="300px">
        <template slot="header">
          <el-button size="mini" type="primary" @click="handleAddProject">Add</el-button>
        </template>
        <template slot-scope="scope">
          <el-button size="mini" type="success" @click="handleVersion(scope.$index, scope.row)">Version</el-button>
          <el-button size="mini" type="danger" @click="handleDelete(scope.$index, scope.row)">Delete</el-button>
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

    <el-dialog class="add_projcet" title="Add Project" :visible.sync="addProjectDialog" width="40%">
      <el-form ref="form" :model="addProjectForm" label-width="150px" label-position="left">
        <el-form-item label="ProjectServer：">
          <el-select v-model="addProjectForm.server_id" placeholder="请选择服务器">
            <el-option
              v-for="server in serverList"
              :key="server.id"
              :label="server.host"
              :value="server.id"
              style="width: 300px"
            />
          </el-select>
        </el-form-item>
        <el-form-item label="ProjectName：">
          <el-input v-model="addProjectForm.name" />
        </el-form-item>
        <el-form-item label="ProjectDesc：">
          <el-input v-model="addProjectForm.desc" />
        </el-form-item>
        <el-form-item label="Project Egg：">
          <el-upload
            class="upload-egg"
            ref="upload"
            :auto-upload="false"
            :data="addProjectForm"
            :headers="token"
            :action="updateEggUrl"
            :limit="1"
            :file-list="files"
            :on-success="UpdateCallback"
          >
            <el-button slot="trigger" size="small" type="primary">Select File</el-button>
            <el-button style="margin-left: 10px;" size="small" type="success" @click="submitUpload">Update</el-button>
          </el-upload>
        </el-form-item>
      </el-form>
    </el-dialog>
  </div>
</template>

<script>
import { projectList, updateProject, deleteProject, spiderList, runSpider, serverList } from '@/api/scrapyd'
import { getToken } from '@/utils/auth'

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
      projectSpiderDialog: false,
      addProjectDialog: false,
      addProjectForm: {},
      files: [],
      updateEggUrl: process.env.VUE_APP_BASE_API + '/scrapy/project',
      token: {
        'authorization': 'Bearer ' + getToken()
      },
      serverList: []
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
    handleAddProject() {
      this.addProjectDialog = true
      serverList().then(response => {
        this.serverList = response.data
      })
    },
    handleDelete(index, row) {
      this.$confirm('此操作将永久删除该项目, 是否继续?', '提示', {
        confirmButtonText: '确定',
        cancelButtonText: '取消',
        type: 'warning'
      }).then(() => {
        deleteProject({ project_id: row.id }).then(response => {
          if (response.code === 200) {
            this.$message.success('删除成功')
            this.getProjectList()
          }
        })
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
    handleEditProject(index, row) {
      updateProject({ project_id: row.id, desc: row.desc })
    },
    getProjectList() {
      this.tableLoading = true
      projectList({ page: 1 }).then(response => {
        this.projectList = response.data.projects
      })
      setTimeout(() => { this.tableLoading = false }, 600)
    },
    submitUpload() {
      this.$refs.upload.submit()
      this.addProjectDialog = false
    },
    UpdateCallback(response, file, fileList) {
      this.addProjectDialog = false
      this.getProjectList()
    }
  }
}
</script>

<style>
.el-input {
  width: 300px;
}
</style>
