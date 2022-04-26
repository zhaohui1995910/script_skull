<template>
  <div id="main" style="width:100%;height:100%">
    <div id="left" style="width:10%;float:left;background:#eef1f6;height:100%">
      <el-button type="primary" icon="el-icon-search" style="margin-left:20px; margin-top:20px; width: 80%" @click="searchData()">过滤/刷新</el-button>
      <el-input v-for="item in fields" :key="item" v-model="filders[item]" :placeholder="item" style="margin-left:20px; margin-top:20px; width: 80%" />
    </div>
    <!-- 视图表格 -->
    <div id="right" style="width:90%;float:left">
      <el-table v-loading="viewsTableLoading" v-el-table-infinite-scroll="loaddata" :data="viewsList" stripe="true" :height="tableHeight" :header-cell-style="{background:'#eef1f6',color:'#606266'}" :row-style="{height:'10px'}" :cell-style="{padding:'7px'}">
        <el-table-column type="index" label="Id" width="60" header-align="center" align="center" />
        <el-table-column v-for="key in fields" :key="key" :label="key" :prop="key" show-overflow-tooltip header-align="center" align="center" />
      </el-table>
    </div>
  </div>
</template>

<script>
import { getSpiderData } from '@/api/scrapyd'
import elTableInfiniteScroll from 'el-table-infinite-scroll'

export default {
  directives: {
    'el-table-infinite-scroll': elTableInfiniteScroll
  },
  data() {
    return {
      viewsId: this.$route.query.viewid,
      viewsTableLoading: false,
      currentPage: 0,
      pageSize: 30,
      viewsList: [],
      fields: [],
      tableHeight: `${document.documentElement.clientHeight}`,
      filders: {}
    }
  },
  created() {
    console.log(this.viewsId)

    var params = {
      page: 0,
      viewid: this.$route.query.viewid
    }
    getSpiderData(params).then(response => {
      this.viewsList = response.data.data
      this.fields = response.data.fields
    })
  },
  methods: {
    loaddata() {
      // this.$message.success('加载下一页')
      this.currentPage += 1
      var param = {
        page: this.currentPage,
        viewid: this.viewsId
      }
      var params = Object.assign(param, this.filders)
      // param.update(this.filders)
      getSpiderData(params).then(response => {
        this.viewsList = this.viewsList.concat(response.data.data)
      })
    },
    searchData() {
      this.currentPage = 0
      var param = {
        page: this.currentPage,
        viewid: this.viewsId
      }
      var params = Object.assign(param, this.filders)
      // params.update(this.filders)
      getSpiderData(params).then(response => {
        this.viewsList = response.data.data
        this.fields = response.data.fields
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
