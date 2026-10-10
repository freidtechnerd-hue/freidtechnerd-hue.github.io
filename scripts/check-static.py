from pathlib import Path
from html.parser import HTMLParser
from urllib.parse import urlparse, unquote, urljoin
import zipfile

root = Path(__file__).resolve().parent.parent
missing = []

class References(HTMLParser):
    def __init__(self, name):
        super().__init__()
        self.name = name
        self.base = ''
    def handle_starttag(self, tag, attrs):
        for key, value in attrs:
            if key not in ('src', 'href') or not value:
                continue
            if tag == 'base' and key == 'href':
                self.base = value
                return
            url = urlparse(urljoin(self.base, value))
            if url.scheme or url.netloc or not url.path:
                continue
            target = root / Path(self.name).parent / unquote(url.path)
            if value.startswith('/') or not target.exists():
                missing.append((self.name, value))

with zipfile.ZipFile(root/'quarter-github-pages.zip') as archive:
    names = set(archive.namelist())
    for name in names:
        if name.endswith('.html'):
            References(name).feed(archive.read(name).decode('utf-8', errors='replace'))
    assert not missing, missing
    assert not any(n.endswith('.mjs') or n.startswith(('node_modules/','.local/')) for n in names)
    assert '.nojekyll' in names and 'index.html' in names
    biggest = max((info.file_size,info.filename) for info in archive.infolist())
    assert biggest[0] < 25*1024*1024, biggest
    print('Static references, repository-relative paths, hidden build marker and upload sizes passed.')
    print(f'{len(names)} files; largest: {biggest[1]} ({biggest[0]} bytes). No backend or certificates.')
