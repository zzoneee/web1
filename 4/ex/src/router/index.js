import Vue from 'vue'
import Router from 'vue-router'
// import HelloWorld from '@/components/HelloWorld'
import loginPage from "../views/loginPage";
import menu from "../views/menu";
import report from '@/components/report.vue'
import setting from '@/components/setting.vue'
import mail from '@/components/mail.vue'
import StuForum from '@/components/TabComponents/forum/StuForum.vue'
import tlForum from '@/components/tlForum/tlForum.vue'

import tea_loginPage from "../views/tea_loginPage";
import tea_info from '@/components/tea_info.vue'

import tmp from '@/components/tmp.vue'

import stu_error from "../views/error/stu_error";
import tea_error from "../views/error/tea_error";



Vue.use(Router)

export default new Router({
  routes: [
    {
      path: '/',
      component: loginPage
    },
    {
      path: '/menu',
      component: menu
    },
    {
      path: '/report',
      component: report
    },
    {
      path: '/setting',
      component: setting
    },
    {
      path: '/tea_login',
      component: tea_loginPage
    },
    {
      path: '/tea_info',
      component: tea_info
    },
    {
      path: '/tmp',
      component: tmp
    },
    {
      path: '/stu_error',
      component: stu_error
    },
    {
      path: '/tea_error',
      component: tea_error
    },
    {
      path: '/mail',
      component: mail
    },
    {
      path: '/forum',
      component: StuForum
    },
    {
      path: '/tlForum',
      component: tlForum
    },
  ]
})
