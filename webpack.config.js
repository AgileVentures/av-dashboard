var ManifestPlugin = require('webpack-manifest-plugin');
var path = require('path');

module.exports = {
  entry: { main: './src/index.js' },
  output: {
    path: path.resolve(__dirname, 'av_dashboard/static'),
    filename: 'main.js'
  },
  module: {
    rules: [
      {
        test: /\.js$/,
        exclude: /node_modules/,
        use: {
          loader: "babel-loader"
        }
      }
    ]
  },
  plugins: [
    new ManifestPlugin({fileName: './webpack-manifest.json'})
  ]
};
