<script>
  export let persist = false;
  export let persistKey = "theme";
  export let theme = "g10";
  export const themes = ["g10", "g100"];

  import { afterUpdate} from "svelte";
  import { writable } from "svelte/store";

  const isValidTheme = (value) => themes.includes(value);
  const isDark = (value) =>
    isValidTheme(value) && (value === "g90" || value === "g100");

  const dark = writable(isDark(theme));

  afterUpdate(() => {
    if (isValidTheme(theme)) {
      document.documentElement.setAttribute("theme", theme);
      if (persist) {
        localStorage.setItem(persistKey, theme);
      }
    } else {
      console.warn(
        `"${theme}" is not a valid Carbon theme. Choose from available themes: ${JSON.stringify(
          themes
        )}`
      );
    }
  });

  $: dark.set(isDark(theme));
</script>

<slot />
