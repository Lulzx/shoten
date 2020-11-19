import HMR from '@roxi/routify/hmr'
// @ts-ignore
import App from './App.svelte';

const app = HMR(App, { target: document.body }, 'routify-app')

export default app;
