<template>
    <div class="menu">
        <el-row>
            <el-col :span="17">
                <div class="menuBtnList">
                    <div class="menuBtnListCon">
                        <ul>
                            <li v-for="(list,index) in cur_exLists">
                                <!-- <el-button type="primary" size="small" class="exDelete" @click="goToEx(list.url)" plain>进入实验</el-button> -->
                                <el-button type="primary" size="small" class="exDelete" @click="seeIntroduction(list.introduction, list.introductionUrl)" plain>查看简介</el-button>
                                <!-- <el-button type="danger" size="small" class="exDelete" plain>删除实验</el-button> -->
                                <el-popconfirm title="是否删除？" @confirm="deleteEx(list.id)">
                                    <el-button slot="reference" style="float: right; margin-top: 30px;" type="danger" icon="el-icon-delete" circle size="mini"></el-button>
                                </el-popconfirm>
                                <span class="menuBtnListP">{{ list.name }}</span>
                                <el-divider></el-divider>
                            </li>
                        </ul>

                        <nav aria-label="page_navigation" class="page-bar">
                            <el-pagination background layout="prev, pager, next" :total="numTotal" :page-size="pageSize"
                            @prev-click="pre_page()"
                            @next-click="next_page()"
                            @current-change="curPage"
                            :hide-on-single-page="numTotal<=pageSize"></el-pagination>
                        </nav>
                        
                    </div>
                </div>
            </el-col>
            <el-col :span="7">
                <el-button type="primary" class="exAdd" @click="addEx">添加实验</el-button>
            </el-col>
        </el-row>

        <el-dialog customClass="createEx" title="添加实验" :visible.sync="dialogFormVisible"  @closed="handleClose" :append-to-body="true">
            <el-form :model="form" :rules="rules" ref="ruleForm">

                <el-form-item label="实验名称" :label-width="formLabelWidth" prop="name">
                    <el-input v-model="form.name" autocomplete="off" class="createGroupDiagInput"></el-input>
                </el-form-item>
                <el-form-item label="实验链接" :label-width="formLabelWidth" prop="url">
                    <el-input v-model="form.url" autocomplete="off" class="createGroupDiagInput"></el-input>
                </el-form-item>
                <el-form-item label="实验简介" :label-width="formLabelWidth" prop="introduction">
                    <el-input type="textarea" :rows="2" maxlength="2000" show-word-limit v-model="form.introduction" autocomplete="off" class="createGroupDiagInput"></el-input>
                </el-form-item>
                <el-form-item label="实验简介链接" :label-width="formLabelWidth" prop="introductionUrl">
                    <el-input v-model="form.introductionUrl" autocomplete="off" class="createGroupDiagInput"></el-input>
                </el-form-item>
                
            </el-form>

            <div slot="footer" class="dialog-footer">
                <el-button @click="dialogFormVisible = false">取消</el-button>
                <el-button type="primary" @click="handleSave">确定</el-button>
            </div>
        </el-dialog>

        <el-dialog customClass="releaseDialog" title="实验简介" :visible.sync="exiVisible"  @closed="exihandleClose" :append-to-body="true">
            <p v-if="introduction!=null&&introduction!=''">{{ introduction }}</p>
            <!-- <a href=introductionUrl></a> -->
            <el-link v-if="introductionUrl!=null&&introductionUrl!=''" :href="introductionUrl" target="_blank" type="primary">实验简介链接</el-link>
            <p style="margin-left: 43%;" v-if="(introduction==null||introduction=='')&&(introductionUrl==null||introductionUrl=='')">无实验说明</p>
            <div slot="footer" class="dialog-footer">
                <el-button type="primary" @click="exihandleSave">确定</el-button>
            </div>
        </el-dialog>
    </div>
</template>

<script>
    import axios from 'axios'
    export function get_exLists() {
        return axios({
            method: 'get',
            url: "/api/experiment/exLists",
            headers: {'Authorization': window.localStorage['tea_Authorization']},
        })
    }
    export function post_addEx(name, url, introduction, introductionUrl) {
        return axios({
            method: 'post',
            url: "/api/experiment/addEx",
            headers: {'Authorization': window.localStorage['tea_Authorization']},
            data: {name: name, url: url, introduction: introduction, introductionUrl: introductionUrl},
        })
    }
    export function post_deleteEx(id) {
        return axios({
            method: 'post',
            url: "/api/experiment/deleteEx",
            headers: {'Authorization': window.localStorage['tea_Authorization']},
            data: {id: id},
        })
    }
    export default {
        data() {
            return {
                exLists:[],
                cur_exLists:[],
                // pageTotal:3,
                // rows:1,
                numTotal:0,
                pageNo:1,
                pageSize:3,

                dialogFormVisible: false,
                form: {
                    name: '',
                    url: '',
                    introduction: '',
                    introductionUrl: '',
                },
                rules: {
                    name: [
                        { message: '请输入实验名称', required: true, trigger: 'blur' },
                        { min: 0, max: 20, message: '长度应小于 20 个字符', trigger: 'blur' }
                    ],
                    url: [
                        { message: '请输入url', required: true, trigger: 'blur' },
                        { min: 0, max: 255, message: '长度应小于 255 个字符', trigger: 'blur' }
                    ],
                },
                formLabelWidth: '120px',

                exiVisible: false,
                introduction: '',
                introductionUrl: '',
            }
        },
        created() {
            // 获取实验列表
            this.getExLists();
        },
        methods:{
            // 获取实验列表
            getExLists(){
                get_exLists().then(res => {
                    // console.log(res.data.err);
                    if(res.data.status == 200){
                        this.exLists = res.data.data;
                        this.numTotal = this.exLists.length;
                        // this.pageNo = 1;
                        this.getlist(this.pageNo);
                    }
                    else if(res.data.status == 403){
                        this.$router.replace('/tea_error')
                    }
                }).catch( error =>{
                    console.log(error);
                });
            },
            getlist(index = -1){
                if(index != -1){
                    this.pageNo = index;
                }
                this.cur_exLists = [];
                for(var a in this.exLists){
                    if(a >= (this.pageNo - 1) * this.pageSize && a < this.pageNo * this.pageSize){
                        this.cur_exLists.push(this.exLists[a]);
                    }
                }
                // console.log(this.cur_exLists);
            },
            pre_page(){
                if(this.pageNo > 1){
                    this.pageNo--;
                    this.getlist(this.pageNo);
                }
            },
            next_page(){
                if(this.pageNo < this.pageTotal){
                    this.pageNo++;
                    this.getlist(this.pageNo);
                }
            },
            curPage(index){
                this.pageNo = index;
                this.getlist(index);
            },
            handleClose () {
                this.$refs.ruleForm.resetFields();
                this.form.exName = '';
                this.form.url = '';
            },
            handleSave () {
                this.$refs.ruleForm.validate((valid) => {
                    if (valid) {
                        post_addEx(this.form.name, this.form.url, this.form.introduction, this.form.introductionUrl).then(res => {
                            if(res.data.status == 200){
                                this.getExLists();
                                this.dialogFormVisible = false;

                                this.$message.success("添加成功");
                            }
                            else if(res.data.status == 403){
                                this.$router.replace('/tea_error');
                            }
                            else{
                                this.$message.error("添加失败, "+res.data.msg);
                                return false;
                            }
                        }).catch( error =>{
                            console.log(error);
                        });
                    } else {
                        this.$message.error("添加失败");
                    }
                })
            },
            addEx(){
                this.dialogFormVisible = true;
            },
            deleteEx(id){
                post_deleteEx(id).then(res => {
                    if(res.data.status == 200){
                        if(this.numTotal % this.pageSize == 1 && this.pageNo * this.pageSize > this.numTotal - 1){
                            this.pageNo--;
                        }
                        this.getExLists();
                        this.$message.success("删除成功");
                    }
                    else if(res.data.status == 403){
                        this.$router.replace('/tea_error');
                    }
                    else{
                        this.$message.error("添加失败, "+res.data.msg);
                        return false;
                    }
                }).catch( error =>{
                    console.log(error);
                });
            },
            goToEx(url){
                window.open(url);
            },
            seeIntroduction(introduction, introductionUrl){
                this.introduction = introduction;
                this.introductionUrl = introductionUrl;
                this.exiVisible = true;
            },
            exihandleClose () {
                this.exiVisible = false;
            },
            exihandleSave () {
                this.exiVisible = false;
            },
        }
    }
</script>

<style scoped>
    .menuBtnList{
        margin-left: 311px;
        /* margin-top: 5%; */
        box-shadow: 0 2px 12px 0 rgba(43, 34, 34, 0.1);
        background-color: #fff;
        opacity: 0.91;
        height: 500px;
        width: 800px;
    }
    
    .menuBtnListCon{
        /* margin-left: 23px; */
        /* margin-top: 50px; */
        margin: 50px;
    }

    .menuBtnListP{
        /* font-size: 20px;
        font-weight: 600;
        text-align:center;
        margin-right: 20px;
        color: rgb(69, 74, 73); */
        font-size: 20px;
        font-weight: 600;
        /* margin-top: 50px; */
        /* margin-bottom: 20px; */
        margin-left: 31px;
    }
    .page-bar{
        margin-top: 43px;
    }

    .menuBtnListRight{
        margin-left: 100px;
        margin-top: 55px;
        box-shadow: 0 2px 12px 0 rgba(43, 34, 34, 0.1);
        background-color: #fff;
        opacity: 0.91;
        height: 600px;
        width: 200px;
    }
    .ex_name{
        font-size: 23px;
        font-weight: 600;
        /* text-align: center; */
        margin-top: 71px;
        color: #87D2FC;
        margin-left: 40px;
    }
    .ex_name_exit{
        font-size: 23px;
        font-weight: 600;
        /* text-align: center; */
        margin-top: 71px;
        /* color: rgb(255, 146, 146); */
        margin-left: 33px;
    }
    .exDelete{
        /* float: right; */
        margin-top: 30px;
        margin-bottom: 20px;
    }
    .exAdd{
        margin-left: 70px;
        margin-top: 55px;
    }

    .createGroupDiagInput>>>.el-textarea__inner {
        /* border: 0; */
        resize: none;/* 这个是去掉 textarea 下面拉伸的那个标志，如下图 */
        height: 150px;
        overflow-y: auto;
    }
</style>

<style>
    .createEx{
        width:700px;
    }
</style>
