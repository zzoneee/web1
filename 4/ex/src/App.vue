<template>
  <div id="app">
    <router-view/>
  </div>
</template>

<script>

</script>

<style>

  *{
    margin: 0;
    padding: 0;
    /* font-size: 14px; */
    letter-spacing: 0.35px;
    font-family:-apple-system,BlinkMacSystemFont, Segoe UI,
    Roboto,PingFang SC,Hiragino Sans GB,Microsoft YaHei,
    Helvetica Neue,Helvetica,Arial,sans-serif
  }
  a,a:hover,a:focus{
      text-decoration: none;
  }
  .icon_top{
    vertical-align: bottom;
  }
  .icon_6_l{
    margin-left: 6px;
  }
  ul, ol {
    margin: 0;
  }
  ul,li{
    list-style: none;
  }

  /* 去掉抽屉黑框 */
  .el-drawer /deep/ :focus {
    outline: none;
  }
  .el-drawer:focus {
    outline: none;
  }

</style>
