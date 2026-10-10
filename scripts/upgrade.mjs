import fs from 'node:fs';
let html=fs.readFileSync('index.html','utf8');
if(!html.includes('assets/upgrade.css'))html=html.replace('</head>','<link rel="stylesheet" href="assets/upgrade.css">\n</head>');
if(!html.includes('assets/upgrade.js'))html=html.replace('</body>','<script src="assets/upgrade.js"></script>\n</body>');
html=html.replace('Super_Mario_World__USA_.html','smw.html');fs.writeFileSync('index.html',html);
for(const [file,id] of [['smb.html',101],['smk.html',102],['smw.html',103]]){let page=fs.readFileSync(file,'utf8');if(!page.includes('EJS_netplayServer'))page=page.replace('EJS_player =',`EJS_gameID = ${id};\n            EJS_netplayServer = location.origin;\n            EJS_netplayICEServers = [{ urls: 'stun:stun.l.google.com:19302' }];\n            EJS_player =`);if(!page.includes('EJS_EXPERIMENTAL_NETPLAY'))page=page.replace('EJS_gameID =', 'EJS_DEBUG_XX = true;\n            EJS_EXPERIMENTAL_NETPLAY = true;\n            EJS_gameID =');if(!page.includes('EJS_Buttons'))page=page.replace('EJS_gameID =','EJS_Buttons = { netplay: true };\n            EJS_gameID =');fs.writeFileSync(file,page);}
