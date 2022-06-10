<template>
  <div class="app-container">
    <el-table
      v-loading="listLoading"
      :data="tableData"
      :header-cell-style="{background:'#eef1f6',color:'#606266'}"
      :row-style="{height:'10px'}"
      :cell-style="{padding:'5px'}"
      style="width: 100%"
      stripe="true"
    >
      <el-table-column type="index" label=" " width="50" align="center"/>
      <el-table-column prop="host" label="Host" min-width="150"/>
      <el-table-column prop="port" label="Port" min-width="150"/>
      <el-table-column prop="hostname" label="HostName"/>
      <el-table-column prop="status" label="Status" min-width="80"/>
      <el-table-column prop="pending" label="Pending" width="120">
        <template slot-scope="scope">
          <span style="color:#00CC00; font-weight:600">{{ scope.row.pending }}</span>
        </template>
      </el-table-column>
      <el-table-column prop="running" label="Running" width="120">
        <template slot-scope="scope">
          <span style="color:#00CC00; font-weight:600">{{ scope.row.running }}</span>
        </template>
      </el-table-column>
      <el-table-column prop="finished" label="Finished" width="120">
        <template slot-scope="scope">
          <span style="color:#00CC00; font-weight:600">{{ scope.row.finished }}</span>
        </template>
      </el-table-column>
      <el-table-column align="center" fixed="right" header-align="center" width="150">
        <template slot="header">
          <el-button type="primary" size="mini" @click="handleAddServer">Add</el-button>
        </template>
        <template slot-scope="scope">
          <el-button size="mini" type="danger" @click="handleDelete(scope.$index, scope.row)">Delete</el-button>
        </template>
      </el-table-column>
    </el-table>

    <el-dialog title="Add Scrapyd-Server" :visible.sync="addServerDialog" width="30%">
      <el-form label-position="left" label-width="120px" :model="serverForm">
        <el-form-item label="IP">
          <el-input v-model="serverForm.host" style="width:250px"/>
        </el-form-item>
        <el-form-item label="Port">
          <el-input v-model="serverForm.port" style="width:250px"/>
        </el-form-item>
        <el-form-item label="Auth">
          <el-switch v-model="serverForm.auth"/>
        </el-form-item>
        <el-form-item label="Auth-UName">
          <el-input v-model="serverForm.username" style="width:250px"/>
        </el-form-item>
        <el-form-item label="Auth-PWord">
          <el-input v-model="serverForm.password" style="width:250px"/>
        </el-form-item>
      </el-form>
      <el-button type="primary" style="margin-left:10px;margin-top: 20px;" @click="handleAdd">Submit</el-button>
    </el-dialog>

  </div>
</template>

<script>
import { serverList, serverAdd, serverDel } from '@/api/scrapyd'

export default {
  name: 'ScrapydScrverTable',

  data() {
    return {
      tableData: [],
      listLoading: false,
      addServerDialog: false,
      serverForm: {
        host: '',
        port: '',
        auth: '',
        auth_username: '',
        auth_password: ''
      }
    }
  },
  created() {
    this.getList()
  },
  methods: {
    getList() {
      this.listLoading = true
      serverList().then(response => {
        this.tableData = response.data
        setTimeout(() => {
          this.listLoading = false
        }, 600)
      })
    },
    handleAddServer() {
      this.addServerDialog = true
      this.serverForm.host = ''
      this.serverForm.port = ''
      this.serverForm.auth = true
      this.serverForm.auth_username = ''
      this.serverForm.auth_password = ''
    },
    handleAdd() {
      serverAdd(this.serverForm).then(response => {
        if (response.code === 200) {
          this.addServerDialog = false
          this.getList()
        }
      })
    },
    handleDelete(index, row) {
      this.serverForm.host = row.host
      this.serverForm.port = row.port
      this.$confirm('此操作将永久删除数据库中该服务器及所属项目和爬虫记录, 是否继续?', '提示', {
        confirmButtonText: '确定',
        cancelButtonText: '取消',
        type: 'warning'
      }).then(() => {
        serverDel({ id: row.id }).then(response => {
          if (response.code === 200) {
            this.tableData.splice(index, 1)
          }
        })
      })
    }
  }
}
</script>
