import fs from 'node:fs';
let s=fs.readFileSync('assets/upgrade.js','utf8');
s=s.replace('clearInterval(musicTimer);if(music.checked','clearInterval(musicTimer);musicTimer=null;if(music.checked');
s=s.replace('if(!audioCtx&&music.checked){tone(261,.01,.01);syncMusic();}','if(music.checked&&!musicTimer){syncMusic();}');
s=s.replace('launchOriginal(id,name,url);syncMusic();',"launchOriginal(id,name,url);const game=GAMES.find(g=>g.id===id);if(url&&game?.platform==='browser')stageHelp.textContent='Use the game controls shown above. Close to return to the library.';syncMusic();");
s=s.replace('renderPlatforms();refresh();renderStats();finishSession();','renderPlatforms();refresh();renderStats();renderLeaderboard();finishSession();');
fs.writeFileSync('assets/upgrade.js',s);
let main=fs.readFileSync('index.html','utf8');main=main.replace("GAMES.filter(g=>!isLinked(g) && !g.placeholder)","GAMES.filter(g=>(!isLinked(g)||g.platform==='browser'&&!g.multiplayer)&&!g.placeholder)");fs.writeFileSync('index.html',main);
