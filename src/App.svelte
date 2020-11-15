<script>
  import { Router } from "@roxi/routify";
  import { routes } from "../.routify/routes";
</script>

<style lang="scss" global>
  @import "../assets/global.css";
  // @import "carbon-components-svelte/css/all";
  @import "../assets/custom.scss";
</style>

<Router {routes} />
