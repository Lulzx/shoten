<script>
  import { Router } from "@roxi/routify";
  import { routes } from "../.routify/routes";
  import './tailwind.css';
</script>

<style lang="scss" global>
  @import "../assets/global.css";
  @import "carbon-components-svelte/css/all";
</style>


<Router {routes} />