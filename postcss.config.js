const cssnano = require('cssnano')({ preset: 'default' });

const production = true;

export const plugins = [
  require('autoprefixer'),
  ...(production ? [cssnano] : []),
];