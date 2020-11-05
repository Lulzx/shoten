<script>
  import { metatags } from "@roxi/routify";
  metatags.title = "Shoten Search";
  metatags.description = "Book search engine";
  import { Button, InlineLoading } from "carbon-components-svelte";
  import { onDestroy } from "svelte";
  import { Content } from "carbon-components-svelte";
  import { Search } from "carbon-components-svelte";
  import { DataTable } from "carbon-components-svelte";
  import { Row, Column } from "carbon-components-svelte";
  import { Form } from "carbon-components-svelte";
  import { DataTableSkeleton } from "carbon-components-svelte";
  import Search32 from "carbon-icons-svelte/lib/Search32";
  let query = "ikigai";
  let rows = [];
  const search = async () => {
    state = "active";
    let url = "https://lulzx.herokuapp.com/query/" + query;
    let response = await fetch(url);
    let data = await response.json();
    rows = data.results;
    state = "dormant";
  };

  const descriptionMap = {
    active: "searching...",
    finished: "found!",
  };

  const stateMap = {
    active: "finished",
    finished: "dormant",
  };

  let timeout = undefined;
  let state = "dormant";

  function reset(incomingState) {
    if (typeof timeout === "number") {
      clearTimeout(timeout);
    }

    if (incomingState) {
      timeout = setTimeout(() => {
        state = incomingState;
      }, 2000);
    }
  }

  onDestroy(reset);

  $: reset(stateMap[state]);
</script>

<div class="h-screen w-full">
  <Content style="background: none; padding: 1rem">
    <Form on:submit={search}>
      <Row>
        <Column>
          <Search bind:value={query} />
        </Column>
        <Column>
          {#if state !== 'dormant'}
            <InlineLoading status={state} description={descriptionMap[state]} />
          {:else}
            <Button icon={Search32} on:click={search} type="submit">
              Search
            </Button>
          {/if}
        </Column>
      </Row>
    </Form>
    {#if state === 'active'}
      <DataTableSkeleton
        headers={['Title', 'Author', 'Publisher', 'Year', 'Size']}
        rows={3} />
    {:else}
      <DataTable
        sortable
        zebra
        on:click:row={({ detail }) => {
          console.log(detail);
          const str = detail.download;
          const words = str.split('main/');
          const hash = words[1];
          const url = window.location.href + "book?id=" + hash
          window.open(url);
        }}
        title="Search Results"
        description="The following are results for your query."
        headers={[{ key: 'title', value: 'Author' }, { key: 'author', value: 'Title' }, { key: 'publisher', value: 'Publisher' }, { key: 'year', value: 'Year' }, { key: 'size', value: 'Size' }]}
        {rows}>
        <!-- <span slot="cell" let:cell>
          {#if cell.key === 'download'}
            <Link
              inline
              href="https://en.wikipedia.org/wiki/Round-robin_DNS"
              target="_blank">
              {cell.value}
            </Link>
          {:else}{cell.value}{/if}
        </span> -->
      </DataTable>
    {/if}
  </Content>
</div>
