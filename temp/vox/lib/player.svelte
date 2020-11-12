<script>
  import PlayIcon from './IconPlay.svelte'
  import PauseIcon from './icon_pause.svelte'
  import StopIcon from './icon_stop.svelte'
  import VolumeOnIcon from './icon_volume_on.svelte'
  import VolumeOffIcon from './icon_volume_off.svelte'
  import Dragger from './dragger.svelte'

  // === props ===

  export let audioElement
  export const className = ''

  // === state ===

  let loading = true
  let playing = false
  let classes = [className, 'audio-player-component-line']
    .filter(Boolean)
    .join(' ')
  let playTime = 0
  let totalTime = 0
  let playRate = 0
  let volume = 1
  let muted = false

  $: {
    if (totalTime) {
      playRate = playTime / totalTime
    }
    muted = volume === 0
  }

  // === setup ===

  console.log(audioElement)
  audioElement.style.display = 'none'

  function init() {
    totalTime = isNaN(audioElement.duration) ? 0 : audioElement.duration
    if (totalTime) {
      loading = false
    }
  }

  if (audioElement.readyState >= 2) {
    init()
  }

  audioElement.addEventListener('canplay', init)
  audioElement.addEventListener('ended', stop)
  audioElement.addEventListener('timeupdate', function() {
    playTime = audioElement.currentTime
  })
  audioElement.addEventListener('volumechange', function() {
    volume = audioElement.volume
  })

  // === events ===

  function play() {
    if (!loading) {
      playing = true
      audioElement.play()
    }
  }

  function pause() {
    playing = false
    audioElement.pause()
  }

  function stop() {
    pause()
    audioElement.currentTime = 0
  }

  function mute() {
    audioElement.volume = 0
  }

  function unmute() {
    audioElement.volume = 1
  }

  function selectTime(e) {
    dragging = true
    console.log(dragging)
    let x
    if ('touches' in e) {
      x = e.touches[0].clientX
    } else {
      x = e.clientX
    }

    if (timeline) {
      const box = timeline.getBoundingClientRect()
      if (box && x && totalTime) {
        const time = ((x - box.left) / box.width) * totalTime
        audioElement.currentTime = time
      }
    }
  }

  function setTime(e) {
    audioElement.currentTime = e.detail * totalTime
  }

  function setVolume(e) {
    audioElement.volume = e.detail
  }

  // === helpers ===

  function formatTime(time) {
    const seconds = Math.floor(time % 60)
    const minutes = Math.floor(time / 60)
    return minutes + ':' + ('0' + seconds).substr(-2)
  }

  // === live cycle ===
</script>

<style>
  .audio-player-component-line {
    height: 40px;
    width: 100%;
    min-width: 450px;
    background-color: black;
    color: white;
    display: inline-flex;
    box-sizing: content-box;
  }
  .audio-player-component-line * {
    box-sizing: content-box;
  }
  .btn {
    position: relative;
    height: 100%;
    margin: 0;
    padding: 0;
    border: 0;
    background: transparent;
  }
  .btn span {
    position: absolute;
    font-size: 1px;
    color: black;
  }
  .timeline {
    flex: 2 2 auto;
    margin-left: 1rem;
    margin-right: 1rem;
  }
  .volume {
    width: 65px;
    max-width: 20vw;
    margin-right: 1rem;
  }
  @media (max-width: 600px) {
    .volume {
      display: none;
    }
    .audio-player-component-line {
      min-width: 360px;
    }
  }
  @media (max-width: 480px) {
    .timeline {
      display: none;
    }
    .audio-player-component-line {
      min-width: 0;
    }
  }
  .timer {
    margin: auto;
    padding: 0.3em 1em;
  }
</style>

<div class={classes}>
  {#if playing}
    <button class="btn" on:click={pause}>
      <span>Pause</span>
      <PauseIcon />
    </button>
  {:else}
    <button class="btn" on:click={play}>
      <span>Play</span>
      <PlayIcon />
    </button>
  {/if}
  <div class="timeline">
    <Dragger value={playRate} on:change={setTime} />
  </div>
  <p class="timer">{formatTime(playTime)} / {formatTime(totalTime)}</p>
  {#if muted}
    <button class="btn" on:click={unmute}>
      <span>Unmute</span>
      <VolumeOffIcon />
    </button>
  {:else}
    <button class="btn" on:click={mute}>
      <span>Mute</span>
      <VolumeOnIcon />
    </button>
  {/if}
  <div class="volume">
    <Dragger value={volume} on:change={setVolume} />
  </div>
</div>
