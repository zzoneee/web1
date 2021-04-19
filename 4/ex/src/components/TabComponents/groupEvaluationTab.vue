<template>
    <div id="rc2">
        <div class="plane_table2">
            <el-table
                    :data="hp_tableData"
                    height="520"
                    border
                    id="tb2"
                    :header-cell-style="tableHeaderColor"
                    style="width: 100%">
                <!-- <el-table-column align='center'
                                 prop="hp_ex_ID"
                                 label="实验报告ID"
                                 width="120">
                </el-table-column> -->
                <el-table-column align='center'
                                 prop="hp_ex_groupName"
                                 label="团队名称"
                                 width="200">
                </el-table-column>
                <el-table-column align='center'
                                 prop="hp_ex_Date"
                                 label="日期"
                                 width="150">
                </el-table-column>
                <el-table-column align='center'
                                 prop="hp_ex_name"
                                 label="实验名称"
                                 width="260">
                </el-table-column>
                <el-table-column align='center'
                                 prop="hp_ex_address"
                                 label="实验报告"
                                 width="131">
                    <template slot-scope="scope">
                        <el-button size="mini" class="download" @click="downLoadReport(scope.$index, hp_tableData)">下载</el-button>
                    </template>
                </el-table-column>
                <el-table-column align='center'
                                 prop="hp_ex_score"
                                 label="评分">
                    <template slot-scope="scope">
                        <el-row :gutter="0" v-if="hp_tableData[scope.$index].hp_ex_score!=-1">
                            <el-col :span="9" :offset="3">
                                <p>{{ hp_tableData[scope.$index].hp_ex_score }}</p>
                            </el-col>
                            <el-col :span="9">
                                <el-button type="primary" size="mini" @click="handleJudge(scope.$index, hp_tableData)">重新评分</el-button>
                            </el-col>
                        </el-row>
                        <el-button v-if="hp_tableData[scope.$index].hp_ex_score==-1"
                            type="success" size="mini" @click="handleJudge(scope.$index, hp_tableData)">评分</el-button>
                    </template>
                </el-table-column>
            </el-table>
        </div>
    </div>
</template>

<script>

    export default {

        data() {
            return {
                hp_tableData: []
            }
        },
        created() {
            this.gethpReportList();
        },
        methods:{
            gethpReportList(){
                this.$axios({
                    method: 'post',
                    url: "/api/report/hpReportList",
                    data:{userId:window.localStorage['userId']}
                }).then(res=> {
                    if(res.data.status == 200){
                        this.hp_tableData=res.data.data;
                    }
                }).catch( error =>{
                    console.log(error);
                });
            },
            handleJudge(index, row) {
                this.$prompt('请输入给该团队的评分', '评分', {
                    confirmButtonText: '确定',
                    cancelButtonText: '取消',
                }).then(({ value }) => {
                    if(value<=100&&value>0)
                    {
                        console.log(row[index].hp_ex_ID);
                        this.$axios({
                            method: 'post',
                            url: "/api/report/hpReportMark",
                            data:{userId:window.localStorage['userId'],id:row[index].hp_ex_ID,score:value}
                        }).then(res=> {
                            if(res.data.status == 200){
                                this.gethpReportList();
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
                    params:{id:row[index].hp_ex_ID}
                }).then(res=> {
                    if(res.data.status == 200){
                        let url = 'http://47.111.151.229/downLoad/report/' + res.data.data;
                        window.open(url);
                    }
                }).catch( error =>{
                    console.log(error);
                });
            },
        }
    }
</script>

<style scoped>
    #rc2{
        width:960px;
        margin:0 auto;
        margin-top: 10px;
    }
    #tb2{
        box-shadow:2px 2px 2px 2px rgba(0,0,0,0.16);
    }
    .download{
        color: #FFF;
        background-color: #123456;
        border-color: #123456;
    }
    #new {
        margin-top: 20px;
        float: right;
    }
    .download:active{
        background-color:#305274;
    }
    .el-table {
        background-color: transparent !important;
    }
    .plane_table2 /deep/ tr, .plane_table2 /deep/ th, .plane_table2 /deep/ td {
        background: #5692ca1c !important;
        color:#095b74;
        font-weight: bold;
        font-size: 17px;
        border-bottom: 0;
    }
    .plane_table2 /deep/  .el-table tbody tr:nth-child(odd) {
        background-color: #c9e5ec !important
    }
    .plane_table2 /deep/ .el-table__row {
        background: #1439391c !important;
        color: #46d4ff;
    }
</style>
