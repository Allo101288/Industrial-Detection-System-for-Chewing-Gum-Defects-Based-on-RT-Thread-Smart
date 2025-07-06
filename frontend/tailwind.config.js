/** @type {import('tailwindcss').Config} */
module.exports = {
	separator: '__', // 如果是小程序项目需要设置这一项，将 : 选择器替换成 __，之后 hover:bg-red-500 将改为 hover__bg-red-500  
	corePlugins: {
		// 预设样式  
		preflight: false, // 一般uniapp都有预设样式，所以不需要tailwindcss的预设  

		// 以下功能小程序不支持  
		space: false, // > 子节点选择器  
		divideWidth: false,
		divideColor: false,
		divideStyle: false,
		divideOpacity: false,
	},

	// 指定要处理的文件  
	content: [
		'./pages/**/*.{vue,js}',
		'./main.js',
		'./App.vue',
		'./index.html'
	],
	theme: {
		// 字号，使用 App.vue 中的 --x-font-size 样式变量配置  
		fontSize(config) {
			const list = ['2xs', 'xs', 'sm', 'base', 'md', 'lg', 'xl', '2xl', '3xl'];
			let result = {}
			list.forEach(it => {
				result[it] = `var(--x-font-size-${it})`
			})
			return result
		},
		extend: {
			// 间距，tailwindcss中默认间距是rem单位，可以统一设置为uniapp的rpx单位。  
			// 类似的设置根据项目需求自己调整一下就好了，没必要去安装别人的预设，其实主要是小程序不兼容的css比较多，H5和App基本都直接兼容tailwindcss默认的预设  
			spacing(config) {
				let result = {
					0: '0'
				}
				// 允许的数值大一些也无所谓，最后打包tailwindcss会摇树优化，未使用的样式并不会打包  
				for (let i = 1; i <= 300; i) {
					result[i] = `${i}rpx`
				}
				return result
			},
			// 增加颜色板，现在主流UI组件库大都是采用css变量实现定制主题，所以这里引用了全局的css变量，这个css变量的定义位置可以在 App.vue 中 page{} 选择器下  
			// 其实tailwindcss只是一个css工具，不必局限于它内部提供的东西，灵活运用css变量这些特性完全可以整合出自己的生产力工具  
			colors: {
				'primary': 'var(--x-color-primary)',
				'tips': 'var(--x-color-tips)'
			},
		},
	},
	plugins: [],
}