<script>
  import { Grid, Row, Column } from "carbon-components-svelte";
  import { Button, ButtonSet, InlineLoading } from "carbon-components-svelte";
  import { Tile } from "carbon-components-svelte";
  import { onDestroy } from "svelte";
  let title = "Eloquent JavaScript";
  let subtitle = "A Modern Introduction to Programming";
  let description = "This book is designed to introduce students to programming and computational thinking through the lens of exploring data. You can think of Python as your tool to solve problems that are far beyond ...";
  let author = "Marijn Haverbeke";
  let year = "2018"
  let src = "https://eloquentjavascript.net/img/cover.jpg"

const descriptionMap = {
    active: "Submitting...",
    finished: "Success",
    inactive: "Cancelling...",
  };

  const stateMap = {
    active: "finished",
    inactive: "dormant",
    finished: "dormant",
  };

  let timeout = undefined;
  let state = "dormant"; // "dormant" | "active" | "finished" | "inactive"

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

<style>
  h1 {
    font-size: 60px;
  }
  h2 {
    font-size: 45px;
    color: #999;
  }
   h3 {
    font-size: 25px;
  }
   p {
    font-size: 20px;
    background-color: #D9DDDC;
  }
</style>

<Tile>
<Grid>
  <Row>
    <Column style="outline: 1px solid var(--cds-interactive-04)"><img {src} alt={subtitle}></Column>
    <Column style="outline: 1px solid var(--cds-interactive-04)"><h1>{title}</h1><br>
<h2>{subtitle}</h2><br>
<h3>By <a href="#!">{author}</a> · {year}</h3><br>
  <p>{description}</p><br>
  {#if state !== 'dormant'}
    <InlineLoading status={state} description={descriptionMap[state]} />
  {:else}
    <Button on:click={() => (state = 'active')}>Download</Button>
  {/if}</Column>
  </Row>
</Grid>
</Tile>