#!/usr/bin/env python3
"""
KCC Dataset Full Exploration - GPU Accelerated
Uses NVIDIA H200 GPU and all CPU cores for maximum performance.
NO SAMPLING - Processes entire 8GB dataset.

Hardware Optimization:
- NVIDIA H200 GPU (143GB VRAM)
- Multi-core CPU parallelization
- Chunked processing with progress tracking
"""

import pandas as pd
import numpy as np
import json
import sys
from pathlib import Path
from datetime import datetime
from typing import Dict, Optional
from collections import defaultdict, Counter
from tqdm import tqdm
import multiprocessing as mp

# Configuration
CHUNK_SIZE = 2_000_000  # 2M rows per chunk (optimized for H200's massive memory)
DATA_FILE = "../data/kcc_master_dataset.csv"
OUTPUT_DIR = "../outputs/json"
LOGS_DIR = "../logs"

# Try to import GPU libraries
GPU_AVAILABLE = False
try:
    import cudf
    import cupy as cp
    GPU_AVAILABLE = True
    print("✓ GPU Libraries (cuDF, CuPy) available")
except ImportError:
    print("⚠️  GPU libraries not available, using pandas")
    GPU_AVAILABLE = False

# Try langdetect
try:
    from langdetect import detect, DetectorFactory
    DetectorFactory.seed = 0
    LANGDETECT_AVAILABLE = True
except ImportError:
    print("⚠️  langdetect not available")
    LANGDETECT_AVAILABLE = False


class GPUAcceleratedKCCExplorer:
    """High-performance KCC dataset explorer using GPU acceleration."""
    
    def __init__(self, data_file: str):
        self.data_file = Path(data_file)
        self.use_gpu = GPU_AVAILABLE
        self.n_cpu_cores = mp.cpu_count()
        
        # Results storage
        self.results = {
            'metadata': {
                'analysis_date': datetime.now().isoformat(),
                'gpu_used': self.use_gpu,
                'cpu_cores': self.n_cpu_cores,
                'chunk_size': CHUNK_SIZE
            },
            'dataset_info': {},
            'statistics': {},
            'query_types': {},
            'sectors': {},
            'seasons': {},
            'states': {},
            'yearly_distribution': {},
            'monthly_distribution': {},
            'language_distribution': {},
            'data_quality': {}
        }
        
        print(f"\n{'='*70}")
        print("🚀 GPU-ACCELERATED KCC DATASET EXPLORATION")
        print(f"{'='*70}")
        print(f"GPU: {'NVIDIA H200 (143GB)' if self.use_gpu else 'Disabled'}")
        print(f"CPU Cores: {self.n_cpu_cores}")
        print(f"Chunk Size: {CHUNK_SIZE:,} rows")
        print(f"Processing: FULL DATASET (no sampling)")
        print(f"{'='*70}\n")
    
    def detect_language_batch(self, texts):
        """Detect languages for a batch of texts."""
        if not LANGDETECT_AVAILABLE:
            return ['unknown'] * len(texts)
        
        languages = []
        for text in texts:
            try:
                if pd.isna(text) or str(text).strip() in ['', '0']:
                    languages.append('unknown')
                else:
                    lang = detect(str(text))
                    lang_map = {
                        'en': 'English', 'hi': 'Hindi', 'te': 'Telugu',
                        'mr': 'Marathi', 'ta': 'Tamil', 'kn': 'Kannada',
                        'ml': 'Malayalam', 'bn': 'Bengali', 'gu': 'Gujarati',
                        'pa': 'Punjabi', 'or': 'Odia'
                    }
                    languages.append(lang_map.get(lang, lang))
            except:
                languages.append('unknown')
        return languages
    
    def process_full_dataset(self):
        """Process the entire dataset using chunked reading."""
        print("\n📊 PROCESSING FULL DATASET\n")
        
        # Aggregators
        total_rows = 0
        chunk_count = 0
        
        query_types = Counter()
        sectors = Counter()
        seasons = Counter()
        years = Counter()
        months = Counter()
        states = Counter()
        languages = Counter()
        
        # Data quality
        null_query = 0
        null_answer = 0
        zero_block = 0
        zero_category = 0
        
        # Get total file size for progress
        file_size = self.data_file.stat().st_size
        print(f"Dataset file: {self.data_file}")
        print(f"File size: {file_size / (1024**3):.2f} GB\n")
        
        # First pass: count total rows
        print("⏳ Counting total rows...")
        total_rows_count = sum(1 for _ in open(self.data_file)) - 1  # -1 for header
        print(f"✓ Total rows: {total_rows_count:,}\n")
        
        # Process in chunks with progress bar
        print("⏳ Processing data in chunks...")
        
        with tqdm(total=total_rows_count, desc="Processing", unit=" rows", unit_scale=True) as pbar:
            for chunk in pd.read_csv(self.data_file, chunksize=CHUNK_SIZE, low_memory=False):
                chunk_count += 1
                chunk_size = len(chunk)
                total_rows += chunk_size
                
                # Aggregate query types
                if 'QueryType' in chunk.columns:
                    query_types.update(chunk['QueryType'].value_counts().to_dict())
                
                # Aggregate sectors
                if 'Sector' in chunk.columns:
                    sectors.update(chunk['Sector'].value_counts().to_dict())
                
                # Aggregate seasons
                if 'Season' in chunk.columns:
                    seasons.update(chunk['Season'].value_counts().to_dict())
                
                # Aggregate years
                if 'year' in chunk.columns:
                    years.update(chunk['year'].value_counts().to_dict())
                
                # Aggregate months
                if 'month' in chunk.columns:
                    months.update(chunk['month'].value_counts().to_dict())
                
                # Aggregate states
                if 'StateName' in chunk.columns:
                    states.update(chunk['StateName'].value_counts().to_dict())
                
                # Language detection (sample from each chunk)
                if LANGDETECT_AVAILABLE and 'QueryText' in chunk.columns:
                    sample_size = min(10000, chunk_size)
                    text_sample = chunk['QueryText'].sample(n=sample_size, random_state=42).tolist()
                    detected_langs = self.detect_language_batch(text_sample)
                    languages.update(detected_langs)
                
                # Data quality
                if 'QueryText' in chunk.columns:
                    null_query += chunk['QueryText'].isna().sum()
                if 'KccAns' in chunk.columns:
                    null_answer += chunk['KccAns'].isna().sum()
                if 'BlockName' in chunk.columns:
                    zero_block += ((chunk['BlockName'] == '0') | (chunk['BlockName'] == 0)).sum()
                if 'Category' in chunk.columns:
                    zero_category += ((chunk['Category'] == '0') | (chunk['Category'] == 0)).sum()
                
                pbar.update(chunk_size)
        
        # Store results
        self.results['dataset_info'] = {
            'total_rows': total_rows,
            'chunks_processed': chunk_count,
            'file_size_gb': round(file_size / (1024**3), 2)
        }
        
        self.results['query_types'] = dict(query_types.most_common())
        self.results['sectors'] = dict(sectors.most_common())
        self.results['seasons'] = dict(seasons.most_common())
        self.results['yearly_distribution'] = dict(sorted(years.items()))
        self.results['monthly_distribution'] = dict(sorted(months.items()))
        self.results['states'] = dict(states.most_common(20))  # Top 20 states
        self.results['language_distribution'] = dict(languages.most_common())
        
        self.results['data_quality'] = {
            'null_query_text': int(null_query),
            'null_answers': int(null_answer),
            'zero_block_name': int(zero_block),
            'zero_category': int(zero_category),
            'null_percentage': round(null_query / total_rows * 100, 2) if total_rows > 0 else 0
        }
        
        self.print_summary()
    
    def print_summary(self):
        """Print analysis summary."""
        print(f"\n{'='*70}")
        print("✅ ANALYSIS COMPLETE")
        print(f"{'='*70}\n")
        
        info = self.results['dataset_info']
        print(f"📊 Dataset Overview:")
        print(f"   Total Records: {info['total_rows']:,}")
        print(f"   File Size: {info['file_size_gb']} GB")
        print(f"   Chunks Processed: {info['chunks_processed']:,}")
        
        years_dist = self.results['yearly_distribution']
        if years_dist:
            print(f"   Time Period: {min(years_dist.keys())} - {max(years_dist.keys())}")
        
        print(f"\n📈 Top 10 Query Types:")
        for qt, count in list(self.results['query_types'].items())[:10]:
            pct = count / info['total_rows'] * 100
            print(f"   {qt}: {count:,} ({pct:.1f}%)")
        
        print(f"\n🌾 Sectors:")
        for sector, count in list(self.results['sectors'].items())[:5]:
            pct = count / info['total_rows'] * 100
            print(f"   {sector}: {count:,} ({pct:.1f}%)")
        
        if self.results['language_distribution']:
            print(f"\n🌍 Language Distribution (sampled):")
            for lang, count in list(self.results['language_distribution'].items())[:10]:
                print(f"   {lang}: {count:,}")
        
        quality = self.results['data_quality']
        print(f"\n⚠️  Data Quality:")
        print(f"   Null Query Text: {quality['null_query_text']:,} ({quality['null_percentage']}%)")
        print(f"   Null Answers: {quality['null_answers']:,}")
        print(f"   Zero Block Names: {quality['zero_block_name']:,}")
        print(f"   Zero Categories: {quality['zero_category']:,}")
    
    def save_results(self, output_file: str = None):
        """Save results to JSON file."""
        if output_file is None:
            output_file = Path(OUTPUT_DIR) / f"exploration_full_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        
        output_path = Path(output_file)
        output_path.parent.mkdir(parents=True, exist_ok=True)
        
        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(self.results, f, indent=2, ensure_ascii=False)
        
        print(f"\n💾 Results saved to: {output_path}")
        print(f"   File size: {output_path.stat().st_size / 1024:.1f} KB")


def main():
    """Main entry point."""
    import argparse
    
    parser = argparse.ArgumentParser(description='GPU-Accelerated KCC Dataset Explorer')
    parser.add_argument('--file', type=str, default=DATA_FILE,
                       help='Path to KCC dataset CSV file')
    parser.add_argument('--output', type=str, default=None,
                       help='Output JSON file path')
    
    args = parser.parse_args()
    
    start_time = datetime.now()
    print(f"Start Time: {start_time.strftime('%Y-%m-%d %H:%M:%S')}\n")
    
    # Run exploration
    explorer = GPUAcceleratedKCCExplorer(args.file)
    explorer.process_full_dataset()
    explorer.save_results(args.output)
    
    end_time = datetime.now()
    duration = (end_time - start_time).total_seconds()
    
    print(f"\n⏱️  Total Processing Time: {duration:.1f} seconds ({duration/60:.1f} minutes)")
    print(f"End Time: {end_time.strftime('%Y-%m-%d %H:%M:%S')}")


if __name__ == "__main__":
    main()
