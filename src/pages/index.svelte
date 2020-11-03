<script>
  import { metatags } from "@roxi/routify";
  metatags.title = "Shoten Search";
  metatags.description = "Description coming soon...";
  import { Button, InlineLoading } from "carbon-components-svelte";
  import { onDestroy } from "svelte";
  import { Content } from "carbon-components-svelte";
  import { Search } from "carbon-components-svelte";
  import { DataTable } from "carbon-components-svelte";
  import { Row, Column } from "carbon-components-svelte";
  import { Form } from "carbon-components-svelte";
  import { DataTableSkeleton } from "carbon-components-svelte";
  let query = "da vinci";
  let rows = [];
  const search = async () => {
    state = 'active';
    let url = "https://lulzx.herokuapp.com/query/" + query;
    let response = await fetch(url);
    let data = await response.json();
    rows = data.results;
    state = 'dormant';
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
            <Button on:click={search} type="submit">
              Submit
            </Button>
          {/if}
        </Column>
      </Row>
    </Form>
    {#if state === 'active'}
      <DataTableSkeleton
        headers={['Title', 'Author', 'Publisher', 'Year', 'Size', 'Download']}
        rows={3} />
    {:else}
      <DataTable
        sortable
        zebra
        title="Search Results"
        description="The following are results for your query."
        headers={[{ key: 'title', value: 'Title' }, { key: 'author', value: 'Author' }, { key: 'publisher', value: 'Publisher' }, { key: 'year', value: 'Year' }, { key: 'size', value: 'Size' }, { key: 'download', value: 'Download' }]}
        {rows}>
        <!-- <span slot="cell" let:row let:cell>
          {#if cell.key === 'download'}
            <Link inline href={cell.value} target="_blank">
              Download
              <Launch16 />
            </Link>
          {:else}{cell.value}{/if}
        </span> -->
      </DataTable>
    {/if}
    <!-- <PaginationNav total={3} loop /> -->
  </Content>
</div>
