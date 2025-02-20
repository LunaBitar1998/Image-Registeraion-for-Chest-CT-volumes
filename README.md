# Image-Registeraion-for-Chest-CT-volumes
![image](https://github.com/user-attachments/assets/07fd9bfa-80ad-4ecc-8aea-1dcafc341a47)


## **Overview**  
This repository contains a pipeline developed as part of the **[4DCT DIR-Lab Challenge]**,which addresses Chronic Obstructive Pulmonary Disease (COPD) The objective is to register inhale and exhale CT images, aligning anatomical landmarks to minimize the **Target Registration Error (TRE)**. Given the inhale landmarks, the goal is to estimate the corresponding exhale landmarks with the lowest possible error.  

---

## **Dataset Summary**  
The dataset is available for download at **[https://drive.google.com/drive/folders/1_fWCUPDjhVR5nT0u5x4tiMtRZ0tmPfhF?usp=drive_link](#)**. It consists of **4 patient folders**, each containing:  
- **Two NIfTI files**: CT scans at two different respiratory phases (inhale and exhale).
- **Two TXT files**: Containing landmark coordinates for both phases.  

| Patient ID | Inhale Image | Exhale Image | Inhale Landmarks | Exhale Landmarks |
|------------|--------------|--------------|------------------|------------------|
| COPD1      | `copd1_iBHCT.nii` | `copd1_eBHCT.nii` | `copd1_300_iBH_xyz_r1.txt` | `copd1_300_eBH_xyz_r1.txt` |
| COPD2      | `copd2_iBHCT.nii` | `copd2_eBHCT.nii` | `copd2_300_iBH_xyz_r1.txt` | `copd2_300_eBH_xyz_r1.txt` |
| COPD3      | `copd3_iBHCT.nii` | `copd3_eBHCT.nii` | `copd3_300_iBH_xyz_r1.txt` | `copd3_300_eBH_xyz_r1.txt` |
| COPD4      | `copd4_iBHCT.nii` | `copd4_eBHCT.nii` | `copd4_300_iBH_xyz_r1.txt` | `copd4_300_eBH_xyz_r1.txt` |

The table in the image below specify **voxel sizes and image dimensions** for each case along with the initial displacement before registeration.
![image](https://github.com/user-attachments/assets/9c337e89-1965-4b4e-9b7e-54211f8db50b)


---

## **Pipeline Overview**  

### **1️⃣ Preprocessing**  
- Perform **histogram matching** to standardize intensity distributions.  
- Normalize image intensity values.  

### **2️⃣ Lung Segmentation**  
- Apply **K-Means clustering** followed by **morphological operations** to refine the lung region.  
- Identify the **connected component closest to the center**, corresponding to the lungs.  

![![image](https://github.com/user-attachments/assets/379b22e4-ce84-4c48-8517-abb5feba5e8c)]  


### **3️⃣ Registration**  
- The two images are aligned using **Elastix registration**.  
- The provided **parameter files** guide the registration:  
  - **Affine transformation** for global alignment.  
  - **B-Spline transformation** for local deformations.  

### **4️⃣ Landmark Transformation**  
- Apply **Transformix** to predict the exhale landmarks from the inhale landmarks using the transformation file resulting from the registerion step.

### **5️⃣ Evaluation**  
- Compute the **TRE (Target Registration Error) after registration** to assess alignment accuracy.  

---

## **Results**  
The table below shows the **TRE values before and after registration** for all four patient images:  

| Patient ID | TRE Before (mm) | TRE After (mm)|
|------------|---------------|--------------|
| COPD1      | **25.9**      | **1.48**      |
| COPD2      | **21.77**      | **3.19**     |
| COPD3      | **12.29**      | **1.28**     |        
| COPD4      | **30.90**      | **1.67**     |



---

## **Repository Structure**  
   
├── 📂 Parameters/  
│   ├── Parameters.Par0011.affine.txt  
│   ├── Parameters.Par0011.bspline1_s.txt  
│  
├── 📂 src/  
│   ├── evaluation.py  
│   ├── main.py  
│   ├── preprocessing.py  
│   ├── registration.py  
│   ├── segmentation.py  
│   ├── utils.py  
│  
├── 📜 README.md  # Project documentation  
├── 📜 Run_Pipeline.ipynb  # Jupyter notebook to run the pipeline  

##  **How to Use This Repository**  

Follow these steps to set up and run the pipeline:

### 1️ Download the Dataset  
- Download the dataset from **[https://drive.google.com/drive/folders/1_fWCUPDjhVR5nT0u5x4tiMtRZ0tmPfhF?usp=drive_link]** (insert dataset link).  
- Extract the dataset to a location on your computer.  

### 2️ Clone the Repository Configure Paths 
Open a terminal or command prompt and run the following command:  

```bash
git clone <repository_link>
cd <repository_folder>
 
 
### 3️ Configure Paths  
- Open **`Run_Pipeline.ipynb`** in Jupyter Notebook.  
- Set the necessary paths in the notebook:  
  - **`base_path`** → Path to the dataset location.  
  - **`elastix_path` & `transformix_path`** → Paths to your local installation of **Elastix** and **Transformix**.  
  - **Voxel sizes and image dimensions** for each dataset are available in the **dataset folder**.  

### 4️ Run the Pipeline  
- Open **`Run_Pipeline.ipynb`** in Jupyter Notebook.  
- Execute all cells sequentially to process:  
  - **Preprocessing**  
  - **Lung Segmentation**  
  - **Registration using Elastix**  
  - **Evaluation of TRE**  
- The results will be saved in the corresponding output directories.  

