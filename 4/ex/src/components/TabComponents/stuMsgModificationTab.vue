<template>
    <div class="setting1">
        <el-form :model="ruleForm" :rules="rules" ref="ruleForm">
            <el-form-item label="学号" prop="stu_num" class="ps4">
                <el-input :disabled="true" v-model="stu_num"></el-input>
            </el-form-item>
            <el-form-item label="姓名" prop="name" class="ps1">
                <el-input v-model="ruleForm.name"></el-input>
            </el-form-item>
            <el-form-item label="学院" prop="college" class="ps2">
                <el-input :disabled="true" v-model="ruleForm.college"></el-input>
            </el-form-item>
            <el-form-item label="班级" prop="class_name" class="ps5">
                <el-input :disabled="true" v-model="ruleForm.class_name"></el-input>
            </el-form-item>
            <el-form-item label="手机号码" prop="phone" class="ps3">
                <el-input v-model="ruleForm.phone"></el-input>
            </el-form-item>
            <el-form-item>
                <el-button type="primary" @click="submitForm('ruleForm')" class="btn_modify">修改</el-button>
            </el-form-item>
        </el-form>
    </div>
</template>

<script>
    import axios from 'axios'
    export function get_stuMsg() {
        return axios({
            method: 'get',
            url: "/api/user/stuMsg",
            headers: {'Authorization': window.localStorage['Authorization']}
        })
    }
    export function post_editStuMsg(editMsg) {
        return axios({
            method: 'post',
            url: "/api/user/editStuMsg",
            headers: {'Authorization': window.localStorage['Authorization']},
            data: {editMsg: editMsg}
        })
    }
    export default {
        data(){
            return{
                stu_num: '',
                editMsg:{},
                ruleForm: {
                    name: '',
                    college: '',
                    class_name: '',
                    phone: ''
                },
                rules: {
                    name:[
                        { message: '请输入姓名', required: true, trigger: 'blur' },
                        {min:0,max:20,message:"长度应小于20位",trigger:"blur"}
                    ],
                    // college: [
                    //     { trigger: 'blur' },
                    //     {min:0,max:20,message:"长度应小于20位",trigger:"blur"}
                    // ],
                    // college: [
                    //     { trigger: 'blur' },
                    //     {min:0,max:20,message:"长度应小于20位",trigger:"blur"}
                    // ],
                    phone: [
                        { trigger: 'blur' },
                        {min:0,max:20,message:"长度应小于20位",trigger:"blur"}
                    ]
                }
            }
        },
        created() {
            get_stuMsg().then(res => {
                if(res.data.status == 200){
                    this.stu_num = res.data.data.stu_num;
                    this.ruleForm.name = res.data.data.name;
                    this.ruleForm.college = res.data.data.college;
                    this.ruleForm.class_name = res.data.data.class_name;
                    this.ruleForm.phone = res.data.data.phone;
                }
                else if(res.data.status == 403){
                    this.$router.replace('/stu_error');
                }
            }).catch( error =>{
                console.log(error);
            });
        },
        methods:{
            submitForm(formName) {
                this.$refs[formName].validate((valid) => {
                    if (valid) {
                        this.$confirm('确认修改信息, 是否继续?', '提示', {
                            confirmButtonText: '确定',
                            cancelButtonText: '取消',
                            type: 'warning'
                        }).then(() => {
                            //点击确定按钮的操作, 提交修改的操作
                            this.editMsg.stu_num = window.localStorage['userId'];
                            this.editMsg.name = this.ruleForm.name;
                            this.editMsg.college = this.ruleForm.college;
                            this.editMsg.class_name = this.ruleForm.class_name;
                            this.editMsg.phone = this.ruleForm.phone;
                            post_editStuMsg(this.editMsg).then(res => {
                                if(res.data.status == 200){
                                    this.$message.success("修改信息成功");
                                }
                                else if(res.data.status == 403){
                                    this.$router.replace('/stu_error');
                                }
                                else{
                                    this.$message.error("修改失败, "+res.data.msg);
                                    return false;
                                }
                            }).catch( error =>{
                                console.log(error);
                            });
                        })
                    } else {
                        this.$message.error("修改失败");
                        return false;
                    }
                });
            }
        }
    }
</script>

<style scoped>
    >>>.el-form-item__label{
        color:rgb(10, 42, 128);
        font-size: 20px;
    }
    .setting1{
        margin-top: 90px;
        margin-left: 150px;
        margin-right: 30px;
        margin-bottom: 30px;
    }
    .ps1 .el-input{
        width: 300px;
        padding-left: 48px;
        /* margin-top: 10px; */
    }
    .ps2 .el-input{
        width: 300px;
        padding-left: 60px;
        /* margin-top: 10px; */
    }
    .ps3 .el-input{
        width: 300px;
        padding-left: 20px;
        /* margin-top: 10px; */
    }
    .ps4 .el-input{
        width: 300px;
        padding-left: 60px;
        /* margin-top: 10px; */
    }
    .ps5 .el-input{
        width: 300px;
        padding-left: 60px;
        /* margin-top: 10px; */
    }
    .btn_modify{
        margin-left: 180px;
        margin-top: 19px;
    }
</style>
