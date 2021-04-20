<template>
    <div class="info">
        <el-form :inline="true">

            <p>基本资料</p>
            <el-form-item label="登录账号" prop="username" class="ps0">
                <button class="user_msg" type="input" disabled="disabled">{{group.username}}</button>
            </el-form-item>
            <el-form-item label="团队名称" prop="username" class="ps0">
                <button class="user_msg" type="input" disabled="disabled">{{group.realName}}</button>
            </el-form-item>
            <!-- <el-form-item label="团队名称" prop="realName" class="ps0">
                <el-input :disabled="true" v-model="group.realName"></el-input>
            </el-form-item> -->

            <ul>
                <li v-for="(users_list,index) in cur_users_lists">
                    <span class="people">队员{{index + 1 + (pageNo - 1) * pageSize}}</span>
                    <el-button type="success" class="editRole" size="small" @click="editRole(users_list.fields.stu_num)">修改承担角色</el-button>
                    <el-col>
                        <el-form-item label="队员姓名" prop="name1" class="ps0">
                                <button class="user_msg" type="input" disabled="disabled">{{users_list.fields.name}}</button>
                        </el-form-item>

                        <el-form-item label="队员学号" prop="name1" class="ps0">
                            <!-- <div class = "user_msg">{{users_list.pk}}</div> -->
                            <button class="user_msg" type="input" disabled="disabled">{{users_list.fields.stu_num}}</button>
                        </el-form-item>

                        <el-form-item label="承担角色" prop="name1" class="ps0">
                            <!-- <div class = "user_msg">{{users_list.fields.role}}</div> -->
                            <button class="user_msg" type="input" disabled="disabled">{{users_list.fields.role}}</button>
                        </el-form-item>
                    </el-col>
                    <el-col>
                        <el-form-item label="队员学院" prop="name1" class="ps0">
                            <!-- <div class = "user_msg">{{users_list.fields.name}}</div> -->
                            <button class="user_msg" type="input" disabled="disabled">{{users_list.fields.college}}</button>
                        </el-form-item>

                        <el-form-item label="队员班级" prop="name1" class="ps0">
                            <!-- <div class = "user_msg">{{users_list.pk}}</div> -->
                            <button class="user_msg" type="input" disabled="disabled">{{users_list.fields.class_name}}</button>
                        </el-form-item>

                        <el-form-item label="手机号码" prop="name1" class="ps0">
                            <!-- <div class = "user_msg">{{users_list.fields.role}}</div> -->
                            <button class="user_msg" type="input" disabled="disabled">{{users_list.fields.phone}}</button>
                        </el-form-item>
                    </el-col>
                </li>
            </ul>

            <div class="settingGroupInfoBottom">
                <el-row :gutter="0">
                    <el-col :span="6" :offset="0">
                        <el-button type="primary" class="addStu" @click="addStu()" icon="el-icon-circle-plus-outline">添加新队员</el-button>
                    </el-col>
                    <el-col :span="6">
                        <el-button type="danger" class="quitTeam" @click="quitTeam()" icon="el-icon-remove-outline">退出团队</el-button>
                    </el-col>
                    <el-col :span="12">
                        <!-- <nav aria-label="page_navigation" class="page-bar">
                            <ul class="pagination">
                                <li :class="pageNO<=1?'disabled':''" @click="pre_page()">
                                    <a aria-label="previous">
                                        <span aria-hidden="true">&laquo;</span>
                                    </a>
                                </li>
                                <li :class="index==pageNO?'active':''" v-for="index in pageTotal" @click="curPage(index)">
                                    <a :class="qq">{{index}}</a>
                                </li> 
                                <li :class="pageNO>=pageTotal?'disabled':''" @click="next_page()">
                                    <a aria-label="next">
                                        <span aria-hidden="true">&raquo;</span>
                                    </a>
                                </li>
                            </ul>
                        </nav> -->
                        <nav aria-label="page_navigation" class="page-bar">
                            <el-pagination background layout="prev, pager, next" :total="numTotal" :page-size="pageSize"
                            @prev-click="pre_page()"
                            @next-click="next_page()"
                            @current-change="curPage"
                            :hide-on-single-page="pageTotal<=1"></el-pagination>
                        </nav>
                    </el-col>
                </el-row>
            </div>

        </el-form>

        <el-dialog customClass="addStuDialog" title="添加队员" :visible.sync="dialogFormVisible"  @closed="handleClose" :append-to-body="true">
            <el-form :model="form" :rules="rules" ref="ruleForm">

                <el-form-item label="学号" :label-width="formLabelWidth" prop="stu_num">
                    <el-input v-model="form.stu_num" autocomplete="off" class="addStuDiagInput"></el-input>
                </el-form-item>
                <el-form-item label="承担角色" :label-width="formLabelWidth" prop="role">
                    <el-input v-model="form.role" autocomplete="off" class="addStuDiagInput"></el-input>
                </el-form-item>
                
            </el-form>

            <div slot="footer" class="dialog-footer">
                <el-button @click="dialogFormVisible = false">取消</el-button>
                <el-button type="primary" @click="handleSave">确定</el-button>
            </div>
        </el-dialog>

        <el-dialog customClass="addStuDialog" title="修改承担角色" :visible.sync="editRoleVisible" @closed="handleClose" :append-to-body="true">
            <el-form :model="editRoleForm" :rules="editRoleRules" ref="ruleForm">
                <el-form-item label="承担角色" :label-width="formLabelWidth" prop="role">
                    <el-input v-model="editRoleForm.role" autocomplete="off" class="addStuDiagInput"></el-input>
                </el-form-item>
            </el-form>
            <div slot="footer" class="dialog-footer">
                <el-button @click="editRoleVisible = false">取消</el-button>
                <el-button type="primary" @click="editRoleSave">确定</el-button>
            </div>
        </el-dialog>

    </div>
</template>

<script>
    import axios from 'axios'
    export function get_addStuCheck(value) {
        return axios({
            method: 'get',
            url: "/api/user/addStuCheck",
            headers: {'Authorization': window.localStorage['Authorization']},
            params:{stuNum: value}
        })
    }
    export function post_addGroupNumber(stu_num, groupName, role) {
        return axios({
            method: 'post',
            url: "/api/user/addGroupNumber",
            headers: {'Authorization': window.localStorage['Authorization']},
            data:{stu_num: stu_num, groupName: groupName, role: role}
        })
    }
    export function post_editRole(stu_num, role) {
        return axios({
            method: 'post',
            url: "/api/user/editRole",
            headers: {'Authorization': window.localStorage['Authorization']},
            data:{stu_num: stu_num, role: role}
        })
    }
    export function post_quitTeam() {
        return axios({
            method: 'post',
            url: "/api/user/quitTeam",
            headers: {'Authorization': window.localStorage['Authorization']}
        })
    }
    export default {
        // name: "GroupInfoTab.vue",
        // inject:['reload'],
        data () {
            let validateStu_num = (rule, value, callback) => {
                if(value == ""){
                    callback(new Error('请输入学号'));
                }
                get_addStuCheck(value).then(res => {
                    if(res.data.status == 200){
                        if(res.data.data.stuStatus == 0){
                            callback();
                        }
                        else if(res.data.data.stuStatus == 1){
                            callback(new Error('学号不存在'));
                        }
                        else{
                            callback(new Error('该学生已加入团队，请添加没有加入团队的学生'));
                        }
                    }
                    else if(res.data.status == 403){
                        this.$router.replace('/stu_error');
                    }
                    else{
                        callback(new Error(res.data.msg));
                    }
                }).catch( error =>{
                    console.log(error);
                    callback(new Error(error));
                });
            };
            return {
                group:{
                    id:null,
                    name:null,
                    username:'',
                    realName:'',
                },
                user:{
                    userId:'',
                    class:'',
                    sex:1,
                    phoneNumber:'',
                    email:'',
                },
                users_lists:[],
                cur_users_lists:[],
                pageTotal:1,
                rows:1,
                numTotal:0,
                pageNo:1,
                pageSize:2,
                dialogFormVisible: false,
                form: {
                    stu_num: '',
                    role: '',
                },
                rules: {
                    stu_num: [
                        { validator: validateStu_num, required: true, trigger: 'blur' },
                        { min: 0, max: 20, message: '长度应小于 20 个字符', trigger: 'blur' }
                    ],
                    role: [
                        { min: 0, max: 20, message: '长度应小于 20 个字符', trigger: 'blur' }
                    ],
                },
                formLabelWidth: '120px',
                editRoleVisible: false,
                editRoleForm: {
                    role: '',
                },
                editRoleRules: {
                    role: [
                        { min: 0, max: 20, message: '长度应小于 20 个字符', trigger: 'blur' }
                    ],
                },
                editRoleStu_num: ''
            };
        },
        created() {
            this.init_groupInfo();
        },
        methods:{
            init_groupInfo(){
                this.$axios({
                    method: 'post',
                    url: "/api/user/groupInfo",
                    headers: {'Authorization': window.localStorage['Authorization']},
                    // headers: {'Authorization':window.localStorage['Authorization']}
                    // headers: {'userId':window.localStorage['userId']}
                    data:{userId:window.localStorage['userId']}
                }).then((res) => {
                    // console.log(res.data.status);
                    if(res.data.status == 200){
                        // console.log(window.localStorage['userId'] + " 156");
                        // console.log(res.data.status);
                        
                        // this.username=res.data.data.username;
                        this.group.username = window.localStorage['userId'];
                        // this.group=res.data.data;
                        this.group.realName=res.data.data.group_name;
                        // console.log(window.localStorage['userId'] + " " + this.group.username);

                        // console.log(res.data.data.users);
                        this.users_lists = JSON.parse(res.data.data.users);

                        // console.log(typeof(this.users_lists))
                        // var ull = [];
                        // for(var a in this.users_lists){
                        //     if(a < 2)
                        //     ull.push(this.users_lists[a]);
                        //     // console.log(this.users_lists[a]);
                        // }
                        // // console.log(ull);
                        // this.users_lists = ull;
                        this.rows = Object.keys(this.users_lists).length;
                        this.numTotal = this.rows;
                        if(this.rows % this.pageSize == 0){
                            this.pageTotal = this.rows / this.pageSize;
                        }
                        else{
                            this.rows -= this.rows % this.pageSize;
                            this.pageTotal = this.rows / this.pageSize + 1;
                        }
                        // console.log(this.pageTotal);

                        // this.cur_users_lists = [];
                        // for(var a in this.users_lists){
                        //     if(a < this.pageSize){
                        //         this.cur_users_lists.push(this.users_lists[a]);
                        //     }
                        // }
                        this.cur_users_lists = [];
                        for(var a in this.users_lists){
                            if(a >= (this.pageNo - 1) * this.pageSize && a < this.pageNo * this.pageSize){
                                this.cur_users_lists.push(this.users_lists[a]);
                            }
                        }
                        // console.log(this.cur_users_lists);
                    }
                    else if(res.data.status == 403){
                        this.$router.replace('/stu_error')
                    }
                }).catch( error =>{
                    console.log(error);
                });
                // console.log(this.pageNo);
            },
            getlist(index = -1){
                if(index != -1){
                    this.pageNo = index;
                }
                // console.log(index + "   " + this.pageNo);
                this.cur_users_lists = [];
                for(var a in this.users_lists){
                    if(a >= (this.pageNo - 1) * this.pageSize && a < this.pageNo * this.pageSize){
                        this.cur_users_lists.push(this.users_lists[a]);
                    }
                }
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
            addStu(){
                this.dialogFormVisible = true;
            },
            handleClose () {
                this.$refs.ruleForm.resetFields();
                this.form.stu_num = '';
                this.form.role = '';
                this.editRoleForm.role = '';
            },
            handleSave () {
                this.$refs.ruleForm.validate((valid) => {
                    if (valid) {
                        post_addGroupNumber(this.form.stu_num, this.group.realName, this.form.role).then(res => {
                            if(res.data.status == 200){
                                this.$message.success("添加队员成功");
                                this.dialogFormVisible = false;
                                this.init_groupInfo();
                                this.handleClose();
                            }
                            else if(res.data.status == 403){
                                this.$router.replace('/stu_error');
                            }
                            else{
                                this.$message.error("添加队员失败");
                            }
                        }).catch( error =>{
                            console.log(error);
                        });
                    } else {
                        this.$message.error("添加队员失败");
                    }
                })
            },
            editRole(stu_num){
                // console.log(stu_num);
                this.editRoleStu_num = stu_num;
                this.editRoleVisible = true;
            },
            editRoleSave(){
                this.$refs.ruleForm.validate((valid) => {
                    if (valid) {
                        post_editRole(this.editRoleStu_num, this.editRoleForm.role).then(res => {
                            if(res.data.status == 200){
                                this.$message.success("修改承担角色成功");
                                this.editRoleVisible = false;
                                this.init_groupInfo();
                                this.handleClose();
                            }
                            else if(res.data.status == 403){
                                this.$router.replace('/stu_error');
                            }
                            else{
                                this.$message.error("修改承担角色失败");
                            }
                        }).catch( error =>{
                            console.log(error);
                        });
                    } else {
                        this.$message.error("修改承担角色失败");
                    }
                })
            },
            quitTeam(){
                post_quitTeam().then(res => {
                    // console.log(res.data.status);
                    if(res.data.status == 200){
                        // this.$message.success("退出团队成功");
                        this.$router.go(0);
                    }
                    else if(res.data.status == 403){
                        this.$router.replace('/stu_error');
                    }
                    else{
                        this.$message.error("退出团队失败");
                    }
                }).catch( error =>{
                    console.log(error);
                });
            },
        }
    }
</script>

<style scoped>
    >>> .el-form-item__label{
        color:#000;
    }
    .info{
        margin-top: 30px;
        height: 600px;
        width: 1000px;
        margin-left: 20px;
        color:#000;
    }
    .ps1 .el-input{
        width: 245px;
        padding-left: 10px;
    }
    .ps0 .el-input{
        width: 220px;
        padding-left: 5px;
        padding-right: 8px;
    }
    .ps0{
        color:#000;
    }
    .ps2 .el-input{
        width: 320px;
        padding-left: 50px;
    }
    #r1{
        padding-left: 60px;
    }
    .ps4 .el-input{
        width: 320px;
        padding-left: 60px;
    }
    .ps5 .el-input{
        width: 320px;
        padding-left: 50px;
    }
    .el-form p{
        margin-bottom: 15px;
        font-size: 25px;
    }
    
    .user_msg{
        width: 220px;
        height: 40px;
        color:#000;
        /* font-size: 18px; */
        outline: none;
        background-color: #fff;
        border:1px solid rgb(22, 51, 81);;
        border-radius: 5px;
    }

    /* 分页索引 */
    .page-bar{
        /* margin:40px auto; */
        margin-top: 50px;
        margin-left: 30px;
    }
    .page-bar li:first-child>a {
        margin-left: 0px
    }
    .page-bar a{
        border: 1px solid #000;
        text-decoration: none;
        position: relative;
        float: left;
        padding: 6px 12px;
        margin-left: -1px;
        line-height: 1.42857143;
        color: #000;
        cursor: pointer;
        margin-right: 20px;
        font-size: 15px;
        font-weight: bolder;
    }
    .page-bar a:hover{
        background-color: #87D2FC;
        color: #fff;
    }
    .page-bar a.banclick{
        cursor:not-allowed;
    }
    .qq{
        background-color: #87D2FC;
        /* margin-left: 100px; */
    }

    .addStu{
        margin-top: 47px;
        margin-left: 0px;
    }
    .quitTeam{
        margin-top: 47px;
        margin-left: 27px;
    }
    .addStuDiagInput{
        width: 300px;
    }
    .people{
        margin-bottom: 15px;
        font-size: 25px;
    }
    .editRole{
        margin-bottom: 20px;
        float: right;
        margin-right: 103px;
    }
    .settingGroupInfoBottom{
        position: absolute;
        bottom: 0px;
        margin-bottom: 155px;
    }

</style>

<style>
    .addStuDialog{
        width:500px;
    }
</style>
