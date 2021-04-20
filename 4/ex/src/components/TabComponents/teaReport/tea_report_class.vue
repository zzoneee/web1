<template>
    <div id="rc">
        <div class="plane_table">
            <el-row>
                <el-col :span="18">
                    <el-table
                            :data="tableData"
                            height="520"
                            border
                            id="tb"
                            style="width: 100%">
                        <el-table-column align='center'
                                        prop="stu_num"
                                        label="学号"
                                        width="150">
                        </el-table-column>
                        <el-table-column align='center'
                                        prop="name"
                                        label="姓名"
                                        width="120">
                        </el-table-column>
                        <el-table-column align='center'
                                 prop="group"
                                 label="团队"
                                 width="140">
                        </el-table-column>
                        <el-table-column align='center'
                                        prop="role"
                                        label="承担角色"
                                        width="100">
                        </el-table-column>
                        <el-table-column align='center'
                                        prop="hasReport1"
                                        label="实验报告">
                            <template slot-scope="scope">
                                <el-button v-if="tableData[scope.$index].hasReport==1" size="mini" class="download" 
                                @click="ReportDetail(scope.$index, tableData)">查看实验报告详情并评分</el-button>
                                <p v-if="tableData[scope.$index].hasReport==0">未提交</p>
                            </template>
                        </el-table-column>
                    </el-table>
                </el-col>

                <el-col :span="5" :offset='1'>
                    <el-select v-model="PostOptionsValue" placeholder=""  @change="PostOptionsChange(PostOptionsValue)">
                        <el-option
                            v-for="item in PostOptions"
                            :key="item.id"
                            :label="item.name"
                            :value="item.id">
                        </el-option>
                    </el-select>

                    <el-select class="PostOptionsValueClass" v-model="PostOptionsValueClass" placeholder=""  @change="PostOptionsChangeClass(PostOptionsValueClass)">
                        <el-option
                            v-for="item in PostOptionsClass"
                            :key="item.id"
                            :label="item.name"
                            :value="item.id">
                        </el-option>
                    </el-select>

                    <el-button class="searchBtn3" type="danger" v-if="searchBtn3==0" icon="el-icon-search" @click="search3()">搜索未提交</el-button>
                    <el-button class="searchBtn3" type="success" v-if="searchBtn3==1" icon="el-icon-search" @click="search3()">搜索已提交</el-button>
                    <el-button class="searchBtn3" type="primary" v-if="searchBtn3==2" @click="search3()">显示全部信息</el-button>
                </el-col>
            </el-row>
        </div>

        <el-dialog customClass="dialog_ReportDetail" title="实验报告" :visible.sync="ReportDetailVisible"  @closed="handleClose" :append-to-body="true">
            <el-table
                    :data="ReportDetailTableData"
                    height="400"
                    border
                    id="GroupNumberDetailTable"
                    style="width: 100%">
                <!-- <el-table-column align='center'
                                 prop="id"
                                 label="实验报告ID"
                                 width="120">
                </el-table-column> -->
                <el-table-column align='center'
                                 prop="create_time"
                                 label="日期"
                                 width="200">
                </el-table-column>
                <el-table-column align='center'
                                 prop="system_score"
                                 label="系统评分"
                                 width="150">
                </el-table-column>
                <el-table-column align='center'
                                 prop="hp_score"
                                 label="团队互评平均分"
                                 width="180">
                </el-table-column>
                <el-table-column align='center'
                                 prop="url"
                                 label="实验报告">
                    <template slot-scope="scope">
                        <el-button size="mini" class="download" @click="downLoadReport(scope.$index, ReportDetailTableData)">下载</el-button>
                    </template>
                </el-table-column>
                <el-table-column align='center'
                                 prop="teacher_score"
                                 label="教师评分">
                    <template slot-scope="scope">
                        <el-row :gutter="0" v-if="ReportDetailTableData[scope.$index].teacher_score!=-1">
                            <el-col :span="9" :offset="3">
                                <p>{{ ReportDetailTableData[scope.$index].teacher_score }}</p>
                            </el-col>
                            <el-col :span="9">
                                <el-button type="primary" size="mini" @click="handleJudge(scope.$index, ReportDetailTableData)">重新评分</el-button>
                            </el-col>
                        </el-row>
                        <el-button v-if="ReportDetailTableData[scope.$index].teacher_score==-1"
                            type="success" size="mini" @click="handleJudge(scope.$index, ReportDetailTableData)">评分</el-button>
                    </template>
                </el-table-column>
            </el-table>
        </el-dialog>

    </div>
</template>

<script>
    import axios from 'axios'
    export function get_exLists() {
        return axios({
            method: 'get',
            url: "/api/experiment/exLists",
            headers: {'Authorization': window.localStorage['tea_Authorization']}
        })
    }
    export function get_classesLists() {
        return axios({
            method: 'get',
            url: "/api/classes/classesLists",
            headers: {'Authorization': window.localStorage['tea_Authorization']}
        })
    }
    export function get_StuReportMsgLists(classesID, exID, OP) {
        return axios({
            method: 'get',
            url: "/api/report/StuReportMsgLists",
            headers: {'Authorization': window.localStorage['tea_Authorization']},
            params: {'classesID': classesID, 'exID': exID, 'OP': OP}
        })
    }
    export default {
        data() {
            return {
                tableData: [],

                ReportDetailVisible: false,
                ReportDetailTableData: [],

                cur_index: 0,
                cur_groupName: "实验一",

                PostOptions: [],
                PostOptionsValue: '',

                PostOptionsClass: [],
                PostOptionsValueClass: '',

                searchBtn3: 0,
            }
        },
        created() {
            // 获取实验列表
            get_exLists().then(res => {
                // console.log(res.data.data);
                if(res.data.status == 200){
                    this.PostOptions = res.data.data;
                    this.PostOptionsValue = this.PostOptions[0].id;
                    this.getClassesLists(); // 获取班级列表
                }
                else if(res.data.status == 403){
                    this.$router.replace('/tea_error')
                }
            }).catch( error =>{
                console.log(error);
            });
        },
        methods:{
            // 获取学生信息及对应的实验报告列表
            getStuReportMsgLists(){
                // console.log(878);
                get_StuReportMsgLists(this.PostOptionsValueClass, this.PostOptionsValue, this.searchBtn3).then(res => {
                    // console.log(res.data.err);
                    if(res.data.status == 200){
                        this.tableData = res.data.data;
                    }
                    else if(res.data.status == 403){
                        this.$router.replace('/tea_error')
                    }
                }).catch( error =>{
                    console.log(error);
                });
            },
            // 获取班级列表
            getClassesLists(){
                get_classesLists().then(res => {
                    // console.log(res.data.data);
                    if(res.data.status == 200){
                        this.PostOptionsClass = res.data.data;
                        this.PostOptionsValueClass = this.PostOptionsClass[0].id;
                        this.getStuReportMsgLists(); // 获取学生信息及对应的实验报告列表
                    }
                    else if(res.data.status == 403){
                        this.$router.replace('/tea_error')
                    }
                }).catch( error =>{
                    console.log(error);
                });
            },
            getteaReportList(index, row, reportNum){
                this.$axios({
                    method: 'get',
                    url: "/api/teacher/reportDetail",
                    params:{groupName: row[index].group, reportNum: reportNum}
                }).then(res=> {
                    if(res.status == 200){
                        this.ReportDetailTableData=res.data.data;
                        this.ReportDetailTableData.forEach(item=>{
                            if(item['system_score']==-1){
                                item['system_score']='暂无评分'
                            }
                            if(item['hp_score']==-1){
                                item['hp_score']='暂无评分'
                            }
                        })
                    }
                }).catch( error =>{
                    console.log(error);
                });
            },
            GroupNumberDetail(index, row){
                this.GroupNumberDetailVisible = true;
                this.$axios({
                    method: 'get',
                    url: "/api/teacher/groupNumberDetail",
                    params:{groupName: row[index].name}
                }).then(res=> {
                    // console.log(res.data.status);
                    if(res.status == 200){
                        this.GroupNumberDetailTableData=res.data.data;
                        this.allTableData=res.data.data;
                        this.password = res.data.password;
                    }
                }).catch( error =>{
                    console.log(error);
                });
            },
            ReportDetail(index, row){
                this.ReportDetailVisible = true;
                this.getteaReportList(index, row, this.PostOptionsValue);
                this.cur_index = index;
                this.cur_groupName = this.PostOptionsValue;
            },
            handleClose () {
            },
            handleJudge(index, row) {
                this.$prompt('请输入给该团队的评分', '评分', {
                    confirmButtonText: '确定',
                    cancelButtonText: '取消',
                }).then(({ value }) => {
                    if(value<=100&&value>0)
                    {
                        this.$axios({
                            method: 'post',
                            url: "/api/teacher/teaReportMark",
                            data:{userId:window.localStorage['tea_userId'],id:row[index].id,score:value}
                        }).then(res=> {
                            if(res.status == 200){
                                this.getteaReportList(this.cur_index, this.tableData, this.cur_groupName);
                                this.$message({
                                    type: 'success',
                                    message: '评分成功'
                                });
                            }
                        }).catch( error =>{
                            console.log(error);
                        });
                    }
                    else {
                        this.$message({
                            type: 'warning',
                            message: '输入不合法'
                        });
                    }
                }).catch(() => {
                    this.$message({
                        type: 'info',
                        message: '取消输入'
                    });
                });
            },
            downLoadReport(index, row) {
                this.$axios({
                    method: 'get',
                    url: "/api/teacher/getReportUrl",
                    params:{id:row[index].id}
                }).then(res=> {
                    if(res.status == 200){
                        // let url = 'http://47.111.151.229/downLoad/report/' + res.data.data;
                        let url = 'http://127.0.0.1:8000/downLoad/report/' + res.data.data;
                        // console.log(row[index].id + "*** " + url + " ***");
                        window.open(url);
                    }
                }).catch( error =>{
                    console.log(error);
                });
            },
            PostOptionsChange(PostOptionsValue){
                // console.log(PostOptionsValue);
                this.getStuReportMsgLists(); // 获取学生信息及对应的实验报告列表
            },
            PostOptionsChangeClass(PostOptionsValueClass){
                // console.log(PostOptionsValue);
                this.getStuReportMsgLists(); // 获取学生信息及对应的实验报告列表
            },
            search3(){
                this.searchBtn3 = (this.searchBtn3 + 1) % 3;
                this.getStuReportMsgLists();
            },
        }
    }
</script>

<style scoped>
    #rc{
        width:960px;
        margin:0 auto;
        margin-top: 10px;
    }
    #tb{
        box-shadow:2px 2px 2px 2px rgba(0,0,0,0.16);
        font-weight: bolder;
        font-size: 17px;
    }
    .download{
        color: #FFF;
        background-color: #124856;
        border-color: #123456;
    }

    .download:active{
        background-color:#095b74;
    }
    .el-table {
        background-color: transparent !important;
    }
    .plane_table /deep/ tr, .plane_table /deep/ th, .plane_table /deep/ td {
        background: #5692ca1c !important;
        color:#095b74;
        border-bottom: 0;
    }

    .plane_table /deep/  .el-table tbody tr:nth-child(odd) {
        background-color: #c9e5ec !important
    }
    #GroupNumberDetailTable{
        font-weight: bolder;
        font-size: 17px;
    }
    .PostOptionsValueClass{
        margin-top: 35px;
    }
    .searchBtn3{
        margin-top: 35px;
    }
</style>

<style>
    .dialog_GroupNumberDetail{
        width:1000px;
    }
    .dialog_ReportDetail{
        width:1000px;
    }
</style>
