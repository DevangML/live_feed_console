import os, json, re

BASE_DIR = '/Users/devang/Desktop/live_feed_console'

def build_tree():
    result = []
    scan_paths = ['src', 'utils', 'kata', 'tests', 'docs']
    for sp in scan_paths:
        full_sp = os.path.join(BASE_DIR, sp)
        if not os.path.exists(full_sp): continue
        for root, dirs, files in os.walk(full_sp):
            if any(x in root for x in ['node_modules', '.git']): continue
            for f in sorted(files):
                if f.endswith(('.js', '.mjs', '.md', '.json')) and not f.endswith('concept_graph.json'):
                    fp = os.path.join(root, f)
                    rel = os.path.relpath(fp, BASE_DIR)
                    with open(fp, 'r', encoding='utf-8', errors='ignore') as fh:
                        content = fh.read()
                    lines = content.splitlines()
                    result.append({
                        "path": rel,
                        "filename": f,
                        "ext": os.path.splitext(f)[1],
                        "lines": len(lines),
                        "bytes": len(content),
                        "mtime": os.path.getmtime(fp)
                    })
    return result

if __name__ == '__main__':
    tree = build_tree()
    print(f"Discovered {len(tree)} files across repository.")
