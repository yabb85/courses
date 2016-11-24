var ExtractTextPlugin = require("extract-text-webpack-plugin");

module.exports = {
	entry: {
		app: [
			'./js/app.js'
		]
	},
	output: {
		path: './app/static/',
		filename: 'app.js'
	},
	module: {
		loaders: [
			{
				test: /\.js$/,
				loader: 'babel',
				exclude: /(node_modules|bower_components)/,
				query: {
					presets: ['react', 'es2015'],
					comments: false
				}
			}
		]
	},
	plugins: [
	]
}
