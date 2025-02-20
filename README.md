# Image-Registeraion-for-Chest-CT-volumes
![image](https://github.com/user-attachments/assets/d655d302-458e-4bb9-8342-2f3e3f10484c)
 

## **Overview**  
This repository contains a pipeline developed as part of the **[Challenge Name]**. The objective is to register inhale and exhale CT images, aligning anatomical landmarks to minimize the **Target Registration Error (TRE)**. Given the inhale landmarks, the goal is to estimate the corresponding exhale landmarks with the lowest possible error.  

---

## **Dataset Summary**  
The dataset is available for download at **[Dataset Link](#)**. It consists of **4 patient folders**, each containing:  
- **Two NIfTI files**: CT scans at two different respiratory phases.  
- **Two TXT files**: Containing landmark coordinates for both phases.  

| Patient ID | Inhale Image | Exhale Image | Inhale Landmarks | Exhale Landmarks |
|------------|--------------|--------------|------------------|------------------|
| COPD1      | `copd1_iBHCT.nii` | `copd1_eBHCT.nii` | `copd1_300_iBH_xyz_r1.txt` | `copd1_300_eBH_xyz_r1.txt` |
| COPD2      | `copd2_iBHCT.nii` | `copd2_eBHCT.nii` | `copd2_300_iBH_xyz_r1.txt` | `copd2_300_eBH_xyz_r1.txt` |
| COPD3      | `copd3_iBHCT.nii` | `copd3_eBHCT.nii` | `copd3_300_iBH_xyz_r1.txt` | `copd3_300_eBH_xyz_r1.txt` |
| COPD4      | `copd4_iBHCT.nii` | `copd4_eBHCT.nii` | `copd4_300_iBH_xyz_r1.txt` | `copd4_300_eBH_xyz_r1.txt` |

A separate file in the dataset directory provides **voxel sizes and image dimensions** for each case.

---

## **Pipeline Overview**  

### **1️⃣ Preprocessing**  
- Perform **histogram matching** to standardize intensity distributions.  
- Normalize image intensity values.  

### **2️⃣ Lung Segmentation**  
- Apply **K-Means clustering** followed by **morphological operations** to refine the lung region.  
- Identify the **connected component closest to the center**, corresponding to the lungs.  

![Placeholder for Segmentation Results 1]  
![Placeholder for Segmentation Results 2]  

### **3️⃣ Registration**  
- The two images are aligned using **Elastix registration**.  
- The provided **parameter files** guide the registration:  
  - **Affine transformation** for global alignment.  
  - **B-Spline transformation** for local deformations.  

### **4️⃣ Landmark Transformation**  
- Apply **Transformix** to predict the exhale landmarks from the inhale landmarks.  

### **5️⃣ Evaluation**  
- Compute the **TRE (Target Registration Error) after registration** to assess alignment accuracy.  

---

## **Results**  
The table below shows the **TRE values before and after registration** for all four patient images:  

| Patient ID | TRE Before (mm) | TRE After (mm) | Improvement (%) |
|------------|---------------|--------------|----------------|
| COPD1      | **X.XX**      | **Y.YY**     | **Z%**         |
| COPD2      | **X.XX**      | **Y.YY**     | **Z%**         |
| COPD3      | **X.XX**      | **Y.YY**     | **Z%**         |
| COPD4      | **X.XX**      | **Y.YY**     | **Z%**         |

(*Replace X.XX, Y.YY, and Z% with actual results.*)  

---

## **Repository Structure**  
