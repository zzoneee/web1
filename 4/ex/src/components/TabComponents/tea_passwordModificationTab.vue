<template>
    <div class="setting2">
        <el-form :model="ruleForm" :rules="rules" ref="ruleForm">
            <el-form-item label="旧密码" prop="oldpass" class="ps1">
                <el-input v-model="ruleForm.oldpass"></el-input>
            </el-form-item>
            <el-form-item label="修改密码" prop="pass" class="ps2">
                <el-input v-model="ruleForm.pass"></el-input>
            </el-form-item>
            <el-form-item label="确认密码" prop="checkPass" class="ps3">
                <el-input v-model="ruleForm.checkPass"></el-input>
            </el-form-item>
            <el-form-item>
                <el-button type="primary" @click="submitForm('ruleForm')" class="btn_modifyPswd">修改</el-button>
            </el-form-item>
        </el-form>
    </div>
</template>

<script>
    export default {
        // name: "passwordModificationTab",
        // inject:['reload'],
        data(){
            let validateOldPass = (rule, value, callback) => {
                // console.log(value);
                if (value === '') {
                    callback(new Error('请输入密码'));
                } else {
                    if (this.ruleForm.pass !== '') {
                        this.$refs.ruleForm.validateField('pass');
                    }
                    callback();
                }
            };
            let validatePass = (rule, value, callback) => {
                if (value === '') {
                    callback(new Error('请输入密码'));
                } else {
                    if (value === this.ruleForm.oldpass) {
                        callback(new Error('新旧密码不能一样!'));
                    }else if(this.ruleForm.checkPass !== ''){
                        this.$refs.ruleForm.validateField('checkPass');
                    }
                    callback();
                }
            };
            let validatePass2 = (rule, value, callback) => {
                if (value === '') {
                    callback(new Error('请再次输入密码'));
                } else if (value !== this.ruleForm.pass) {
                    callback(new Error('两次输入密码不一致!'));
                } else {
                    callback();
                }
            };
            return{
                editPwd:{},
                ruleForm: {
                    oldpass: '',
                    pass: '',
                    checkPass: ''
                },
                rules: {
                    oldpass:[
                        { message: '请输入密码', required: true, trigger: 'blur' },
                        { validator: validateOldPass, trigger: 'blur' }
                    ],
                    pass: [
                        { message: '请输入新密码', required: true, trigger: 'blur' },
                        { validator: validatePass, trigger: 'blur' },
                        {min:6,max:16,message:"长度在6-16位",trigger:"blur"}
                    ],
                    checkPass: [
                        { message: '请再次输入密码', required: true, trigger: 'blur' },
                        { validator: validatePass2, trigger: 'blur' }
                    ]
                }
            }
        },
        methods:{
            submitForm(formName) {
                this.$refs[formName].validate((valid) => {
                    if (valid) {
                        this.$confirm('确认修改密码, 是否继续?', '提示', {
                            confirmButtonText: '确定',
                            cancelButtonText: '取消',
                            type: 'warning'
                        }).then(() => {
                            //点击确定按钮的操作, 提交修改的操作
                            this.editPwd.userId = window.localStorage['tea_userId'];
                            this.editPwd.editPassword = this.ruleForm.pass;
                            this.editPwd.oldPassword = this.ruleForm.oldpass;
                            this.$axios({
                                method: 'post',
                                url: "/api/teacher/editPwd",
                                data: this.editPwd
                            }).then(res=> {
                                if(res.data.status === 200){
                                    this.$message.success("修改密码成功");
                                    this.ruleForm.oldpass = "";
                                    this.ruleForm.pass = "";
                                    this.ruleForm.checkPass = "";
                                }else{
                                    this.$message.error("修改失败, "+res.data.msg);
                                    return false;
                                }
                            }) .catch( error =>{
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
    .setting2{
        margin-top: 150px;
        margin-left: 550px;
        margin-right: 30px;
        margin-bottom: 30px;
    }
    .ps1 .el-input{
        width: 300px;
        padding-left: 40px;
    }
    .ps2 .el-input{
        width: 300px;
        padding-left: 20px;
    }
    .ps3 .el-input{
        width: 300px;
        padding-left: 20px;
    }
    .btn_modifyPswd{
        margin-left: 180px;
        margin-top: 19px;
    }
</style>
