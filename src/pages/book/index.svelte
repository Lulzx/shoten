<script>
  import { Grid, Row, Column } from "carbon-components-svelte";
  import Download32 from "carbon-icons-svelte/lib/Download32";

  import { Button, InlineLoading } from "carbon-components-svelte";
  import { Tile } from "carbon-components-svelte";
  import { onDestroy } from "svelte";
  let title = "Eloquent JavaScript";
  let subtitle = "A Modern Introduction to Programming";
  let description =
    "This book is designed to introduce students to programming and computational thinking through the lens of exploring data. You can think of Python as your tool to solve problems that are far beyond ...";
  let author = "Marijn Haverbeke";
  let year = "2020";
  let src = "https://eloquentjavascript.net/img/cover.jpg";

  const descriptionMap = {
    active: "fetching...",
    finished: "Success!",
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

<style>
  h1 {
    font-size: 45px;
  }
  h2 {
    font-size: 25px;
    color: #989;
  }
  h3 {
    font-size: 18px;
  }
  p {
    font-size: 18px;
    background-color: #d9dddc;
    font-family: "Georgia";
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
    margin-top: 50px;
    margin-left: min(50%, 75px);
    margin-right: min(50%, 75px);
  }
</style>

<div class="container">
  <div class="paper">
    <Grid>
      <Row>
        <Column style="outline: 1px solid var(--cds-interactive-04)">
          <img {src} alt={subtitle} />
        </Column>
        <Column style="outline: 1px solid var(--cds-interactive-04)">
          <h1>{title}</h1><br />
          <h2>{subtitle}</h2><br />
          <h3>By <a href="#!">{author}</a> · {year}</h3><br />
          <Tile />
          <p>{description}</p><br />
          {#if state !== 'dormant'}
            <InlineLoading status={state} description={descriptionMap[state]} />
          {:else}
            <Button icon={Download32} on:click={() => (state = 'active')}>
              Download
            </Button>
          {/if}
        </Column>
      </Row>
    </Grid>
  </div>
</div>
