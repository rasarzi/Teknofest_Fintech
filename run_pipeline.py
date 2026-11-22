"""Run the source project's existing data pipelines in dependency order."""
import argparse
import os
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent
STAGES = {
    'stock': ['raw_stock.py', 'clean_stock_data.py', 'standardize_stock_schema.py', 'compute_technical_features.py', 'create_stock_insight.py'],
    'macro': ['build_fred_extractor.py', 'clean_macro_data.py', 'standardize_macro_schema.py', 'build_macro_features.py'],
}

def main():
    parser = argparse.ArgumentParser(description='Financial market data pipeline')
    parser.add_argument('pipeline', choices=['stock', 'macro'])
    parser.add_argument('--with-ai', action='store_true', help='Generate Gemini macro narrative (requires GEMINI_API_KEY)')
    args = parser.parse_args()
    if args.pipeline == 'macro' and not os.getenv('FRED_API_KEY'):
        parser.error('FRED_API_KEY is required for macro extraction')
    if args.with_ai and args.pipeline != 'macro':
        parser.error('--with-ai only applies to the macro pipeline')
    if args.with_ai and not os.getenv('GEMINI_API_KEY'):
        parser.error('GEMINI_API_KEY is required with --with-ai')
    stages = STAGES[args.pipeline] + (['create_macro_insight.py'] if args.with_ai else [])
    for stage in stages:
        print(f'Running {stage}', flush=True)
        subprocess.run([sys.executable, str(ROOT / stage)], cwd=ROOT, check=True)

if __name__ == '__main__':
    main()
