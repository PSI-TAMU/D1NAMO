import os
import glob
import tqdm
import pickle
import argparse
import pandas as pd
import matplotlib.pyplot as plt

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Preprocess the dataset")
    parser.add_argument("--data_dir", type=str, default="raw_data", help="Directory containing the dataset files")
    parser.add_argument("--out_dir", type=str, default="./processed/cgm", help="Directory to save the processed data")
    args = parser.parse_args()

    os.makedirs(args.out_dir, exist_ok=True)

    # Load the data
    data_dir = os.path.join(os.path.dirname(__file__), "data")
    data_files = glob.glob(os.path.join(data_dir, "*.csv"))
    
    # Read and concatenate all CSV files
    df = pd.concat([pd.read_csv(file) for file in data_files], ignore_index=True)
    
    # Display the first few rows of the dataframe
    print(df.head())
    
    # Save the dataframe to a pickle file
    with open(os.path.join(data_dir, "data.pkl"), "wb") as f:
        pickle.dump(df, f)
    

    for subject_id in sorted(glob.glob(f'{args.data_dir}/diabetes_subset_ecg_data/diabetes_subset_ecg_data/*')):
        subject_id = os.path.basename(subject_id)
        glucose_df = pd.read_csv(os.path.join(f'{args.data_dir}/diabetes_subset_pictures-glucose-food-insulin/diabetes_subset_pictures-glucose-food-insulin', subject_id, 'glucose.csv'))
        ecg_paths = sorted(glob.glob(os.path.join(f'{args.data_dir}/diabetes_subset_ecg_data/diabetes_subset_ecg_data', subject_id, 'sensor_data', '*', '*.csv')))
        summary_paths = sorted(glob.glob(os.path.join(f'{args.data_dir}/diabetes_subset_sensor_data/diabetes_subset_sensor_data', subject_id, 'sensor_data', '*', '*_Summary.csv')))

        ecg_df = []
        for ecg_path in ecg_paths:
            ecg_df.append(pd.read_csv(ecg_path))
        ecg_df = pd.concat(ecg_df, ignore_index=True)
        ecg_df['Time'] = pd.to_datetime(ecg_df['Time'], format='%d/%m/%Y %H:%M:%S.%f')
        ecg_df = ecg_df.sort_values('Time')

        summary_df = []
        for summary_path in summary_paths:
            summary_df.append(pd.read_csv(summary_path))
        summary_df = pd.concat(summary_df, ignore_index=True)
        summary_df['Time'] = pd.to_datetime(summary_df['Time'], format='%d/%m/%Y %H:%M:%S.%f')
        summary_df = summary_df.sort_values('Time')

        glucose_df = glucose_df[glucose_df['type'] == 'cgm']
        glucose_df['Time'] = pd.to_datetime(glucose_df['date'] + ' ' + glucose_df['time'], format='%Y-%m-%d %H:%M:%S')

        print(f'Processing subject {subject_id}...')
        for i in tqdm.tqdm(range(glucose_df.shape[0])):
            out = {}
            timestamp = glucose_df['Time'].iloc[i]
            previous_timestamp = timestamp - pd.Timedelta(seconds=60*5)
            
            # find ecg time within the range
            ecg_time = ecg_df[(ecg_df['Time'] >= previous_timestamp) & (ecg_df['Time'] <= timestamp)]
            if ecg_time.shape[0] == 0:
                # print(f'No ECG data found for CGM index {i} at timestamp {timestamp}')
                continue

            summary = summary_df[(summary_df['Time'] >= previous_timestamp) & (summary_df['Time'] <= timestamp)]
            
            out = {
                'Index': i,
                'Timestamp': timestamp,
                'glucose': glucose_df['glucose'].iloc[i] * 70.0 / 3.88,
                'zephyr': {
                    'ECG': {
                        'Time': ecg_time['Time'].tolist(),
                        'EcgWaveform': ecg_time['EcgWaveform'].tolist(),
                    },
                    'Summary': {
                        'Time': summary['Time'].tolist(),
                        'HR': summary['HR'].tolist(),
                        'BR': summary['BR'].tolist(),
                        'Posture': summary['Posture'].tolist(),
                        'Activity': summary['Activity'].tolist(),
                        'HRConfidence': summary['HRConfidence'].tolist(),
                        'ECGNoise': summary['ECGNoise'].tolist(),
                    }
                }
            }

            sample_out_dir = os.path.join(args.out_dir, 'c1s{}'.format(subject_id))
            os.makedirs(sample_out_dir, exist_ok=True)
            with open(os.path.join(sample_out_dir, f'{i}.pkl'), 'wb') as f:
                pickle.dump(out, f)
