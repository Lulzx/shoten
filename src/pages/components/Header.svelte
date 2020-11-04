<script>
  import {
    SkipToContent,
    Header,
    HeaderUtilities,
    HeaderAction,
    HeaderPanelLinks,
    HeaderPanelDivider,
    HeaderPanelLink,
  } from "carbon-components-svelte";
  import { getContext } from "svelte";

  const ctx = getContext("Theme");

  $: if (ctx) {
    ctx.dark.subscribe((value) => {
      console.log("dark mode?", value);
    });
    ctx.light.subscribe((value) => {
      console.log("light mode?", value);
    });
    ctx.updateVar("--cds-productive-heading-06-font-size", "4rem");
  }
  let isOpen = false;
</script>

<Header company="Shoten" platformName="Book Search Engine" href="/">
  <div slot="skip-to-content">
    <SkipToContent />
  </div>
  <HeaderUtilities>
    <HeaderAction bind:isOpen>
      <HeaderPanelLinks>
        <HeaderPanelDivider>topic 1</HeaderPanelDivider>
        <HeaderPanelLink>subtopic 1</HeaderPanelLink>
        <HeaderPanelDivider>topic 2</HeaderPanelDivider>
        <HeaderPanelLink>subtopic 1</HeaderPanelLink>
        <HeaderPanelLink>subtopic 2</HeaderPanelLink>
        <HeaderPanelLink>subtopic 3</HeaderPanelLink>
        <HeaderPanelLink>subtopic 4</HeaderPanelLink>
        <HeaderPanelLink>subtopic 5</HeaderPanelLink>
      </HeaderPanelLinks>
    </HeaderAction>
  </HeaderUtilities>
</Header>
