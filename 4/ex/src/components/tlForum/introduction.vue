<template>
    <div class="introductionContainer">
        <div class="introductionText">
            <p class="introTittle">
                图灵问答实验
            </p>
            <br/>
            <p>
                1.可以在论坛中发帖，也可以在贴子下进行评论（也会有AI在贴子下进行评论）。
                <br/>
                <br/>
                2.选择一条评论（不能是自己发布的），选择截止时间并发起投票活动，可以在投票界面看到自己发起的投票活动，也可以看到别人发起的投票活动。
                <br/>
                <br/>
                3.在投票界面，可以选择自己发起的或别人发起的正在进行中的投票活动，根据帖子内容和用户的评论内容，推测发表该评论的用户是‘人’还是‘AI’，并进行投票。
                <br/>
                <br/>
                4.投票活动截止后，将会公布正确答案，实验到此便完成了。
                <br/>
                <br/>
                5.实验完成后，投票页面将会出现提交实验报告的按钮，点击后可以查看本次实验的实验数据，输入实验心得后便可提交实验报告。
            </p>
        </div>
    </div>
</template>

<script>
    export default {
        data() {
            return {

            }
        },
        created() {
            
        },
        methods:{
            
        }
    }

</script>

<style scoped>
    .introductionText{
        width: 603px;
        /* height: 300px; */
        background-color: #fff;
        opacity: 0.75;
        margin-left: 27%;
        box-shadow: 0 2px 4px rgba(0, 0, 0, .12), 0 0 6px rgba(0, 0, 0, .04);

        height: auto;  
        word-wrap:break-word;  
        word-break:break-all;  
        overflow: hidden;
        padding: 50px;
        font-size: 20px;
    }
    .introTittle{
        font-weight: 900;
        font-size: 25px;
    }
</style>
