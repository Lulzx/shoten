const cssnano = require("cssnano")({ preset: "advanced" });

export default (options) => {
  const plugins = [require("autoprefixer"), cssnano];
  return plugins;
};
