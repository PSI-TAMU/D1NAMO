# D1NAMO

## Overview
We provide the preprocessing code for the paper <b>[The open D1NAMO dataset: A multi-modal dataset for research on non-invasive type 1 diabetes management](https://www.sciencedirect.com/science/article/pii/S2352914818301059)</b>.

* It includes data from multiple modalities: Electrocardiography (ECG), breathing, accelerometry, glucose levels, and annotated food pictures.
* The dataset was collected over real-life, non-clinical conditions using the Zephyr BioHarness 3 wearable chest-belt device.
* It contains recordings from 29 participants—20 healthy individuals and 9 patients with Type 1 diabetes.
* The dataset is openly available to the scientific community to support research in hypoglycemia detection and broader healthcare monitoring applications.
  
For more information, please consult [here](https://www.kaggle.com/datasets/sarabhian/d1namo-ecg-glucose-data).

## Quick Start
```
git clone https://github.com/PSI-TAMU/D1NAMO.git
cd D1NAMO
mkdir raw_data
cd raw_data
kaggle datasets download sarabhian/d1namo-ecg-glucose-data
unzip d1namo-ecg-glucose-data.zip
```

## Preprocessing
After downloading the raw data, one can use the [preprocess.ipynb](./preprocess.ipynb) notebook to process the data. The processed data will be stored in the processed folder.

For each processed data, it is saved in a json format that contains multimodal signals within a recorded cgm section (a 5-minute window). In detail, it includes:
* <b>Index</b>
* <b>Timestamp</b>: when the CGM value is being recorded
* <b>glucose</b>: the recorded glucose value (converted into mg/dL)
* <b>zephyr</b>:
    * ECG: collected 12-bit filtered ECG signals (250Hz)
        * 'Time', 'EcgWaveform'
    * Summary: other relevant metrics
        * 'Time', 'HR', 'BR', 'Posture', 'Activity', 'HRConfidence', 'ECGNoise'

We have also included a [jupyter notebook](./visualize.ipynb) that provides an interactive demo for visualizing the signal. This notebook walks you through key steps in analyzing and processing the data, allowing you to explore and better understand the signal.

## Citation
```
@article{DUBOSSON201892,
title = {The open D1NAMO dataset: A multi-modal dataset for research on non-invasive type 1 diabetes management},
journal = {Informatics in Medicine Unlocked},
volume = {13},
pages = {92-100},
year = {2018},
issn = {2352-9148},
doi = {https://doi.org/10.1016/j.imu.2018.09.003},
url = {https://www.sciencedirect.com/science/article/pii/S2352914818301059},
author = {Fabien Dubosson and Jean-Eudes Ranvier and Stefano Bromuri and Jean-Paul Calbimonte and Juan Ruiz and Michael Schumacher},
keywords = {Diabetes management, Wearable devices, Glucose, ECG, Accelerometers, Annotated food pictures},
abstract = {The usage of wearable devices has gained popularity in the latest years, especially for health-care and well being. Recently there has been an increasing interest in using these devices to improve the management of chronic diseases such as diabetes. The quality of data acquired through wearable sensors is generally lower than what medical-grade devices provide, and existing datasets have mainly been acquired in highly controlled clinical conditions. In the context of the D1NAMO project — aiming to detect glycemic events through non-invasive ECG pattern analysis — we elaborated a dataset that can be used to help developing health-care systems based on wearable devices in non-clinical conditions. This paper describes this dataset, which was acquired on 20 healthy subjects and 9 patients with type-1 diabetes. The acquisition has been made in real-life conditions with the Zephyr BioHarness 3 wearable device. The dataset consists of ECG, breathing, and accelerometer signals, as well as glucose measurements and annotated food pictures. We open this dataset to the scientific community in order to allow the development and evaluation of diabetes management algorithms.}
}
```


## Help
If you have any questions, please contact [mtseng@tamu.edu](mailto:rgutier@cse.tamu.edu).
