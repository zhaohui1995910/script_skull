<template>
  <div class="app-container">
    <el-table
      v-loading="dataLoading"
      v-el-table-infinite-scroll="loadData"
      :data="dataList"
      :header-cell-style="{background:'#eef1f6',color:'#606266'}"
      height="400"
      stripe="true"
    >
      <el-table-column label="评论日期" prop="createDate" header-align="center" align="center" width="150px" show-overflow-tooltip />
      <el-table-column label="评论标题" prop="title" header-align="center" align="center" width="200px" show-overflow-tooltip />
      <el-table-column label="评论分数" prop="level" header-align="center" align="center" width="100px" />
      <el-table-column label="评论内容" prop="content" header-align="center" />
    </el-table>
    <div style="padding-top: 20px">
      <div class="block">
        <el-date-picker
          v-model="dateSelect"
          type="daterange"
          range-separator="至"
          start-placeholder="开始日期"
          end-placeholder="结束日期"
          style="margin-left: 50px;"
          value-format="yyyy-MM-dd"
          @change="getHistoryData"
        />
      </div>
      <line-chart id="price" :chart-data="linePriceData" :legend-data="legendDataprice" :width="chartwidth" style="display: inline-block;margin-right: 50px" />
      <line-chart id="review" :chart-data="lineReviewData" :legend-data="legendDataReview" :width="chartwidth" style="display: inline-block" />
    </div>
  </div>
</template>

<script>
import { getReivew, getHistory } from '@/api/spider-data'
// import Chart from '@/components/Charts/MixChart'
import elTableInfiniteScroll from 'el-table-infinite-scroll'
import LineChart from './components/LineChart'

export default {
  components: {
    LineChart
    // Chart
  },
  directives: {
    'el-table-infinite-scroll': elTableInfiniteScroll
  },
  data() {
    return {
      // dateSelect: ['2020-12-27', '2021-01-26'],
      dateSelect: [],
      asin: '',
      page: 1,
      brand: '',
      dataLoading: false,
      dataList: [],
      tableHeight: `${document.documentElement.clientHeight}`,
      chartwidth: '45%',
      legendDataReview: ['review'],
      legendDataprice: ['price'],
      linePriceData: {
        expectedData: [],
        xAxisData: []
      },
      lineReviewData: {
        actualData: [],
        xAxisData: []
      }
    }
  },
  created() {
    this.asin = this.$route.query.asin
    this.page = this.$route.query.page
    this.brand = this.$route.query.brand
    // this.$route.meta.title = this.$route.query.asin
    this.getProductReview()
    // this.initDateSelect()
    this.getHistoryData()
  },
  methods: {
    getProductReview() {
      getReivew({ asin: this.asin, page: this.page, brand: this.brand }).then(response => {
        this.dataList = response.data
      })
    },
    loadData() {
      this.page = this.page + 1
      getReivew({ asin: this.asin, page: this.page, brand: this.brand }).then(response => {
        this.dataList = this.dataList.concat(response.data)
      })
    },
    getHistoryData() {
      var start_date = this.dateSelect[0]
      var end_date = this.dateSelect[1]
      getHistory({ start_date: start_date, end_date: end_date, asin: this.asin, brand: this.brand }).then(response => {
        this.linePriceData.expectedData = response.data.price_list
        this.linePriceData.xAxisData = response.data.x_axis
        this.lineReviewData.actualData = response.data.review_list
        this.lineReviewData.xAxisData = response.data.x_axis
        this.dateSelect = [response.start_date, response.end_date]
      })
    }
  }
}
</script>

<style scoped>
.chart-container{
  position: relative;
  width: 50%;
  display: inline;
  height: calc(100vh - 500px);
}
</style>
