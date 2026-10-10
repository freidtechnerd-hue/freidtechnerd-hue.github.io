// Retire the previous development proxy worker if this origin had one installed.
// New installs use plain static files and do not register a service worker.
self.addEventListener('install',()=>self.skipWaiting());
self.addEventListener('activate',event=>event.waitUntil((async()=>{await self.registration.unregister();const clients=await self.clients.matchAll({type:'window'});for(const client of clients)client.postMessage({type:'quarter-worker-retired'});})()));
