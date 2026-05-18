declare global {
  namespace App {
    interface Platform {
      env?: {
        // bindings can be declared here once we add KV / D1 / etc.
      };
      context?: { waitUntil(promise: Promise<unknown>): void };
      caches?: CacheStorage & { default: Cache };
    }
  }
}

export {};
