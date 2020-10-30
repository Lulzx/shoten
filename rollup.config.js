import skypack from 'rollup-plugin-skypack';
 
module.exports = {
  input: 'src/index.js',
  output: {
    format: 'es',
  },
  plugins: [
    skypack({
      modules: ['libgen'],
      optimize: true,
    }),
  ],
};