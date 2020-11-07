<script>
  import { metatags } from "@roxi/routify";
  metatags.title = "Shoten Search";
  metatags.description = "Book search engine";
  import { Content } from "carbon-components-svelte";
  import { Search } from "carbon-components-svelte";
  import { DataTable, DataTableSkeleton } from "carbon-components-svelte";
  import { Form } from "carbon-components-svelte";
  import { FormGroup } from "carbon-components-svelte";
  import { Header } from "carbon-components-svelte";
  import { ToggleSmall } from "carbon-components-svelte";
  import { ContentSwitcher, Switch } from "carbon-components-svelte";
  import { getContext } from "svelte";
  import Theme from "./components/Theme.svelte";
  const ctx = getContext("Theme");

  $: if (ctx) {
    ctx.dark.subscribe((value) => {
      console.log("dark mode?", value);
    });
    ctx.light.subscribe((value) => {
      console.log("light mode?", value);
    });
    ctx.updateVar("--cds-productive-heading-06-font-size", "4rem");
  }
  let theme = "g10";
  let dark = false;
  function toggle_theme() {
    theme = dark ? "g10" : "g100";
  }
  let query = "";
  let rows = [];
  let state = "onload";
  let type = "title";
  let types = ["title", "author", "publisher", "year"];
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
    shown = data.results.length;
    total = data.count;
    state = "completed";
  };
</script>

<Theme persist bind:theme>
  <Header company="Shoten" platformName="Book Search Engine" href="/">
    <ToggleSmall
      labelA=""
      labelB=""
      bind:toggled={dark}
      on:change={toggle_theme} />
  </Header>
  <Content style="background: none; padding: 1rem">
    <Form on:submit={search}>
      <Search
        bind:value={query}
        placeholder="type book {type}..."
        autofocus="true" />
    </Form>
    <FormGroup legendText="Filter (fields)">
      <ContentSwitcher selectedIndex={types.indexOf(type)} light="true">
        {#each types as k}
          <Switch text={k} on:click={() => (type = k)} />
        {/each}
      </ContentSwitcher>
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
        headers={headers.map((x) => ({ key: x.toLowerCase(), value: x }))}
        {rows} />
    {/if}
  </Content>
</Theme>
