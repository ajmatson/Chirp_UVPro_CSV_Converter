#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Copyright 2025 Alan Matson

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is furnished
to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
"""

__author__ = "Alan Matson"
__email__ = "alan(@)offgrid.technology"
__version__ = "0.1a"

import subprocess
import sys
import os

# Ensure pandas is installed
try:
    import pandas as pd
except ModuleNotFoundError:
    print("pandas not found. Installing...")
    subprocess.check_call(["python3", "-m", "pip", "install", "pandas"])
    import pandas as pd

# Check for command-line arguments
if len(sys.argv) != 3:
    print("Usage: python3 convert_chirp_uvpro.py <chirp_export.csv> <output.csv>")
    sys.exit(1)

chirp_export_path = sys.argv[1]
uv_pro_output_path = sys.argv[2]

# Load chirp export file
chirp_df = pd.read_csv(chirp_export_path)

# Define transformation functions
def calculate_rx_freq(row):
    if row['Duplex'] == '+':
        return row['Frequency'] + row['Offset']
    elif row['Duplex'] == '-':
        return row['Frequency'] - row['Offset']
    else:
        return row['Frequency']

def tone_to_sub_audio(tone, freq, dtcs):
    if tone in ['Tone', 'TSQL']:
        return int(freq * 1000)  # Convert MHz to Hz for CTCSS
    elif tone == 'DTCS':
        return int(dtcs)
    return 0

# Prepare the output dataframe
output_columns = [
    'title', 'tx_freq', 'rx_freq', 'tx_sub_audio(CTCSS=freq/DCS=number)',
    'rx_sub_audio(CTCSS=freq/DCS=number)', 'tx_power(H/M/L)', 'bandwidth(12500/25000)',
    'scan(0=OFF/1=ON)', 'talk around(0=OFF/1=ON)', 'pre_de_emph_bypass(0=OFF/1=ON)',
    'sign(0=OFF/1=ON)', 'tx_dis(0=OFF/1=ON)', 'mute(0=OFF/1=ON)', 'rx_modulation(0=FM/1=AM)', 'tx_modulation(0=FM/1=AM)'
]
uv_pro_data = []

for _, row in chirp_df.iterrows():
    rx_freq = int(row['Frequency'] * 1_000_000)  # Convert MHz to Hz
    tx_freq = int(calculate_rx_freq(row) * 1_000_000)
    tx_sub_audio = tone_to_sub_audio(row['Tone'], row['rToneFreq'], row['DtcsCode'])
    rx_sub_audio = tone_to_sub_audio(row['Tone'], row['cToneFreq'], row['DtcsCode'])
    power_map = {'5.0W': 'H', '2.5W': 'M', '0.5W': 'L'}
    tx_power = power_map.get(row['Power'], 'H')
    bandwidth = 25000 if row['Mode'] in ['WFM', 'FM'] else 12500

    uv_pro_data.append([
        row['Name'], tx_freq, rx_freq, tx_sub_audio, rx_sub_audio, tx_power,
        bandwidth, 1, 0 if row['Duplex'] == '' else 1, 0, 1, 0, 0, 0, 0
    ])


# Create and save the UV-Pro import DataFrame
uv_pro_df = pd.DataFrame(uv_pro_data, columns=output_columns)
uv_pro_df.to_csv(uv_pro_output_path, index=False)

print(f"Converted data saved to: {uv_pro_output_path}")
