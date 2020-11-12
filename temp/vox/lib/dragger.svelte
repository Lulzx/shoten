<script>
  import { createEventDispatcher } from 'svelte'
  import { onMount } from 'svelte'
  const dispatch = createEventDispatcher()

  export let value

  let marker
  let element
  let dragging = false

  $: {
    let percentPlayed = Math.floor(value * 100) + '%'

    if (marker) {
      marker.style.left = percentPlayed
    }
  }

  function selectValue(e) {
    dragging = true
    let x
    if ('touches' in e) {
      x = e.touches[0].clientX
    } else {
      x = e.clientX
    }

    if (element) {
      const box = element.getBoundingClientRect()
      if (box && x) {
        const val = Math.max(0, Math.min((x - box.left) / box.width, 1))

        dispatch('change', val)
      }
    }
  }

  function onDrag(e) {
    if (dragging) {
      selectValue(e)
    }
  }

  onMount(() => {
    function stopDrag() {
      dragging = false
    }
    document.body.addEventListener('mouseup', stopDrag)
    document.body.addEventListener('mouseleave', stopDrag)

    return () => {
      document.body.removeEventListener('mouseup', stopDrag)
      document.body.removeEventListener('mouseleave', stopDrag)
    }
  })
</script>

<style>
  .audio-player-component-dragger {
    position: relative;
    margin: auto 0;
    cursor: pointer;
    height: 100%;
    width: 100%;
  }
  .audio-player-component-dragger::after {
    content: ' ';
    position: absolute;
    display: block;
    top: 0;
    left: 0;
    right: 0;
    bottom: 0;
    height: 3px;
    background: white;
    z-index: 0;
    margin: auto;
  }
  .marker {
    display: block;
    position: absolute;
    top: 50%;
    transform: translateY(-50%) translateX(-50%);
    width: 5px;
    height: 16px;
    background-color: white;
    border: 3px solid black;
    z-index: 1;
    margin: auto;
    cursor: grab;
  }
</style>

<div
  class="audio-player-component-dragger"
  bind:this={element}
  on:mousedown={selectValue}
  on:mousemove={onDrag}
  on:touchstart={selectValue}
  on:touchmove={selectValue}>
  <span class="marker" bind:this={marker} />
</div>
