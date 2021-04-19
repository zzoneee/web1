<template>
    <div id="rc">
        <div class="plane_table">
            <el-table
                    :data="tableData"
                    height="520"
                    border
                    id="tb"
                    :header-cell-style="tableHeaderColor"
                    style="width: 100%">
                <el-table-column align='center'
                                 prop="college"
                                 label="学院"
                                 width="150">
                </el-table-column>
                <el-table-column align='center'
                                 prop="class_ID"
                                 label="班级"
                                 width="130">
                </el-table-column>
                <el-table-column align='center'
                                 prop="stu_num"
                                 label="学号"
                                 width="140">
                </el-table-column>
                <el-table-column align='center'
                                 prop="stu_name"
                                 label="姓名"
                                 width="130">
                </el-table-column>
                <el-table-column align='center'
                                 prop="group"
                                 label="团队"
                                 width="160">
                </el-table-column>
                <el-table-column align='center'
                                 prop="role"
                                 label="承担角色"
                                 width="100">
                </el-table-column>
                <el-table-column align='center'
                                 prop="report"
                                 label="实验报告">
                    <template slot-scope="scope">
                        <el-button size="mini" class="download">查看实验报告</el-button>
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
                tableData: []
            }
        },
        created() {
            // let _this=this;
            this.$axios({
                method: 'get',
                url: "/api/teacher/studentMessageReport",
                data:{userId:window.localStorage['userId']}
            }).then(res=> {
                if(res.status == 200){
                    this.tableData=res.data.data;
                    // this.tableData.forEach(item=>{
                    //     if(item['system_score']==-1){
                    //         item['system_score']='未批改'
                    //     }
                    //     if(item['teacher_score']==-1){
                    //         item['teacher_score']='未批改'
                    //     }
                    // })
                }
            }).catch( error =>{
                console.log(error);
            });
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
        /* margin-left: 15%; */
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
        /* background-color: transparent !important; */
    }
    .plane_table /deep/ tr, .plane_table /deep/ th, .plane_table /deep/ td {
        background: #5692ca1c !important;
        color:#095b74;
        border-bottom: 0;
    }

    .plane_table /deep/  .el-table tbody tr:nth-child(odd) {
        background-color: #c9e5ec !important
    }
    /* .plane_table /deep/ .el-table__row {
        background: #1439391c !important;
        color: #46d4ff;
    } */
</style>