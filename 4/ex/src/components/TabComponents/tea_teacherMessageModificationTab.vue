<template>
    <div class="setting1">
        <el-form :model="ruleForm" :rules="rules" ref="ruleForm">
            <el-form-item label="登录账号" prop="id" class="ps4">
                <el-input :disabled="true" v-model="id"></el-input>
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
                <el-button type="primary" @click="submitForm('ruleForm')" class="btn_modify">修改</el-button>
            </el-form-item>
        </el-form>
    </div>
</template>

<script>
    export default {
        data(){
            return{
                id: '',
                editMsg:{},
                ruleForm: {
                    name: '',
                    college: '',
                    phone: ''
                },
                rules: {
                    name:[
                        { message: '请输入姓名', required: true, trigger: 'blur' },
                        {min:0,max:20,message:"长度应小于20位",trigger:"blur"}
                    ],
                    college: [
                        { message: '请输入学院', required: true, trigger: 'blur' },
                        {min:0,max:20,message:"长度应小于20位",trigger:"blur"}
                    ],
                    phone: [
                        { trigger: 'blur' },
                        {min:0,max:20,message:"长度应小于20位",trigger:"blur"}
                    ]
                }
            }
        },
        created() {
            this.$axios({
                method: 'get',
                url: "/api/teacher/teacherMessage",
                params:{tea_userId:window.localStorage['tea_userId']}
            }).then((res) => {
                // console.log(window.localStorage['tea_userId']);
                if(res.data.status == 200){

                    this.id = res.data.data.id;
                    this.ruleForm.name = res.data.data.name;
                    this.ruleForm.college = res.data.data.college;
                    this.ruleForm.phone = res.data.data.phone;
                    
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
                            this.editMsg.id = window.localStorage['tea_userId'];
                            this.editMsg.name = this.ruleForm.name;
                            this.editMsg.college = this.ruleForm.college;
                            this.editMsg.phone = this.ruleForm.phone;
                            // console.log(this.editMsg);
                            this.$axios({
                                method: 'post',
                                url: "/api/teacher/editTeacherMessage",
                                data: this.editMsg
                            }).then(res=> {
                                // console.log(res.data.status);
                                if(res.data.status == 200){
                                    this.$message.success("修改信息成功");
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
    .setting1{
        margin-top: 150px;
        margin-left: 550px;
        margin-right: 30px;
        margin-bottom: 30px;
    }
    .ps1 .el-input{
        width: 300px;
        padding-left: 60px;
        /* margin-top: 10px; */
    }
    .ps2 .el-input{
        width: 300px;
        padding-left: 60px;
        /* margin-top: 10px; */
    }
    .ps3 .el-input{
        width: 300px;
        padding-left: 32px;
        /* margin-top: 10px; */
    }
    .ps4 .el-input{
        width: 300px;
        padding-left: 32px;
        /* margin-top: 10px; */
    }
    .btn_modify{
        margin-left: 180px;
        margin-top: 19px;
    }
</style>
