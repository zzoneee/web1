<template>
    <div class="container">

        <el-menu
            :default-active="activeIndex"
            class="el-menu"
            mode="horizontal"
            @select="handleSelect"
            text-color="#000"
            active-text-color="#4099b4">
            <!-- <span class="titleTL"><i class="el-icon-pie-chart"></i>图灵测试论坛</span> -->
            <el-menu-item class="forumTop" index="3" :class="{'active_index':activeIndex=='3'}">实验说明</el-menu-item>
            <el-menu-item index="1" :class="{'active_index':activeIndex=='1'}">论坛</el-menu-item>
            <el-menu-item index="2" :class="{'active_index':activeIndex=='2'}">投票</el-menu-item>
            
            <el-menu-item index="4" class="userInfo">
                <template slot="title"><el-avatar src="http://file.tuling123.com/upload/image/202103/6bc5b8fc-103c-4b66-b288-8aaf131cd443.JPG"></el-avatar> {{ group_name }}</template>
            </el-menu-item>
            
        </el-menu>

        <div class="info">

            <div class="message">
                <step3 v-if="exNo==3"></step3>
                <step1 v-if="exNo==1"></step1>
                <step2 v-if="exNo==2"></step2>
            </div>
        </div>

    </div>
</template>

<script>
    import axios from 'axios'
    const introduction = () => import('./introduction');
    const post = () => import('./post');
    const vote = () => import('./vote');
    export function get_getGroupName(group_id) {
        return axios({
            method: 'get',
            url: "/api/user/getGroupName",
            headers: {'Authorization': window.localStorage['Authorization']},
            params: {group_id: group_id}
        })
    }
    export default {
        components:{
            "step1":post,
            "step2":vote,
            "step3":introduction,
        },
        data() {
            return {
                exNo:3,
                activeIndex: '3',
                group_id: this.$route.query.group,
                group_name: '',
            }
        },
        created() {
            // console.log(this.$route.query.zz);
            // this.group_id = this.$route.query.group;
            get_getGroupName(this.group_id).then(res => {
                // console.log(res.data.data);
                if(res.data.status == 200){
                    this.group_name = res.data.data;
                }
                else if(res.data.status == 403){
                    this.$router.replace('/stu_error');
                }
            }).catch( error =>{
                console.log(error);
            });
        },
        methods:{
            handleSelect(key, keyPath) {
                this.activeIndex = key;
                // console.log(key, keyPath, this.activeIndex[0]);
                if(this.activeIndex == "1"){
                    this.exNo = 1;
                }
                else if(this.activeIndex == "2"){
                    this.exNo = 2;
                }
                else if(this.activeIndex == "3"){
                    this.exNo = 3;
                }
            },
        }
    }

</script>

<style scoped>
    .container{
        margin:0 auto;
        position:fixed;
        top:0;
        left:0;
        width: 100%;
        height:100%;
        min-width: 1000px;
        zoom:1;
        background: url('../../assets/tea/tea_info_bkg.jpg');
        background-repeat: no-repeat;
        background-size: cover;
        -webkit-background-size: cover;
        -o-background-size: cover;
        background-position: center 0;
    }
    .info{
        margin-top: 3%;
    }
    .message{
        margin-top: 2%;
    }
    .tea_info_btn{
        color:#000;
        width: 140px;
        height:50px;
        font-size: 18px;
        outline: none;
        background-color: #c2e6f1;
        border:1px solid rgb(22, 51, 81);
        border-radius: 25px;
    }
    .color_click{
        color: #c2e6f1;
        background-color: #61b3cc;
    }
    .stuMsg{
        margin-left: 100px;
    }
    .userInfo{
        float:right;
    }
    .el-menu-item{
        font-size: 16px;
    }
    .active_index{
        font-weight: 600;
    }
    .forumTop{
        margin-left: 87px;
    }
    .titleTL{
        float: left;
        font-size: 25px;
        font-weight: 900;
        margin-left: 87px;
        margin-top: 11px;
        /* font-family: "Goudy Bookletter 1911", sans-serif; */
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
