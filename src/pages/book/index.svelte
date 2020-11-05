<script>
  import { Grid, Row, Column } from "carbon-components-svelte";
  import Download32 from "carbon-icons-svelte/lib/Download32";
  import { ExpandableTile } from "carbon-components-svelte";
  import { SkeletonText, SkeletonPlaceholder } from "carbon-components-svelte";
  import { Button } from "carbon-components-svelte";
  import { onMount } from "svelte";

  let loading = true;
  let title, subtitle, description, author, year, src, download;

  onMount(async () => {
    let hash = new URL(window.location.href).searchParams.get("id")
    let url = "https://lulzx.herokuapp.com/book/" + hash
    let res = await fetch(url);
    let data = await res.json();
    title = data.title;
    subtitle = data.subtitle;
    description = data.description;
    author = data.author;
    year = data.year; 
    src = data.image;
    download = data.direct_url
    setTimeout(() => {
      loading = false;
    }, 1000);
  });
  function description_handler(where){
    if (where === 'above'){
      return description.slice(0,465)
    }
    else {
      return description.slice(465)
    }
  }
</script>

<style>
  h1 {
    font-size: 35px;
  }
  h2 {
    font-size: 20px;
    color: #989;
  }
  h3 {
    font-size: 16px;
  }
  a {
    color: #0062FF
  }
  .container {
    padding: 0 60px;
    min-width: 600px;
  }

  .paper {
    display: -webkit-box;
    display: flex;
    -webkit-box-align: center;
    align-items: center;
    box-sizing: border-box;
    width: 100%;
    max-width: 900px;
    padding: 26px;
    margin: 26px auto;
    background: white;
    box-shadow: 0 4px 4px rgba(0, 0, 0, 0.2);
    border-radius: 4px;
    margin-left: min(50%, 75px);
    margin-right: min(50%, 75px);
  }
</style>

<div class="container">
  <div class="paper">
    <Grid>
      <Row>
        <Column style="outline: 1px solid var(--cds-interactive-04)">
          {#if loading === true}
            <SkeletonPlaceholder style="height: 31.25rem; width: 23rem;" />
          {:else}<img {src} alt={subtitle} />{/if}
        </Column>
        <Column style="outline: 1px solid var(--cds-interactive-04)">
          <h1>
            {#if loading === true}
              <SkeletonText paragraph lines={2} width="50%" />
            {:else}{title}{/if}
          </h1><br />
          <h2>
            {#if loading === true}
              <SkeletonText paragraph lines={2} width="50%" />
            {:else}{subtitle}{/if}
          </h2><br />
          <h3>
            {#if loading === true}
              <SkeletonText paragraph lines={2} width="50%" />
            {:else}By <a href="#!">{author}</a> · {year}{/if}
          </h3><br />
            {#if loading === true}
              <SkeletonText paragraph lines={2} width="50%" />
            {:else}<ExpandableTile>
  <div slot="above" style="height: 10rem">{description_handler('above')}</div>
  <div slot="below" style="height: 10rem">{description_handler('below')}</div>
</ExpandableTile>{/if}
          <br />
          {#if loading === true}
            <SkeletonPlaceholder style="height: 3rem; width: 9rem;" />
          {:else}
          <Button href="{download}" icon={Download32}>Download</Button>
          {/if}
        </Column>
      </Row>
    </Grid>
  </div>
</div>
