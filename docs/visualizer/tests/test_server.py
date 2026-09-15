"""Discovery and file-boundary regression checks, independent of project source."""
import importlib.util
import json
from pathlib import Path
import tempfile
import unittest

spec = importlib.util.spec_from_file_location('visualizer_server', Path(__file__).parents[1] / 'server.py')
server = importlib.util.module_from_spec(spec)
spec.loader.exec_module(server)

class GraphTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        for folder in ['docs/visualizer', 'src', 'utils', 'tests', 'kata']:
            (self.root / folder).mkdir(parents=True)
        graph = {'nodes': [], 'edges': [], 'zones': [dict(id=id, bounds={}) for id in ['zone-tests', 'zone-foundations']]}
        (self.root / 'docs/visualizer/pipeline_graph.json').write_text(json.dumps(graph))

    def test_add_modify_delete_and_imports(self):
        (self.root / 'src/a.js').write_text("import { x } from '../utils/a.js';")
        (self.root / 'utils/a.js').write_text('export const x = 1;')
        (self.root / 'tests/a.test.js').write_text("import '../src/a.js';")
        (self.root / 'kata/curry.js').write_text('export const curry = true;')
        before = server.build_graph(self.root)
        self.assertEqual(len(before['nodes']), 3)
        self.assertEqual(len({n['id'] for n in before['nodes']}), 3)
        self.assertTrue(any(e['type'] == 'tests' for e in before['edges']))
        self.assertEqual(before['revision'], server.build_graph(self.root)['revision'])
        (self.root / 'utils/a.js').write_text('export const x = 2;')
        self.assertNotEqual(before['revision'], server.build_graph(self.root)['revision'])
        (self.root / 'utils/a.js').unlink()
        after = server.build_graph(self.root)
        self.assertEqual(len(after['nodes']), 2)
        self.assertFalse(any(e['target'] == 'utils/a.js' for e in after['edges']))

    def test_canonical_containment_and_symlinks(self):
        (self.root / 'src/a.js').write_text('hello')
        self.assertIsNotNone(server.safe_file(self.root, 'src/a.js'))
        self.assertIsNone(server.safe_file(self.root, '../outside.js'))
        self.assertIsNone(server.safe_file(self.root, 'src'))
        with tempfile.TemporaryDirectory() as outside:
            target = Path(outside) / 'secret.js'; target.write_text('secret')
            (self.root / 'src/link.js').symlink_to(target)
            self.assertIsNone(server.safe_file(self.root, 'src/link.js'))
            self.assertEqual(len(server.build_graph(self.root)['nodes']), 1)

    def test_new_tests_fit_inside_dock(self):
        for i in range(12): (self.root / f'tests/{i}.test.js').write_text('')
        graph = server.build_graph(self.root)
        dock = graph['zones'][0]['bounds']
        for node in graph['nodes']:
            self.assertLess(abs(node['pos'][0]) + 7, dock['width'] / 2)
            self.assertEqual(node['pos'][1], dock['y'])

if __name__ == '__main__': unittest.main()
