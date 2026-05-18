<script lang="ts">
  import { page } from '$app/state';
</script>

<div class="min-h-screen flex flex-col items-center justify-center px-6 text-center">
  <p class="font-display text-7xl mb-2">{page.status}</p>
  <p class="text-muted-foreground mb-6">{page.error?.message ?? 'something went sideways'}</p>
  <a href="/" class="text-sm underline hover:text-accent">back to search</a>
</div>
