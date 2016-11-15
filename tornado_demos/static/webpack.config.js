/**
 * Created by youzipi on 16/4/29.
 */
// webpack.config.js
module.exports = {
    entry: './base.js',
    output: {
        path: "./build",
        publicPath: "/build/",
        filename: "build.js"
    },
};