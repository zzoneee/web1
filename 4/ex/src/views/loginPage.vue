<template>
    <div class="login">
        <div class="conAll">
            <el-row>
                <el-col :span="12">
                    <div class="chartCon">
                        <div id="myChart" :style="{width: '600px', height: '300px'}"></div>
                    </div>
                </el-col>
                <el-col :span="12">
                    <div class="loginarea">
                        <div class="loginCon">
                            <p class="loginTitle">欢迎登录</p>
                            <div class="loginrow">
                                <input class="logininput" placeholder="用户名" type="text" v-model="user.username"></input>
                            </div>
                            <div class="loginrow">
                                <input class="logininput" placeholder="密码" type="password" v-model="user.password"></input>
                            </div>
                            <div class="loginrow">
                                <input class="verificationCodeInput" placeholder="验证码" type="text" v-model="verificationCode"></input>
                                <button class="verificationCode" :style="`width:${width}; height:${height}`" @click="refreshCode">
                                    <span v-for="(item, index) in codeList" :key="index" :style="getStyle(item)">{{item.code}}</span>
                                </button>
                            </div>
                            <div class="loginrow">
                                <!-- <el-checkbox class="rememberPsw" v-model="rememberPsw">记住我</el-checkbox> -->
                            </div>
                            <div class="loginrow">
                                <button class="loginbtn" type="input" @click="submitForm()">登录</button>
                            </div>
                        </div>
                    </div>
                </el-col>
            </el-row>
        </div>
    </div>
</template>

<script>
    import axios from 'axios'
    const echarts = require('echarts');
    export function login(username, password) {
        return axios({
            method: 'post',
            url: "/api/user/auth",
            data:{username:username,password:password}
        })
    }
    export function post_addLoginRecord(username) {
        return axios({
            method: 'post',
            url: "/api/user/addLoginRecord",
            data:{username:username}
        })
    }
    export function get_getLoginNumber(year, month, day) {
        return axios({
            method: 'get',
            url: "/api/user/getLoginNumber",
            params:{year: year, month: month, day: day}
        })
    }

    export default {
        props: {
            width: {
                type: String,
                default: '100px'
            },
            height: {
                type: String,
                default: '40px'
            },
            length: {
                type: Number,
                default: 4
            },
        },
        data() {
            return {
                user:{
                    username:'',
                    password:''
                },
                verificationCode: '',
                codeList: [],
                rememberPsw: false,
                msg: '',
            }
        },
        mounted () {
            this.createdCode();
            this.drawLine();
        },
        created() {
        },
        methods:{
            submitForm(){
                let vc = this.verificationCode.toLowerCase();
                let verificationCodeRight = this.codeList[0].code + this.codeList[1].code + this.codeList[2].code + this.codeList[3].code;
                verificationCodeRight = verificationCodeRight.toLowerCase();
                // console.log(this.verificationCode,verificationCodeRight,this.codeList);
                if(this.user.username==''){
                    this.$message.error("用户名不能为空");
                    this.createdCode();
                }
                else if(this.user.password==''){
                    this.$message.error("密码不能为空");
                    this.createdCode();
                }
                else if(this.user.password.length>16||this.user.password.length<6){
                    this.$message.error("密码长度在6-16位");
                    this.createdCode();
                }
                else if(vc==''){
                    this.$message.error("验证码不能为空");
                    this.createdCode();
                }
                else if(vc != verificationCodeRight){
                    this.$message.error("验证码错误");
                    this.createdCode();
                }
                else{
                    login(this.user.username,this.user.password).then(res => {
                        if(res.data.status == 200){
                            window.localStorage.setItem("Authorization", res.data.data.Authorization);
                            window.localStorage.setItem("userId",res.data.data.id);

                            post_addLoginRecord(this.user.username).then(res => {
                                if(res.data.status == 200){
                                }
                            }).catch( error =>{
                                console.log(error);
                            });

                            this.$router.push('/menu');
                        }
                        else{
                            this.$message.error("用户名或密码错误");
                            this.createdCode();
                        }
                    }).catch( error =>{
                        console.log(error);
                    });
                }
            },
            refreshCode () {
                this.createdCode();
            },
            createdCode () {
                let len = this.length,
                    codeList = [],
                    chars = 'ABCDEFGHJKMNPQRSTWXYZabcdefhijkmnprstwxyz0123456789',
                    charsLen = chars.length
                // 生成
                for (let i = 0; i < len; i++) {
                    let rgb = [Math.round(Math.random() * 220), Math.round(Math.random() * 240), Math.round(Math.random() * 200)]
                    codeList.push({
                        code: chars.charAt(Math.floor(Math.random() * charsLen)),
                        color: `rgb(${rgb})`,
                        fontSize: `1${[Math.floor(Math.random() * 10)]}px`,
                        padding: `${[Math.floor(Math.random() * 10)]}px`,
                        transform: `rotate(${Math.floor(Math.random() * 90) - Math.floor(Math.random() * 90)}deg)`
                    })
                }
                // 指向
                this.codeList = codeList
                // 将当前数据派发出去
                this.$emit('update:value', codeList.map(item => item.code).join(''))
            },
            getStyle (data) {
                return `color: ${data.color}; font-size: ${data.fontSize}; padding: ${data.padding}; transform: ${data.transform}`
            },
            // 绘制柱状图
            drawLine(){
                // 获取当前时间
                let time = new Date();
                // console.log(time.getMonth() + 1,time.getDate(),time.getHours(),time.getMinutes(),time.getSeconds(),time.toLocaleDateString());
                let er = 28;
                let year = time.getFullYear();
                if(year % 100 != 0 && year % 4 == 0 || year % 400 == 0){
                    er = 29;
                }
                let monthDay = [0,31,er,31,30,31,30,31,31,30,31,30,31];
                let timeData = [];
                let xAxisData = [];
                let seriesData = [];
                timeData.push({year: year, month: time.getMonth() + 1, date: time.getDate()});
                for(let i = 1;i < 7;i++){
                    let year1 = time.getFullYear();
                    let month = timeData[i - 1].month;
                    let date = timeData[i - 1].date - 1;
                    if(date <= 0){
                        month--;
                        if(month <= 0){
                            month = 12;
                            year1--;
                        }
                        date = monthDay[month];
                    }
                    timeData.push({year: year1, month: month, date: date});
                }
                get_getLoginNumber(year, time.getMonth() + 1, time.getDate()).then(res => {
                    // console.log(res.data.err);
                    if(res.data.status == 200){
                        let maxData = 0;
                        let color = ['#3c6071', '#557c8e', '#789eb0', '#8fb1c1' ,'#a9c7d5', '#c2d9e4', '#dde8ec'];
                        for(let i = 6;i >= 0;i--){
                            if(maxData < res.data.data[i]){
                                maxData = res.data.data[i]
                            }
                        }
                        for(let i = 6;i >= 0;i--){
                            xAxisData.push(timeData[i].month.toString() + "-" + timeData[i].date.toString());
                            let cur_color = color[6];
                            for(let j = 0;j < 6;j++){
                                if(res.data.data[i] <= maxData / 7 * (j + 1)){
                                    cur_color = color[j];
                                    break;
                                }
                            }
                            seriesData.push({value: res.data.data[i], itemStyle: {color: cur_color}});
                            // seriesData.push({value: (7 - i) * 10, itemStyle: {color: cur_color}});
                        }
                        // 基于准备好的dom，初始化echarts实例
                        let myChart = this.$echarts.init(document.getElementById('myChart'))
                        // 绘制图表
                        myChart.setOption({
                            title: { text: '使用人数' },
                            tooltip: {},
                            xAxis: {
                                type: 'category',
                                data: xAxisData,
                            },
                            yAxis: {},
                            series: [{
                                // name: '人数',
                                type: 'bar',
                                data: seriesData,
                            }]
                        });
                    }
                }).catch( error =>{
                    console.log(error);
                });
            },
        }
    }

</script>

<style scoped>
    .tmp{
        color: #c2d9e4;
    }
    .login{
        margin:0 auto;
        position:fixed;
        top:0;
        left:0;
        width: 100%;
        height:100%;
        min-width: 1000px;
        zoom:1;
        background: url('../assets/login_bkg.jpg');
        background-repeat: no-repeat;
        background-size: cover;
        -webkit-background-size: cover;
        -o-background-size: cover;
        background-position: center 0;
    }
    .conAll{
        margin-top: 100px;
    }
    .loginCon{
        margin-top: 63px;
    }
    .loginarea{
        width: 400px;
        height:400px;
        text-align: center;
        position: absolute;
        z-index: 200;
        /* left:71%; */
        /* top:27%; */
        margin-left:200px;
        margin-top: 100px;

        box-shadow: 0 2px 4px rgba(0, 0, 0, .12), 0 0 6px rgba(0, 0, 0, .04);
        background-color: #fff;
        border-radius: 15px;
        opacity: 0.95;
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
        border-radius: 11px;
        outline: none;
    }
    .verificationCodeInput{
        padding-left: 15px;
        width: 135px;
        height:40px;
        font-size: 18px;
        color:rgb(22, 51, 81);
        background-color: transparent;
        border:1px solid rgb(22, 51, 81);;
        border-radius: 11px;
        outline: none;
    }
    .verificationCode{
        width: 220px;
        height: 40px;
        color:#000;
        /* font-size: 18px; */
        outline: none;
        background-color: #fff;
        border:1px solid rgb(22, 51, 81);;
        border-radius: 7px;
    }
    .rememberPsw{
        font-size: 18px;
        /* float: left; */
        margin-right: 180px;
    }
    .loginbtn{
        color:#000;
        width: 255px;
        height:40px;
        font-size: 18px;
        outline: none;
        background-color: #e3f1fa;
        border:0.5px solid rgb(112, 151, 193);
        border-radius: 11px;
    }
    .loginTitle{
        font-size: 20px;
        font-weight: 700;
        color: rgb(41, 80, 122);
        margin-bottom: 15px;
    }
    .chartCon{
        background-color: #151031;
        opacity: 0.91;
        width: 600px;
        height: 300px;
        border-radius: 11px;
        margin-left: 120px;
        padding: 10px;
        margin-top: 35%;
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
