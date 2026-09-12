#!/usr/bin/env python3
"""Version 2 additive federation contract. No third-party dependencies."""
import argparse
import hashlib
import json
import re
import uuid
from collections import Counter
from pathlib import Path
from urllib.parse import urlsplit, urlunsplit

SCHEMA = '2.0'
READ = {'ingested', 'partial'}

def require(condition, message):
    if not condition:
        raise ValueError(message)

def read(path):
    return json.loads(Path(path).read_text(encoding='utf-8'))

def write(path, data):
    path = Path(path)
    tmp = path.with_suffix(path.suffix + '.tmp')
    tmp.write_text(json.dumps(data, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
    tmp.replace(path)

def digest(value):
    return hashlib.sha256(value).hexdigest()

def scoped(vault_id, local_id):
    # JSON tuple is unambiguous even if local identifiers contain punctuation.
    return json.dumps([vault_id, local_id], ensure_ascii=False, separators=(',', ':'))

def safe_path(root, relative):
    root = Path(root).resolve()
    p = Path(relative)
    require(not p.is_absolute() and '..' not in p.parts, 'Unsafe relative path')
    out = root / p
    require(out.resolve().is_relative_to(root), 'Path escapes vault')
    require(not out.is_symlink(), 'Symlinks are not supported')
    return out

def source_identity(source):
    """Candidate documentary identity, never automatic equivalence of claims."""
    doi = source.get('doi')
    url = source.get('resolved_url') or source.get('url')
    if not doi and url and urlsplit(url).hostname in {'doi.org', 'dx.doi.org'}:
        doi = urlsplit(url).path.lstrip('/')
    if doi:
        key = 'doi:' + re.sub(r'^https?://(?:dx\.)?doi.org/', '', doi, flags=re.I).lower().strip()
        method = 'doi'
    elif source.get('sha256'):
        key, method = 'sha256:' + source['sha256'], 'bytes'
    elif url:
        parts = urlsplit(url)
        # Preserve query and path: both may identify versions or different resources.
        key = 'url:' + urlunsplit((parts.scheme.lower(), parts.netloc.lower(), parts.path, parts.query, ''))
        method = 'url'
    else:
        return {'key': None, 'method': 'unresolved', 'version': source.get('version')}
    return {'key': key, 'method': method, 'version': source.get('version')}

def snapshot(root):
    root = Path(root).resolve()
    graph = read(root / 'Grafo/graph.json')
    paths = {'Grafo/graph.json', 'Grafo/ontology.json', 'Grafo/sources.json'}
    paths.update(n['path'] for n in graph['nodes'])
    files = []
    for relative in sorted(paths):
        raw = safe_path(root, relative).read_bytes()
        files.append({'path': relative, 'sha256': digest(raw), 'bytes': len(raw)})
    revision = digest(json.dumps(files, sort_keys=True, separators=(',', ':')).encode())
    return revision, files

def validate_evidence(items, source_map):
    require(isinstance(items, list), 'Evidence must be a list')
    for ev in items:
        require(ev.get('source_id') in source_map, 'Unknown evidence source')
        require(source_map[ev['source_id']]['status'] in READ, 'Evidence source not read')
        require(isinstance(ev.get('locator'), str) and ev['locator'].strip(), 'Evidence needs a locator')

def validate_federation(root):
    root = Path(root).resolve()
    meta = read(root / 'Grafo/federation.json')
    require(meta.get('schema_version') == SCHEMA, 'Unsupported federation schema')
    require(isinstance(meta.get('vault_id'), str) and meta['vault_id'].startswith('urn:uuid:'), 'vault_id must be a UUID URN')
    uuid.UUID(meta['vault_id'][9:])
    require(isinstance(meta.get('title'), str) and meta['title'].strip(), 'Missing vault title')
    for key in ('languages', 'topics'):
        require(isinstance(meta.get(key), list) and all(isinstance(v, str) and v.strip() for v in meta[key]), 'Invalid ' + key)
    revision, files = snapshot(root)
    require(meta.get('revision') == revision and meta.get('files') == files, 'Stale federation export; run prepare_federation.py')
    graph = read(root / 'Grafo/graph.json')
    ontology = read(root / 'Grafo/ontology.json')
    sources = read(root / 'Grafo/sources.json')['references']
    by_source = {s['id']: s for s in sources}
    require(meta.get('source_identities') == {s['id']: source_identity(s) for s in sources}, 'Stale source identities')
    require(meta.get('coverage') == dict(Counter(s['status'] for s in sources)), 'Stale source coverage')
    require(meta.get('domain') == ontology['domain'] and meta.get('problem') == ontology['problem'], 'Stale domain/problem')
    mappings = meta.get('type_mappings', {})
    require(isinstance(mappings, dict), 'type_mappings must be an object')
    require(set(mappings) <= set(ontology['node_types']), 'Mapping for unknown local type')
    require(all(isinstance(x, str) and x.strip() for x in mappings.values()), 'Invalid type mapping')
    for node in graph['nodes']:
        validate_evidence(node.get('evidence', []), by_source)
    return meta

def prepare(root, title=None, languages=None, topics=None, fork=False):
    """Refresh a valid canonical v1/v2 vault in place; user should migrate a copy."""
    root = Path(root).resolve()
    try:
        from .validate_pack import validate
    except ImportError:
        from validate_pack import validate
    validate(root, write_reports=False, check_federation=False)
    path = root / 'Grafo/federation.json'
    old = read(path) if path.exists() else {}
    if old:
        require(old.get('schema_version') == SCHEMA, 'Unsupported federation schema')
        uuid.UUID(old['vault_id'][9:])
    ontology = read(root / 'Grafo/ontology.json')
    sources = read(root / 'Grafo/sources.json')['references']
    revision, files = snapshot(root)
    result = dict(old)
    result.update(schema_version=SCHEMA,
                  vault_id='urn:uuid:' + str(uuid.uuid4()) if fork or not old else old['vault_id'],
                  revision=revision, title=title or old.get('title') or root.name,
                  domain=ontology['domain'], problem=ontology['problem'],
                  languages=languages if languages is not None else old.get('languages', []),
                  topics=topics if topics is not None else old.get('topics', []),
                  type_mappings=old.get('type_mappings', {}),
                  source_identities={s['id']: source_identity(s) for s in sources},
                  coverage=dict(Counter(s['status'] for s in sources)), files=files)
    write(path, result)
    validate_federation(root)
    return result

def main():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument('vault', type=Path)
    p.add_argument('--title')
    p.add_argument('--language', action='append', dest='languages')
    p.add_argument('--topic', action='append', dest='topics')
    p.add_argument('--fork', action='store_true', help='Explicitly create a new vault identity')
    a = p.parse_args()
    try:
        result = prepare(a.vault, a.title, a.languages, a.topics, a.fork)
    except (ValueError, KeyError, TypeError, OSError) as exc:
        p.exit(1, str(exc) + '\n')
    print(json.dumps({k: result[k] for k in ('schema_version', 'vault_id', 'revision', 'coverage')}, ensure_ascii=False, indent=2))

if __name__ == '__main__':
    main()
