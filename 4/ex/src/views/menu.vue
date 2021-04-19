<template>
    <div class="menu">
        <div class="menuBtnList">
            <el-row :gutter="0">
                <el-col :span="7" :offset="0">
                    <div class="btn_menu">
                        <button plain class="btn_menu1" type="input" @click="to_ex1">实验一</button>
                    </div>
                </el-col>
                <el-col :span="7">
                    <div class="btn_menu">
                        <button plain class="btn_menu1" type="input" @click="to_ex2">实验二</button>
                    </div>
                </el-col>
                <el-col :span="7">
                    <div class="btn_menu">
                        <button plain class="btn_menu1" type="input" @click="to_ex3">实验三</button>
                    </div>
                </el-col>
            </el-row>

            <el-row :gutter="0">
                <el-col :span="7" :offset="0">
                    <div class="btn_menu">
                        <button plain class="btn_menu1" type="input" @click="to_report">实验报告</button>
                    </div>
                </el-col>
                <el-col :span="7">
                    <div class="btn_menu">
                        <button plain class="btn_menu1" type="input" @click="to_setting">设置</button>
                    </div>
                </el-col>
                <el-col :span="7">
                    <div class="btn_menu">
                        <button plain class="btn_menu1" type="input" @click="exit_to_login">退出登录</button>
                    </div>
                </el-col>
            </el-row>
        </div>
    </div>
</template>

<script>
    import axios from 'axios'
    export function get_isStuHasGroup() {
        return axios({
            method: 'get',
            url: "/api/user/isStuHasGroup",
            headers: {'Authorization': window.localStorage['Authorization']}
        })
    }
    export default {
        data() {
            return {
                
            }
        },
        methods:{
            to_ex1(){
                this.noGroup(1);
            },
            to_ex2(){
                this.noGroup(2);
            },
            to_ex3(){
                this.noGroup(3);
            },
            to_setting(){
                this.$router.push('/setting');
            },
            to_report(){
                this.noGroup(4);
            },
            exit_to_login(){
                this.$router.push('/');
            },
            noGroup(num){
                get_isStuHasGroup().then(res => {
                    // console.log(res.data.status + " " + res.data.data.hasGroup);
                    if(res.data.status == 200){
                        if(res.data.data.hasGroup){
                            if(num == 1){
                                console.log("toex1");
                            }
                            else if(num == 2){
                                console.log("toex2");
                            }
                            else if(num == 3){
                                console.log("toex3");
                            }
                            else if(num == 4){
                                this.$router.push('/report');
                            }
                        }
                        else{
                            this.noGroupToSetting();
                        }
                    }
                    else if(res.data.status == 403){
                        this.$router.replace('/stu_error')
                    }
                }).catch( error =>{
                    console.log(error);
                });
            },
            noGroupToSetting(){
                const h = this.$createElement;
                this.$notify.error({
                    title: '请先前往设置加入团队',
                    message: h('p', null, [
                        // h('span', null, '内容可以是 '),
                        h('el-button', {
                            on: {
                                click:this.to_setting
                            },
                            // type: 'primary'
                        }, "点击前往设置")
                    ]),
                    position: 'bottom-right'
                    // duration: 0
                });
            },
        }
    }
</script>

<style scoped>
    .menu{
        margin:0 auto;
        position:fixed;
        top:0;
        left:0;
        width: 100%;
        height:100%;
        min-width: 1000px;
        zoom:1;
        background: url('../assets/bg.png');
        background-repeat: no-repeat;
        background-size: cover;
        -webkit-background-size: cover;
        -o-background-size: cover;
        background-position: center 0;
    }
    .menuBtnList{
        margin-left: 30%;
        margin-top: 11%;
        box-shadow: 0 2px 12px 0 rgba(43, 34, 34, 0.1);
        background-color: #fff;
        opacity: 0.8;
        height: 400px;
        width: 600px;
    }
    .btn_menu{
        margin-top: 30px;
        margin-left: 53px;
        width: 150px;
    }
    .btn_menu1{
        color:#000;
        width: 150px;
        height: 150px;
        font-size: 23px;
        outline: none;
        background-color: #f4f9fa;
        border:1px solid rgb(22, 51, 81);
        border-radius: 15px;

        /* margin-left: 100px; */
    }
    .btn_menu1:hover{
        color:#000;
        background-color: #d7eef3;
        border:1px solid rgb(22, 51, 81);
        font-weight: 900;
    }
    .btn_menu1:active{
        background-color: #cbe9f0;
    }
</style>
