<script>
  import { metatags } from "@roxi/routify";
  metatags.title = "Shoten Search";
  metatags.description = "Book search engine";
  import { Content } from "carbon-components-svelte";
  import { Search } from "carbon-components-svelte";
  import { DataTable } from "carbon-components-svelte";
  import { Form } from "carbon-components-svelte";
  import { DataTableSkeleton } from "carbon-components-svelte";
  let query = "";
  let rows = [];
  let state = "onload";
  const search = async () => {
    state = "loading";
    let url = "https://lulzx.herokuapp.com/query/" + query;
    let response = await fetch(url);
    let data = await response.json();
    rows = data.results;
    state = "completed";
  };
</script>

<div class="h-screen w-full">
  <Content style="background: none; padding: 1rem">
    <Form on:submit={search}>
      <Search bind:value={query} placeholder="type book name..." />
    </Form>
    {#if state === "loading"}
      <DataTableSkeleton
        headers={["Author", "Title", "Publisher", "Year", "Size"]}
        rows={3} />
    {:else if state === "onload"}
      <hr />
    {:else}
      <DataTable
        sortable
        zebra
        on:click:row={({ detail }) => {
          let str = detail.download,
            hash = str.split("main/")[1],
            url = window.location.href + "book?id=" + hash;
          window.open(url);
        }}
        title="Search Results"
        description="The following are results for your query."
        headers={[{ key: "title", value: "Author" }, { key: "author", value: "Title" }, { key: "publisher", value: "Publisher" }, { key: "year", value: "Year" }, { key: "size", value: "Size" }]}
        {rows} />
    {/if}
  </Content>
</div>
