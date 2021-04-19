<template>
    <div class="error">
        <!-- <div class="img">
            <img src="../../assets/error_page.png">
        </div> -->
        <el-button class='jumpBtn' @click="toLogin" type="primary" plain>马上登录！</el-button>
    </div>
</template>

<script>
    
    export default {
        data() {
            return {
                
            }
        },
        methods:{
            toLogin() {
                this.$router.push({path:'/'});
            }
        }
    }

</script>

<style scoped>
    .jumpBtn{
        position: absolute;
        left: 430px;
        top:540px;
    }
    .error{
        margin:0 auto;
        position:fixed;
        top:0;
        left:0;
        width: 100%;
        height:100%;
        min-width: 1000px;
        zoom:1;
        background: url('../../assets/error_page.png');
        background-repeat: no-repeat;
        background-size: cover;
        -webkit-background-size: cover;
        -o-background-size: cover;
        background-position: center 0;
    }
</style>
