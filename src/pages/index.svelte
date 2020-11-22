<script lang="ts">
  import { metatags } from "@roxi/routify";
  import Theme from "./components/Theme.svelte";
  import {
    Content,
    ContentSwitcher,
    DataTable,
    Form,
    FormGroup,
    Header,
    HeaderGlobalAction,
    HeaderUtilities,
    Icon,
    PaginationNav,
    Search,
    Switch,
    StructuredList,
    StructuredListHead,
    StructuredListRow,
    StructuredListCell,
    StructuredListBody,
    Tag,
  } from "carbon-components-svelte";
  import { onMount } from "svelte";
  import Sun24 from "carbon-icons-svelte/lib/Sun24";
  import Moon24 from "carbon-icons-svelte/lib/Moon24";
  import Calendar24 from "carbon-icons-svelte/lib/Calendar24";
  import Network_224 from "carbon-icons-svelte/lib/Network_224";
  import UserProfile24 from "carbon-icons-svelte/lib/UserProfile24";
  import InformationSquare24 from "carbon-icons-svelte/lib/InformationSquare24";

  metatags.title = "Shoten Search";
  metatags.description = "Book search engine";

  let ref: HTMLInputElement;
  let theme: string;
  let page: any = 0;
  let pages: number = 1;
  let shown: number = 10;
  let rows: any[] = [];
  let total: number;
  let type: string = "title";
  let state: string = "onload";
  let autofocus: boolean = true;
  const themes: string[] = ["g10", "g100"];
  let types: string[] = ["title", "author", "publisher", "year"];
  let headers: string[] = [...types, "size", "extension"];
  let previous_page: number = 0;
  let current_query: string = "";
  let previous_query: string = "";

  let icons = [InformationSquare24, UserProfile24, Network_224, Calendar24];

  const persisted_theme: string = localStorage.getItem("theme");
  if (themes.indexOf(persisted_theme) > -1) {
    theme = persisted_theme;
  } else {
    if (window.matchMedia) {
      const darkModeOn = window.matchMedia("(prefers-color-scheme: dark)");
      theme = darkModeOn.matches ? "g100" : "g10";
    }
  }
  let dark: boolean = theme === "g100";
  let theme_icon = !dark ? Sun24 : Moon24;

  function toggle_theme(): void {
    theme = dark ? "g10" : "g100";
    theme_icon = dark ? Sun24 : Moon24;
    dark = !dark;
    ref.focus();
  }

  async function retrieve<T>(request: RequestInfo): Promise<T> {
    const response = await fetch(request);
    const body = await response.json();
    return body;
  }

  interface info {
    results: [];
    count: string;
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
    if (previous_query !== current_query) {
      current_page = 1;
      page = 0;
    }
    let base_url: string = "https://lulzx.herokuapp.com/query/";
    let url: string =
      base_url + type + "/" + current_query + "/" + current_page;
    const data = await retrieve<info[]>(url);
    rows = data["results"];
    total = data["count"];
    if (total <= 25) {
      pages = 1;
    } else {
      pages = ~~(total / 25);
    }
    let nextState = "?" + type + "=" + current_query;
    window.history.replaceState("", "", nextState);
    previous_page = current_page;
    previous_query = current_query;
    state = "completed";
  };
  function mobile() {
    let status: boolean = false;
    if (typeof window.orientation !== "undefined") {
      status = true;
      shown = 5;
    }
    return status;
  }
  onMount(async () => {
    if (typeof window != "undefined") {
      let location = new URL(window.location.href);
      if (location.search !== "") {
        let current_type: string;
        state = "loading";
        for (let x of types) {
          if (location.searchParams.has(x)) {
            current_type = x;
            type = current_type;
            break;
          }
        }
        current_query = location.searchParams.get(current_type);
        await search();
      }
      let url = "https://lulzx.herokuapp.com/";
      await fetch(url)
        .then(() => {
          console.log("feels good man!");
        })
        .catch((error) => {
          console.error(error);
        });
      ref.focus();
    }
  });
</script>

<style>
  h1 {
    display: flex;
    padding-top: 15vmin;
    justify-content: center;
    text-align: center;
    position: relative;
    font-weight: bold;
    font-size: 15vw;
    min-width: auto;
    text-shadow: 0.03em 0.03em 0 rgb(15, 98, 254);
  }

  h1:after {
    content: attr(data-shadow);
    position: absolute;
    right: 0;
    min-width: auto;
    padding-top: 0.06em;
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
    background-clip: initial;
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
  :global(.bx--header__action:focus) {
    border-color: #00000000;
  }

  :global(.bx--header__action:hover) {
    background-color: #00000000;
  }
  :global(.bx--header__action) {
    display: -webkit-box;
  }
  :global(.bx--header__menu-toggle) {
    display: none;
  }
  :global(.bx--content) {
    background: none;
    padding: 1.5rem;
  }
  :global(.bx--fieldset) {
    margin-bottom: 1rem;
    min-width: auto;
  }
  :global(.bx--structured-list) {
    display: inherit;
  }
</style>

{#if ['onload', 'completed'].includes(state)}
  <Theme persist bind:theme>
    <Header
      company="Shoten"
      platformName="Book Search Engine"
      on:click={() => {
        window.location.href = '/';
      }}
      href="/">
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
    <Content>
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
                <Icon render={icons[types.indexOf(k)]} />
                &nbsp;&nbsp;{k}
              </div>
            </Switch>
          {/each}
        </ContentSwitcher>
      </FormGroup>
      {#if state === 'completed'}
        {#if mobile()}
          <StructuredList>
            <StructuredListHead>
              <StructuredListRow head>{total} results found!</StructuredListRow>
            </StructuredListHead>
            <StructuredListBody>
              {#each rows as row}
                <StructuredListRow
                  on:click={() => {
                    let str = row['download'],
                      hash = str.split('main/')[1],
                      book_url = window.location.origin + '/book?id=' + hash;
                    window.open(book_url, '_blank');
                  }}>
                  <StructuredListCell>
                    <span style="font-weight: bold;">{row['title']}</span>
                    {#if row['author']}by{/if}
                    <span style="font-style: italic;">{row['author']}</span>
                    {#if row['publisher']}from{/if}
                    <span
                      style="font-family: monospace;">{row['publisher']}</span>
                    <br />
                    <Tag type="green">{row['year']}</Tag>
                    <Tag type="teal">{row['extension']}</Tag>
                    <Tag type="magenta">{row['size']}</Tag>
                  </StructuredListCell>
                </StructuredListRow>
              {/each}
            </StructuredListBody>
          </StructuredList>
        {:else}
          <DataTable
            sortable
            zebra
            on:click:row={({ detail }) => {
              let str = detail['download'],
                hash = str.split('main/')[1],
                book_url = window.location.origin + '/book?id=' + hash;
              window.open(book_url, '_blank');
            }}
            title="Search Results"
            description="A total of {total} results were found for your query."
            headers={headers.map((x) => ({ key: x, value: x }))}
            {rows} />
        {/if}
        <PaginationNav
          bind:page
          on:change={search}
          total={pages}
          {shown}
          on:click:button--previous={page}
          on:click:button--next={page} />
      {/if}
    </Content>
  </Theme>
{:else if state === 'loading'}
  <div id="search" />
{/if}
