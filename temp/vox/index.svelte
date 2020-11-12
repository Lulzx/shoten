<script>
  import { ButtonSet, Button } from "carbon-components-svelte";
  import ChevronLeftGlyph from "carbon-icons-svelte/lib/ChevronLeftGlyph";
  import ChevronRightGlyph from "carbon-icons-svelte/lib/ChevronRightGlyph";
  import Pause32 from "carbon-icons-svelte/lib/Pause32";

  let json = `{"title": "Art of War", "description": "The Art of War is a Chinese military treatise written during the 6th century BC by Sun Tzu. Composed of 13 chapters, each of which is devoted to one aspect of warfare, it has long been praised as the definitive work on military strategies and tactics of its time. The Art of War is one of the oldest and most famous studies of strategy and has had a huge influence on both military planning and beyond. The Art of War has also been applied, with much success, to business and managerial strategies.", "authors": "[BookAuthor(Sun Tzu 孙武, 3534)]", "url": "https://librivox.org/the-art-of-war-by-sun-tzu/", "streams": ["http://www.archive.org/download/art_of_war_librivox/art_of_war_01-02_sun_tzu_64kb.mp3", "http://www.archive.org/download/art_of_war_librivox/art_of_war_03-04_sun_tzu_64kb.mp3", "http://www.archive.org/download/art_of_war_librivox/art_of_war_05-06_sun_tzu_64kb.mp3", "http://www.archive.org/download/art_of_war_librivox/art_of_war_07-08_sun_tzu_64kb.mp3", "http://www.archive.org/download/art_of_war_librivox/art_of_war_09-10_sun_tzu_64kb.mp3", "http://www.archive.org/download/art_of_war_librivox/art_of_war_11_sun_tzu_64kb.mp3", "http://www.archive.org/download/art_of_war_librivox/art_of_war_12-13_sun_tzu_64kb.mp3"]}`;

  let book = JSON.parse(json);
  console.log(book.streams);
  console.log(book.title);
  console.log(book.title);
  console.log(book.description);
  console.log(book.authors);
  console.log(book.url);
  console.log(book.streams);
  let audioTracks = book.streams;
  console.log(typeof audioTracks);

  let current = 0;
  function pause(){
      return true;
  }
</script>

<!-- 
Here we will have an interface for the audiobooks
we will fetch the books available in public domain
on librevox website.

components for inspiration:

https://www.carbondesignsystem.com/community/component-index/

! -->

currently playing:
{audioTracks[current]}

<ButtonSet>
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
    icon={Pause32}
    hasIconOnly
    tooltipPosition="bottom"
    tooltipAlignment="center"
    iconDescription="pause"
    on:click={pause}
     />
  <Button
    size="field"
    icon={ChevronRightGlyph}
    hasIconOnly
    tooltipPosition="bottom"
    tooltipAlignment="center"
    iconDescription="next"
    on:click={() => (current += 1)}
    disabled={current > audioTracks.length - 2} />
</ButtonSet>

<!-- svelte-ignore a11y-media-has-caption -->
<audio controls src={audioTracks[current]} />

<ul>
  {#each audioTracks as audio}
    <li>{audio}</li>
  {/each}
</ul>
