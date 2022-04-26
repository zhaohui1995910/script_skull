import request from '@/utils/request'

export function dpgxList(query) {
  return request({
    url: '/spider/dpgxwh',
    method: 'get',
    params: query
  })
}

export function addDpgx(data) {
  return request({
    url: '/spider/dpgxwh',
    method: 'post',
    data
  })
}

export function putDpgx(data) {
  return request({
    url: '/spider/dpgxwh',
    method: 'put',
    data
  })
}

export function deleteDpgx(data) {
  return request({
    url: '/spider/dpgxwh',
    method: 'delete',
    data
  })
}

export function plpmList(data) {
  return request({
    url: '/spider/amazon/plpm',
    method: 'post',
    data
  })
}

export function getReivew(query) {
  return request({
    url: '/spider/amazon/detail',
    method: 'get',
    params: query
  })
}

export function getHistory(query) {
  return request({
    url: '/spider/amazon/product/history',
    method: 'get',
    params: query
  })
}

export function getClientBrands(query) {
  return request({
    url: '/spider/client/brands',
    method: 'get',
    params: query
  })
}

export function getAmazonInfo(data) {
  return request({
    url: '/spider/amazon/info',
    method: 'post',
    data
  })
}

export function getLumiAppLogs(query) {
  return request({
    url: '/spider/lumi/logs',
    method: 'get',
    params: query
  })
}

export function downloadAppLogs(query) {
  return request({
    url: '/spider/download/lumi/logs',
    method: 'get',
    params: query
  })
}

export function getAmazonSearch(query) {
  return request({
    url: '/spider/amazon/search',
    method: 'get',
    params: query
  })
}

export function deleteAmazonSearch(data) {
  return request({
    url: '/spider/amazon/search',
    method: 'delete',
    data
  })
}

export function getZscqSearch(query) {
  return request({
    url: '/spider/zscq',
    method: 'get',
    params: query
  })
}
