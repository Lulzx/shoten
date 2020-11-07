<!-- App.svelte -->
<script>
  import { LottiePlayer } from '@lottiefiles/svelte-lottie-player';

</script>
  <style>
    div {
        position: absolute;
        top: 50%;
        left: 50%;
        margin-right: -50%;
        transform: translate(-50%, -50%) }
  </style>
<div>
<LottiePlayer
  src="https://assets4.lottiefiles.com/temp/lf20_0txt7u.json"
  autoplay="{true}"
  loop="{true}"
  controls="{true}"
  renderer="svg"
  background="transparent"
  height="{600}"
  width="{600}"
  controlsLayout="false"
  align="center"
/></div>