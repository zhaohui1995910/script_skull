<template>
  <div class="app-container">
    <div class="one">
      <el-collapse>
        <el-collapse-item title="Max.VESA" name="1">
          <template>
            <el-checkbox-group v-model="MaxVesa" @change="getDataList">
              <el-checkbox label="100x100" size="medium" />
              <el-checkbox label="200x100" size="medium" />
              <el-checkbox label="200x200" size="medium" />
              <el-checkbox label="400x200" size="medium" />
              <el-checkbox label="400x400" size="medium" />
              <el-checkbox label="600x400" size="medium" />
            </el-checkbox-group>
          </template>
        </el-collapse-item>
        <el-collapse-item title="Product Category" name="2">
          <template>
            <el-checkbox-group v-model="productCategory" @change="getDataList">
              <el-checkbox label="Best Sellers in Home Office Desks" size="medium" />
              <el-checkbox label="TV MOUNT" size="medium" />
              <el-checkbox label="Monitor Arms & Monitor Stands" size="medium" />
              <el-checkbox label="Best Sellers in Computer Workstations" size="medium" />
            </el-checkbox-group>
          </template>
        </el-collapse-item>
        <el-collapse-item title="是否新品" name="4">
          <el-radio v-model="isNew" label="1" size="medium">是</el-radio>
          <el-radio v-model="isNew" label="0" size="medium">否</el-radio>
        </el-collapse-item>
      </el-collapse>
    </div>
    <div class="two">
      <el-table
        v-loading="dataLoading"
        :data="dataList"
        class="tableBox"
        :header-cell-style="{background:'#eef1f6',color:'#606266'}"
        :row-style="{padding:'5px'}"
        @cell-dblclick="toDetail"
      >
        <el-table-column label="产品描述" prop="title" header-align="center" align="center" width="360px" show-overflow-tooltip />
        <el-table-column label="产品图片" align="center">
          <template slot-scope="scope">
            <el-popover placement="top-start" title="" trigger="hover">
              <img :src="scope.row.imgLink" alt="" style="width: 150px;height: 150px">
              <img slot="reference" :src="scope.row.imgLink" style="width: 30px;height: 30px">
            </el-popover>
          </template>
        </el-table-column>
        <el-table-column label="所属品类" prop="department" header-align="center" align="center" show-overflow-tooltip>
          <template slot-scope="scope">
            <a :href="scope.row.departmentLink" target="_blank">{{ scope.row.department }}</a>
          </template>
        </el-table-column>
        <el-table-column label="产品排名" prop="number" header-align="center" align="center" width="80" />
        <el-table-column label="产品星级" prop="level" header-align="center" align="center" width="80" />
        <el-table-column label="三星上好品数" prop="praise_count" header-align="center" align="center" width="100" />
        <el-table-column label="三星下差评数" prop="negative_count" header-align="center" align="center" width="100" />
        <el-table-column label="包装尺寸" prop="dimensions" header-align="center" align="center" width="100" show-overflow-tooltip />
        <el-table-column label="是否断货" prop="stock" header-align="center" align="center" width="100" show-overflow-tooltip />
        <el-table-column label="价格" prop="price" header-align="center" align="center" />
        <el-table-column label="链接" width="80px">
          <template slot-scope="scope">
            <a :href="scope.row.productUrl" target="_blank" style="color:blue">查看</a>
          </template>
        </el-table-column>
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
import { plpmList } from '@/api/spider-data'

export default {
  name: 'AmazonPlpm',
  data() {
    return {
      dataLoading: false,
      dataList: [],
      dataTotal: 100,
      pageSize: 15,
      currentPage: 1,
      productCategory: [],
      MaxVesa: [],
      isNew: '1'
    }
  },
  created() {
    this.getDataList()
  },
  methods: {
    getDataList() {
      plpmList({
        page: this.currentPage,
        vesa: this.MaxVesa,
        category: this.productCategory,
        isnew: this.isNew
      }).then(response => {
        this.dataList = response.data
        this.dataTotal = response.total
      })
    },
    toDetail(row, column, cell, event) {
      // var detaulUrl = this.$router.resolve({
      //   path: '/cpxq',
      //   query: {
      //     page: 1,
      //     asin: row.asin,
      //     brand: row.brand
      //   }
      // })
      var query = { page: 1, asin: row.asin, brand: row.brand }
      var path = '/cpxq/' + row.asin
      this.$router.push({ path: path, query: query })
      // window.open(detaulUrl.href)
    }
  }
}
</script>

<style>
  .one {
    width: 12%;
    float: left;
  }
  .two {
    width: 88%;
    float: left;
  }
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
