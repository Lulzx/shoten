<script>
  import { metatags } from "@roxi/routify";
  metatags.title = "Shoten Search";
  metatags.description = "Book search engine";
  import { Content } from "carbon-components-svelte";
  import { Search } from "carbon-components-svelte";
  import { DataTable } from "carbon-components-svelte";
  import { Form } from "carbon-components-svelte";
  import { FormGroup } from "carbon-components-svelte";
  import {
    Header,
    HeaderUtilities,
    HeaderGlobalAction,
  } from "carbon-components-svelte";
  import { ContentSwitcher, Switch } from "carbon-components-svelte";
  import { getContext } from "svelte";
  import Theme from "./components/Theme.svelte";
  import { Icon } from "carbon-components-svelte";
  import Sun24 from "carbon-icons-svelte/lib/Sun24";
  import Moon24 from "carbon-icons-svelte/lib/Moon24";
  import UserProfile24 from "carbon-icons-svelte/lib/UserProfile24";
  import Network_224 from "carbon-icons-svelte/lib/Network_224";
  import Calendar24 from "carbon-icons-svelte/lib/Calendar24";
  import InformationSquare24 from "carbon-icons-svelte/lib/InformationSquare24";
  import { PaginationNav } from "carbon-components-svelte";

  let icons = [InformationSquare24, UserProfile24, Network_224, Calendar24];
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
  let theme_icon = Sun24;
  function toggle_theme() {
    theme = dark ? "g10" : "g100";
    theme_icon = dark ? Sun24 : Moon24;
    dark = !dark;
  }
  let page = 0;
  let pages = 1;
  let current_query = "";
  let rows = [];
  let state = "onload";
  let type = "title";
  let types = ["title", "author", "publisher", "year"];
  let headers = [...types, "size", "extension"];
  let previous_page = 0;
  let previous_query = "";
  let shown, total;
  const search = async () => {
    state = "loading";
    let current_page = page + 1;
    if (!page) {
      current_page = 1;
    }
    if (previous_page === current_page && previous_query === current_query) {
      state = "completed";
      return;
    }
    if (previous_query != current_query) {
      current_page = 1;
      page = 0;
    }
    let base_url = "https://lulzx.herokuapp.com/query/";
    let url = base_url + type + "/" + current_query + "/" + current_page;
    let response = await fetch(url);
    let data = await response.json();
    rows = data.results;
    shown = data.results.length;
    total = data.count;
    if (total <= 25) {
      pages = 1;
    } else {
      pages = parseInt(total / 25);
    }
    previous_page = current_page;
    previous_query = current_query;
    state = "completed";
  };
</script>

<style>
  :global(.bx--header) {
    background-color: #161616;
  }
  :global(.bx--content-switcher-btn:focus) {
    box-shadow: inset 0 0 0 2px #ffffff;
  }
  :global(.bx--content-switcher--light .bx--content-switcher-btn) {
    background-color: var(--cds-ui-01, #ffffff);
  }
  :global(.bx--content-switcher--light
      .bx--content-switcher-btn.bx--content-switcher--selected) {
    color: var(--cds-inverse-01, #ffffff);
    background-color: var(--cds-ui-05, #161616);
  }
  :global(.bx--content-switcher--dark
      .bx--content-switcher-btn.bx--content-switcher--selected) {
    color: var(--cds-inverse-01, #000000);
    background-color: var(--cds-ui-05, #161616);
  }
  :global(.bx--header__action) {
    padding: revert;
  }
  :global(.bx--header__action:focus) {
    border-color: #161616;
  }
  :global(.bx--header__action:hover) {
    background-color: #161616;
  }
</style>

{#if ['onload', 'completed'].includes(state)}
  <Theme persist bind:theme>
    <Header company="Shoten" platformName="Book Search Engine" href="/">
      <HeaderUtilities>
        <HeaderGlobalAction icon={theme_icon} on:click={toggle_theme} />
      </HeaderUtilities>
    </Header>
    <Content style="background: none; padding: 1rem">
      <Form on:submit={search}>
        <Search
          bind:value={current_query}
          placeholder="type book {type}..."
          autofocus="true" />
      </Form>
      <FormGroup legendText="Filter (fields)">
        <ContentSwitcher selectedIndex={types.indexOf(type)} light="true">
          {#each types as k}
            <Switch on:click={() => (type = k)}>
              <div style="display: flex; align-items: center;">
                <Icon
                  render={icons[types.indexOf(k)]}
                  style="margin-right: 0.5rem;" />
                {k}
              </div>
            </Switch>
          {/each}
        </ContentSwitcher>
      </FormGroup>
      <!-- <DataTableSkeleton {headers} rows={3} /> -->
      {#if state === 'completed'}
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
          headers={headers.map((x) => ({ key: x, value: x }))}
          {rows} />
        <PaginationNav
          bind:page
          on:change={search}
          total={pages}
          on:click:button--previous={page}
          on:click:button--next={page}
          loop="true" />
      {/if}
    </Content>
  </Theme>
{:else if state === 'loading'}
  <div id="search" />
{/if}
