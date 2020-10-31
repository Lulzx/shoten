<script>
  import { metatags } from '@roxi/routify'
  metatags.title = 'Bruh'
  metatags.description = 'Description coming soon...'
  import { Button } from "carbon-components-svelte";
  import { ComboBox } from "carbon-components-svelte";
  import { Content } from "carbon-components-svelte";
  import { Select, SelectItem } from "carbon-components-svelte";
  import {Header} from "./components/Header.svelte";
  import {Theme} from "./components/Theme.svelte";
  import { Search } from "carbon-components-svelte";
  import { PaginationNav } from "carbon-components-svelte";
  import { InlineLoading } from "carbon-components-svelte";
  import { DataTable } from "carbon-components-svelte";
  import { Grid, Row, Column } from "carbon-components-svelte";
  import { Form } from "carbon-components-svelte";
  import { TextArea } from "carbon-components-svelte";
  // import libgen from 'libgen'; REPLACE with FastApi
  let theme = "g10";
  let query = "";
  let text = "here we will see the result";
  let rows = [
    {
      id: "a",
      name: "Book 3",
      author: "Human",
      year: 3000,
      cost: 100,
      addDate: "2020-10-21",
    },
    {
      id: "b",
      name: "Book 1",
      author: "Human",
      year: 443,
      cost: 200,
      addDate: "2020-09-10",
    },
    {
      id: "c",
      name: "Book 2",
      author: "Human",
      year: 80,
      cost: 150,
      addDate: "2020-11-24",
    },
    {
      id: "d",
      name: "Book 6",
      author: "Human",
      year: 3000,
      cost: 250,
      addDate: "2020-12-01",
    },
    {
      id: "e",
      name: "Book 4",
      author: "Human",
      year: 443,
      cost: 550,
      addDate: "2021-03-21",
    },
    {
      id: "f",
      name: "Book 5",
      author: "Human",
      year: 80,
      cost: 400,
      addDate: "2020-11-14",
    },
  ];
  const search = async () => {
    alert(query);
    text = query;
    return // TODO
    const options = {
      mirror: "http://gen.lib.rus.ec",
      query: query,
      count: 20,
      sort_by: "title",
      reverse: false,
    };
    const data = await libgen.search(options);

    for (let item of data) {
      const url = `http://libgen.rs/covers/${item.coverurl}`;
      text += url;
      console.log(
        `Title: ${item.title}\nYear: ${item.year}\nAuthor: ${item.author}\nDownload: ${url}`
      );
      text += `Title: ${item.title}\nYear: ${item.year}\nAuthor: ${item.author}\nDownload: ${url}`;
    }
  };
</script>

<div class="h-screen w-full">
  <Content style="background: none; padding: 1rem">
    <Form on:submit={search}>
      <Row>
        <Column>
            <Search bind:value={query} />
        </Column>
        <Column>
            <Button type="submit">Submit</Button>
        </Column>
      </Row>
    </Form>
    <TextArea labelText="App description" placeholder="Enter a description..." bind:value={text}/>
    <Grid>
      <Row>
        <Column style="outline: 0px solid var(--cds-interactive-04)">
          <InlineLoading status="active" description="Searching..." />
        </Column>
        <Column style="outline: 0px solid var(--cds-interactive-04)">
          <InlineLoading status="finished" description="Found" />
        </Column>
        <Column style="outline: 0px solid var(--cds-interactive-04)">
          <InlineLoading status="error" description="Not found" />
        </Column>
      </Row>
    </Grid>
    <DataTable
      sortable
      title="Search Results"
      description="The following are results for your query."
      headers={[{ key: 'name', value: 'Name' }, { key: 'author', value: 'Author' }, { key: 'year', value: 'Year' }, { key: 'cost', value: 'Cost', display: (cost) => cost + ' €' }, { key: 'addDate', value: 'Add date', display: (date) => new Date(date).toLocaleString(), sort: (a, b) => (new Date(a) <= new Date(b) ? -1 : 1) }]}
      {rows} />
    <PaginationNav total={3} loop />
  </Content>
</div>