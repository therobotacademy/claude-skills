#!/usr/bin/env python3
"""Extract supplied WebArchive frames and links, without executing HTML. Stdlib only."""
import argparse, hashlib, json, plistlib, shutil
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import urljoin

class Extractor(HTMLParser):
    def __init__(self, base):
        super().__init__(convert_charrefs=True)
        self.base, self.skip, self.parts, self.links = base, 0, [], []
    def handle_starttag(self, tag, attrs):
        a = dict(attrs)
        if tag in ('script', 'style'): self.skip += 1
        if tag == 'a' and a.get('href'):
            self.links.append({'href': a['href'], 'resolved_url': urljoin(self.base, a['href'])})
    def handle_endtag(self, tag):
        if tag in ('script', 'style'): self.skip = max(0, self.skip-1)
    def handle_data(self, data):
        if not self.skip and data.strip(): self.parts.append(data.strip())

def main():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument('archive', type=Path); p.add_argument('output', type=Path)
    args = p.parse_args()
    raw = args.archive.read_bytes(); archive = plistlib.loads(raw)
    args.output.mkdir(parents=True, exist_ok=False)
    shutil.copyfile(args.archive, args.output/'original.webarchive')
    frames = []
    def walk(item, frame_id):
        resource = item.get('WebMainResource', {})
        body = resource.get('WebResourceData', b'')
        if isinstance(body, str): body = body.encode('utf-8')
        encoding = resource.get('WebResourceTextEncodingName', 'utf-8') or 'utf-8'
        try: content = body.decode(encoding, errors='replace')
        except LookupError: content = body.decode('utf-8', errors='replace')
        url = resource.get('WebResourceURL', '')
        parser = Extractor(url); parser.feed(content)
        (args.output/f'{frame_id}.html').write_bytes(body)
        text = '\n'.join(parser.parts)
        (args.output/f'{frame_id}.txt').write_text(text, encoding='utf-8')
        frames.append({'id':frame_id, 'url':url, 'bytes':len(body), 'characters':len(text),
                       'sha256':hashlib.sha256(body).hexdigest(), 'links':parser.links})
        for i, child in enumerate(item.get('WebSubframeArchives', [])):
            walk(child, f'{frame_id}-{i}')
    walk(archive, 'frame-0')
    result = {'input':args.archive.name, 'sha256':hashlib.sha256(raw).hexdigest(),
              'frames':frames, 'note':'Inspect frames; links extracted are not sources ingested.'}
    (args.output/'extraction.json').write_text(json.dumps(result, ensure_ascii=False, indent=2),encoding='utf-8')
    print(json.dumps({'frames':len(frames),'links':sum(len(f['links']) for f in frames),'output':str(args.output)}))
if __name__ == '__main__': main()
