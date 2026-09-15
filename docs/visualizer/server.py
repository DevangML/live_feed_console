#!/usr/bin/env python3
"""Local architecture viewer. Curated semantics + a fresh repository inventory."""
import hashlib
import http.server
import json
import os
from pathlib import Path
import re
from urllib.parse import parse_qs, unquote, urlsplit

BASE_DIR = Path(__file__).resolve().parents[2]
VISUALIZER_DIR = BASE_DIR / 'docs' / 'visualizer'
PORT = int(os.environ.get('VISUALIZER_PORT', '8088'))
SOURCE_SUFFIXES = {'.js', '.mjs', '.cjs', '.ts', '.tsx', '.jsx'}


def safe_file(root, relative):
    root = Path(root).resolve()
    candidate = (root / relative).resolve()
    return candidate if candidate.is_relative_to(root) and candidate.is_file() else None


def build_graph(root=BASE_DIR):
    """Preserve curated fields; discover files and literal relative imports.

    Import discovery is a lightweight heuristic, not a JavaScript parser. Test
    edges indicate source references, never an assertion that tests have passed.
    """
    root = Path(root)
    graph = json.loads((root / 'docs/visualizer/pipeline_graph.json').read_text())
    curated = {n['path']: n for n in graph['nodes']}
    nodes, contents = [], {}
    for folder in ('src', 'utils', 'tests'):
        for path in sorted((root / folder).rglob('*')):
            if path.suffix not in SOURCE_SUFFIXES or not safe_file(root, path):
                continue
            relative = path.relative_to(root).as_posix()
            text = path.read_text(encoding='utf-8')
            contents[relative] = text
            node = curated.get(relative)
            if node is None:
                test = folder == 'tests'
                node = dict(id=relative, name=path.name, path=relative,
                            cluster='test-dock' if test else 'foundations',
                            stage='Verification Dock' if test else 'Discovered source',
                            color='#1dd1a1' if test else '#ffb700', pos=[0, 48 if test else -42, 0],
                            semanticsAndFlow={'executionRole': 'Discovered from disk',
                                              'flow': 'Imports and line counts are inferred from source. Architectural role and contracts await review.'})
            node['metrics'] = {'lines': len(text.splitlines()), 'bytes': len(text.encode())}
            node['sourceHash'] = hashlib.sha256(text.encode()).hexdigest()
            node['evidence'] = 'Source discovered; semantics need review' if relative not in curated else 'Curated explanation · inspect live source'
            nodes.append(node)
    by_path = {n['path']: n for n in nodes}
    ids = {n['id'] for n in nodes}
    graph['nodes'] = nodes
    graph['edges'] = [e for e in graph['edges'] if e['source'] in ids and e['target'] in ids]
    for edge in graph['edges']:
        edge.setdefault('evidence', 'Curated relationship')
    pairs = {(e['source'], e['target'], e['type']) for e in graph['edges']}
    for relative, text in contents.items():
        source = by_path[relative]
        # Static imports, exports-from and literal dynamic imports / require.
        imports = re.findall(r'''(?:\bfrom\s*|\bimport\s*\(?\s*|\brequire\s*\(\s*)['"](\.[^'"]+)['"]''', text)
        source['imports'] = sorted(set(imports))
        for specifier in source['imports']:
            target = (root / relative).parent / specifier
            candidates = [target, *(Path(str(target) + ext) for ext in sorted(SOURCE_SUFFIXES)), target / 'index.js']
            resolved = next((p.resolve().relative_to(root.resolve()).as_posix() for p in candidates
                             if p.resolve().is_relative_to(root.resolve()) and p.resolve().relative_to(root.resolve()).as_posix() in by_path), None)
            if not resolved:
                continue
            destination = by_path[resolved]
            kind = 'tests' if relative.startswith('tests/') else 'imports'
            key = (source['id'], destination['id'], kind)
            if key not in pairs:
                graph['edges'].append(dict(source=key[0], target=key[1], type=kind,
                    label='Test source reference' if kind == 'tests' else 'Source import',
                    concept=specifier, evidence='Literal import scan; not execution coverage'))
                pairs.add(key)
    # Keep every test inside its dock; size both support zones to fit discovery.
    for cluster, zone_id, y in [('test-dock', 'zone-tests', 48), ('foundations', 'zone-foundations', -42)]:
        members = [n for n in nodes if n['cluster'] == cluster]
        for i, node in enumerate(members):
            node['pos'] = [(i - (len(members) - 1) / 2) * 25, y, 0]
        zone = next(z for z in graph['zones'] if z['id'] == zone_id)
        zone['bounds'].update(x=0, y=y, z=0, width=max(90, len(members) * 25 + 10), height=26, depth=28)
    graph['discovery'] = {'intervalSeconds': 5, 'files': len(nodes), 'method': 'Literal import scan; curated runtime relationships'}
    graph['revision'] = hashlib.sha256(json.dumps(graph, sort_keys=True).encode()).hexdigest()
    return graph


class LiveFeedVisualizerHandler(http.server.SimpleHTTPRequestHandler):
    def end_headers(self):
        self.send_header('Cache-Control', 'no-store')
        super().end_headers()

    def translate_path(self, path):
        route = unquote(urlsplit(path).path)
        aliases = {'/': 'index.html', '/index.html': 'index.html', '/katas': 'katas.html',
                   '/katas.html': 'katas.html', '/visualizer/katas.html': 'katas.html'}
        if route in aliases:
            return str(VISUALIZER_DIR / aliases[route])
        relative = route.lstrip('/')
        candidate = safe_file(BASE_DIR, relative) or safe_file(VISUALIZER_DIR, relative)
        return str(candidate or VISUALIZER_DIR / '__not_found__')

    def do_GET(self):
        url = urlsplit(self.path)
        if url.path == '/api/graph':
            try:
                data = json.dumps(build_graph()).encode()
            except (OSError, ValueError, KeyError) as error:
                self.send_error(500, str(error))
                return
            self.send_response(200)
            self.send_header('Content-Type', 'application/json; charset=utf-8')
            self.send_header('Content-Length', str(len(data)))
            self.end_headers()
            self.wfile.write(data)
            return
        if url.path == '/api/file-content':
            relative = parse_qs(url.query).get('path', [''])[0]
            target = safe_file(BASE_DIR, relative)
            if target is None:
                self.send_error(404)
                return
            data = target.read_bytes()
            self.send_response(200)
            self.send_header('Content-Type', 'text/plain; charset=utf-8')
            self.send_header('Content-Length', str(len(data)))
            self.end_headers()
            self.wfile.write(data)
            return
        super().do_GET()


if __name__ == '__main__':
    with http.server.ThreadingHTTPServer(('127.0.0.1', PORT), LiveFeedVisualizerHandler) as httpd:
        print(f'Visualizer: http://localhost:{PORT}', flush=True)
        httpd.serve_forever()
