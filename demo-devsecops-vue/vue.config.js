module.exports = {
  lintOnSave: false,
  devServer: {
    disableHostCheck: true,
    proxy: {
      "/api": {
        target: "http://122.9.67.46:8080/",
        ws: true,
        changeOrigin: true,
        // pathRewrite: {
        //   '^/api': ''
        // }
      },
    },
  },
};
