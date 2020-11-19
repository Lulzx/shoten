<script lang="ts">
  import { Grid, Row, Column } from 'carbon-components-svelte'
  import Download32 from 'carbon-icons-svelte/lib/Download32'
  import { Button } from 'carbon-components-svelte'
  import { Accordion, AccordionItem } from 'carbon-components-svelte'
  import { onMount } from 'svelte'

  let loading = true
  let open = true

  let title: string,
    subtitle: string,
    description: string,
    author: string,
    year: string,
    src: string,
    download: string

  async function retrieve<T>(request: RequestInfo): Promise<T> {
    const response = await fetch(request)
    const body = await response.json()
    return body
  }

  interface book {
    title: string
    subtitle: string
    description: string
    year: string
    author: string
    image: string
    direct_url: string
  }

  onMount(async () => {
    let hash = new URL(window.location.href).searchParams.get('id')
    if (hash === null) {
      return
    }
    let base_url = 'https://lulzx.herokuapp.com/book/'
    let url = base_url + hash
    const data = await retrieve<book[]>(url)
    title = data['title']
    subtitle = data['subtitle']
    description = data['description']
    author = data['author']
    year = data['year']
    src = data['image']
    if (src === 'NO_IMAGE') {
      src = 'https://picsum.photos/312/500'
    }
    download = data['direct_url']
    loading = false
  })
  function description_handler() {
    let remaining_chars = 500
    let accordion_text = ''
    let description_list = description.split('.')
    for (let i of description_list) {
      if (i.length < remaining_chars) {
        accordion_text += i + '.'
        remaining_chars -= i.length
      }
    }
    return accordion_text
  }
</script>

<style>
  :global(body) {
    min-height: 100vh;
    display: -webkit-box;
    display: flex;
    -webkit-box-pack: center;
    justify-content: center;
    -webkit-box-align: center;
    align-items: center;
  }
  h1 {
    font-size: 35px;
  }
  h2 {
    font-size: 20px;
    color: #989;
  }
  h3 {
    font-size: 16px;
  }
  a {
    color: #0062ff;
  }
  .container {
    padding: 0 60px;
    min-width: 600px;
  }

  .paper {
    padding: 26px;
    background: white;
    box-shadow: 0 4px 4px rgba(0, 0, 0, 0.2);
    border-radius: 4px;
    margin: 26px min(50%, 75px);
  }

  .book {
    --color: #fff;
    --duration: 6.8s;
    width: 32px;
    height: 12px;
    top: auto;
    bottom: 50%;
    left: auto;
    right: 50%;
    position: absolute;
    margin: 32px 0 0;
    zoom: 1.5;
  }
  .book .inner {
    width: 32px;
    height: 12px;
    position: absolute;
    -webkit-transform-origin: 2px 2px;
    transform-origin: 2px 2px;
    -webkit-transform: rotateZ(-90deg);
    transform: rotateZ(-90deg);
    -webkit-animation: book var(--duration) ease infinite;
    animation: book var(--duration) ease infinite;
  }
  .book .inner .left,
  .book .inner .right {
    width: 60px;
    height: 4px;
    top: 0;
    border-radius: 2px;
    background: var(--color);
    position: absolute;
  }
  .book .inner .left:before,
  .book .inner .right:before {
    content: '';
    width: 48px;
    height: 4px;
    border-radius: 2px;
    background: inherit;
    position: absolute;
    top: -10px;
    left: 6px;
  }
  .book .inner .left {
    right: 28px;
    -webkit-transform-origin: 58px 2px;
    transform-origin: 58px 2px;
    -webkit-transform: rotateZ(90deg);
    transform: rotateZ(90deg);
    -webkit-animation: left var(--duration) ease infinite;
    animation: left var(--duration) ease infinite;
  }
  .book .inner .right {
    left: 28px;
    -webkit-transform-origin: 2px 2px;
    transform-origin: 2px 2px;
    -webkit-transform: rotateZ(-90deg);
    transform: rotateZ(-90deg);
    -webkit-animation: right var(--duration) ease infinite;
    animation: right var(--duration) ease infinite;
  }
  .book .inner .middle {
    width: 32px;
    height: 12px;
    border: 4px solid var(--color);
    border-top: 0;
    border-radius: 0 0 9px 9px;
    -webkit-transform: translateY(2px);
    transform: translateY(2px);
  }
  .book ul {
    margin: 0;
    padding: 0;
    list-style: none;
    position: absolute;
    left: 50%;
    top: 0;
  }
  .book ul li {
    height: 4px;
    border-radius: 2px;
    -webkit-transform-origin: 100% 2px;
    transform-origin: 100% 2px;
    width: 48px;
    right: 0;
    top: -10px;
    position: absolute;
    background: var(--color);
    -webkit-transform: rotateZ(0deg) translateX(-18px);
    transform: rotateZ(0deg) translateX(-18px);
    -webkit-animation-duration: var(--duration);
    animation-duration: var(--duration);
    -webkit-animation-timing-function: ease;
    animation-timing-function: ease;
    -webkit-animation-iteration-count: infinite;
    animation-iteration-count: infinite;
  }
  .book ul li:nth-child(0) {
    -webkit-animation-name: page-0;
    animation-name: page-0;
  }
  .book ul li:nth-child(1) {
    -webkit-animation-name: page-1;
    animation-name: page-1;
  }
  .book ul li:nth-child(2) {
    -webkit-animation-name: page-2;
    animation-name: page-2;
  }
  .book ul li:nth-child(3) {
    -webkit-animation-name: page-3;
    animation-name: page-3;
  }
  .book ul li:nth-child(4) {
    -webkit-animation-name: page-4;
    animation-name: page-4;
  }
  .book ul li:nth-child(5) {
    -webkit-animation-name: page-5;
    animation-name: page-5;
  }
  .book ul li:nth-child(6) {
    -webkit-animation-name: page-6;
    animation-name: page-6;
  }
  .book ul li:nth-child(7) {
    -webkit-animation-name: page-7;
    animation-name: page-7;
  }
  .book ul li:nth-child(8) {
    -webkit-animation-name: page-8;
    animation-name: page-8;
  }
  .book ul li:nth-child(9) {
    -webkit-animation-name: page-9;
    animation-name: page-9;
  }
  .book ul li:nth-child(10) {
    -webkit-animation-name: page-10;
    animation-name: page-10;
  }
  .book ul li:nth-child(11) {
    -webkit-animation-name: page-11;
    animation-name: page-11;
  }
  .book ul li:nth-child(12) {
    -webkit-animation-name: page-12;
    animation-name: page-12;
  }
  .book ul li:nth-child(13) {
    -webkit-animation-name: page-13;
    animation-name: page-13;
  }
  .book ul li:nth-child(14) {
    -webkit-animation-name: page-14;
    animation-name: page-14;
  }
  .book ul li:nth-child(15) {
    -webkit-animation-name: page-15;
    animation-name: page-15;
  }
  .book ul li:nth-child(16) {
    -webkit-animation-name: page-16;
    animation-name: page-16;
  }
  .book ul li:nth-child(17) {
    -webkit-animation-name: page-17;
    animation-name: page-17;
  }
  .book ul li:nth-child(18) {
    -webkit-animation-name: page-18;
    animation-name: page-18;
  }
  @-webkit-keyframes page-0 {
    4% {
      -webkit-transform: rotateZ(0deg) translateX(-18px);
      transform: rotateZ(0deg) translateX(-18px);
    }
    13%,
    54% {
      -webkit-transform: rotateZ(180deg) translateX(-18px);
      transform: rotateZ(180deg) translateX(-18px);
    }
    63% {
      -webkit-transform: rotateZ(0deg) translateX(-18px);
      transform: rotateZ(0deg) translateX(-18px);
    }
  }
  @keyframes page-0 {
    4% {
      -webkit-transform: rotateZ(0deg) translateX(-18px);
      transform: rotateZ(0deg) translateX(-18px);
    }
    13%,
    54% {
      -webkit-transform: rotateZ(180deg) translateX(-18px);
      transform: rotateZ(180deg) translateX(-18px);
    }
    63% {
      -webkit-transform: rotateZ(0deg) translateX(-18px);
      transform: rotateZ(0deg) translateX(-18px);
    }
  }
  @-webkit-keyframes page-1 {
    5.86% {
      -webkit-transform: rotateZ(0deg) translateX(-18px);
      transform: rotateZ(0deg) translateX(-18px);
    }
    14.74%,
    55.86% {
      -webkit-transform: rotateZ(180deg) translateX(-18px);
      transform: rotateZ(180deg) translateX(-18px);
    }
    64.74% {
      -webkit-transform: rotateZ(0deg) translateX(-18px);
      transform: rotateZ(0deg) translateX(-18px);
    }
  }
  @keyframes page-1 {
    5.86% {
      -webkit-transform: rotateZ(0deg) translateX(-18px);
      transform: rotateZ(0deg) translateX(-18px);
    }
    14.74%,
    55.86% {
      -webkit-transform: rotateZ(180deg) translateX(-18px);
      transform: rotateZ(180deg) translateX(-18px);
    }
    64.74% {
      -webkit-transform: rotateZ(0deg) translateX(-18px);
      transform: rotateZ(0deg) translateX(-18px);
    }
  }
  @-webkit-keyframes page-2 {
    7.72% {
      -webkit-transform: rotateZ(0deg) translateX(-18px);
      transform: rotateZ(0deg) translateX(-18px);
    }
    16.48%,
    57.72% {
      -webkit-transform: rotateZ(180deg) translateX(-18px);
      transform: rotateZ(180deg) translateX(-18px);
    }
    66.48% {
      -webkit-transform: rotateZ(0deg) translateX(-18px);
      transform: rotateZ(0deg) translateX(-18px);
    }
  }
  @keyframes page-2 {
    7.72% {
      -webkit-transform: rotateZ(0deg) translateX(-18px);
      transform: rotateZ(0deg) translateX(-18px);
    }
    16.48%,
    57.72% {
      -webkit-transform: rotateZ(180deg) translateX(-18px);
      transform: rotateZ(180deg) translateX(-18px);
    }
    66.48% {
      -webkit-transform: rotateZ(0deg) translateX(-18px);
      transform: rotateZ(0deg) translateX(-18px);
    }
  }
  @-webkit-keyframes page-3 {
    9.58% {
      -webkit-transform: rotateZ(0deg) translateX(-18px);
      transform: rotateZ(0deg) translateX(-18px);
    }
    18.22%,
    59.58% {
      -webkit-transform: rotateZ(180deg) translateX(-18px);
      transform: rotateZ(180deg) translateX(-18px);
    }
    68.22% {
      -webkit-transform: rotateZ(0deg) translateX(-18px);
      transform: rotateZ(0deg) translateX(-18px);
    }
  }
  @keyframes page-3 {
    9.58% {
      -webkit-transform: rotateZ(0deg) translateX(-18px);
      transform: rotateZ(0deg) translateX(-18px);
    }
    18.22%,
    59.58% {
      -webkit-transform: rotateZ(180deg) translateX(-18px);
      transform: rotateZ(180deg) translateX(-18px);
    }
    68.22% {
      -webkit-transform: rotateZ(0deg) translateX(-18px);
      transform: rotateZ(0deg) translateX(-18px);
    }
  }
  @-webkit-keyframes page-4 {
    11.44% {
      -webkit-transform: rotateZ(0deg) translateX(-18px);
      transform: rotateZ(0deg) translateX(-18px);
    }
    19.96%,
    61.44% {
      -webkit-transform: rotateZ(180deg) translateX(-18px);
      transform: rotateZ(180deg) translateX(-18px);
    }
    69.96% {
      -webkit-transform: rotateZ(0deg) translateX(-18px);
      transform: rotateZ(0deg) translateX(-18px);
    }
  }
  @keyframes page-4 {
    11.44% {
      -webkit-transform: rotateZ(0deg) translateX(-18px);
      transform: rotateZ(0deg) translateX(-18px);
    }
    19.96%,
    61.44% {
      -webkit-transform: rotateZ(180deg) translateX(-18px);
      transform: rotateZ(180deg) translateX(-18px);
    }
    69.96% {
      -webkit-transform: rotateZ(0deg) translateX(-18px);
      transform: rotateZ(0deg) translateX(-18px);
    }
  }
  @-webkit-keyframes page-5 {
    13.3% {
      -webkit-transform: rotateZ(0deg) translateX(-18px);
      transform: rotateZ(0deg) translateX(-18px);
    }
    21.7%,
    63.3% {
      -webkit-transform: rotateZ(180deg) translateX(-18px);
      transform: rotateZ(180deg) translateX(-18px);
    }
    71.7% {
      -webkit-transform: rotateZ(0deg) translateX(-18px);
      transform: rotateZ(0deg) translateX(-18px);
    }
  }
  @keyframes page-5 {
    13.3% {
      -webkit-transform: rotateZ(0deg) translateX(-18px);
      transform: rotateZ(0deg) translateX(-18px);
    }
    21.7%,
    63.3% {
      -webkit-transform: rotateZ(180deg) translateX(-18px);
      transform: rotateZ(180deg) translateX(-18px);
    }
    71.7% {
      -webkit-transform: rotateZ(0deg) translateX(-18px);
      transform: rotateZ(0deg) translateX(-18px);
    }
  }
  @-webkit-keyframes page-6 {
    15.16% {
      -webkit-transform: rotateZ(0deg) translateX(-18px);
      transform: rotateZ(0deg) translateX(-18px);
    }
    23.44%,
    65.16% {
      -webkit-transform: rotateZ(180deg) translateX(-18px);
      transform: rotateZ(180deg) translateX(-18px);
    }
    73.44% {
      -webkit-transform: rotateZ(0deg) translateX(-18px);
      transform: rotateZ(0deg) translateX(-18px);
    }
  }
  @keyframes page-6 {
    15.16% {
      -webkit-transform: rotateZ(0deg) translateX(-18px);
      transform: rotateZ(0deg) translateX(-18px);
    }
    23.44%,
    65.16% {
      -webkit-transform: rotateZ(180deg) translateX(-18px);
      transform: rotateZ(180deg) translateX(-18px);
    }
    73.44% {
      -webkit-transform: rotateZ(0deg) translateX(-18px);
      transform: rotateZ(0deg) translateX(-18px);
    }
  }
  @-webkit-keyframes page-7 {
    17.02% {
      -webkit-transform: rotateZ(0deg) translateX(-18px);
      transform: rotateZ(0deg) translateX(-18px);
    }
    25.18%,
    67.02% {
      -webkit-transform: rotateZ(180deg) translateX(-18px);
      transform: rotateZ(180deg) translateX(-18px);
    }
    75.18% {
      -webkit-transform: rotateZ(0deg) translateX(-18px);
      transform: rotateZ(0deg) translateX(-18px);
    }
  }
  @keyframes page-7 {
    17.02% {
      -webkit-transform: rotateZ(0deg) translateX(-18px);
      transform: rotateZ(0deg) translateX(-18px);
    }
    25.18%,
    67.02% {
      -webkit-transform: rotateZ(180deg) translateX(-18px);
      transform: rotateZ(180deg) translateX(-18px);
    }
    75.18% {
      -webkit-transform: rotateZ(0deg) translateX(-18px);
      transform: rotateZ(0deg) translateX(-18px);
    }
  }
  @-webkit-keyframes page-8 {
    18.88% {
      -webkit-transform: rotateZ(0deg) translateX(-18px);
      transform: rotateZ(0deg) translateX(-18px);
    }
    26.92%,
    68.88% {
      -webkit-transform: rotateZ(180deg) translateX(-18px);
      transform: rotateZ(180deg) translateX(-18px);
    }
    76.92% {
      -webkit-transform: rotateZ(0deg) translateX(-18px);
      transform: rotateZ(0deg) translateX(-18px);
    }
  }
  @keyframes page-8 {
    18.88% {
      -webkit-transform: rotateZ(0deg) translateX(-18px);
      transform: rotateZ(0deg) translateX(-18px);
    }
    26.92%,
    68.88% {
      -webkit-transform: rotateZ(180deg) translateX(-18px);
      transform: rotateZ(180deg) translateX(-18px);
    }
    76.92% {
      -webkit-transform: rotateZ(0deg) translateX(-18px);
      transform: rotateZ(0deg) translateX(-18px);
    }
  }
  @-webkit-keyframes page-9 {
    20.74% {
      -webkit-transform: rotateZ(0deg) translateX(-18px);
      transform: rotateZ(0deg) translateX(-18px);
    }
    28.66%,
    70.74% {
      -webkit-transform: rotateZ(180deg) translateX(-18px);
      transform: rotateZ(180deg) translateX(-18px);
    }
    78.66% {
      -webkit-transform: rotateZ(0deg) translateX(-18px);
      transform: rotateZ(0deg) translateX(-18px);
    }
  }
  @keyframes page-9 {
    20.74% {
      -webkit-transform: rotateZ(0deg) translateX(-18px);
      transform: rotateZ(0deg) translateX(-18px);
    }
    28.66%,
    70.74% {
      -webkit-transform: rotateZ(180deg) translateX(-18px);
      transform: rotateZ(180deg) translateX(-18px);
    }
    78.66% {
      -webkit-transform: rotateZ(0deg) translateX(-18px);
      transform: rotateZ(0deg) translateX(-18px);
    }
  }
  @-webkit-keyframes page-10 {
    22.6% {
      -webkit-transform: rotateZ(0deg) translateX(-18px);
      transform: rotateZ(0deg) translateX(-18px);
    }
    30.4%,
    72.6% {
      -webkit-transform: rotateZ(180deg) translateX(-18px);
      transform: rotateZ(180deg) translateX(-18px);
    }
    80.4% {
      -webkit-transform: rotateZ(0deg) translateX(-18px);
      transform: rotateZ(0deg) translateX(-18px);
    }
  }
  @keyframes page-10 {
    22.6% {
      -webkit-transform: rotateZ(0deg) translateX(-18px);
      transform: rotateZ(0deg) translateX(-18px);
    }
    30.4%,
    72.6% {
      -webkit-transform: rotateZ(180deg) translateX(-18px);
      transform: rotateZ(180deg) translateX(-18px);
    }
    80.4% {
      -webkit-transform: rotateZ(0deg) translateX(-18px);
      transform: rotateZ(0deg) translateX(-18px);
    }
  }
  @-webkit-keyframes page-11 {
    24.46% {
      -webkit-transform: rotateZ(0deg) translateX(-18px);
      transform: rotateZ(0deg) translateX(-18px);
    }
    32.14%,
    74.46% {
      -webkit-transform: rotateZ(180deg) translateX(-18px);
      transform: rotateZ(180deg) translateX(-18px);
    }
    82.14% {
      -webkit-transform: rotateZ(0deg) translateX(-18px);
      transform: rotateZ(0deg) translateX(-18px);
    }
  }
  @keyframes page-11 {
    24.46% {
      -webkit-transform: rotateZ(0deg) translateX(-18px);
      transform: rotateZ(0deg) translateX(-18px);
    }
    32.14%,
    74.46% {
      -webkit-transform: rotateZ(180deg) translateX(-18px);
      transform: rotateZ(180deg) translateX(-18px);
    }
    82.14% {
      -webkit-transform: rotateZ(0deg) translateX(-18px);
      transform: rotateZ(0deg) translateX(-18px);
    }
  }
  @-webkit-keyframes page-12 {
    26.32% {
      -webkit-transform: rotateZ(0deg) translateX(-18px);
      transform: rotateZ(0deg) translateX(-18px);
    }
    33.88%,
    76.32% {
      -webkit-transform: rotateZ(180deg) translateX(-18px);
      transform: rotateZ(180deg) translateX(-18px);
    }
    83.88% {
      -webkit-transform: rotateZ(0deg) translateX(-18px);
      transform: rotateZ(0deg) translateX(-18px);
    }
  }
  @keyframes page-12 {
    26.32% {
      -webkit-transform: rotateZ(0deg) translateX(-18px);
      transform: rotateZ(0deg) translateX(-18px);
    }
    33.88%,
    76.32% {
      -webkit-transform: rotateZ(180deg) translateX(-18px);
      transform: rotateZ(180deg) translateX(-18px);
    }
    83.88% {
      -webkit-transform: rotateZ(0deg) translateX(-18px);
      transform: rotateZ(0deg) translateX(-18px);
    }
  }
  @-webkit-keyframes page-13 {
    28.18% {
      -webkit-transform: rotateZ(0deg) translateX(-18px);
      transform: rotateZ(0deg) translateX(-18px);
    }
    35.62%,
    78.18% {
      -webkit-transform: rotateZ(180deg) translateX(-18px);
      transform: rotateZ(180deg) translateX(-18px);
    }
    85.62% {
      -webkit-transform: rotateZ(0deg) translateX(-18px);
      transform: rotateZ(0deg) translateX(-18px);
    }
  }
  @keyframes page-13 {
    28.18% {
      -webkit-transform: rotateZ(0deg) translateX(-18px);
      transform: rotateZ(0deg) translateX(-18px);
    }
    35.62%,
    78.18% {
      -webkit-transform: rotateZ(180deg) translateX(-18px);
      transform: rotateZ(180deg) translateX(-18px);
    }
    85.62% {
      -webkit-transform: rotateZ(0deg) translateX(-18px);
      transform: rotateZ(0deg) translateX(-18px);
    }
  }
  @-webkit-keyframes page-14 {
    30.04% {
      -webkit-transform: rotateZ(0deg) translateX(-18px);
      transform: rotateZ(0deg) translateX(-18px);
    }
    37.36%,
    80.04% {
      -webkit-transform: rotateZ(180deg) translateX(-18px);
      transform: rotateZ(180deg) translateX(-18px);
    }
    87.36% {
      -webkit-transform: rotateZ(0deg) translateX(-18px);
      transform: rotateZ(0deg) translateX(-18px);
    }
  }
  @keyframes page-14 {
    30.04% {
      -webkit-transform: rotateZ(0deg) translateX(-18px);
      transform: rotateZ(0deg) translateX(-18px);
    }
    37.36%,
    80.04% {
      -webkit-transform: rotateZ(180deg) translateX(-18px);
      transform: rotateZ(180deg) translateX(-18px);
    }
    87.36% {
      -webkit-transform: rotateZ(0deg) translateX(-18px);
      transform: rotateZ(0deg) translateX(-18px);
    }
  }
  @-webkit-keyframes page-15 {
    31.9% {
      -webkit-transform: rotateZ(0deg) translateX(-18px);
      transform: rotateZ(0deg) translateX(-18px);
    }
    39.1%,
    81.9% {
      -webkit-transform: rotateZ(180deg) translateX(-18px);
      transform: rotateZ(180deg) translateX(-18px);
    }
    89.1% {
      -webkit-transform: rotateZ(0deg) translateX(-18px);
      transform: rotateZ(0deg) translateX(-18px);
    }
  }
  @keyframes page-15 {
    31.9% {
      -webkit-transform: rotateZ(0deg) translateX(-18px);
      transform: rotateZ(0deg) translateX(-18px);
    }
    39.1%,
    81.9% {
      -webkit-transform: rotateZ(180deg) translateX(-18px);
      transform: rotateZ(180deg) translateX(-18px);
    }
    89.1% {
      -webkit-transform: rotateZ(0deg) translateX(-18px);
      transform: rotateZ(0deg) translateX(-18px);
    }
  }
  @-webkit-keyframes page-16 {
    33.76% {
      -webkit-transform: rotateZ(0deg) translateX(-18px);
      transform: rotateZ(0deg) translateX(-18px);
    }
    40.84%,
    83.76% {
      -webkit-transform: rotateZ(180deg) translateX(-18px);
      transform: rotateZ(180deg) translateX(-18px);
    }
    90.84% {
      -webkit-transform: rotateZ(0deg) translateX(-18px);
      transform: rotateZ(0deg) translateX(-18px);
    }
  }
  @keyframes page-16 {
    33.76% {
      -webkit-transform: rotateZ(0deg) translateX(-18px);
      transform: rotateZ(0deg) translateX(-18px);
    }
    40.84%,
    83.76% {
      -webkit-transform: rotateZ(180deg) translateX(-18px);
      transform: rotateZ(180deg) translateX(-18px);
    }
    90.84% {
      -webkit-transform: rotateZ(0deg) translateX(-18px);
      transform: rotateZ(0deg) translateX(-18px);
    }
  }
  @-webkit-keyframes page-17 {
    35.62% {
      -webkit-transform: rotateZ(0deg) translateX(-18px);
      transform: rotateZ(0deg) translateX(-18px);
    }
    42.58%,
    85.62% {
      -webkit-transform: rotateZ(180deg) translateX(-18px);
      transform: rotateZ(180deg) translateX(-18px);
    }
    92.58% {
      -webkit-transform: rotateZ(0deg) translateX(-18px);
      transform: rotateZ(0deg) translateX(-18px);
    }
  }
  @keyframes page-17 {
    35.62% {
      -webkit-transform: rotateZ(0deg) translateX(-18px);
      transform: rotateZ(0deg) translateX(-18px);
    }
    42.58%,
    85.62% {
      -webkit-transform: rotateZ(180deg) translateX(-18px);
      transform: rotateZ(180deg) translateX(-18px);
    }
    92.58% {
      -webkit-transform: rotateZ(0deg) translateX(-18px);
      transform: rotateZ(0deg) translateX(-18px);
    }
  }
  @-webkit-keyframes page-18 {
    37.48% {
      -webkit-transform: rotateZ(0deg) translateX(-18px);
      transform: rotateZ(0deg) translateX(-18px);
    }
    44.32%,
    87.48% {
      -webkit-transform: rotateZ(180deg) translateX(-18px);
      transform: rotateZ(180deg) translateX(-18px);
    }
    94.32% {
      -webkit-transform: rotateZ(0deg) translateX(-18px);
      transform: rotateZ(0deg) translateX(-18px);
    }
  }
  @keyframes page-18 {
    37.48% {
      -webkit-transform: rotateZ(0deg) translateX(-18px);
      transform: rotateZ(0deg) translateX(-18px);
    }
    44.32%,
    87.48% {
      -webkit-transform: rotateZ(180deg) translateX(-18px);
      transform: rotateZ(180deg) translateX(-18px);
    }
    94.32% {
      -webkit-transform: rotateZ(0deg) translateX(-18px);
      transform: rotateZ(0deg) translateX(-18px);
    }
  }
  @-webkit-keyframes left {
    4% {
      -webkit-transform: rotateZ(90deg);
      transform: rotateZ(90deg);
    }
    10%,
    40% {
      -webkit-transform: rotateZ(0deg);
      transform: rotateZ(0deg);
    }
    46%,
    54% {
      -webkit-transform: rotateZ(90deg);
      transform: rotateZ(90deg);
    }
    60%,
    90% {
      -webkit-transform: rotateZ(0deg);
      transform: rotateZ(0deg);
    }
    96% {
      -webkit-transform: rotateZ(90deg);
      transform: rotateZ(90deg);
    }
  }
  @keyframes left {
    4% {
      -webkit-transform: rotateZ(90deg);
      transform: rotateZ(90deg);
    }
    10%,
    40% {
      -webkit-transform: rotateZ(0deg);
      transform: rotateZ(0deg);
    }
    46%,
    54% {
      -webkit-transform: rotateZ(90deg);
      transform: rotateZ(90deg);
    }
    60%,
    90% {
      -webkit-transform: rotateZ(0deg);
      transform: rotateZ(0deg);
    }
    96% {
      -webkit-transform: rotateZ(90deg);
      transform: rotateZ(90deg);
    }
  }
  @-webkit-keyframes right {
    4% {
      -webkit-transform: rotateZ(-90deg);
      transform: rotateZ(-90deg);
    }
    10%,
    40% {
      -webkit-transform: rotateZ(0deg);
      transform: rotateZ(0deg);
    }
    46%,
    54% {
      -webkit-transform: rotateZ(-90deg);
      transform: rotateZ(-90deg);
    }
    60%,
    90% {
      -webkit-transform: rotateZ(0deg);
      transform: rotateZ(0deg);
    }
    96% {
      -webkit-transform: rotateZ(-90deg);
      transform: rotateZ(-90deg);
    }
  }
  @keyframes right {
    4% {
      -webkit-transform: rotateZ(-90deg);
      transform: rotateZ(-90deg);
    }
    10%,
    40% {
      -webkit-transform: rotateZ(0deg);
      transform: rotateZ(0deg);
    }
    46%,
    54% {
      -webkit-transform: rotateZ(-90deg);
      transform: rotateZ(-90deg);
    }
    60%,
    90% {
      -webkit-transform: rotateZ(0deg);
      transform: rotateZ(0deg);
    }
    96% {
      -webkit-transform: rotateZ(-90deg);
      transform: rotateZ(-90deg);
    }
  }
  @-webkit-keyframes book {
    4% {
      -webkit-transform: rotateZ(-90deg);
      transform: rotateZ(-90deg);
    }
    10%,
    40% {
      -webkit-transform: rotateZ(0deg);
      transform: rotateZ(0deg);
      -webkit-transform-origin: 2px 2px;
      transform-origin: 2px 2px;
    }
    40.01%,
    59.99% {
      -webkit-transform-origin: 30px 2px;
      transform-origin: 30px 2px;
    }
    46%,
    54% {
      -webkit-transform: rotateZ(90deg);
      transform: rotateZ(90deg);
    }
    60%,
    90% {
      -webkit-transform: rotateZ(0deg);
      transform: rotateZ(0deg);
      -webkit-transform-origin: 2px 2px;
      transform-origin: 2px 2px;
    }
    96% {
      -webkit-transform: rotateZ(-90deg);
      transform: rotateZ(-90deg);
    }
  }
  @keyframes book {
    4% {
      -webkit-transform: rotateZ(-90deg);
      transform: rotateZ(-90deg);
    }
    10%,
    40% {
      -webkit-transform: rotateZ(0deg);
      transform: rotateZ(0deg);
      -webkit-transform-origin: 2px 2px;
      transform-origin: 2px 2px;
    }
    40.01%,
    59.99% {
      -webkit-transform-origin: 30px 2px;
      transform-origin: 30px 2px;
    }
    46%,
    54% {
      -webkit-transform: rotateZ(90deg);
      transform: rotateZ(90deg);
    }
    60%,
    90% {
      -webkit-transform: rotateZ(0deg);
      transform: rotateZ(0deg);
      -webkit-transform-origin: 2px 2px;
      transform-origin: 2px 2px;
    }
    96% {
      -webkit-transform: rotateZ(-90deg);
      transform: rotateZ(-90deg);
    }
  }

  :global(html) {
    box-sizing: border-box;
    -webkit-font-smoothing: antialiased;
  }

  * {
    box-sizing: inherit;
  }
  *:before,
  *:after {
    box-sizing: inherit;
  }
</style>

{#if loading}
  <div
    class="cover"
    style="background-color: #275efe; height:100vh;width:100vw">
    <div class="book">
      <div class="inner">
        <div class="left" />
        <div class="middle" />
        <div class="right" />
      </div>
      <ul>
        {#each [...Array(18).keys()] as _k}
          <li />
        {/each}
      </ul>
    </div>
  </div>
{:else}
  <div class="container">
    <div class="paper">
      <Grid>
        <Row>
          <Column>
            <img {src} alt={subtitle} />
          </Column>
          <Column>
            <h1>{title}</h1>
            <br />
            <h2>{subtitle}</h2>
            <br />
            <h3>
              By
              <a href={window.location.origin + '?author=' + author}>
                {author}
              </a>
              · {year}
            </h3>
            <br />
            <Accordion>
              <AccordionItem title="Description" bind:open>
                <p style="text-align:justify">{description_handler()}</p>
              </AccordionItem>
            </Accordion>
            <br />
            <Button href={download} icon={Download32}>Download</Button>
          </Column>
        </Row>
      </Grid>
    </div>
  </div>
{/if}
