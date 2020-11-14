<script>
  import { metatags } from "@roxi/routify";
  metatags.title = "Shoten Search";
  metatags.description = "Book search engine";
  import Theme from "./components/Theme.svelte";
  import {
    Icon,
    Form,
    Switch,
    Header,
    Search,
    Content,
    DataTable,
    FormGroup,
    PaginationNav,
    ContentSwitcher,
    HeaderUtilities,
    HeaderGlobalAction,
  } from "carbon-components-svelte";
  import Sun24 from "carbon-icons-svelte/lib/Sun24";
  import Moon24 from "carbon-icons-svelte/lib/Moon24";
  import UserProfile24 from "carbon-icons-svelte/lib/UserProfile24";
  import Network_224 from "carbon-icons-svelte/lib/Network_224";
  import Calendar24 from "carbon-icons-svelte/lib/Calendar24";
  import InformationSquare24 from "carbon-icons-svelte/lib/InformationSquare24";
  import { onMount } from "svelte";

  let ref;
  let theme;
  let page = 0;
  let pages = 1;
  let rows = [];
  let shown, total;
  let type = "title";
  let state = "onload";
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
    if (window.matchMedia) {
      const darkModeOn = window.matchMedia("(prefers-color-scheme: dark)");
      if (darkModeOn.matches) {
        theme = "g100";
        console.log(`Dark mode is ${darkModeOn ? "🌒 on" : "☀️ off"}.`);
      }
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
  function header_href() {
    if (typeof window != "undefined") {
      return "javascript:history.go()";
    }
    return "/";
  }
  onMount(async () => {
    if (typeof window != "undefined") {
      let url = "https://lulzx.herokuapp.com/";
      let res = await fetch(url).catch((error) => {
        console.error("Error:", error);
      });
      let data = await res.json();
      if (data.message) {
        console.log("feels good man!");
      }
    }
    ref.focus();
  });
</script>

<style>
  @import url(https://fonts.googleapis.com/css?family=Righteous);

  h1 {
    display: flex;
    top: 0.25em;
    flex-direction: column;
    justify-content: center;
    text-align: center;
    position: relative;
    font-family: "Righteous";
    font-size: 12em;
    text-shadow: 0.03em 0.03em 0 rgb(15, 98, 254);
  }
  h1:after {
    content: attr(data-shadow);
    position: absolute;
    right: 0vw;
    top: 0.06em;
    left: 0.06em;
    z-index: -1;
    text-shadow: none;
    background-image: linear-gradient(
      45deg,
      transparent 45%,
      rgb(51, 51, 51) 45%,
      rgb(44, 44, 44) 55%,
      transparent 0
    );
    background-size: 0.05em 0.05em;
    background-clip: text;
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;

    animation: shad-anim 30s linear infinite;
  }

  @keyframes shad-anim {
    0% {
      background-position: 0 0;
    }
    0% {
      background-position: 100% -100%;
    }
  }
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
      href={header_href()}>
      <HeaderUtilities>
        <HeaderGlobalAction
          aria-label="toggle theme"
          icon={theme_icon}
          on:click={toggle_theme} />
      </HeaderUtilities>
    </Header>
    {#if state === 'onload'}
      <h1 data-shadow="Shoten">Shoten</h1>
    {/if}
    <Content style="background: none; padding: 1rem">
      <Form on:submit={search}>
        <Search
          bind:ref
          bind:value={current_query}
          placeholder="type book {type}..."
          autofocus="true" />
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
              hash = str.split('main/')[1];
            window.location.href += 'book?id=' + hash;
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
