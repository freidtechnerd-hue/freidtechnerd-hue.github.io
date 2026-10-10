import fs from 'node:fs';
let s=fs.readFileSync('assets/games.js','utf8');
if(!s.includes('function saveBest')){
s=s.replace('function start(){',`function saveBest(value){try{const key='quarter_best_'+mode;localStorage.setItem(key,Math.max(Number(localStorage.getItem(key)||0),Math.floor(value)));}catch{}}\nfunction start(){`);
s=s.replace("score.textContent=values.some(Boolean)?moves+' moves':'Cleared in '+moves+' moves!';", "if(!values.some(Boolean))saveBest(Math.max(1,1000-moves));score.textContent=values.some(Boolean)?moves+' moves':'Cleared in '+moves+' moves!';");
s=s.replace("score.textContent=won?'Solved in '+moves+' moves!':moves+' moves';", "if(won)saveBest(Math.max(1,1000-moves));score.textContent=won?'Solved in '+moves+' moves!':moves+' moves';");
s=s.replace("score.textContent='Black '+black", "if(over&&black>white)saveBest(black);score.textContent='Black '+black");
s=s.replace("score.textContent=Math.floor(points)+' points'", "if(over)saveBest(points);score.textContent=Math.floor(points)+' points'");
fs.writeFileSync('assets/games.js',s);
}
