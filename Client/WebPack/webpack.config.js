const path = require('path')
const MiniCssExtractPlugin = require('mini-css-extract-plugin')
const { CleanWebpackPlugin } = require('clean-webpack-plugin');

 module.exports = {
    mode : "development",
    entry : "./src/index.js",
    output : {
        filename : "[name]-[contenthash].js",
        path : path.resolve(__dirname , "dist")
    },
    module : {
        rules : [
            {
                test : /\.js$/i,  
                exclude : /(node_modules | bower_components)/,               
                use : {
                    loader : 'babel-loader',                     
                    options : {
                        presets : ['@babel/preset-env']
                    }
                }
            },
            {
                test : /\.tsx$/,                       
                exclude : /(node_modules | bower_components)/,         
                use : {
                    loader : 'ts-loader'
                }
            },
            {
                test : /\.css$/i,
                use : [ 
                    MiniCssExtractPlugin.loader
                ]
            }
        ]
    },
    plugins : [
        new CleanWebpackPlugin(),        
        new MiniCssExtractPlugin({ filename : 'application.css' })
    ]
 }