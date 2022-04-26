import request from '@/utils/request'

export function serverList(query) {
  return request({
    url: '/scrapy/server',
    method: 'get',
    params: query
  })
}

export function serverAdd(data) {
  return request({
    url: '/scrapy/server',
    method: 'post',
    data
  })
}

export function serverDel(data) {
  return request({
    url: '/scrapyd/servers',
    method: 'delete',
    data
  })
}

export function projectList(query) {
  return request({
    url: '/scrapy/project',
    method: 'get',
    params: query
  })
}

export function projectSet() {
  return request({
    url: '/scrapyd/project/set',
    method: 'get'
  })
}

export function projectSpiderList(query) {
  return request({
    url: '/scrapyd/projects/spiders',
    method: 'get',
    params: query
  })
}

export function activateProjectSpider(data) {
  return request({
    url: '/scrapyd/projects/spiders',
    method: 'post',
    data
  })
}

export function updateProject(data) {
  return request({
    url: '/scrapyd/projects',
    method: 'post',
    data
  })
}

export function updateSpider(data) {
  return request({
    url: '/scrapyd/spiders/info',
    method: 'post',
    data
  })
}

export function spiderList(query) {
  return request({
    url: '/scrapyd/spiders/info',
    method: 'get',
    params: query
  })
}

export function addTask(data) {
  return request({
    url: '/scrapyd/tasks/info',
    method: 'post',
    data
  })
}

export function updateTask(data) {
  return request({
    url: '/scrapyd/tasks/info',
    method: 'put',
    data
  })
}

export function taskList(query) {
  return request({
    url: '/scrapyd/tasks/info',
    method: 'get',
    params: query
  })
}

export function deleteTask(data) {
  return request({
    url: '/scrapyd/tasks/delete',
    method: 'post',
    data
  })
}

export function statusTask(data) {
  return request({
    url: '/scrapyd/tasks/status',
    method: 'post',
    data
  })
}

export function jobList(query) {
  return request({
    url: '/scrapyd/jobs',
    method: 'get',
    params: query
  })
}

export function deleteJob(data) {
  return request({
    url: '/scrapyd/jobs',
    method: 'post',
    data
  })
}

export function getJob(query) {
  return request({
    url: '/scrapyd/get/job',
    method: 'get',
    params: query
  })
}

export function LogList(query) {
  return request({
    url: '/scrapyd/logs',
    method: 'get',
    params: query
  })
}

export function LogInfo(query) {
  return request({
    url: '/scrapyd/log/info',
    method: 'get',
    params: query
  })
}

export function runSpider(data) {
  return request({
    url: '/scrapyd/spider/run',
    method: 'post',
    data
  })
}

export function stopSpider(data) {
  return request({
    url: '/scrapyd/spider/cancel',
    method: 'post',
    data
  })
}

export function jobStats(query) {
  return request({
    url: '/scrapyd/job/stats',
    method: 'get',
    params: query
  })
}

export function getMongoTree(query) {
  return request({
    url: '/home/mongo/tree',
    method: 'get',
    params: query
  })
}

export function getMongoCollFields(query) {
  return request({
    url: '/home/mongo/coll/fields',
    method: 'get',
    params: query
  })
}

export function getSpiderTree(query) {
  return request({
    url: '/scrapyd/spider/tree',
    method: 'get',
    params: query
  })
}

export function addViews(data) {
  return request({
    url: '/scrapyd/views',
    method: 'post',
    data
  })
}

export function getViews(query) {
  return request({
    url: '/scrapyd/views',
    method: 'get',
    params: query
  })
}

export function deleteViews(data) {
  return request({
    url: '/scrapyd/views',
    method: 'delete',
    data
  })
}

export function putViews(data) {
  return request({
    url: '/scrapyd/views',
    method: 'put',
    data
  })
}

export function getSpiderData(query) {
  return request({
    url: '/scrapyd/data',
    method: 'get',
    params: query
  })
}

export function getNoticeLinechartData(query) {
  return request({
    url: '/scrapyd/notice/linechart',
    method: 'get',
    params: query
  })
}

export function getNoticeUnreadCount(query) {
  return request({
    url: '/scrapyd/notice/unread/count',
    method: 'get',
    params: query
  })
}

export function getNoticeData(query) {
  return request({
    url: '/scrapyd/notice',
    method: 'get',
    params: query
  })
}

export function putNoticeData(query) {
  return request({
    url: '/scrapyd/notice',
    method: 'put',
    params: query
  })
}
