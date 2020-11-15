<!-- 
Here we will have an interface for the audiobooks
we will fetch the books available in public domain
on librevox website.

components for inspiration:

https://www.carbondesignsystem.com/community/component-index/

! -->
<script>
  import {
    StructuredList,
    StructuredListHead,
    StructuredListRow,
    StructuredListCell,
    StructuredListBody,
    StructuredListInput,
    Slider,
  } from "carbon-components-svelte";
  import PlayOutline32 from "carbon-icons-svelte/lib/PlayOutline32";
  import { Button } from "carbon-components-svelte";
  import ChevronLeftGlyph from "carbon-icons-svelte/lib/ChevronLeftGlyph";
  import ChevronRightGlyph from "carbon-icons-svelte/lib/ChevronRightGlyph";
  import Pause32 from "carbon-icons-svelte/lib/Pause32";
  import Play32 from "carbon-icons-svelte/lib/Play32";

  let json = `{"title": "Art of War", "description": "The Art of War is a Chinese military treatise written during the 6th century BC by Sun Tzu. Composed of 13 chapters, each of which is devoted to one aspect of warfare, it has long been praised as the definitive work on military strategies and tactics of its time. The Art of War is one of the oldest and most famous studies of strategy and has had a huge influence on both military planning and beyond. The Art of War has also been applied, with much success, to business and managerial strategies.", "authors": "[BookAuthor(Sun Tzu 孙武, 3534)]", "url": "https://librivox.org/the-art-of-war-by-sun-tzu/", "streams": ["http://www.archivexyz.org/download/art_of_war_librivox/art_of_war_01-02_sun_tzu_64kb.mp3", "http://www.archivexyz.org/download/art_of_war_librivox/art_of_war_03-04_sun_tzu_64kb.mp3", "http://www.archivexyz.org/download/art_of_war_librivox/art_of_war_05-06_sun_tzu_64kb.mp3", "http://www.archivexyz.org/download/art_of_war_librivox/art_of_war_07-08_sun_tzu_64kb.mp3", "http://www.archivexyz.org/download/art_of_war_librivox/art_of_war_09-10_sun_tzu_64kb.mp3", "http://www.archivexyz.org/download/art_of_war_librivox/art_of_war_11-11_sun_tzu_64kb.mp3", "http://www.archivexyz.org/download/art_of_war_librivox/art_of_war_12-13_sun_tzu_64kb.mp3"]}`;

  let book = JSON.parse(json);
  let audioTracks = book.streams;
  let total = audioTracks.length;
  let current = 0;
  let playing = false;
  let pause_play_icon = Pause32;
  function pause() {
    if (playing) {
      pause_play_icon = Pause32;
    } else {
      pause_play_icon = Play32;
    }
    playing = !playing;
  }

  function values(link) {
    let filename = link.split("/");
    let mid;
    let info = filename[filename.length - 1].split("_");
    for (let i of info) {
      if (i.includes("-")) {
        mid = i;
        break;
      }
    }
    let index = info.indexOf(mid);
    let title = info.slice(0, index).join(" ");
    let author = info.slice(index + 1, -1).join(" ");
    return [mid, title, author];
  }
</script>

currently playing:
{audioTracks[current].split('/').slice(5)}
<br />
total tracks:
{total}
<hr />
<Slider
  labelText="Now playing (audiobook)"
  min={0}
  max={60}
  maxLabel="1:00"
  value={60}
  step={1} />
<br />
<Button
  size="field"
  icon={ChevronLeftGlyph}
  hasIconOnly
  tooltipPosition="bottom"
  tooltipAlignment="center"
  iconDescription="previous"
  on:click={() => (current -= 1)}
  disabled={current < 1} />
<Button
  size="field"
  icon={pause_play_icon}
  hasIconOnly
  tooltipPosition="bottom"
  tooltipAlignment="center"
  iconDescription="pause"
  on:click={pause} />
<Button
  size="field"
  icon={ChevronRightGlyph}
  hasIconOnly
  tooltipPosition="bottom"
  tooltipAlignment="center"
  iconDescription="next"
  on:click={() => (current += 1)}
  disabled={current > audioTracks.length - 2} />
<hr />
<!-- svelte-ignore a11y-media-has-caption -->
<audio controls src={audioTracks[current]} style="display:none;" />
<StructuredList selection selected="row-1-value">
  <StructuredListHead>
    <StructuredListRow head>
      <StructuredListCell head>track number</StructuredListCell>
      <StructuredListCell head>book</StructuredListCell>
      <StructuredListCell head>writer</StructuredListCell>
      <StructuredListCell head>{''}</StructuredListCell>
    </StructuredListRow>
  </StructuredListHead>
  <StructuredListBody>
    {#each audioTracks as audio}
      <StructuredListRow label for="row-{audio}">
        <StructuredListCell>{values(audio)[0]}</StructuredListCell>
        <StructuredListCell>{values(audio)[1]}</StructuredListCell>
        <StructuredListCell>{values(audio)[2]}</StructuredListCell>
        <StructuredListInput
          id="row-{audio}"
          value="row-{audio}-value"
          title="row-{audio}-title"
          name="row-{audio}-name" />
        <StructuredListCell>
          <PlayOutline32
            class="bx--structured-list-svg"
            aria-label="select an option"
            title="select an option" />
        </StructuredListCell>
      </StructuredListRow>
    {/each}
  </StructuredListBody>
</StructuredList>
