import os
import pickle
import ledapy
import tqdm
import glob
import datetime
import argparse
import neurokit2 as nk
import numpy as np
import seaborn as sns
import pandas as pd
import matplotlib.pyplot as plt

def extract_beat(cgm_path, fs=250, window=3):
    with open(cgm_path, 'rb') as f:
        cgm_data = pickle.load(f)
    window_size = window * fs 
    ecg_data = cgm_data['zephyr']['ECG']
    summary_data = cgm_data['zephyr']['Summary']
    ecg_data['Time'] = pd.to_datetime(ecg_data['Time'])
    summary_data = pd.DataFrame(summary_data)

    try:
        ecg_clean = nk.ecg_clean(ecg_data['EcgWaveform'], sampling_rate=fs)
        _, rpeaks = nk.ecg_peaks(ecg_clean, sampling_rate=fs, correct_artifacts=True)
        r_peaks = np.unique(rpeaks['ECG_R_Peaks'])

        extracted_ecg = []
        for peak in r_peaks:
            start_idx = peak - window_size//2
            end_idx = min(start_idx + window_size, ecg_clean.shape[0] - 1)

            start_t = ecg_data['Time'][start_idx]
            end_t = ecg_data['Time'][end_idx]
            beat_ecg = ecg_clean[start_idx:end_idx + 1]

            if beat_ecg.shape[0] == 0:
                continue
            
            summary_window = (summary_data['Time'] >= start_t) & (summary_data['Time'] < end_t)
            avg_HRConfidence = summary_data["HRConfidence"][summary_window].mean()
            avg_ECGNoise = summary_data["ECGNoise"][summary_window].mean()

            extracted_ecg.append({
                'ecg': beat_ecg,
                'start_t': start_t,
                'end_t': end_t,
                'glucose': cgm_data['glucose'],
                'CGM_idx': cgm_data['Index'],
                'Timestamp': cgm_data['Timestamp'],
                'HRConfidence': avg_HRConfidence,
                'ECGNoise': avg_ECGNoise
            })
    except Exception as e:
        print(f"Error processing file {cgm_path}: {e}")
        return None

    extracted_ecg = pd.DataFrame(extracted_ecg)
    return extracted_ecg


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Preprocess the dataset")
    parser.add_argument("-s", "--subject_id", type=str, help="Subject ID to process. Ex: c1s001")
    parser.add_argument("--data_dir", type=str, default="./processed/cgm", help="Directory containing the processed files of a subject")
    parser.add_argument("--out_dir", type=str, default="./processed/beat", help="Directory to save the processed data")
    args = parser.parse_args()

    os.makedirs(args.out_dir, exist_ok=True)
    out_path = os.path.join(args.out_dir, f'{args.subject_id}.pkl')

    # Load the data
    cgm_paths = sorted(glob.glob(os.path.join(args.data_dir, args.subject_id, '*.pkl')), key=lambda x: int(os.path.basename(x).replace('.pkl', '')))
    
    extracted_ecg = None
    for cgm_path in tqdm.tqdm(cgm_paths):
        _extracted_ecg = extract_beat(cgm_path)
        if extracted_ecg is None:
            extracted_ecg = _extracted_ecg
        else:
            extracted_ecg = pd.concat([extracted_ecg, _extracted_ecg], ignore_index=True)

    extracted_ecg = extracted_ecg.reset_index(drop=True)
    extracted_ecg.to_pickle(out_path)
    print(f"Extracted ECG data saved to {out_path}")
    print(f"Extracted ECG data shape: {extracted_ecg.shape}")