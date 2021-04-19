<template>
    <div class="noGroupContainer">
        <span class="title">尚未加入团队，请选择以下团队加入或创建新团队</span>
        <el-button type="primary" class="createNewGroup" @click="createNewGroup">创建新团队</el-button>
        <div class="groupList">
            <vue-scroll :ops="ops" style="width:100%;height:100%">
                <li v-for="i in groupNum">
                    <el-card class="msgCard" shadow="hover">
                        <div slot="header" class="clearfix">
                            <span class="msgCardHeader">{{ groupList[i - 1].name }}</span>
                            <el-popconfirm title="是否加入该团队？" @confirm="joinGroup(groupList[i - 1].name)">
                                <el-button slot="reference" style="float: right" type="primary" icon="el-icon-plus" circle size="mini"></el-button>
                            </el-popconfirm>
                        </div>
                        <div class="msgText">
                            <p>团队人数： {{ groupList[i - 1].num }}</p>
                        </div>
                    </el-card>
                </li>
            </vue-scroll>
        </div>

        <el-dialog customClass="createGroupDialog" title="创建团队" :visible.sync="dialogFormVisible"  @closed="handleClose" :append-to-body="true">
            <el-form :model="form" :rules="rules" ref="ruleForm">

                <el-form-item label="团队名称" :label-width="formLabelWidth" prop="groupName">
                    <el-input v-model="form.groupName" autocomplete="off" class="createGroupDiagInput"></el-input>
                </el-form-item>
                
            </el-form>

            <div slot="footer" class="dialog-footer">
                <el-button @click="dialogFormVisible = false">取消</el-button>
                <el-button type="primary" @click="handleSave">确定</el-button>
            </div>
        </el-dialog>

    </div>
</template>

<script>
    import axios from 'axios'
    export function get_groupListMsg() {
        return axios({
            method: 'get',
            url: "/api/user/groupListMsg",
            headers: {'Authorization': window.localStorage['Authorization']}
        })
    }
    export function post_joinGroup(groupName) {
        return axios({
            method: 'post',
            url: "/api/user/joinGroup",
            headers: {'Authorization': window.localStorage['Authorization']},
            data: {'groupName': groupName}
        })
    }
    export function get_groupNameExist(groupName) {
        return axios({
            method: 'get',
            url: "/api/user/groupNameExist",
            headers: {'Authorization': window.localStorage['Authorization']},
            params: {'groupName': groupName}
        })
    }
    export function post_createGroup(groupName) {
        return axios({
            method: 'post',
            url: "/api/user/createGroup",
            headers: {'Authorization': window.localStorage['Authorization']},
            data: {'groupName': groupName}
        })
    }
    
    export default {
        // props: ["exNo"],
        data() {
            let validateGroupName = (rule, value, callback) => {
                if(value == ""){
                    callback(new Error('请输入团队名称'));
                }
                
                get_groupNameExist(value).then(res => {
                    if(res.data.status == 200){
                        if(!res.data.data.groupNameExist){
                            callback();
                        }
                        else{
                            callback(new Error('该团队名称已存在'));
                        }
                    }
                    else if(res.data.status == 403){
                        this.$router.replace('/stu_error');
                    }
                }).catch( error =>{
                    console.log(error);
                    callback(new Error(error));
                });
            };
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
                groupNum: 0,
                groupList: [],
                dialogFormVisible: false,
                form: {
                    groupName: '',
                },
                rules: {
                    groupName: [
                        { validator: validateGroupName, required: true, trigger: 'blur' },
                        { min: 0, max: 20, message: '长度应小于 20 个字符', trigger: 'blur' }
                    ]
                },
                formLabelWidth: '120px'
            }
        },
        created() {
            // console.log("[[[[[" + this.exNo + "*");
            get_groupListMsg().then(res => {
                if(res.data.status == 200){
                    this.groupList = res.data.data;
                    this.groupNum = this.groupList.length
                }
                else if(res.data.status == 403){
                    this.$router.replace('/stu_error')
                }
            }).catch( error =>{
                console.log(error);
            });
        },
        methods:{
            joinGroup(groupName){
                post_joinGroup(groupName).then(res => {
                    if(res.data.status == 200){
                        this.$router.go(0);
                    }
                    else if(res.data.status == 403){
                        this.$router.replace('/stu_error');
                    }
                }).catch( error =>{
                    console.log(error);
                });
            },
            createNewGroup(){
                this.dialogFormVisible = true;
            },
            handleClose () {
                this.$refs.ruleForm.resetFields();
                this.form.groupName = '';
            },
            handleSave () {
                this.$refs.ruleForm.validate((valid) => {
                    if (valid) {
                        post_createGroup(this.form.groupName).then(res => {
                            if(res.data.status == 200){
                                // this.$message.success("创建成功");
                                // this.dialogFormVisible = false;
                                // this.handleClose();
                                this.$router.go(0);
                            }
                            else if(res.data.status == 403){
                                this.$router.replace('/stu_error');
                            }
                            else{
                                this.$message.error("添加失败, "+res.data.msg);
                                return false;
                            }
                        }).catch( error =>{
                            console.log(error);
                        });
                    } else {
                        this.$message.error("创建失败");
                    }
                })
            },
        },
    }
</script>

<style scoped>
    .noGroupContainer{
        margin-top: 30px;
        height: 600px;
        width: 1000px;
        margin-left: 147px;
        color:#000;
    }
    .title{
        font-size: 25px;
        font-weight: 900;
    }
    .createNewGroup{
        /* margin-top: 20px; */
        margin-left: 43px;
    }
    .groupList{
        height: 500px;
        /* margin-left: 95px; */
        margin-top: 20px;
        width: 720px;
        box-shadow: 0 2px 12px 0 rgba(0, 0, 0, 0.1);
    }
    .msgCard{
        width: 700px;
        margin-top: 10px;
        margin-bottom: 10px;
        margin-left: 10px;
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
    .createGroupDiagInput{
        width: 300px;
    }
</style>

<style>
    .createGroupDialog{
        width:500px;
    }
</style>
