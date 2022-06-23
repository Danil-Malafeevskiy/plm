module.exports = {
    publicPath: process.env.NODE_ENV === 'production' ? '/static/dist/' : 'http://localhost:8080',
    outputDir: '../static/dist',
    indexPath: '../../templates/base-vue.html',

    devServer:{
        devMiddleware:{
          writeToDisk : filePath => filePath.endsWith("index.html"),
          headers: {"Acess-Control-Allow-Origin":"*"},
          publicPath: "http://localhost:8080",
        },
        hot: 'only',
    }
}