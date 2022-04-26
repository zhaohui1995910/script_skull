<template>
  <div class="app-container">
    <div class="block" style="margin-bottom: 10px">
      <span class="demonstration" style="font-size: 12px;color: #606266;margin-left: 10px">请输入关键词：</span>
      <el-input v-model="keyword" size="mini" placeholder="请输入内容" style="width: 150px" />
      <el-button type="primary" size="mini" style="margin-left: 20px" @click="getDataList">查询</el-button>
      <el-button type="danger" size="mini" @click="deleteData">删除</el-button>
      <el-button type="success" size="mini" @click="downloadLogs">下载</el-button>
    </div>
    <div id="one">
      <el-table
        class="tableBox"
        ref="multipleTable"
        v-loading="dataLoading"
        :data="dataList"
        :header-cell-style="{background:'#eef1f6',color:'#606266'}"
        @selection-change="handleSelectionChange"
        @sort-change="sortChange"
      >
        <el-table-column type="selection" width="50"/>
        <el-table-column label="ASIN" width="120">
          <template slot-scope="scope">
            <a :href="scope.row.link" target="_blank">{{ scope.row.asin }}</a>
          </template>
        </el-table-column>
        <el-table-column label="产品标题" prop="title" header-align="center" align="center" width="260px" show-overflow-tooltip/>
        <el-table-column label="产品图片" align="center">
          <template slot-scope="scope">
            <el-popover placement="top-start" title="" trigger="hover">
              <img :src="scope.row.image" alt="" style="width: 150px;height: 150px">
              <img slot="reference" :src="scope.row.image" style="width: 30px;height: 30px">
            </el-popover>
          </template>
        </el-table-column>
        <el-table-column label="价格($)" prop="price" header-align="center" align="center"  width="100" sortable="custom" />
        <el-table-column label="颜色" prop="color" header-align="center" align="center" width="100" show-overflow-tooltip />
        <el-table-column label="品牌" prop="brand" header-align="center" align="center" sortable="custom" />
        <el-table-column label="材质" prop="material" header-align="center" align="center" />
        <el-table-column label="产品重量" prop="weight" header-align="center" align="center" />
        <el-table-column label="产品尺寸" prop="product_dimensions" header-align="center" align="center" show-overflow-tooltip />
        <el-table-column label="产品评分" prop="reviews_result" header-align="center" align="center" sortable="custom" />
        <el-table-column label="首次上架时间" prop="data_first_available" header-align="center" align="center" sortable="custom" />
      </el-table>
      <el-pagination
        v-show="dataTotal>pageSize"
        background
        :total="dataTotal"
        :page-size.sync="pageSize"
        :current-page.sync="currentPage"
        layout="total, prev, pager, next"
        style="margin-top:15px;margin-left:30px"
        @current-change="getDataList"
      />
    </div>
  </div>
</template>

<script>
import {getAmazonSearch, deleteAmazonSearch} from '@/api/spider-data'
import axios from "axios";

export default {
  name: 'AmazonPlpm',
  data() {
    return {
      keyword: 'laptop',
      dataLoading: false,
      dataList: [],
      dataTotal: 100,
      pageSize: 14,
      currentPage: 1,
      productCategory: [],
      MaxVesa: [],
      isNew: '1',
      sort: {},
      multipleSelection: []
    }
  },
  created() {
    this.getDataList()
  },
  methods: {
    getDataList() {
      this.dataLoading = true
      getAmazonSearch({
        page: this.currentPage,
        keyword: this.keyword,
        sort: this.sort
      }).then(response => {
        setTimeout(() => {
          this.dataLoading = false
          this.dataList = response.data
          this.dataTotal = response.total
        }, 0.5 * 1000)
      })
    },
    handleSelectionChange(selection) {
      this.itemIdList = selection.map(item => item.asin)
    },
    deleteData() {
      deleteAmazonSearch({'asin_list': this.itemIdList}).then(response => {
        this.getDataList()
      })
    },
    downloadLogs() {
      axios.post(
        process.env.VUE_APP_BASE_API + '/spider/amazon/search',
        { keyword: this.keyword},
        {responseType: 'blob'}
        ).then((response) => {
        const url = window.URL.createObjectURL(new Blob([response.data]))
        const link = document.createElement('a')
        link.style.display = "none";
        link.href = url;

        // let timestamp=new Date().getTime();
        // link.download = timestamp + ".xlsx";
        // document.body.appendChild(link);
        // link.click();
        link.download = this.keyword + '.xlsx'
        // link.setAttribute('download', this.keyword + '.xlsx')
        document.body.appendChild(link)
        link.click()
        document.body.removeChild(link)
        window.URL.revokeObjectURL(url)
      })
    },
    sortChange(column) {
      this.dataLoading = true
      this.sort = {name: column.prop, order: column.order}
      this.getDataList()
    }
  },

}
</script>

<style>
.el-checkbox {
  display: block;
  /*width: 100%;*/
}
</style>

<style lang="scss">
.tableBox {
  td {
    padding: 6px;
  }
}
</style>
