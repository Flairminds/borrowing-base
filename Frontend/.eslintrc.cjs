module.exports = {
	parserOptions: {
		ecmaVersion: "latest",
		sourceType: "module",
		ecmaFeatures: {
			jsx: true
		}
	},
	extends: [
		'eslint:recommended',
		'plugin:import/errors',
		'plugin:import/warnings',
		'plugin:react/recommended'
	],
	plugins: ['react', '@stylistic/js', 'eslint-plugin-no-comments', 'css-modules'],
	globals: {
		JSX: true
	},
	env: {
		es6: true,
		browser: true,
		node: true
	},
	ignorePatterns: ['placeholders', 'vite.config.js'],
	rules: {
		'no-unreachable': 'error',
		'no-func-assign': 'error',
		'no-undef': 'error',
		'no-empty': 'error',
		'no-console': ['error', { allow: ['warn', 'error', 'info'] }],
		'camelcase': 'error',
		'prefer-const': ['error', { destructuring: 'all', ignoreReadBeforeAssign: true }],
		'@stylistic/js/arrow-spacing': "error",
		'@stylistic/js/function-call-spacing': ["error", "never"],
		'@stylistic/js/keyword-spacing': ["error", { "before": true }],
		'@stylistic/js/key-spacing': ["error", { "beforeColon": false }],
		'@stylistic/js/no-mixed-spaces-and-tabs': "error",
		'@stylistic/js/semi': ["error", "always"],
		'@stylistic/js/no-trailing-spaces': "error",
		// 'no-comments/disallowComments': ['error', { allow: ['NOTE:', 'TODO:', 'INFO:', 'DEPR:'] }],
		'@stylistic/js/indent': ["error", "tab"],
		'@stylistic/js/space-infix-ops': "error",
		'@stylistic/js/space-unary-ops': "error",
		'@stylistic/js/comma-spacing': ["error", { "before": false, "after": true }],
		'@stylistic/js/block-spacing': "error",
		'@stylistic/js/space-before-blocks': "error",
		'@stylistic/js/brace-style': "error",
		'@stylistic/js/comma-dangle': ["error", "never"],
		'@stylistic/js/no-multi-spaces': "error",
		'@stylistic/js/semi-spacing': "error",
		'import/extensions': ['error', 'never'],
		'react/jsx-filename-extension': [1, { extensions: ['.tsx', '.jsx'] }],
		'import/no-cycle': ['off', { maxDepth: null }],
		'react/prop-types': 0,
		'import/order': ['error', {
			groups: ['builtin', 'external', 'internal', 'parent', 'sibling', 'index', 'object', 'type'],
			warnOnUnassignedImports: true,
			alphabetize: {
				order: 'asc',
				caseInsensitive: true
			}
		}]
	},
	settings: {
		'react': {
			"version": "detect"
		},
		'import/resolver': {
			node: {
				extensions: ['.tsx', '.mjs', '.ts', '.json', '.jsx', '.js']
			}
		},
		'import/extensions': ['.ts', '.mjs', '.tsx', '.json']
	}
};