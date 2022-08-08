const path = require('path')
const htmlWebpackPlugin = require('html-webpack-plugin')

module.exports = {
    mode: 'production',
    entry: {
        "static/js/index": path.resolve(__dirname, 'src/index.js'),
    },
    output: {
        path: path.resolve(__dirname, '../views'),
        filename: '[name][contenthash].js',
        assetModuleFilename: 'static/assets/[name][ext]',
        clean: true
    },
    performance: {
        hints: false,
        maxAssetSize: 512000,
        maxEntrypointSize: 512000
    },
    devServer: {
        port: 9000,
        compress: true,
        hot: true,
        static: {
            directory: path.join(__dirname, 'dist')
        }
    },
    module: {
        rules: [
            {
                test: /\.(png|svg|jpg|jpeg|gif)$/i,
                type: 'asset/resource'
            },
            {
                test: /\.css$/,
                use: ['style-loader', 'css-loader']
            },
            {
                test: /\.js$/,
                exclude: /node_modules/,
                use: {
                    loader: 'babel-loader',
                    options: {
                        cacheDirectory: true,
                        presets:[ "@babel/preset-react"]
                    },
                },
            },
        ]
    },
    plugins: [
        new htmlWebpackPlugin({
            filename: "index.html",
            template: "public/index.html"
        })
    ]
}