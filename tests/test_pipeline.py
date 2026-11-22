import importlib.util
import json
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

def load(name):
    spec = importlib.util.spec_from_file_location(name, ROOT / (name + '.py'))
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod

class PipelineTests(unittest.TestCase):
    def test_stock_features_leave_warmup_null(self):
        with tempfile.TemporaryDirectory() as temp:
            p = Path(temp)
            records = [{'ticker':'TEST','date':f'2026-01-{i:02d}','close':float(i), 'open':float(i),'high':float(i),'low':float(i),'volume':100} for i in range(1, 29)]
            (p/'input.json').write_text(json.dumps(records))
            load('compute_technical_features').compute_features(p/'input.json', p/'out.json')
            out = json.loads((p/'out.json').read_text())
            self.assertIsNone(out[0]['sma_20'])
            self.assertEqual(out[19]['sma_20'], 10.5)
            self.assertIsNone(out[0]['momentum_20d'])
    def test_macro_features_use_us_names(self):
        with tempfile.TemporaryDirectory() as temp:
            p=Path(temp)
            records=[{'date':f'2026-01-{i:02d}','indicator':name,'value':str(val),'frequency':'daily'} for i in range(1, 29) for name,val in [('us_yield_data',5),('us_interest_rate',3),('us_inflation',100+i)]]
            (p/'input.json').write_text(json.dumps(records))
            load('build_macro_features').build_features(p/'input.json',p/'out.json')
            out=json.loads((p/'out.json').read_text())
            self.assertEqual(out['2026-01-28']['yield_spread'],2)
            self.assertEqual(out['2026-01-01']['macro_regime'],'Insufficient data')

if __name__ == '__main__': unittest.main()
