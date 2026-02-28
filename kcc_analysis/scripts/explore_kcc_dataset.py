#!/usr/bin/env python3
"""
KCC Dataset Explorer
Analyzes the KCC master dataset with multilingual support and sampling strategy.

Dataset: kcc_master_dataset.csv (~8GB, 80-90M records, 2006-2025)
Features:
- Chunked reading for memory efficiency
- 10% sampling for quick analysis
- Language detection
- Data quality assessment
"""

import pandas as pd
import json
from datetime import datetime
from pathlib import Path
from typing import Dict, List
import sys

# Try importing language detection library
try:
    from langdetect import detect, DetectorFactory
    DetectorFactory.seed = 0  # For reproducibility
    LANGDETECT_AVAILABLE = True
except ImportError:
    print("⚠️  langdetect not installed. Language detection will be skipped.")
    print("Install with: pip install langdetect")
    LANGDETECT_AVAILABLE = False


class KCCDatasetExplorer:
    """Explore and analyze KCC dataset with sampling support."""
    
    def __init__(self, filepath: str, sample_fraction: float = 0.1):
        self.filepath = Path(filepath)
        self.sample_fraction = sample_fraction
        self.chunk_size = 500_000  # 500K rows per chunk
        self.stats = {
            'analysis_date': datetime.now().isoformat(),
            'dataset_info': {},
            'basic_stats': {},
            'query_types': {},
            'sectors': {},
            'seasons': {},
            'yearly_distribution': {},
            'language_distribution': {},
            'data_quality': {}
        }
    
    def detect_language(self, text: str) -> str:
        """Detect language of text."""
        if not LANGDETECT_AVAILABLE or pd.isna(text) or str(text).strip() == "" or str(text) == "0":
            return "unknown"
        
        try:
            text_str = str(text).strip()
            if len(text_str) < 10:  # Too short for reliable detection
                return "unknown"
            
            lang_code = detect(text_str)
            
            # Map common language codes to readable names
            lang_map = {
                'en': 'English',
                'hi': 'Hindi',
                'te': 'Telugu',
                'mr': 'Marathi',
                'ta': 'Tamil',
                'kn': 'Kannada',
                'ml': 'Malayalam',
                'bn': 'Bengali',
                'gu': 'Gujarati',
                'pa': 'Punjabi',
                'or': 'Odia'
            }
            
            return lang_map.get(lang_code, lang_code)
        except Exception as e:
            return "unknown"
    
    def analyze_basic_stats(self):
        """Analyze basic dataset statistics with sampling."""
        print("\n" + "="*60)
        print("📊 PHASE 1: BASIC STATISTICS ANALYSIS")
        print("="*60)
        
        total_rows = 0
        sampled_rows = 0
        chunk_count = 0
        
        # Containers for aggregated data
        query_types_counter = {}
        sectors_counter = {}
        seasons_counter = {}
        yearly_counter = {}
        monthly_counter = {}
        state_counter = {}
        language_counter = {}
        
        # Data quality metrics
        null_query_text = 0
        null_answer = 0
        zero_block = 0
        zero_category = 0
        
        print(f"\n📁 Reading file: {self.filepath}")
        print(f"🎲 Sampling strategy: {self.sample_fraction * 100}% of data")
        print(f"💾 Chunk size: {self.chunk_size:,} rows")
        print("\n⏳ Processing chunks...")
        
        # Read in chunks
        try:
            for chunk in pd.read_csv(self.filepath, chunksize=self.chunk_size, low_memory=False):
                chunk_count += 1
                total_rows += len(chunk)
                
                # Sample from chunk
                if self.sample_fraction < 1.0:
                    chunk = chunk.sample(frac=self.sample_fraction, random_state=42)
                
                sampled_rows += len(chunk)
                
                # Aggregate statistics
                for col, counter in [
                    ('QueryType', query_types_counter),
                    ('Sector', sectors_counter),
                    ('Season', seasons_counter),
                    ('year', yearly_counter),
                    ('month', monthly_counter),
                    ('StateName', state_counter)
                ]:
                    if col in chunk.columns:
                        counts = chunk[col].value_counts().to_dict()
                        for key, value in counts.items():
                            counter[key] = counter.get(key, 0) + value
                
                # Language detection on sample
                if LANGDETECT_AVAILABLE and 'QueryText' in chunk.columns:
                    # Detect language for small sample from this chunk (to save time)
                    lang_sample = chunk.sample(min(1000, len(chunk)), random_state=42)
                    for text in lang_sample['QueryText']:
                        lang = self.detect_language(text)
                        language_counter[lang] = language_counter.get(lang, 0) + 1
                
                # Data quality checks
                if 'QueryText' in chunk.columns:
                    null_query_text += chunk['QueryText'].isna().sum()
                if 'KccAns' in chunk.columns:
                    null_answer += chunk['KccAns'].isna().sum()
                if 'BlockName' in chunk.columns:
                    zero_block += (chunk['BlockName'] == '0').sum() + (chunk['BlockName'] == 0).sum()
                if 'Category' in chunk.columns:
                    zero_category += (chunk['Category'] == '0').sum() + (chunk['Category'] == 0).sum()
                
                # Progress update
                if chunk_count % 10 == 0:
                    print(f"  ✓ Processed {chunk_count} chunks ({total_rows:,} total rows, {sampled_rows:,} sampled)")
        
        except Exception as e:
            print(f"❌ Error reading file: {e}")
            sys.exit(1)
        
        # Store results
        self.stats['dataset_info'] = {
            'total_rows': total_rows,
            'sampled_rows': sampled_rows,
            'sample_percentage': self.sample_fraction * 100,
            'chunks_processed': chunk_count,
            'file_path': str(self.filepath)
        }
        
        self.stats['query_types'] = dict(sorted(query_types_counter.items(), key=lambda x: x[1], reverse=True))
        self.stats['sectors'] = dict(sorted(sectors_counter.items(), key=lambda x: x[1], reverse=True))
        self.stats['seasons'] = dict(sorted(seasons_counter.items(), key=lambda x: x[1], reverse=True))
        self.stats['yearly_distribution'] = dict(sorted(yearly_counter.items()))
        self.stats['monthly_distribution'] = dict(sorted(monthly_counter.items()))
        self.stats['top_states'] = dict(sorted(state_counter.items(), key=lambda x: x[1], reverse=True)[:15])
        self.stats['language_distribution'] = dict(sorted(language_counter.items(), key=lambda x: x[1], reverse=True))
        
        self.stats['data_quality'] = {
            'null_query_text': int(null_query_text),
            'null_answer': int(null_answer),
            'zero_block_name': int(zero_block),
            'zero_category': int(zero_category),
            'null_percentage': round(null_query_text / sampled_rows * 100, 2) if sampled_rows > 0 else 0
        }
        
        # Print summary
        print(f"\n{'='*60}")
        print("✅ ANALYSIS COMPLETE")
        print(f"{'='*60}")
        print(f"\n📈 Dataset Overview:")
        print(f"  Total Records: {total_rows:,}")
        print(f"  Sampled Records: {sampled_rows:,}")
        print(f"  Time Period: {min(yearly_counter.keys())} - {max(yearly_counter.keys())}")
        print(f"  Unique Query Types: {len(query_types_counter)}")
        print(f"  Unique States: {len(state_counter)}")
        
        print(f"\n📊 Top 5 Query Types:")
        for qt, count in list(self.stats['query_types'].items())[:5]:
            pct = count / sampled_rows * 100
            print(f"  {qt}: {count:,} ({pct:.1f}%)")
        
        print(f"\n🌾 Top 5 Sectors:")
        for sector, count in list(self.stats['sectors'].items())[:5]:
            pct = count / sampled_rows * 100
            print(f"  {sector}: {count:,} ({pct:.1f}%)")
        
        if language_counter:
            print(f"\n🌍 Language Distribution (sample):")
            for lang, count in list(self.stats['language_distribution'].items())[:10]:
                pct = count / sum(language_counter.values()) * 100
                print(f"  {lang}: {count:,} ({pct:.1f}%)")
        
        print(f"\n⚠️  Data Quality:")
        print(f"  Null QueryText: {null_query_text:,} ({self.stats['data_quality']['null_percentage']}%)")
        print(f"  Null Answers: {null_answer:,}")
        print(f"  Zero BlockName: {zero_block:,}")
        print(f"  Zero Category: {zero_category:,}")
    
    def save_results(self, output_file: str = "kcc_exploration_results.json"):
        """Save analysis results to JSON file."""
        output_path = Path(output_file)
        
        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(self.stats, f, indent=2, ensure_ascii=False)
        
        print(f"\n💾 Results saved to: {output_path}")
        print(f"   File size: {output_path.stat().st_size / 1024:.1f} KB")
    
    def run_full_analysis(self):
        """Run complete exploration analysis."""
        print("\n" + "="*60)
        print("🚀 KCC DATASET EXPLORATION")
        print("="*60)
        print(f"Start time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        
        self.analyze_basic_stats()
        self.save_results()
        
        print(f"\n✅ Exploration complete!")
        print(f"End time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")


def main():
    """Main entry point."""
    import argparse
    
    parser = argparse.ArgumentParser(description='Explore KCC dataset with sampling')
    parser.add_argument('--file', type=str, default='kcc_master_dataset.csv',
                       help='Path to KCC dataset CSV file')
    parser.add_argument('--sample', type=float, default=0.1,
                       help='Sample fraction (0.0-1.0), default 0.1 (10%%)')
    parser.add_argument('--output', type=str, default='kcc_exploration_results.json',
                       help='Output JSON file path')
    
    args = parser.parse_args()
    
    # Validate sample fraction
    if not 0.0 < args.sample <= 1.0:
        print("❌ Error: Sample fraction must be between 0.0 and 1.0")
        sys.exit(1)
    
    # Run exploration
    explorer = KCCDatasetExplorer(args.file, sample_fraction=args.sample)
    explorer.run_full_analysis()
    
    if args.output != 'kcc_exploration_results.json':
        explorer.save_results(args.output)


if __name__ == "__main__":
    main()
