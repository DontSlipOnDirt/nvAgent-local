"""
Usage: python results/quick_analyze.py <result_directory>
Example: python results/quick_analyze.py results/20251118_032946_Qwen2.5-7B-Instruct_NoVision
"""

import pandas as pd
import sys

csv_path = sys.argv[1]
df = pd.read_csv(csv_path + "/detailed_results.csv")

print("=== Chart Type Breakdown ===")
print(df.groupby('chart')['illegal rate'].mean().sort_values(ascending=False))

print("\n=== Single vs Multi Table ===")
print(df.groupby('is_multi_table')['illegal rate'].mean())

print("\n=== Chart Type + Multi Table ===")
print(df.groupby(['chart', 'is_multi_table'])['illegal rate'].mean().sort_values(ascending=False))

print("\n=== Data Check Failures by Chart ===")
print(df.groupby('chart')['data check_fail_rate'].mean().sort_values(ascending=False))

print("\n=== PIE Chart Analysis ===")
pie_df = df[df['chart'] == 'Pie']
print(f"PIE Total: {len(pie_df)//3} queries")
print(f"PIE Illegal Rate: {pie_df['illegal rate'].mean():.2%}")
print(f"PIE Data Check Fail: {pie_df['data check_fail_rate'].mean():.2%}")
print(f"PIE Single-Table Illegal: {pie_df[pie_df['is_multi_table']==False]['illegal rate'].mean():.2%}")
print(f"PIE Multi-Table Illegal: {pie_df[pie_df['is_multi_table']==True]['illegal rate'].mean():.2%}")

print("\n=== LINE Chart Analysis ===")
line_df = df[df['chart'] == 'Line']
if len(line_df) > 0:
    print(f"LINE Total: {len(line_df)//3} queries")
    print(f"LINE Illegal Rate: {line_df['illegal rate'].mean():.2%}")
    print(f"LINE Data Check Fail: {line_df['data check_fail_rate'].mean():.2%}")
else:
    print("No LINE charts in this dataset")
