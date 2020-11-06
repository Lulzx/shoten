<script>
  import { metatags } from "@roxi/routify";
  metatags.title = "Shoten Search";
  metatags.description = "Book search engine";
  import { Content } from "carbon-components-svelte";
  import { Search } from "carbon-components-svelte";
  import { DataTable } from "carbon-components-svelte";
  import { Form } from "carbon-components-svelte";
  import { DataTableSkeleton } from "carbon-components-svelte";
  import {
    FormGroup,
    RadioButtonGroup,
    RadioButton,
  } from "carbon-components-svelte";
  let query = "";
  let rows = [];
  let state = "onload";
  let type = "title";
  let types = ["author", "title", "publisher", "year"];
  let headers = [...types, "size"].map(
    (x) => x.charAt(0).toUpperCase() + x.slice(1)
  );
  let shown, total;
  const search = async () => {
    state = "loading";
    let base_url = "https://lulzx.herokuapp.com/query/";
    let url = base_url + type + "/" + query;
    let response = await fetch(url);
    let data = await response.json();
    rows = data.results;
    shown = data.results.length
    total = data.count;
    state = "completed";
  };
</script>

<div class="h-screen w-full">
  <Content style="background: none; padding: 1rem">
    <Form on:submit={search}>
      <Search
        bind:value={query}
        placeholder="type book {type}..."
        autofocus="true" />
    </Form>
    <FormGroup legendText="Filter (fields)">
      <RadioButtonGroup labelPosition="right" selected={type}>
        {#each types as k}
          <RadioButton labelText={k} value={k} on:change={() => (type = k)} />
        {/each}
      </RadioButtonGroup>
    </FormGroup>
    {#if state === 'loading'}
      <DataTableSkeleton {headers} rows={3} />
    {:else if state === 'onload'}
      <hr />
    {:else}
      <DataTable
        sortable
        zebra
        on:click:row={({ detail }) => {
          let str = detail.download,
            hash = str.split('main/')[1],
            url = window.location.href + 'book?id=' + hash;
          window.open(url);
        }}
        title="Search Results"
        description="Displaying {shown} out of {total} results for your query."
        headers={headers.map(x => ({key: x.toLowerCase(), value:  x }))}
        {rows} />
    {/if}
  </Content>
</div>
