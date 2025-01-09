const path = require('path');
const { plugin } = require('postcss');

module.exports = {
  root: true,
  extends: ['plugin:vinta/recommended', 'airbnb', 'plugin: react/recommended' ],
  rules: {
    "default-param-last": "off",  // due to initialState in Redux
    "@babel/camelcase": "off"
  },
  parserOptions: {
    ecmaFeatures: {
      jsx: true,
    },
    ecmaVersion: 12,
    sourceType: 'module',
  },
  plugins: [
    'react',
  ],
  
  env: {
    es6: true,
    browser: true,
    jest: true
  },
  settings: {
    'import/resolver': {
      webpack: {
        config: path.join(__dirname, '/webpack.config.js'),
        'config-index': 1
      }
    },
    react: {
      "version": "detect"
    },
  }
}
