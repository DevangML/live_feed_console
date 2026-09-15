import os, json, re

BASE_DIR = '/Users/devang/Desktop/live_feed_console'

def deep_analyze_codebase():
    results = {}
    for folder in ['src', 'utils', 'kata', 'tests']:
        full_dir = os.path.join(BASE_DIR, folder)
        if not os.path.exists(full_dir): continue
        for root, dirs, files in os.walk(full_dir):
            for f in sorted(files):
                if f.endswith(('.js', '.mjs')):
                    p = os.path.join(root, f)
                    rel = os.path.relpath(p, BASE_DIR)
                    with open(p, 'r', encoding='utf-8') as fh:
                        src = fh.read()
                    
                    imports = re.findall(r'import\s+(?:{[^}]+}|\w+|\*\s+as\s+\w+)?\s+from\s+[\'"]([^\'"]+)[\'"]', src)
                    exports = re.findall(r'export\s+(?:default\s+)?(?:class|const|function|let|var|{[^}]+})\s*([a-zA-Z0-9_$]+)?', src)
                    classes = re.findall(r'class\s+([A-Za-z0-9_$]+)(?:\s+extends\s+([A-Za-z0-9_$]+))?', src)
                    methods = re.findall(r'([A-Za-z0-9_$#]+)\s*\([^)]*\)\s*\{', src)
                    throws = re.findall(r'throw\s+new\s+([A-Za-z0-9_$]+)\(([^)]*)\)', src)
                    
                    results[rel] = {
                        'path': rel,
                        'name': f,
                        'size': len(src),
                        'lines': len(src.splitlines()),
                        'imports': imports,
                        'exports': exports,
                        'classes': classes,
                        'methods': methods,
                        'throws': throws
                    }
    return results

data = deep_analyze_codebase()
print(f"Deep analyzed {len(data)} codebase files.")
for k, v in data.items():
    print(f" - {k}: {v['lines']} lines, {len(v['imports'])} imports, classes={v['classes']}, throws={len(v['throws'])}")
