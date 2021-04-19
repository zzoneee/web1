<template>
    <div class="login">
        <div class="loginarea">
            <div class="loginrow">
                <input class="logininput" placeholder="用户名" type="text" v-model="user.username"></input>
            </div>
            <div class="loginrow">
                <input class="logininput" placeholder="密码" type="password" v-model="user.password"></input>
            </div>
            <div class="loginrow">
                <button class="loginbtn" type="input" @click="submitForm()">登录</button>
            </div>
        </div>
    </div>
</template>

<script>
    import axios from 'axios'
    export function login(username, password) {
        return axios({
            method: 'post',
            url: "/api/teacher/login",
            data:{username:username,password:password}
        })
    }

    export default {
        data() {
            return {
                user:{
                    username:'',
                    password:''
                }
            }
        },
        methods:{
            submitForm(){
                if(this.user.username==''){
                    this.$message.error("用户名不能为空");
                }
                else if(this.user.password==''){
                    this.$message.error("密码不能为空");
                }
                else if(this.user.password.length>16||this.user.password.length<6){
                    this.$message.error("密码长度在6-16位");
                }
                else{
                    // this.$axios({
                    //     method: 'post',
                    //     url: "/api/teacher/login",
                    //     // params:{username:this.user.username,password:this.user.password}
                    //     data:{username:this.user.username,password:this.user.password}
                    // }).then((res) => {
                    //     if(res.data.status == 200){
                    //         window.localStorage.setItem("tea_userId",res.data.data.tea_id);
                    //         // console.log(res.data.data.tea_id);
                    //         this.$router.push('/tea_info');
                    //     }
                    //     else{
                    //         this.$message.error("用户名或密码错误");
                    //     }
                    // }).catch( error =>{
                    //     console.log(error);
                    // });
                    login(this.user.username,this.user.password).then(res => {
                        if(res.data.status == 200){
                            window.localStorage.setItem("tea_Authorization", res.data.data.Authorization);
                            window.localStorage.setItem("tea_userId",res.data.data.tea_id);
                            this.$router.push('/tea_info');
                        }
                        else{
                            // console.log(res.data.status);
                            this.$message.error("用户名或密码错误");
                        }
                    }).catch( error =>{
                        console.log(error);
                    });
                }
            }
        }
    }

</script>

<style scoped>
    .login{
        margin:0 auto;
        position:fixed;
        top:0;
        left:0;
        width: 100%;
        height:100%;
        min-width: 1000px;
        zoom:1;
        background: url('../assets/tea/tea_login_bkg.jpg');
        background-repeat: no-repeat;
        background-size: cover;
        -webkit-background-size: cover;
        -o-background-size: cover;
        background-position: center 0;
    }
    .loginarea{
        width: 400px;
        height:200px;
        text-align: center;
        position: absolute;
        z-index: 200;
        left:50%;
        top:55%;
        margin-left:-200px;
    }
    .loginrow{
        padding-top: 12px;
    }
    .logininput{
        padding-left: 15px;
        width: 240px;
        height:40px;
        font-size: 18px;
        color:rgb(22, 51, 81);
        background-color: transparent;
        border:1px solid rgb(22, 51, 81);;
        border-radius: 20px;
        outline: none;
    }
    .loginbtn{
        color:#000;
        width: 240px;
        height:40px;
        font-size: 18px;
        outline: none;
        background-color: #bfcdcd;
        border:1px solid rgb(22, 51, 81);;
        border-radius: 20px;
    }
    @keyframes myMove {
        0% {
            top: 0;
        }
        50% {
            top: 4vh;
        }
        100% {
            top: 0;
        }
    } 
</style>
