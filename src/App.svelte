<script>
  import { Router } from "@roxi/routify";
  import { routes } from "../.routify/routes";
  import './tailwind.css';
</script>

<style  global>
  @import "../assets/global.css";
  @import "carbon-components-svelte/css/g10";
</style>


<Router {routes} />