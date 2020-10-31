const fastify = require('fastify')({ logger: true })
const libgen = require('libgen');

// Declare a route
fastify.get('/', async (request, reply) => {
  return { hello: 'darkness' }
})

fastify.get('/:search', async (request, reply) => {
  
  const searchQuery = request.params.search;

    const options = {
      mirror: "http://gen.lib.rus.ec",
      query: searchQuery,
      count: 20
    }
    const results = [];
  
    try {

      const data = await libgen.search(options)
      let n = data.length;

      while (n--){

        // const md5 = data[n].md5;
        // const url = await libgen.utils.check.canDownload(md5);
        // console.log('Working link: ' + url);

        const searchResult = {
          title: data[n].title,
          author: data[n].author,
          year: data[n].year,
          pages: data[n].pages,
          download: 'http://gen.lib.rus.ec/book/index.php?md5=' + data[n].md5.toLowerCase(),
          // directDownload: url,
          extension: data[n].extension
        }
        results.push(searchResult);
      }
      reply.send(results);
    } catch (err) {
      return console.error(err)
    }
  });


fastify.get('/atomic', async (request, reply) => {

  //   const urlString = await libgen.mirror();
  //   console.log(`${urlString} is currently fastest`);

    const options = {
      mirror: 'http://libgen.is',
      query: 'atomic habits',
      count: 5
    }
    const results = [];
  
    try {

      const data = await libgen.search(options)
      let n = data.length;
      // console.log('top ' + n + ' results for "' +
      //             options.query + '"');
      while (n--){
        // console.log('***********');
        // console.log('Title: ' + data[n].title);
        // console.log('Author: ' + data[n].author);
        // console.log('Download: ' +
        //             'http://gen.lib.rus.ec/book/index.php?md5=' +
        //             data[n].md5.toLowerCase());

        const searchResult = {
          title: data[n].title,
          author: data[n].author,
          download: 'http://gen.lib.rus.ec/book/index.php?md5=' + data[n].md5.toLowerCase()
        }
        results.push(searchResult);
      }
      reply.send(results);
    } catch (err) {
      return console.error(err)
    }
  });


// Run the server!
const start = async () => {
  try {
    await fastify.listen(3000)
    fastify.log.info(`server listening on ${fastify.server.address().port}`)
  } catch (err) {
    fastify.log.error(err)
    process.exit(1)
  }
}
start()