const libgen = require("libgen");

const options = {
  mirror: "http://gen.lib.rus.ec",
  query: "da vinci",
  count: 20,
  sort_by: "title",
  reverse: false,
};
const book = async (e) => {
  const data = await libgen.search(options);

  for (let item of data) {
    const url = `http://libgen.rs/covers/${item.coverurl}`;
    console.log(url);
    console.log(
      `Title: ${item.title}\nYear: ${item.year}\nAuthor: ${item.author}\nDownload: ${url}`
    );
  }
};
book();
