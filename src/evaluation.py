import numpy as np
import os

def calculate_tre(exhale_landmarks_path, transformed_landmarks_path, voxel_size):
    """Calculate the Target Registration Error (TRE) if the target landmarks file is available."""

    # Check if the exhale landmarks file exists
    if not os.path.exists(exhale_landmarks_path):
        print(f" Target landmarks file not found: {exhale_landmarks_path}. Skipping TRE calculation.")
        return None

    # Step 1: Load exhale (target) landmarks
    exhale_landmarks = np.loadtxt(exhale_landmarks_path, skiprows=2)  
    exhale_landmarks_mm = exhale_landmarks * voxel_size 

    # Step 2: Load transformed landmarks 
    if not os.path.exists(transformed_landmarks_path):
        print(f" Transformed landmarks file not found: {transformed_landmarks_path}. Skipping TRE calculation.")
        return None

    transformed_landmarks = np.loadtxt(transformed_landmarks_path)
    transformed_landmarks_mm = transformed_landmarks * voxel_size  

    # Step 3: Ensure the number of landmarks match
    if len(transformed_landmarks_mm) != len(exhale_landmarks_mm):
        raise ValueError(f"Mismatch in number of points: {len(transformed_landmarks_mm)} vs {len(exhale_landmarks_mm)}")

    # Step 4: Compute TRE
    tre = np.sqrt(np.sum((transformed_landmarks_mm - exhale_landmarks_mm) ** 2, axis=1))
    mean_tre = np.mean(tre)
    std_tre = np.std(tre)

    # Step 5: Display results
    print(f"Final Mean TRE (Displacement): {mean_tre:.2f} mm")
    print(f"Final Standard Deviation of TRE: {std_tre:.2f} mm")

    return mean_tre, std_tre


