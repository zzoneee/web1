<template>
    <div class="systemNotificationContainer">
        <div class="systemNotificationTop">
            <el-tag effect="plain" type="success" class="systemNotificationTag">公告</el-tag>
            <!-- <p class="systemNotificationTag">系统通知</p> -->
            <el-button type="primary" size="small" round class="releaseNotification" @click="releaseNotification">发布公告</el-button>
        </div>
        <el-divider></el-divider>
        <el-scrollbar :ops="ops" style="width:866px;height:100%;margin-left:20px;">
            <!-- <ul> -->
                <li v-for="item in noticeLists">
                    <!-- <el-badge value="置顶"> -->
                        <el-card class="msgCard" shadow="hover">
                            <div slot="header" class="clearfix">
                                <el-tag type="success" v-if="item.new==1">new</el-tag>
                                <el-tag type="danger" v-if="item.top==1">置顶</el-tag>
                                <span class="msgCardHeader">{{ item.title }}</span>
                                <span class="publishUser">发布人：{{item.user_id}}</span>
                                <span class="publishTime">发布时间：{{item.time}}</span>

                                <el-popconfirm title="是否删除？" @confirm="deleteNotice(item.id)">
                                    <el-button slot="reference" style="float: right" type="danger" icon="el-icon-delete" circle size="mini"></el-button>
                                </el-popconfirm>
                                
                                <el-popconfirm title="是否置顶？" @confirm="topNotice(item.id)" v-if="item.top==0">
                                    <el-button slot="reference" style="float: right; margin-right: 10px" icon="el-icon-top" type="primary" circle size="mini"></el-button>
                                </el-popconfirm>

                                <el-popconfirm title="是否取消置顶？" @confirm="noTopNotice(item.id)" v-if="item.top==1">
                                    <el-button slot="reference" style="float: right; margin-right: 10px" icon="el-icon-bottom" type="warning" circle size="mini"></el-button>
                                </el-popconfirm>

                                <el-popconfirm title="是否编辑？" @confirm="editNotice(item.id, item.title, item.message)">
                                    <el-button slot="reference" style="float: right; margin-right: 10px" icon="el-icon-edit" type="success" circle size="mini"></el-button>
                                </el-popconfirm>
                            </div>
                            <div class="msgText">
                                <p>{{ item.message }}</p>
                            </div>
                        </el-card>
                    <!-- </el-badge> -->
                </li>
            <!-- </ul> -->
        </el-scrollbar>

        <el-dialog customClass="releaseDialog" title="发布公告" :visible.sync="dialogFormVisible"  @closed="handleClose" :append-to-body="true">
            <el-form :model="form" :rules="rules" ref="ruleForm">

                <el-form-item label="标题" :label-width="formLabelWidth" prop="title">
                    <el-input v-model="form.title" autocomplete="off" class="releaseInput"></el-input>
                </el-form-item>
                <el-form-item label="公告内容" :label-width="formLabelWidth" prop="message" class="releaseMsg">
                    <el-input type="textarea" :rows="2" maxlength="500" show-word-limit v-model="form.message" autocomplete="off" class="releaseTextArea"></el-input>
                </el-form-item>
                <el-form-item label="置顶" :label-width="formLabelWidth" prop="top">
                    <el-switch v-model="form.top"></el-switch>
                </el-form-item>
                
            </el-form>

            <div slot="footer" class="dialog-footer">
                <el-button @click="dialogFormVisible = false">取消</el-button>
                <el-button type="primary" @click="handleSave">确定</el-button>
            </div>
        </el-dialog>

        <el-dialog customClass="editDialog" title="编辑公告" :visible.sync="editVisible"  @closed="editClose" :append-to-body="true">
            <el-form :model="editForm" :rules="editRules" ref="editRuleForm">

                <el-form-item label="标题" :label-width="formLabelWidth" prop="title">
                    <el-input v-model="editForm.title" autocomplete="off" class="releaseInput"></el-input>
                </el-form-item>
                <el-form-item label="公告内容" :label-width="formLabelWidth" prop="message" class="releaseMsg">
                    <el-input type="textarea" :rows="2" maxlength="500" show-word-limit v-model="editForm.message" autocomplete="off" class="releaseTextArea"></el-input>
                </el-form-item>
                
            </el-form>

            <div slot="footer" class="dialog-footer">
                <el-button @click="editVisible = false">取消</el-button>
                <el-button type="primary" @click="editSave">确定</el-button>
            </div>
        </el-dialog>

    </div>
</template>

<script>
    import axios from 'axios'
    export function post_releaseNotice(title, message, top) {
        return axios({
            method: 'post',
            url: "/api/notice/releaseNotice",
            headers: {'Authorization': window.localStorage['tea_Authorization']},
            data:{title: title, message: message, top: top}
        })
    }
    export function get_noticeLists() {
        return axios({
            method: 'get',
            url: "/api/notice/noticeLists",
            headers: {'Authorization': window.localStorage['tea_Authorization']}
        })
    }
    export function post_deleteNotice(id) {
        return axios({
            method: 'post',
            url: "/api/notice/deleteNotice",
            headers: {'Authorization': window.localStorage['tea_Authorization']},
            data: {id: id}
        })
    }
    export function post_topNotice(id) {
        return axios({
            method: 'post',
            url: "/api/notice/topNotice",
            headers: {'Authorization': window.localStorage['tea_Authorization']},
            data: {id: id}
        })
    }
    export function post_noTopNotice(id) {
        return axios({
            method: 'post',
            url: "/api/notice/noTopNotice",
            headers: {'Authorization': window.localStorage['tea_Authorization']},
            data: {id: id}
        })
    }
    export function post_editNotice(id, title, message) {
        return axios({
            method: 'post',
            url: "/api/notice/editNotice",
            headers: {'Authorization': window.localStorage['tea_Authorization']},
            data:{id: id, title: title, message: message}
        })
    }
    export default {
        data() {
            return {
                ops: {
                    vuescroll: {},
                    scrollPanel: {},
                    rail: {
                        keepShow: true
                    },
                    bar: {
                        hoverStyle: true,
                        onlyShowBarOnScroll: false, //是否只有滚动的时候才显示滚动条
                        background: "#000",//滚动条颜色
                        opacity: 0.2,//滚动条透明度
                        "overflow-x": "hidden"
                    }
                },
                dialogFormVisible: false,
                form: {
                    title: '',
                    message: '',
                    top: false
                },
                rules: {
                    title: [
                        { required: true, message: '请输入标题', trigger: 'blur' },
                        { min: 1, max: 30, message: '长度应小于 30 个字符', trigger: 'blur' }
                    ],
                    message: [
                        { required: true,  message: '请输入公告内容', trigger: 'blur' },
                        { min: 1, max: 500, message: '长度应小于 500 个字符', trigger: 'blur' }
                    ],
                },
                formLabelWidth: '120px',
                noticeLists: [],
                editVisible: false,
                editForm: {
                    title: '',
                    message: ''
                },
                editRules: {
                    title: [
                        { required: true, message: '请输入标题', trigger: 'blur' },
                        { min: 1, max: 30, message: '长度应小于 30 个字符', trigger: 'blur' }
                    ],
                    message: [
                        { required: true,  message: '请输入公告内容', trigger: 'blur' },
                        { min: 1, max: 500, message: '长度应小于 500 个字符', trigger: 'blur' }
                    ],
                },
                editID: '',
            }
        },
        created() {
            this.getNoticeLists();
        },
        methods:{
            getNoticeLists(){
                get_noticeLists().then(res => {
                    // console.log(res.data.status);
                    if(res.data.status == 200){
                        // console.log(res.data.data);
                        this.noticeLists = res.data.data
                    }
                    else if(res.data.status == 403){
                        this.$router.replace('/tea_error');
                    }
                    else{
                        console.log(res.data.err);
                    }
                }).catch( error =>{
                    console.log(error);
                });
            },
            releaseNotification(){
                this.dialogFormVisible = true;
            },
            handleClose () {
                this.$refs.ruleForm.resetFields();
                this.form.title = '';
                this.form.message = '';
                // this.editRoleForm.role = '';
            },
            handleSave () {
                this.$refs.ruleForm.validate((valid) => {
                    if (valid) {
                        post_releaseNotice(this.form.title, this.form.message, this.form.top).then(res => {
                            if(res.data.status == 200){
                                this.$message.success("发布公告成功");
                                this.dialogFormVisible = false;
                                this.getNoticeLists();
                                this.handleClose();
                                // console.log(res.data.status + " " + res.data.msg);
                            }
                            else if(res.data.status == 403){
                                this.$router.replace('/tea_error');
                            }
                            else{
                                this.$message.error("发布公告失败");
                            }
                        }).catch( error =>{
                            console.log(error);
                        });
                    } else {
                        this.$message.error("发布公告失败");
                    }
                })
            },
            deleteNotice(id){
                post_deleteNotice(id).then(res => {
                    if(res.data.status == 200){
                        this.$message.success("删除公告成功");
                        this.getNoticeLists();
                    }
                    else if(res.data.status == 403){
                        this.$router.replace('/tea_error');
                    }
                    else{
                        this.$message.error("删除公告失败");
                    }
                }).catch( error =>{
                    console.log(error);
                });
            },
            topNotice(id){
                post_topNotice(id).then(res => {
                    if(res.data.status == 200){
                        this.$message.success("置顶公告成功");
                        this.getNoticeLists();
                    }
                    else if(res.data.status == 403){
                        this.$router.replace('/tea_error');
                    }
                    else{
                        this.$message.error("置顶公告失败");
                    }
                }).catch( error =>{
                    console.log(error);
                });
            },
            noTopNotice(id){
                post_noTopNotice(id).then(res => {
                    if(res.data.status == 200){
                        this.$message.success("取消置顶成功");
                        this.getNoticeLists();
                    }
                    else if(res.data.status == 403){
                        this.$router.replace('/tea_error');
                    }
                    else{
                        this.$message.error("取消置顶失败");
                    }
                }).catch( error =>{
                    console.log(error);
                });
            },
            editNotice(id, title, message){
                this.editID = id;
                this.editForm.title = title;
                this.editForm.message = message;
                this.editVisible = true;
            },
            editClose () {
                this.$refs.editRuleForm.resetFields();
                this.editForm.title = '';
                this.editForm.message = '';
            },
            editSave () {
                this.$refs.editRuleForm.validate((valid) => {
                    if (valid) {
                        post_editNotice(this.editID, this.editForm.title, this.editForm.message).then(res => {
                            if(res.data.status == 200){
                                this.$message.success("编辑公告成功");
                                this.editVisible = false;
                                this.getNoticeLists();
                                this.editClose();
                                // console.log(res.data.status + " " + res.data.msg);
                            }
                            else if(res.data.status == 403){
                                this.$router.replace('/tea_error');
                            }
                            else{
                                this.$message.error("编辑公告失败");
                            }
                        }).catch( error =>{
                            console.log(error);
                        });
                    } else {
                        this.$message.error("编辑公告失败");
                    }
                })
            },
        },
    }
</script>

<style scoped>
    
    .systemNotificationContainer{
        height: 520px;
        /* margin-left: 20px; */
    }
    .systemNotificationTop{
        height: 18px;
    }
    .systemNotificationTag{
        margin-top: 5px;
        margin-left: 20px;
    }
    .releaseNotification{
        float: right;
        margin-right: 15px;
        margin-top: 5px;
    }
    .msgCard{
        width: 850px;
        margin-top: 5px;
        /* margin-bottom: 10px; */
    }
    .msgCardHeader{
        font-size: 18px;
        font-weight: 800;
    }
    .clearfix:before,
    .clearfix:after {
        display: table;
        content: "";
    }
    .clearfix:after {
        clear: both
    }
    .msgText{
        width: 100%;  
        height: auto;  
        word-wrap:break-word;  
        word-break:break-all;  
        overflow: hidden;  
        font-size: 14px;
        color: #323232;
        /* font-family: "微软雅黑"; */
    }
    /* 滚动条位置 */
    /deep/.__bar-is-vertical {
        right: -1px !important;
    }
    /* 隐藏横向滚动条 */
    /deep/.__bar-is-horizontal {
        display: none !important;
    }

    .releaseMsg>>>.el-textarea__inner {
        /* border: 0; */
        resize: none;/* 这个是去掉 textarea 下面拉伸的那个标志，如下图 */
        height: 300px;
        overflow-y: auto;
    }

    .publishUser{
        margin-left: 10px;
        font-size: 10px;
    }
    .publishTime{
        margin-left: 10px;
        font-size: 10px;
    }
    .systemNotificationContainer>>>.el-scrollbar__wrap{
        overflow-x: hidden;
    }
</style>
