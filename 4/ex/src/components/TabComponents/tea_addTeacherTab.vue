<template>
    <div class="setting3">
        <el-form :model="ruleForm" :rules="rules" ref="ruleForm">
            <el-form-item label="账号" prop="id" class="ps4">
                <el-input v-model="ruleForm.id"></el-input>
            </el-form-item>
            <el-form-item label="密码" prop="password" class="ps5">
                <el-input v-model="ruleForm.password"></el-input>
            </el-form-item>
            <el-form-item label="姓名" prop="name" class="ps1">
                <el-input v-model="ruleForm.name"></el-input>
            </el-form-item>
            <el-form-item label="学院" prop="college" class="ps2">
                <el-input v-model="ruleForm.college"></el-input>
            </el-form-item>
            <el-form-item label="手机号码" prop="phone" class="ps3">
                <el-input v-model="ruleForm.phone"></el-input>
            </el-form-item>
            <el-form-item>
                <el-button type="primary" @click="submitForm('ruleForm')" class="btn_modify">添加</el-button>
            </el-form-item>
        </el-form>
    </div>
</template>

<script>
    export default {
        data(){
            let validateID = (rule, value, callback) => {
                if(value == ''){
                    callback(new Error('请输入账号'));
                }
                else{
                    this.$axios({
                        method: 'get',
                        url: "/api/teacher/teacherIDExist",
                        params:{tea_userId: value}
                    }).then((res) => {
                        if(res.data.status == 200){
                            callback();
                        }
                        else{
                            callback(new Error('该账号已被注册'));
                        }
                    }).catch( error =>{
                        console.log(error);
                        callback(new Error(error));
                    });
                }
            };
            let validatePassword = (rule, value, callback) => {
                if(value == ''){
                    callback(new Error('请输入密码'));
                }
                else{
                    callback();
                }
                
            };
            let validateName = (rule, value, callback) => {
                if(value == ''){
                    callback(new Error('请输入姓名'));
                }
                else{
                    callback();
                }
                
            };
            let validateCollege = (rule, value, callback) => {
                if(value == ''){
                    callback(new Error('请输入学院'));
                }
                else{
                    callback();
                }
                
            };
            return{
                editMsg:{},
                ruleForm: {
                    id: '',
                    password: '',
                    name: '',
                    college: '',
                    phone: ''
                },
                rules: {
                    id:[
                        { message: '请输入账号', required: true, trigger: 'blur' },
                        { validator: validateID, trigger: 'blur' },
                        {min:0,max:20,message:"长度应小于20位",trigger:"blur"}
                    ],
                    password:[
                        { message: '请输入密码', required: true, trigger: 'blur' },
                        { validator: validatePassword, trigger: 'blur' },
                        {min:6,max:16,message:"长度应在6-16位",trigger:"blur"}
                    ],
                    name:[
                        { message: '请输入姓名', required: true, trigger: 'blur' },
                        { validator: validateName, trigger: 'blur' },
                        {min:0,max:20,message:"长度应小于20位",trigger:"blur"}
                    ],
                    college: [
                        { message: '请输入学院', required: true, trigger: 'blur' },
                        { validator: validateCollege, trigger: 'blur' },
                        {min:0,max:20,message:"长度应小于20位",trigger:"blur"}
                    ],
                    phone: [
                        { trigger: 'blur' },
                        {min:0,max:20,message:"长度应小于20位",trigger:"blur"}
                    ]
                }
            }
        },
        methods:{
            submitForm(formName) {
                this.$refs[formName].validate((valid) => {
                    if (valid) {
                        this.$confirm('确认添加新教师, 是否继续?', '提示', {
                            confirmButtonText: '确定',
                            cancelButtonText: '取消',
                            type: 'warning'
                        }).then(() => {
                            //点击确定按钮的操作, 提交修改的操作
                            this.editMsg.id = this.ruleForm.id;
                            this.editMsg.password = this.ruleForm.password;
                            this.editMsg.name = this.ruleForm.name;
                            this.editMsg.college = this.ruleForm.college;
                            this.editMsg.phone = this.ruleForm.phone;
                            // console.log(this.editMsg);
                            this.$axios({
                                method: 'post',
                                url: "/api/teacher/addTeacher",
                                data: this.editMsg
                            }).then(res=> {
                                // console.log(res.data.status);
                                if(res.data.status == 200){
                                    this.$message.success("添加成功");
                                }else{
                                    this.$message.error("添加失败, "+res.data.msg);
                                    return false;
                                }
                            }) .catch( error =>{
                                console.log(error);
                            });
                        })
                    } else {
                        this.$message.error("添加失败");
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
    .setting3{
        margin-top: 150px;
        margin-left: 550px;
        margin-right: 30px;
        margin-bottom: 30px;
    }
    .ps1 .el-input{
        width: 300px;
        padding-left: 60px;
    }
    .ps2 .el-input{
        width: 300px;
        padding-left: 60px;
    }
    .ps3 .el-input{
        width: 300px;
        padding-left: 32px;
    }
    .ps4 .el-input{
        width: 300px;
        padding-left: 60px;
    }
    .ps5 .el-input{
        width: 300px;
        padding-left: 60px;
    }
    .btn_modify{
        margin-left: 180px;
        margin-top: 19px;
    }
</style>
