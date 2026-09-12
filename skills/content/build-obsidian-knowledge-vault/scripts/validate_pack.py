#!/usr/bin/env python3
"""Validate a domain-specific Obsidian graph and package it. Python stdlib only."""
import argparse, collections, hashlib, json, re, zipfile
from pathlib import Path

ORIGINS = {'transcription','source_synthesis','inference','proposal','navigation'}
STATUSES = {'ingested','partial','blocked','unavailable','excluded'}
def ensure(condition, message):
    if not condition: raise ValueError(message)
def read(path): return json.loads(path.read_text(encoding='utf-8'))
def dump(path,obj): path.write_text(json.dumps(obj,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
def in_root(root,relative):
    p=Path(relative)
    ensure(not p.is_absolute() and '..' not in p.parts, f'Unsafe path: {relative}')
    out=root/p
    ensure(out.resolve().is_relative_to(root), f'Path escapes vault: {relative}')
    return out

def scalar_frontmatter(text,key):
    m=re.match(r'\A---\s*\n(.*?)\n---\s*(?:\n|$)',text,re.S)
    ensure(m is not None,'Missing YAML frontmatter')
    line=re.search(r'^'+re.escape(key)+r':\s*(.*?)\s*$',m[1],re.M)
    ensure(line is not None,f'Missing YAML {key}')
    return line[1].strip().strip('"\'')

def validate(root, archive=None, write_reports=True, check_federation=True):
    ensure(root.is_dir(),'Vault directory not found')
    if archive is not None:
        ensure(not archive.resolve().is_relative_to(root),'ZIP must be outside the vault')
        ensure(not archive.exists(),'Output ZIP exists; choose a new destination')
    for p in root.rglob('*'): ensure(not p.is_symlink(),f'Symlink not allowed: {p}')
    ontology=read(root/'Grafo/ontology.json'); graph=read(root/'Grafo/graph.json'); ledger=read(root/'Grafo/sources.json')
    for key in ('domain','problem','audience'): ensure(ontology.get(key),f'Missing ontology {key}')
    types=set(ontology['node_types']); predicates=ontology['relation_types']
    for label,rule in predicates.items():
        ensure(set(rule['domain'])<=types and set(rule['range'])<=types,f'Unknown type in relation {label}')
    nodes=graph['nodes']; edges=graph['edges']; sources=ledger['references']
    by_id={}; stems={}; by_path={}; contents={}
    for n in nodes:
        ensure(n['id'] not in by_id,f"Duplicate node id {n['id']}")
        ensure(n['type'] in types,f"Undefined node type {n['type']}")
        ensure(n['origin'] in ORIGINS,f"Undefined origin for {n['id']}")
        p=in_root(root,n['path'])
        ensure(p.is_file() and p.suffix=='.md',f"Missing note {n['path']}")
        key=p.stem.casefold()
        ensure(key not in stems,f'Duplicate basename {p.stem}')
        ensure(n['path'] not in by_path,f"Duplicate path {n['path']}")
        text=p.read_text(encoding='utf-8')
        for field in ('id','type','origin'): ensure(scalar_frontmatter(text,field)==n[field],f"YAML {field} differs for {n['path']}")
        by_id[n['id']]=n; stems[key]=n; by_path[n['path']]=n; contents[n['id']]=text
    ensure(set(by_path)=={str(p.relative_to(root)) for p in root.rglob('*.md')},'Unregistered Markdown notes')
    source_ids={}
    for s in sources:
        ensure(s['id'] not in source_ids,f"Duplicate source {s['id']}")
        ensure(s['status'] in STATUSES,f"Invalid status {s['id']}")
        ensure(s['role'] in ('primary','reference','supplemental'),f"Invalid role {s['id']}")
        ensure(s.get('url') or s.get('input_file'),f"Missing source locator {s['id']}")
        ensure(isinstance(s['depth'],int) and s['depth']>=0,f"Invalid depth {s['id']}")
        ensure(s.get('retention') in ('user_supplied_copy','licensed_copy','summary_only','metadata_only'),f"Invalid retention {s['id']}")
        if s['status'] in ('ingested','partial'):
            ensure(s.get('note_id') in by_id,f"Missing source note {s['id']}")
            ensure(s.get('retrieved_at') and s.get('read_scope'),f"Missing read scope/date {s['id']}")
        if s['status']!='ingested':ensure(s.get('reason'),f"Missing status reason {s['id']}")
        if s['depth']>1:ensure(s.get('reason'),f"Missing expansion reason {s['id']}")
        source_ids[s['id']]=s
    ensure(any(s['role']=='primary' for s in sources),'Missing primary source')
    for s in sources:
        if s['role']=='primary':ensure(s['depth']==0 and not s.get('parent'),f"Bad primary lineage {s['id']}")
        if s['role']=='reference':
            ensure(s.get('parent') in source_ids,f"Missing source parent {s['id']}")
            ensure(source_ids[s['parent']]['depth']+1==s['depth'],f"Bad source depth {s['id']}")
    seen_edges=set()
    for e in edges:
        ensure(e['source'] in by_id and e['target'] in by_id,'Edge endpoint missing')
        ensure(e['relation'] in predicates,f"Undefined relation {e['relation']}")
        ensure(e['origin'] in ORIGINS-{'navigation'},'Semantic edge has invalid origin')
        rule=predicates[e['relation']]
        ensure(by_id[e['source']]['type'] in rule['domain'],'Relation domain mismatch')
        ensure(by_id[e['target']]['type'] in rule['range'],'Relation range mismatch')
        key=(e['source'],e['relation'],e['target'])
        ensure(key not in seen_edges,f'Duplicate semantic edge {key}');seen_edges.add(key)
        ensure(e.get('evidence'),'Semantic edge lacks evidence')
        for evidence in e['evidence']:
            sid=evidence['source_id']
            ensure(sid in source_ids and source_ids[sid]['status'] in ('ingested','partial'),'Evidence source not read')
            ensure(evidence.get('locator'),'Evidence lacks locator')
        if e['origin'] in ('inference','proposal'):ensure(e.get('rationale'),'Inference/proposal lacks rationale')
    navigation=set()
    for ident,text in contents.items():
        text=re.sub(r'^---\s*\n.*?\n---\s*\n','',text,count=1,flags=re.S)
        # Fenced and inline code may contain example wikilinks.
        text=re.sub(r'(?ms)^\s*(`{3,}|~{3,})[^\n]*\n.*?^\s*\1\s*$','',text)
        text=re.sub(r'`[^`\n]*`','',text)
        for raw in re.findall(r'\[\[([^\]\n]+)\]\]',text):
            target=raw.split('|',1)[0].split('#',1)[0].strip()
            if not target:continue  # same-note heading
            path=target if target.endswith('.md') else target+'.md'
            n=by_path.get(path) or stems.get(target.removesuffix('.md').casefold())
            if n:navigation.add((ident,n['id']))
            else:ensure(in_root(root,target).is_file(),f'Broken wikilink from {ident}: {raw}')
    coverage=collections.Counter(s['status'] for s in sources if s['status']!='excluded')
    pending=[s['id'] for s in sources if s['status'] in ('partial','blocked','unavailable')]
    result={'notes':len(nodes),'semantic_edges':len(edges),'navigation_links':len(navigation),
            'sources':len(sources),'coverage':dict(coverage),'excluded':sum(s['status']=='excluded' for s in sources),
            'coverage_state':'partial' if pending else 'complete_for_declared_scope','gaps':pending,
            'structural_validation':'passed','fact_check':'not_assessed_by_validator',
            'link_scope':'Wikilink files only; headings and Markdown links require separate review'}
    if check_federation and (root/'Grafo/federation.json').exists():
        try:
            from .federation_contract import validate_federation
        except ImportError:
            from federation_contract import validate_federation
        federation=validate_federation(root)
        result.update(schema_version=federation['schema_version'],vault_id=federation['vault_id'],revision=federation['revision'])
    if not write_reports:return result
    dump(root/'Grafo/validation.json',result)
    dump(root/'Grafo/navigation.json',[{'source':a,'relation':'links_to','target':b} for a,b in sorted(navigation)])
    manifest=[]
    for p in sorted(root.rglob('*')):
        if p.is_file() and p!=root/'Grafo/manifest.json':
            manifest.append({'path':str(p.relative_to(root)),'bytes':p.stat().st_size,'sha256':hashlib.sha256(p.read_bytes()).hexdigest()})
    dump(root/'Grafo/manifest.json',{'excludes':['Grafo/manifest.json'],'files':manifest})
    if archive is None:return result
    archive.parent.mkdir(parents=True,exist_ok=True)
    with zipfile.ZipFile(archive,'w',zipfile.ZIP_DEFLATED) as z:
        for p in sorted(root.rglob('*')):
            if p.is_file():z.write(p,Path(root.name)/p.relative_to(root))
    with zipfile.ZipFile(archive) as z:ensure(z.testzip() is None,'ZIP integrity failure')
    return result

def main():
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument('vault',type=Path);p.add_argument('--zip',required=True,type=Path)
    a=p.parse_args()
    try:result=validate(a.vault.resolve(),a.zip)
    except (ValueError,KeyError,TypeError,OSError,json.JSONDecodeError) as exc:p.exit(1,f'Validation failed: {exc}\n')
    print(json.dumps(result,ensure_ascii=False,indent=2))
if __name__=='__main__': main()
