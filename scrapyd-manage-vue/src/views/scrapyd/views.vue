<template>
  <div class="app-container">
    <el-button type="primary" @click="createView">Create View</el-button>

    <!-- 视图表格 -->
    <el-table v-loading="viewsTableLoading" :data="viewsList.slice((currentPage-1)*pageSize, currentPage*pageSize)" :header-cell-style="{background:'#eef1f6',color:'#383838'}" :row-style="{height:'10px'}" :cell-style="{padding:'6px'}" style="width: 100%;margin-top:10px">
      <el-table-column type="index" label="Id" width="60" header-align="center" align="center" />
      <el-table-column label="Name" prop="name" width="150" show-overflow-tooltip header-align="center" align="center" />
      <el-table-column label="Desc" prop="desc" show-overflow-tooltip header-align="center" align="center" />
      <el-table-column label="Fields" prop="fields" show-overflow-tooltip header-align="center" align="center" />
      <el-table-column label="Project" prop="project" width="100" show-overflow-tooltip header-align="center" align="center" />
      <el-table-column label="Spider" prop="spider" width="150" show-overflow-tooltip header-align="center" align="center" />
      <el-table-column label="Version" prop="version" width="100" show-overflow-tooltip header-align="center" align="center" />
      <el-table-column label="CreateTime" width="150" prop="create_time" header-align="center" align="center" />
      <el-table-column fixed="right" width="260" label="Opthons" header-align="center" align="center">
        <template slot-scope="scope">
          <el-button size="mini" type="success" @click="goViewsLook(scope.$index, scope.row)">Look</el-button>
          <el-button size="mini" type="primary" @click="handleEdit(scope.$index, scope.row)">Edit</el-button>
          <el-button size="mini" type="danger" @click="handleDelete(scope.$index, scope.row)">Delete</el-button>
        </template>
      </el-table-column>
    </el-table>

    <!-- 编辑/创建视图 -->
    <el-dialog title="Edit-View" :visible.sync="edit_dialog">
      <div>
        <!-- 输入视图名字 -->
        <div>
          <el-input v-model="currentViewName" placeholder="请输入名字" style="margin-bottom: 15px;width: 200px" />
        </div>
        <!-- 输入视图简介 -->
        <div>
          <el-input v-model="currentViewDesc" type="textarea" :rows="2" placeholder="请输入简介" style="margin-bottom: 15px;width: 300px" />
        </div>
        <!-- 输入视图简介 -->
      </div>
      <div>
        <!-- 选择数据库 -->
        <el-select v-model="db" filterable placeholder="请选择数据库" style="margin-bottom: 15px; margin-right: 15px; width:200px" @change="filderColl">
          <el-option v-for="item in dbList" :key="item" :label="item" :value="item" />
        </el-select>
        <!-- 选择表 -->
        <el-select v-model="coll" filterable placeholder="请选择表" style="margin-bottom: 15px; margin-right: 15px; width:280px" @change="filderZd">
          <el-option v-for="item in collList" :key="item" :label="item" :value="item" />
        </el-select>
      </div>
      <div>
        <!-- 选择项目 -->
        <el-select v-model="currentProject" filterable placeholder="请选择项目" style="margin-bottom: 30px; margin-right: 15px; width:200px" @visible-change="filderVersion">
          <el-option v-for="item in projectList" :key="item" :label="item" :value="item" />
        </el-select>
        <!-- 选择版本 -->
        <el-select v-model="currentVersion" filterable placeholder="请选择版本" style="margin-bottom: 30px; margin-right: 15px; width:200px" @visible-change="filderSpider">
          <el-option v-for="item in versionList" :key="item" :label="item" :value="item" />
        </el-select>
        <!-- 选择爬虫 -->
        <el-select v-model="currentSpider" filterable placeholder="请选择爬虫" style="margin-bottom: 30px; margin-right: 15px; width:200px">
          <el-option v-for="item in spiderList" :key="item" :label="item" :value="item" />
        </el-select>
      </div>

      <!-- 选择字段 -->
      <el-transfer v-model="fieldsValue" :data="fieldsList" target-order="push" />

      <el-button type="primary" style="margin-top: 30px" @click="addView">Add</el-button>
      <el-button type="success" style="margin-top: 30px" @click="updateView">Update</el-button>
    </el-dialog>

    <!-- 分页器 -->
    <el-pagination
      v-show="viewsList.length>pageSize"
      background
      :total="viewsList.length"
      :page-sizes="[10, 15, 25, 100]"
      :page-size.sync="pageSize"
      :page-count="1"
      :current-page.sync="currentPage"
      :pager-count="5"
      layout="total, sizes, prev, pager, next"
      style="margin-top:30px;margin-left:30px"
    />

  </div>
</template>

<script>
import { getMongoTree, getMongoCollFields, getSpiderTree, addViews, getViews, deleteViews, putViews } from '@/api/scrapyd'

export default {
  data() {
    return {
      viewsList: [],
      viewsTableLoading: false,
      projectEditForm: false,
      currentPage: 0,
      pageSize: 22,
      edit_dialog: false,
      table: '',
      tableList: ['amazon_list', 'amazon'],
      fieldsValue: [],
      fieldsList: [],
      mongoTree: {},
      spiderTree: {},
      dbList: [],
      db: '',
      collList: [],
      coll: '',
      projectList: [],
      versionList: [],
      spiderList: [],
      currentProject: '',
      currentVersion: '',
      currentSpider: '',
      currentViewName: '',
      currentViewDesc: '',
      currentViewId: ''
    }
  },
  created() {
    getViews().then(response => {
      this.viewsList = response.data
    })
    getMongoTree().then(response => {
      this.mongoTree = response.data
      this.dbList = this.mongoTree.dbList
    })
    getSpiderTree().then(response => {
      this.spiderTree = response.data
      this.projectList = response.data.projectList
    })
  },
  methods: {
    handleEdit(index, row) {
      this.edit_dialog = true
      this.currentViewName = row.name
      this.currentViewDesc = row.desc
      this.db = row.db
      this.coll = row.table
      this.filderZd(this.coll)
      this.fieldsValue = row.fields.split(', ')
      this.currentProject = row.project
      this.currentVersion = row.version
      this.currentSpider = row.spider
      this.currentViewId = row.id
    },
    updateView() {
      var data1 = {
        viewId: this.currentViewId,
        name: this.currentViewName,
        desc: this.currentViewDesc,
        db: this.db,
        table: this.coll,
        fields: this.fieldsValue,
        project: this.currentProject,
        spider: this.currentSpider,
        version: this.currentVersion
      }
      putViews(data1).then(response => {
        if (response.code === 20000) {
          // 刷新视图列表
          getViews().then(response => {
            this.viewsList = response.data
          })
          this.$message({
            message: '更新成功',
            type: 'success'
          })
        } else {
          this.$message.error('更新失败')
        }
        this.edit_dialog = false
      })
    },
    handleDelete(index, row) {
      this.$confirm('此操作将永久删除该视图, 是否继续?', '提示', {
        confirmButtonText: '确定',
        cancelButtonText: '取消',
        type: 'warning'
      }).then(() => {
        this.viewsList.splice(index, 1)
        var data = {
          viewId: row.id
        }
        deleteViews(data).then(response => {})
        this.$message({
          type: 'success',
          message: '删除成功!'
        })
      }).catch(() => {
        this.$message({
          type: 'info',
          message: '已取消删除'
        })
      })
    },
    goViewsLook(index, row) {
      var routeUrl = this.$router.resolve({
        path: '/look',
        query: { viewid: row.id }
      })
      window.open(routeUrl.href)
    },
    createView() {
      this.fieldsValue = []
      this.db = ''
      this.currentViewName = ''
      this.currentViewDesc = ''
      this.currentProject = ''
      this.currentSpider = ''
      this.currentVersion = ''
      this.edit_dialog = true
    },
    filderColl(db) {
      console.log(this.mongoTree.db_coll_List)
      this.collList = this.mongoTree.db_coll_List[db]
    },
    filderZd(coll) {
      var param = {
        db: this.db,
        collection: coll
      }
      getMongoCollFields(param).then(response => {
        this.fieldsList = response.data
      })
    },
    filderVersion(project) {
      this.versionList = this.spiderTree.pvgx[project]
    },
    filderSpider(version) {
      this.spiderList = this.spiderTree.vsgx[version]
    },
    addView() {
      var data = {
        name: this.currentViewName,
        desc: this.currentViewDesc,
        db: this.db,
        table: this.coll,
        fields: this.fieldsValue,
        project: this.currentProject,
        version: this.currentVersion,
        spider: this.currentSpider
      }
      // 创建视图
      addViews(data).then(response => {
        console.log(response.data)
        if (response.code === 20000) {
          getViews().then(response => {
            this.viewsList = response.data
          })
          this.edit_dialog = false
        }
      })
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
