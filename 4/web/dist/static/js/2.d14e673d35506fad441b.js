webpackJsonp([2],{"3zE5":function(t,e){},T2Kd:function(t,e,a){"use strict";Object.defineProperty(e,"__esModule",{value:!0});var o=a("mtWM"),l=a.n(o);function n(){return l()({method:"get",url:"/api/experiment/exLists",headers:{Authorization:window.localStorage.tea_Authorization}})}var i={data:function(){return{tableData:[],GroupNumberDetailVisible:!1,GroupNumberDetailTableData:[],ReportDetailVisible:!1,ReportDetailTableData:[],cur_index:0,cur_groupName:"实验一",PostOptions:[],PostOptionsValue:"",searchBtn3:0}},created:function(){var t=this;n().then(function(e){200==e.data.status?(t.PostOptions=e.data.data,t.PostOptionsValue=t.PostOptions[0].id,t.getGroupList(t.PostOptionsValue)):403==e.data.status&&t.$router.replace("/tea_error")}).catch(function(t){console.log(t)})},methods:{getGroupList:function(t){var e=this;this.$axios({method:"get",url:"/api/teacher/getGroupListDetail",params:{id:t,OP:this.searchBtn3}}).then(function(t){200==t.status?e.tableData=t.data.data:console.log(t.data.msg)}).catch(function(t){console.log(t)})},getteaReportList:function(t,e,a){var o=this;this.$axios({method:"get",url:"/api/teacher/reportDetail",params:{groupName:e[t].name,reportNum:a}}).then(function(t){200==t.status&&(o.ReportDetailTableData=t.data.data,o.ReportDetailTableData.forEach(function(t){-1==t.system_score&&(t.system_score="暂无评分"),-1==t.hp_score&&(t.hp_score="暂无评分")}))}).catch(function(t){console.log(t)})},GroupNumberDetail:function(t,e){var a=this;this.GroupNumberDetailVisible=!0,this.$axios({method:"get",url:"/api/teacher/groupNumberDetail",params:{groupName:e[t].name}}).then(function(t){200==t.status&&(a.GroupNumberDetailTableData=t.data.data,a.allTableData=t.data.data,a.password=t.data.password)}).catch(function(t){console.log(t)})},ReportDetail:function(t,e){this.ReportDetailVisible=!0,this.getteaReportList(t,e,this.PostOptionsValue),this.cur_index=t,this.cur_groupName=this.PostOptionsValue},handleClose:function(){},handleJudge:function(t,e){var a=this;this.$prompt("请输入给该团队的评分","评分",{confirmButtonText:"确定",cancelButtonText:"取消"}).then(function(o){var l=o.value;l<=100&&l>0?a.$axios({method:"post",url:"/api/teacher/teaReportMark",data:{userId:window.localStorage.tea_userId,id:e[t].id,score:l}}).then(function(t){200==t.status&&(a.getteaReportList(a.cur_index,a.tableData,a.cur_groupName),a.$message({type:"success",message:"评分成功"}))}).catch(function(t){console.log(t)}):a.$message({type:"warning",message:"输入不合法"})}).catch(function(){a.$message({type:"info",message:"取消输入"})})},downLoadReport:function(t,e){this.$axios({method:"get",url:"/api/teacher/getReportUrl",params:{id:e[t].id}}).then(function(t){if(200==t.status){var e="http://47.111.151.229/downLoad/report/"+t.data.data;window.open(e)}}).catch(function(t){console.log(t)})},PostOptionsChange:function(t){this.getGroupList(this.PostOptionsValue)},search3:function(){this.searchBtn3=(this.searchBtn3+1)%3,this.getGroupList(this.PostOptionsValue)}}},r={render:function(){var t=this,e=t.$createElement,a=t._self._c||e;return a("div",{attrs:{id:"rc"}},[a("div",{staticClass:"plane_table"},[a("el-row",[a("el-col",{attrs:{span:18}},[a("el-table",{staticStyle:{width:"100%"},attrs:{data:t.tableData,height:"520",border:"",id:"tb","header-cell-style":t.tableHeaderColor}},[a("el-table-column",{attrs:{align:"center",prop:"name",label:"团队",width:"200"}}),t._v(" "),a("el-table-column",{attrs:{align:"center",prop:"roles",label:"队员",width:"300"},scopedSlots:t._u([{key:"default",fn:function(e){return[a("p",[t._v(t._s(t.tableData[e.$index].stu_nameString))]),t._v(" "),a("el-button",{staticClass:"download",attrs:{size:"mini"},on:{click:function(a){return t.GroupNumberDetail(e.$index,t.tableData)}}},[t._v("查看队员详情")])]}}])}),t._v(" "),a("el-table-column",{attrs:{align:"center",prop:"hasReport1",label:"实验报告"},scopedSlots:t._u([{key:"default",fn:function(e){return[1==t.tableData[e.$index].hasReport?a("el-button",{staticClass:"download",attrs:{size:"mini"},on:{click:function(a){return t.ReportDetail(e.$index,t.tableData)}}},[t._v("查看实验报告详情并评分")]):t._e(),t._v(" "),0==t.tableData[e.$index].hasReport?a("p",[t._v("未提交")]):t._e()]}}])})],1)],1),t._v(" "),a("el-col",{attrs:{span:5,offset:1}},[a("el-select",{attrs:{placeholder:""},on:{change:function(e){return t.PostOptionsChange(t.PostOptionsValue)}},model:{value:t.PostOptionsValue,callback:function(e){t.PostOptionsValue=e},expression:"PostOptionsValue"}},t._l(t.PostOptions,function(t){return a("el-option",{key:t.id,attrs:{label:t.name,value:t.id}})}),1),t._v(" "),0==t.searchBtn3?a("el-button",{staticClass:"searchBtn3",attrs:{type:"danger",icon:"el-icon-search"},on:{click:function(e){return t.search3()}}},[t._v("搜索未提交")]):t._e(),t._v(" "),1==t.searchBtn3?a("el-button",{staticClass:"searchBtn3",attrs:{type:"success",icon:"el-icon-search"},on:{click:function(e){return t.search3()}}},[t._v("搜索已提交")]):t._e(),t._v(" "),2==t.searchBtn3?a("el-button",{staticClass:"searchBtn3",attrs:{type:"primary"},on:{click:function(e){return t.search3()}}},[t._v("显示全部信息")]):t._e()],1)],1)],1),t._v(" "),a("el-dialog",{attrs:{customClass:"dialog_GroupNumberDetail",title:"队员",visible:t.GroupNumberDetailVisible,"append-to-body":!0},on:{"update:visible":function(e){t.GroupNumberDetailVisible=e},closed:t.handleClose}},[a("el-table",{staticStyle:{width:"100%"},attrs:{data:t.GroupNumberDetailTableData,height:"400",border:"",id:"GroupNumberDetailTable","header-cell-style":t.tableHeaderColor}},[a("el-table-column",{attrs:{align:"center",prop:"college",label:"学院",width:"210"}}),t._v(" "),a("el-table-column",{attrs:{align:"center",prop:"class_name",label:"班级",width:"150"}}),t._v(" "),a("el-table-column",{attrs:{align:"center",prop:"stu_num",label:"学号",width:"160"}}),t._v(" "),a("el-table-column",{attrs:{align:"center",prop:"name",label:"姓名",width:"150"}}),t._v(" "),a("el-table-column",{attrs:{align:"center",prop:"phone",label:"电话号码",width:"160"}}),t._v(" "),a("el-table-column",{attrs:{align:"center",prop:"role",label:"承担角色"}})],1),t._v(" "),a("div",{staticClass:"dialog-footer",attrs:{slot:"footer"},slot:"footer"},[a("el-button",{attrs:{type:"primary"},on:{click:function(e){t.GroupNumberDetailVisible=!1}}},[t._v("确定")])],1)],1),t._v(" "),a("el-dialog",{attrs:{customClass:"dialog_ReportDetail",title:"实验报告",visible:t.ReportDetailVisible,"append-to-body":!0},on:{"update:visible":function(e){t.ReportDetailVisible=e},closed:t.handleClose}},[a("el-table",{staticStyle:{width:"100%"},attrs:{data:t.ReportDetailTableData,height:"400",border:"",id:"GroupNumberDetailTable"}},[a("el-table-column",{attrs:{align:"center",prop:"create_time",label:"日期",width:"200"}}),t._v(" "),a("el-table-column",{attrs:{align:"center",prop:"system_score",label:"系统评分",width:"150"}}),t._v(" "),a("el-table-column",{attrs:{align:"center",prop:"hp_score",label:"团队互评平均分",width:"180"}}),t._v(" "),a("el-table-column",{attrs:{align:"center",prop:"url",label:"实验报告"},scopedSlots:t._u([{key:"default",fn:function(e){return[a("el-button",{staticClass:"download",attrs:{size:"mini"},on:{click:function(a){return t.downLoadReport(e.$index,t.ReportDetailTableData)}}},[t._v("下载")])]}}])}),t._v(" "),a("el-table-column",{attrs:{align:"center",prop:"teacher_score",label:"教师评分"},scopedSlots:t._u([{key:"default",fn:function(e){return[-1!=t.ReportDetailTableData[e.$index].teacher_score?a("el-row",{attrs:{gutter:0}},[a("el-col",{attrs:{span:9,offset:3}},[a("p",[t._v(t._s(t.ReportDetailTableData[e.$index].teacher_score))])]),t._v(" "),a("el-col",{attrs:{span:9}},[a("el-button",{attrs:{type:"primary",size:"mini"},on:{click:function(a){return t.handleJudge(e.$index,t.ReportDetailTableData)}}},[t._v("重新评分")])],1)],1):t._e(),t._v(" "),-1==t.ReportDetailTableData[e.$index].teacher_score?a("el-button",{attrs:{type:"success",size:"mini"},on:{click:function(a){return t.handleJudge(e.$index,t.ReportDetailTableData)}}},[t._v("评分")]):t._e()]}}])})],1)],1)],1)},staticRenderFns:[]};a.d(e,"get_exLists",function(){return n});var s=a("VU/8")(i,r,!1,function(t){a("3zE5"),a("cXP6")},"data-v-3c065dce",null);e.default=s.exports},cXP6:function(t,e){}});
//# sourceMappingURL=2.d14e673d35506fad441b.js.map