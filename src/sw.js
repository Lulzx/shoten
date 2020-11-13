// @ts-nocheck

import {
  registerRoute,
  setDefaultHandler,
  setCatchHandler,
} from "workbox-routing";
import { CacheFirst, NetworkFirst } from "workbox-strategies";
import { skipWaiting, clientsClaim } from "workbox-core";
import { precacheAndRoute, matchPrecache } from "workbox-precaching";
import { ExpirationPlugin } from "workbox-expiration";
import { RoutifyPlugin, freshCacheData } from "@roxi/routify/workbox-plugin";

const entrypointUrl = "__app.html";
const fallbackImage = "404.svg";
const files = self.__WB_MANIFEST;

const externalAssetsConfig = () => ({
  cacheName: "external",
  plugins: [
    RoutifyPlugin({
      validFor: 60,
    }),
    new ExpirationPlugin({
      maxEntries: 50,
      purgeOnQuotaError: true,
    }),
  ],
});

precacheAndRoute(files);

skipWaiting();
clientsClaim();

registerRoute(isLocalPage, matchPrecache(entrypointUrl));
registerRoute(isLocalAsset, new CacheFirst());
registerRoute(hasFreshCache, new CacheFirst(externalAssetsConfig()));
setDefaultHandler(new NetworkFirst(externalAssetsConfig()));

setCatchHandler(async ({ event }) => {
  switch (event.request.destination) {
    case "document":
      return await matchPrecache(entrypointUrl);
    case "image":
      return await matchPrecache(fallbackImage);
    default:
      return Response.error();
  }
});

function isLocalAsset({ url, request }) {
  return url.host === self.location.host && request.destination != "document";
}
function isLocalPage({ url, request }) {
  return url.host === self.location.host && request.destination === "document";
}
function hasFreshCache(event) {
  return !!freshCacheData(event);
}
