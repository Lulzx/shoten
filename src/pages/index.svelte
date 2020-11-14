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
  import { onMount } from "svelte";
  
  let ref;
  let theme;
  let page = 0;
  let pages = 1;
  let rows = [];
  let shown, total;
  let type = "title";
  let state = "onload";
  let autofocus = true;
  const themes = ["g10", "g100"];
  let types = ["title", "author", "publisher", "year"];
  let headers = [...types, "size", "extension"];
  let previous_page = 0;
  let current_query = "";
  let previous_query = "";
  let icons = [InformationSquare24, UserProfile24, Network_224, Calendar24];
  const persisted_theme = localStorage.getItem("theme");
  if (themes.includes(persisted_theme)) {
    theme = persisted_theme;
  } else {
    const darkModeOn = window.matchMedia("(prefers-color-scheme: dark)");
    if (darkModeOn.matches) {
      theme = "g100";
      console.log(`Dark mode is ${darkModeOn ? "🌒 on" : "☀️ off"}.`);
    } else {
      theme = "g10";
    }
  }
  let dark = theme === "g100";
  let theme_icon = !dark ? Sun24 : Moon24;
  function toggle_theme() {
    theme = dark ? "g10" : "g100";
    theme_icon = dark ? Sun24 : Moon24;
    dark = !dark;
    ref.focus();
  }
  const search = async () => {
    if (!current_query) {
      return;
    }
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
    let response = await fetch(url).catch((error) => {
      console.error("Error:", error);
    });
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
  onMount(async () => {
    ref.focus();
    let url = "https://lulzx.herokuapp.com/";
    let res = await fetch(url).catch((error) => {
      console.error("Error:", error);
    });
    let data = await res.json();
    if (data.message) {
      console.log("Connection established!");
    }
  });
</script>

<style>
  :global(.bx--header) {
    background-color: #161616;
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
    <Header
      company="Shoten"
      platformName="Book Search Engine"
      href="javascript:history.go(0)">
      <HeaderUtilities>
        <HeaderGlobalAction
          aria-label="toggle theme"
          icon={theme_icon}
          on:click={toggle_theme} />
      </HeaderUtilities>
    </Header>
    <Content style="background: none; padding: 1rem">
      <Form on:submit={search}>
        <Search
          bind:ref
          bind:value={current_query}
          placeholder="type book {type}..."
          bind:autofocus />
      </Form>
      <FormGroup legendText="Filter (fields)">
        <ContentSwitcher selectedIndex={types.indexOf(type)}>
          {#each types as k}
            <Switch
              on:mouseleave={() => {
                ref.focus();
              }}
              on:click={() => {
                type = k;
              }}>
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
