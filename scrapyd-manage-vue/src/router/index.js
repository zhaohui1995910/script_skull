import Vue from 'vue'
import Router from 'vue-router'

Vue.use(Router)

/* Layout */
import Layout from '@/layout'

/**
 * constantRoutes
 * a base page that does not have permission requirements
 * all roles can be accessed
 */
export const constantRoutes = [
  {
    path: '/redirect',
    component: Layout,
    hidden: true,
    children: [
      {
        path: '/redirect/:path*',
        component: () => import('@/views/redirect/index')
      }
    ]
  },
  {
    path: '/login',
    component: () => import('@/views/login/index'),
    hidden: true
  },
  {
    path: '/auth-redirect',
    component: () => import('@/views/login/auth-redirect'),
    hidden: true
  },
  {
    path: '/404',
    component: () => import('@/views/error-page/404'),
    hidden: true
  },
  {
    path: '/401',
    component: () => import('@/views/error-page/401'),
    hidden: true
  },
  {
    name: 'Dashboard',
    path: '/',
    hidden: true,
    component: Layout,
    children: [
      {
        path: '/',
        component: () => import('@/views/dashboard/index'),
        meta: {
          title: 'Dashboard',
          icon: 'dashboard',
          affix: false
        }
      }
    ]
  },
  {
    path: '/profile',
    component: Layout,
    redirect: '/profile/index',
    hidden: true,
    children: [
      {
        path: 'index',
        component: () => import('@/views/profile/index'),
        name: 'Profile',
        meta: {
          title: 'Profile',
          icon: 'user',
          noCache: true
        }
      }
    ]
  }
]
/**
 * asyncRoutes
 * the routes that need to be dynamically loaded based on user roles
 */
export const asyncRoutes = [
  {
    path: '*',
    redirect: '/404',
    hidden: true
  },
  {
    path: 'scrapy',
    component: Layout,
    children: [
      {
        path: '/server',
        component: () => import('@/views/scrapyd/server-table'),
        meta: {
          title: 'Server',
          icon: 'guide',
          noCache: true
        }
      }
    ]
  },
  {
    component: Layout,
    path: 'scrapy',
    children: [
      {
        path: '/project',
        component: () => import('@/views/scrapyd/project-table'),
        meta: {
          title: 'Project',
          icon: 'clipboard',
          noCache: true
        }
      }
    ]
  },
  {
    component: Layout,
    path: 'scrapy',
    children: [
      {
        path: '/task',
        component: () => import('@/views/scrapyd/timer-tasks-table'),
        meta: {
          title: 'Timer Tasks',
          icon: 'example',
          noCache: true
        }
      }
    ]
  },
  {
    component: Layout,
    path: 'scrapy',
    children: [
      {
        path: '/job',
        component: () => import('@/views/scrapyd/jobs-table'),
        meta: {
          title: 'Jobs',
          icon: 'nested',
          noCache: true
        }
      }
    ]
  },
  {
    component: Layout,
    path: 'scrapy',
    children: [
      {
        path: '/logs',
        component: () => import('@/views/scrapyd/logs-table'),
        meta: {
          title: 'Logs',
          icon: 'documentation',
          noCache: true
        }
      }
    ]
  }
]

const createRouter = () => new Router({
  // mode: 'browserHistory', // require service support
  mode: 'history', // require service support
  scrollBehavior: () => ({ y: 0 }),
  routes: constantRoutes
})
const router = createRouter()

export function resetRouter() {
  const newRouter = createRouter()
  router.matcher = newRouter.matcher // reset router
}

export default router
