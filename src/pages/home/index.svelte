<script>
  import { LottiePlayer } from "@lottiefiles/svelte-lottie-player";
  import { Grid, Row, Column } from "carbon-components-svelte";
</script>

<style>
h1 {
  text-align: center;
}

.card {
  background: #fff;
  border-radius: 65px;
  display: block;
  margin: 1rem;
}

.card-1 {
  box-shadow: 0 1px 3px rgba(0,0,0,0.12), 0 1px 2px rgba(0,0,0,0.24);
  transition: all 0.3s cubic-bezier(.25,.8,.25,1);
}

.card-1:hover {
  box-shadow: 0 14px 28px rgba(0,0,0,0.25), 0 10px 10px rgba(0,0,0,0.22);
}

</style>

  <Grid>
    <Row>
      <Column><div class="card card-1">
          <LottiePlayer
  src="https://assets3.lottiefiles.com/packages/lf20_2gB0PZ.json"
  autoplay={true}
    loop={true}
    controls={true}
    renderer="svg"
  height={500}
    width={500}
    controlsLayout="false"
    align="center" />
    <h1>Audiobooks</h1></div>
      </Column>
      <Column><div class="card card-1">
          <LottiePlayer
    src="https://assets8.lottiefiles.com/datafiles/5FFwoVNq8EcKMH4/data.json"
    autoplay={true}
    loop={true}
    controls={true}
    renderer="svg"
    height={500}
    width={500}
    controlsLayout="false"
    align="center" />
    <h1>E-books</h1></div>
      </Column>
    </Row>
  </Grid>