"""One-time static migration and upload packaging. Not needed to run the site."""
from pathlib import Path
import re, zipfile

root = Path(__file__).resolve().parent.parent
upgrade = root / 'assets/upgrade.js'
source = upgrade.read_text(encoding='utf-8-sig')
source = source.replace('share a keyboard or create a private Wi-Fi room.', 'share a keyboard or connect directly over Wi-Fi.')
source = source.replace('Private rooms for Pong, Tic-Tac-Toe and Connect Four. Open this server on another device on the same Wi-Fi, then share your room code.', 'Pong, Tic-Tac-Toe and Connect Four work on one device or directly between two browsers on the same Wi-Fi. Exchange an invite and a reply to connect — no server or account needed.')
source = source.replace('🏓 Pong rooms', '🏓 Pong together')
source = source.replace('Checking local server…', 'GitHub Pages ready · no installation required')
source = source.replace('Console multiplayer: open Mario Kart, Mario World or Mario Bros, select the emulator’s Netplay menu, then create or join the same room. In Mario Bros and Mario World, players take turns.', 'Console games support same-device play through the emulator’s Control Settings. Mario Kart supports two controllers; Mario Bros and Mario World use alternating turns. Console netplay needs an external service and is not enabled in this static edition.')
source = source.replace('🌐 Open web proxy', '🌐 Web launcher')
source = re.sub(r"fetch\('/api/status'\).*?;\n", '', source, count=1)
upgrade.write_text(source, encoding='utf-8')
for file in ['games.html']:
    p = root / file
    p.write_text(p.read_text(encoding='utf-8-sig').replace('href="/"', 'href="index.html"'), encoding='utf-8')
for file in ['smb.html', 'smk.html', 'smw.html']:
    p = root / file
    s = p.read_text(encoding='utf-8-sig')
    s = re.sub(r'^\s*EJS_(DEBUG_XX|EXPERIMENTAL_NETPLAY|netplayServer|netplayICEServers|Buttons)\s*=.*?;\s*$', '', s, flags=re.M)
    p.write_text(s, encoding='utf-8')
css = root / 'assets/play.css'
s = css.read_text(encoding='utf-8-sig')
if '#connection textarea' not in s:
    s += '\n#connection textarea{display:block;width:100%;resize:vertical;border:1px solid #414d72;border-radius:12px;padding:12px;margin:8px 0;background:#080d1d;color:#dce6ff;font:12px monospace;overflow-wrap:anywhere}#connection label{display:block;margin-top:16px}#connection p{color:#bcc7e6}\n'
css.write_text(s, encoding='utf-8')
# Move Slope's embedded Unity JSON into a normal asset. This keeps each upload
# below GitHub's browser-upload size limit and removes an enormous data URL.
import base64
p = root / 'slope.html'
s = p.read_text(encoding='utf-8-sig')
match = re.search(r'UnityLoader.instantiate\([^,]+,([\x22\x27])(data:application/json;base64,[A-Za-z0-9+/=]+)\1', s)
if match:
    (root / 'assets/slope-build.json').write_bytes(base64.b64decode(match[2].split(',', 1)[1]))
    s = s[:match.start(2)] + 'assets/slope-build.json' + s[match.end(2):]
    p.write_text(s, encoding='utf-8')
import json
build = root / 'assets/slope-build.json'
if build.exists():
    config = json.loads(build.read_text(encoding='utf-8'))
    for key, value in list(config.items()):
        if isinstance(value, str) and value.startswith('data:application/octet-stream;base64,'):
            name = 'slope-' + key.replace('Url', '') + '.unityweb'
            (build.parent / name).write_bytes(base64.b64decode(value.split(',', 1)[1]))
            config[key] = name
    build.write_text(json.dumps(config, separators=(',', ':')), encoding='utf-8')
files = [p for p in root.iterdir() if p.is_file() and p.suffix.lower() in ['.html', '.jpg', '.png', '.gif', '.ico']]
files += [root / '.nojekyll', root / 'README.md', root / 'sw.js']
for folder in ['assets','img','media','fb','pacman']:
    files += [p for p in (root/folder).rglob('*') if p.is_file()]
out = root / 'quarter-github-pages.zip'
with zipfile.ZipFile(out, 'w', zipfile.ZIP_DEFLATED) as z:
    for p in sorted(set(files)):
        z.write(p, p.relative_to(root).as_posix())
print(f'Packaged {len(set(files))} static files: {out}')
