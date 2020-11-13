const cssnano = require('cssnano')({ preset: 'default' });

const production = process.env.NODE_ENV === 'production';

module.exports = {
  plugins: [
    require('autoprefixer'),
    ...(production ? [cssnano] : []),
  ],
};