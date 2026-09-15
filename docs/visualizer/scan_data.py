import os, json, re

BASE_DIR = '/Users/devang/Desktop/live_feed_console'

def analyze_codebase():
    files_to_scan = [
        # Feeds domain
        {'path': 'src/feeds/Feed.js', 'type': 'src', 'cluster': 'feeds'},
        {'path': 'src/feeds/errors.js', 'type': 'src', 'cluster': 'errors'},
        {'path': 'src/feeds/pipeline.js', 'type': 'src', 'cluster': 'pipeline'},
        {'path': 'src/feeds/PollingFeed.js', 'type': 'src', 'cluster': 'feeds'},
        # Utils
        {'path': 'utils/helpers.js', 'type': 'utils', 'cluster': 'utils'},
        {'path': 'utils/assertions.js', 'type': 'utils', 'cluster': 'assertions'},
        {'path': 'utils/validators.js', 'type': 'utils', 'cluster': 'validators'},
        # Katas
        {'path': 'kata/curry.js', 'type': 'kata', 'cluster': 'kata'},
        {'path': 'kata/partial_application.js', 'type': 'kata', 'cluster': 'kata'},
        {'path': 'kata/currying.js', 'type': 'kata', 'cluster': 'kata'},
        {'path': 'kata/test_curry.mjs', 'type': 'kata', 'cluster': 'kata'},
        # Tests
        {'path': 'tests/src/feeds/Feed.test.js', 'type': 'test', 'cluster': 'test'},
        {'path': 'tests/src/feeds/pipeline.test.js', 'type': 'test', 'cluster': 'test'},
        {'path': 'tests/src/feeds/errors.test.js', 'type': 'test', 'cluster': 'test'},
        {'path': 'tests/utils/helpers.test.js', 'type': 'test', 'cluster': 'test'},
        {'path': 'tests/utils/assertions.test.js', 'type': 'test', 'cluster': 'test'},
        {'path': 'tests/utils/validators.test.js', 'type': 'test', 'cluster': 'test'},
    ]

    scanned = []
    for item in files_to_scan:
        full_path = os.path.join(BASE_DIR, item['path'])
        if os.path.exists(full_path):
            with open(full_path, 'r', encoding='utf-8') as f:
                content = f.read()
            lines = content.splitlines()
            imports = re.findall(r'import\s+(?:{[^}]+}|\w+|\*\s+as\s+\w+)?\s+from\s+[\'"]([^\'"]+)[\'"]', content)
            exports = re.findall(r'export\s+(?:default\s+)?(?:class|const|function|let|var|{[^}]+})\s*([a-zA-Z0-9_$]+)?', content)
            scanned.append({
                'path': item['path'],
                'name': os.path.basename(item['path']),
                'type': item['type'],
                'cluster': item['cluster'],
                'line_count': len(lines),
                'byte_size': len(content),
                'imports': imports,
                'raw_content': content
            })
    return scanned

if __name__ == '__main__':
    data = analyze_codebase()
    print(f"Scanned {len(data)} files successfully.")
