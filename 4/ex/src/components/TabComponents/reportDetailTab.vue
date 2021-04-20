<template>
    <div id="rc">
        <div class="plane_table">
            <el-table
                    :data="tableData"
                    height="520"
                    border
                    id="tb"
                    style="width: 100%">
                <!-- <el-table-column align='center'
                                 prop="ex_ID"
                                 label="实验报告ID"
                                 width="120">
                </el-table-column> -->
                <el-table-column align='center'
                                 prop="ex_Date"
                                 label="日期"
                                 width="150">
                </el-table-column>
                <el-table-column align='center'
                                 prop="ex_name"
                                 label="实验名称"
                                 width="235">
                </el-table-column>
                <el-table-column align='center'
                                 prop="system_score"
                                 label="系统评分"
                                 width="120">
                </el-table-column>
                <el-table-column align='center'
                                 prop="teacher_score"
                                 label="教师评分"
                                 width="120">
                </el-table-column>
                <el-table-column align='center'
                                 prop="hp_score"
                                 label="团队互评平均分"
                                 width="160">
                </el-table-column>
                <el-table-column align='center'
                                 prop="address"
                                 label="实验报告">
                    <template slot-scope="scope">
                        <el-button size="mini" class="download" @click="downLoadReport(scope.$index, tableData)">下载</el-button>
                        <el-button size="mini" type="danger" @click="deleteReport(scope.$index, tableData)">删除</el-button>
                    </template>
                </el-table-column>
            </el-table>

            <!-- <el-button type="primary" @click="submitReport" class="submitReport">提交实验报告</el-button> -->

            <el-dialog customClass="createGroupDialog" title="提交实验报告" :visible.sync="dialogFormVisible"  @closed="handleClose" :append-to-body="true">
                <el-form :model="form" :rules="rules" ref="ruleForm">
                    
                    <el-form-item label="实验名称" :label-width="formLabelWidth" prop="exName">
                        <!-- <el-input :disabled="true" v-model="form.exName" autocomplete="off"></el-input> -->
                        <el-select v-model="PostOptionsValue" placeholder=""  @change="PostOptionsChange(PostOptionsValue)">
                            <el-option
                                v-for="item in PostOptions"
                                :key="item.id"
                                :label="item.name"
                                :value="item.id">
                            </el-option>
                        </el-select>
                    </el-form-item>
                    <el-form-item label="团队名称" :label-width="formLabelWidth" prop="groupName">
                        <el-input :disabled="true" v-model="form.groupName" autocomplete="off"></el-input>
                    </el-form-item>
                    <el-form-item label="团队成员信息" :label-width="formLabelWidth" prop="groupNumberMsg">
                        <el-input :disabled="true" v-model="form.groupNumberMsg" autocomplete="off"></el-input>
                    </el-form-item>
                    <el-form-item label="实验目的（要求）" :label-width="formLabelWidth" prop="exPurpose">
                        <el-input :disabled="true" v-model="form.exPurpose" autocomplete="off"></el-input>
                    </el-form-item>
                    <el-form-item label="实验主要步骤" :label-width="formLabelWidth" prop="exSteps">
                        <el-input :disabled="true" v-model="form.exSteps" autocomplete="off"></el-input>
                    </el-form-item>
                    <el-form-item label="实验结果" :label-width="formLabelWidth" prop="exResult" class="exMsg2">
                        <!-- <el-input v-model="form.exResult" autocomplete="off" class="createGroupDiagInput"></el-input> -->
                        <el-input type="textarea" :rows="2" maxlength="500" show-word-limit v-model="form.exResult" autocomplete="off" class="createGroupDiagInput"></el-input>
                    </el-form-item>
                    <el-form-item label="系统评分" :label-width="formLabelWidth" prop="systemScore">
                        <el-input :disabled="true" v-model="form.systemScore" autocomplete="off"></el-input>
                    </el-form-item>
                    <el-form-item label="实验心得" :label-width="formLabelWidth" prop="exExperience" class="exMsg2">
                        <!-- <el-input v-model="form.exExperience" autocomplete="off" class="createGroupDiagInput"></el-input> -->
                        <el-input type="textarea" :rows="2" maxlength="500" show-word-limit v-model="form.exExperience" autocomplete="off" class="createGroupDiagInput"></el-input>
                    </el-form-item>
                    <el-form-item label="实验日期" :label-width="formLabelWidth" prop="exDate">
                        <el-input :disabled="true" v-model="form.exDate" autocomplete="off"></el-input>
                    </el-form-item>
                    
                </el-form>

                <div slot="footer" class="dialog-footer">
                    <el-button @click="dialogFormVisible = false">取消</el-button>
                    <el-button type="primary" @click="handleSave">确定</el-button>
                </div>
            </el-dialog>
        </div>
    </div>
</template>

<script>
    import axios from 'axios'
    export function post_createReport(exResult, exExperience) {
        return axios({
            method: 'post',
            url: "/api/report/createReport",
            headers: {'Authorization': window.localStorage['Authorization']},
            data:{'exResult':exResult, 'exExperience':exExperience}
        })
    }
    export function get_exLists() {
        return axios({
            method: 'get',
            url: "/api/experiment/exLists",
            headers: {'Authorization': window.localStorage['Authorization']}
        })
    }
    export default {

        data() {
            return {
                tableData: [],

                dialogFormVisible: false,
                form: {
                    exName: '无人机集群编队三维模拟实验',
                    groupName: 'group2',
                    groupNumberMsg: '张三/计算机171/2020003/项目统筹   王五/计算机174/2020012/算法研究',
                    exPurpose: '按照要求完成无人机编队及灯光设计。',
                    exSteps: '1.H型编队设计；\n2.H型变换Z型路线设计；\n3.夜间灯光设计；\n4.N型变换Z型。',
                    exResult: '',
                    systemScore: '87',
                    exExperience: '',
                    exDate: '2021-3-10',
                },
                rules: {
                    exResult: [
                        { message: '请输入实验结果', required: true, trigger: 'blur' },
                        { min: 0, max: 500, message: '长度应小于 500 个字符', trigger: 'blur' }
                    ],
                    exExperience: [
                        { message: '请输入实验心得', required: true, trigger: 'blur' },
                        { min: 0, max: 500, message: '长度应小于 500 个字符', trigger: 'blur' }
                    ],
                },
                formLabelWidth: '120px',

                PostOptions: [],
                PostOptionsValue: '',
            }
        },
        created() {
            this.getReportList();
            // 获取实验列表
            get_exLists().then(res => {
                // console.log(res.data.data);
                if(res.data.status == 200){
                    this.PostOptions = res.data.data;
                    this.PostOptionsValue = this.PostOptions[0].id;
                }
                else if(res.data.status == 403){
                    this.$router.replace('/tea_error')
                }
            }).catch( error =>{
                console.log(error);
            });
        },
        methods:{
            PostOptionsChange(PostOptionsValue){
                // console.log(PostOptionsValue);
                // this.getGroupList(this.PostOptionsValue);
            },
            handleClose () {
                this.$refs.ruleForm.resetFields();
                this.form.exResult = '';
                this.form.exExperience = '';
            },
            handleSave () {
                this.$refs.ruleForm.validate((valid) => {
                    if (valid) {
                        this.createReport(this.form.exResult, this.form.exExperience);
                    } else {
                        this.$message.error("提交失败");
                    }
                })
            },
            submitReport(){
                this.dialogFormVisible = true;
            },
            createReport(exResult, exExperience){
                post_createReport(exResult, exExperience).then(res => {
                    if(res.data.status == 200){
                        this.getReportList(); // 获取实验报告列表
                        this.dialogFormVisible = false;
                        this.$message.success("提交成功");
                    }
                    else if(res.data.status == 403){
                        this.$router.replace('/tea_error');
                    }
                    else{
                        this.$message.error("提交失败");
                    }
                }).catch( error =>{
                    console.log(error);
                });
            },
            getReportList(){
                this.$axios({
                    method: 'post',
                    url: "/api/report/reportList",
                    headers: {'Authorization': window.localStorage['Authorization']},
                    data:{userId:window.localStorage['userId']}
                }).then(res=> {
                    // console.log(res.data.err);
                    if(res.data.status == 200){
                        this.tableData=res.data.data;
                        this.tableData.forEach(item=>{
                            if(item['system_score']==-1){
                                item['system_score']='暂无评分'
                            }
                            if(item['teacher_score']==-1){
                                item['teacher_score']='暂无评分'
                            }
                            if(item['hp_score']==-1){
                                item['hp_score']='暂无评分'
                            }
                        })
                    }
                    else if(res.data.status == 403){
                        this.$router.replace('/stu_error')
                    }
                }).catch( error =>{
                    console.log(error);
                });
            },
            // download(){
            //     window.open('http://127.0.0.1:8000/downLoad/report/report1.docx');
            // },
            downLoadReport(index, row) {
                this.$axios({
                    method: 'get',
                    url: "/api/teacher/getReportUrl",
                    params:{id:row[index].ex_ID}
                }).then(res=> {
                    if(res.data.status == 200){
                        // let url = 'http://47.111.151.229/downLoad/report/' + res.data.data;
                        let url = 'http://127.0.0.1:8000/downLoad/report/' + res.data.data;
                        window.open(url);
                    }
                }).catch( error =>{
                    console.log(error);
                });
            },
            deleteReport(index, row) {
                this.$axios({
                    method: 'post',
                    url: "/api/teacher/deleteReport",
                    data:{id:row[index].ex_ID}
                }).then(res=> {
                    // console.log(row[index].ex_ID);
                    if(res.data.status == 200){
                        this.getReportList();
                        this.$message.success("删除成功");
                    }
                }).catch( error =>{
                    console.log(error);
                });
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
    .plane_table /deep/ tr, .plane_table /deep/ th, .plane_table /deep/ td {
        background: #5692ca1c !important;
        color:#095b74;
        font-weight: bold;
        font-size: 17px;
        border-bottom: 0;
    }

    .plane_table /deep/  .el-table tbody tr:nth-child(odd) {
        background-color: #c9e5ec !important
    }
    .plane_table /deep/ .el-table__row {
        background: #1439391c !important;
        color: #46d4ff;
    }

    .submitReport{
        margin-top: 50px;
    }

    .exMsg2>>>.el-textarea__inner {
        /* border: 0; */
        resize: none;/* 这个是去掉 textarea 下面拉伸的那个标志，如下图 */
        height: 150px;
        overflow-y: auto;
    }
</style>
