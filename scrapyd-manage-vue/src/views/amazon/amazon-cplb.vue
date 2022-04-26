<template>
  <div class="app-container">
    <div class="one">
      <div class="search" style="background-color: #eef1f6;height: 40px; padding-top: 5px;padding-left: 5px">
        <span style="font-size: 13px;color: #303133">客户：</span>
        <el-input v-model="searchInput" placeholder="请输入客户编码" style="width: 130px" @change="getBrands" />
      </div>
      <el-collapse v-model="activeNames" style="color: #eef1f6">
        <el-collapse-item title="Max.VESA" name="1">
          <template>
            <el-checkbox-group v-model="MaxVesa" @change="getDataList">
              <el-checkbox label="100mm x 100mm" size="medium" />
              <el-checkbox label="200mm x 100mm" size="medium" />
              <el-checkbox label="200mm x 200mm" size="medium" />
              <el-checkbox label="400mm x 200mm" size="medium" />
              <el-checkbox label="400mm x 400mm" size="medium" />
              <el-checkbox label="600mm x 400mm" size="medium" />
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
        <el-collapse-item v-show="brandList.length" title="Brand" name="3">
          <template>
            <el-checkbox-group v-model="Brand" @change="getDataList">
              <el-checkbox v-for="brand in brandList" :key="brand" :label="brand" size="medium" />
            </el-checkbox-group>
          </template>
        </el-collapse-item>
        <el-collapse-item title="是否新品" name="4">
          <el-radio-group v-model="isNew" @change="getDataList">
            <el-radio label="1" size="medium">是</el-radio>
            <el-radio label="0" size="medium">否</el-radio>
          </el-radio-group>
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
        <el-table-column label="产品描述" prop="title" header-align="center" align="center" width="280px" show-overflow-tooltip />
        <el-table-column label="产品图片" align="center">
          <template slot-scope="scope">
            <el-popover placement="top-start" title="" trigger="hover">
              <img :src="scope.row.image" alt="" style="width: 150px;height: 150px">
              <img slot="reference" :src="scope.row.image" style="width: 30px;height: 30px">
            </el-popover>
          </template>
        </el-table-column>
        <el-table-column label="产品排名" prop="mostTopNumber" header-align="center" align="center" width="80" show-overflow-tooltip>
          <template slot-scope="scope">
            <a :key="scope" :href="scope.row.topCategoryUrl" target="_blank">{{ scope.row.mostTopNumber }}</a>
          </template>
        </el-table-column>
        <el-table-column label="产品类目" prop="bestSellersRank" header-align="center" align="center" width="80" show-overflow-tooltip />
        <el-table-column label="产品星级" prop="rating" header-align="center" align="center" width="80" />
        <el-table-column label="三星上好品率" prop="goodReviewRate" header-align="center" align="center" width="100" />
        <el-table-column label="三星下差评率" prop="badReviewRate" header-align="center" align="center" width="100" />
        <el-table-column label="包装尺寸" prop="dimensions" header-align="center" align="center" min-width="140px" show-overflow-tooltip />
        <el-table-column label="是否断货" prop="stock" header-align="center" align="center" width="80" show-overflow-tooltip />
        <el-table-column label="价格" prop="price" header-align="center" align="center" show-overflow-tooltip />
        <el-table-column label="最低价" prop="marketMinPrice" header-align="center" align="center" show-overflow-tooltip />
        <el-table-column label="发布时间" prop="release_date" header-align="center" align="center" />
        <el-table-column label="链接" width="80">
          <template slot-scope="scope">
            <a :href="scope.row.url" target="_blank" style="color:blue">查看</a>
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
import Cookies from 'js-cookie'
import { getClientBrands, getAmazonInfo } from '@/api/spider-data'

export default {
  name: 'AmazonCplb',
  data() {
    return {
      activeNames: '',
      searchInput: '',
      dataLoading: false,
      dataList: [],
      dataTotal: 500,
      pageSize: 15,
      currentPage: 1,
      productCategory: [],
      MaxVesa: [],
      isNew: '0',
      Brand: [],
      brandList: []
    }
  },
  // created() {
  //   this.getBrands()
  // },
  methods: {
    getDataList() {
      this.dataLoading = true

      getAmazonInfo({
        page: this.currentPage,
        vesa: this.MaxVesa,
        category: this.productCategory,
        brands: this.Brand,
        isnew: this.isNew
      }).then(response => {
        this.dataList = response.data
        this.dataTotal = response.total
        this.dataLoading = false
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
    },
    getBrands() {
      if (this.searchInput !== '') {
        getClientBrands({ qcbm: this.searchInput, userCode: Cookies.get('user_id') }).then(response => {
          this.brandList = response.data
          this.Brand = response.data
          getAmazonInfo({
            page: this.currentPage,
            vesa: this.MaxVesa,
            category: this.productCategory,
            brands: response.data,
            isnew: this.isNew
          }).then(response => {
            this.dataList = response.data
            this.dataTotal = response.total
          })
        })
      }
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
  .search {
    width: 100%;
    padding-bottom: 5px;
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
