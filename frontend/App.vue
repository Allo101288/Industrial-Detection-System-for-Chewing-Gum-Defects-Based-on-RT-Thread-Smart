<script>
export default {
  onLaunch: function () {
    console.log("App Launch");
    window.addEventListener("beforeunload", () => {
      console.log("H5 页面即将关闭");
      uni.removeStorageSync("token"); // 清除 token
    });
  },
  onShow: function () {
    console.log("App Show");
  },
  onHide: function () {
    console.log("App Hide");
  },
};
</script>

<style>
/*每个页面公共css */
</style>
