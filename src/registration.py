import os
import subprocess
import numpy as np



def run_elastix_registration(
    elastix_path, fixed_image_path, moving_image_path, fixed_mask_path, moving_mask_path, output_dir, affine_param_file, bspline_param_file
):
    """Run Elastix registration with specified parameter files."""

    elastix_command = [
        elastix_path,
        "-f", fixed_image_path,  
        "-m", moving_image_path,  
        "-fMask", fixed_mask_path,  
        "-mMask", moving_mask_path,  
        "-out", output_dir,  
        "-p", affine_param_file,  
        "-p", bspline_param_file  
    ]



    try:
        print(" Registering images...")
        subprocess.run(elastix_command, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, check=True)
        print(" Registration finished.")
    except subprocess.CalledProcessError as e:
        print(f" Registration failed: {e}")



def apply_transformix_landmarks(transformix_path, input_landmarks, output_directory, transform_parameters):
    """Apply Transformix to landmarks."""
    
    os.makedirs(output_directory, exist_ok=True)

    transformix_command = [
        transformix_path,
        "-def", input_landmarks,
        "-out", output_directory,
        "-tp", transform_parameters
    ]

    try:
        print(" Transforming landmarks...")
        subprocess.run(transformix_command, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, check=True)
        print(" Landmark transformation finished.")
    except subprocess.CalledProcessError as e:
        print(f" Landmark transformation failed: {e}")

    transformed_landmarks_file = os.path.join(output_directory, "outputpoints.txt")
    transformed_landmarks = []

    with open(transformed_landmarks_file, "r") as infile:
        for line in infile:
            if "OutputPoint" in line:
                start_idx = line.find("OutputIndexFixed = [") + len("OutputIndexFixed = [")
                end_idx = line.find("]", start_idx)
                if start_idx != -1 and end_idx != -1:
                    point_str = line[start_idx:end_idx]
                    point = [float(coord) for coord in point_str.split()]
                    transformed_landmarks.append(point)

    transformed_landmarks_voxel = np.array(transformed_landmarks)

    txt_filename = os.path.join(output_directory, "transformed_landmarks.txt")
    with open(txt_filename, "w") as txt_file:
        for point in transformed_landmarks_voxel:
            txt_file.write(" ".join(f"{int(coord) if coord.is_integer() else coord:.6f}".rstrip("0").rstrip(".") for coord in point) + "\n")

    print(f" Transformed landmarks saved to: {txt_filename}")
