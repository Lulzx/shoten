const fastify = require("fastify")({ logger: false });
const libgen = require("libgen");
const perf = require("execution-time")();

// Declare a route
fastify.get("/", async (request, reply) => {
  return { hello: "darkness" };
});

fastify.get("/:search", async (request, reply) => {
  perf.start("apiCall");

  const searchQuery = request.params.search;

  const options = {
    mirror: "https://libgen.be",
    query: searchQuery,
    count: 20,
  };
  const results = [];

  try {
    const data = await libgen.search(options);
    console.log(data);
    let n = data.length;

    while (n--) {
      // const md5 = data[n].md5;
      // const url = await libgen.utils.check.canDownload(md5);
      // console.log('Working link: ' + url);

      const searchResult = {
        title: data[n].title,
        author: data[n].author,
        year: data[n].year,
        pages: data[n].pages,
        publisher: data[n].publisher,
        download:
          "http://library.lol/main/" + data[n].md5.toLowerCase(),
        // directDownload: url,
        extension: data[n].extension,
      };
      results.push(searchResult);
    }
    const tick = perf.stop("apiCall");
    console.log(tick.time); // in milliseconds
    console.log(tick.preciseWords); // in words
    reply.send(results);
  } catch (err) {
    return console.error(err);
  }
});

fastify.get("/atomic", async (request, reply) => {
  //   const urlString = await libgen.mirror();
  //   console.log(`${urlString} is currently fastest`);

  const options = {
    mirror: "http://libgen.is",
    query: "atomic habits",
    count: 5,
  };
  const results = [];

  try {
    const data = await libgen.search(options);
    let n = data.length;
    // console.log('top ' + n + ' results for "' +
    //             options.query + '"');
    while (n--) {
      // console.log('***********');
      // console.log('Title: ' + data[n].title);
      // console.log('Author: ' + data[n].author);
      // console.log('Download: ' +
      //             'http://gen.lib.rus.ec/book/index.php?md5=' +
      //             data[n].md5.toLowerCase());

      const searchResult = {
        title: data[n].title,
        author: data[n].author,
        download:
          "http://gen.lib.rus.ec/book/index.php?md5=" +
          data[n].md5.toLowerCase(),
      };
      results.push(searchResult);
    }
    reply.send(results);
  } catch (err) {
    return console.error(err);
  }
});

// Run the server!
const start = async () => {
  try {
    await fastify.listen(3000);
    fastify.log.info(
      `server listening on ${fastify.server.address().port}`
    );
  } catch (err) {
    fastify.log.error(err);
    process.exit(1);
  }
};
start();
