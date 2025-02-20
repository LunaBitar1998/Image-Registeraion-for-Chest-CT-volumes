import os
from preprocessing import preprocess_image
from segmentation import segment_lungs
from registration import run_elastix_registration, apply_transformix_landmarks
from evaluation import calculate_tre
from utils import load_nifti_image, save_nifti_image

def main(base_path, image_number, image_dimensions, voxel_size, elastix_path, transformix_path, affine_param_file, bspline_param_file):
    """ Main function to execute preprocessing, segmentation, registration, and evaluation """
    
    # Step 1: Define Paths
    inhale_nifti_path = os.path.join(base_path, f"copd{image_number}",f"copd{image_number}", f"copd{image_number}_iBHCT.nii")
    exhale_nifti_path = os.path.join(base_path, f"copd{image_number}",f"copd{image_number}", f"copd{image_number}_eBHCT.nii")
    inhale_landmarks_path = os.path.join(base_path, f"copd{image_number}",f"copd{image_number}", f"copd{image_number}_300_iBH_xyz_r1.txt")
    exhale_landmarks_path = os.path.join(base_path, f"copd{image_number}",f"copd{image_number}", f"copd{image_number}_300_eBH_xyz_r1.txt")

    segmentation_output_dir = os.path.join(base_path, f"copd{image_number}", "segmentationOutput")
    registration_output_dir = os.path.join(base_path, f"copd{image_number}", "registrationOutput")
    transformed_landmarks_output_dir = os.path.join(base_path, f"copd{image_number}", "landmarkTransformationOutput")

    os.makedirs(segmentation_output_dir, exist_ok=True)
    os.makedirs(registration_output_dir, exist_ok=True)
    os.makedirs(transformed_landmarks_output_dir, exist_ok=True)

    # Step 2: Preprocessing
    print("\nPreprocessing Images...")
    preprocessed_inhale_path = os.path.join(segmentation_output_dir, "inhale_preprocessed.nii")
    preprocessed_exhale_path = os.path.join(segmentation_output_dir, "exhale_preprocessed.nii")

    preprocess_image(inhale_nifti_path, inhale_nifti_path, preprocessed_inhale_path)  
    preprocess_image(exhale_nifti_path, inhale_nifti_path, preprocessed_exhale_path)

    print("Preprocessing Completed.\n")

    # Step 3: Segmentation
    print(" Performing Lung Segmentation...")
    inhale_lung_mask_path, exhale_lung_mask_path = segment_lungs(preprocessed_inhale_path, preprocessed_exhale_path, segmentation_output_dir)
    print("Segmentation Completed.\n")

    # Step 4: Registration
    print(" Running Image Registration with Elastix...")
    run_elastix_registration(
        elastix_path,  
        inhale_nifti_path,
        exhale_nifti_path,
        inhale_lung_mask_path,
        exhale_lung_mask_path,
        registration_output_dir,
        affine_param_file, 
        bspline_param_file  
    )
    print("Registration Completed.\n")

    # Step 5: Transforming Landmarks
    print(" Applying Transformix to Landmarks...")
    transform_parameters = os.path.join(registration_output_dir, "TransformParameters.1.txt")

    apply_transformix_landmarks(
        transformix_path=transformix_path,  
        input_landmarks=inhale_landmarks_path,
        output_directory=transformed_landmarks_output_dir,
        transform_parameters=transform_parameters,
    )

    transformed_landmarks_path = os.path.join(transformed_landmarks_output_dir, "transformed_landmarks.txt")
    print("Landmark Transformation Completed.\n")

    # Step 6: Evaluation
    print(" Calculating TRE for Evaluation...")
    calculate_tre(exhale_landmarks_path, transformed_landmarks_path, voxel_size)
    print("Evaluation Completed.\n")

    print("\n 🎉 **Pipeline Execution Finished Successfully!** 🎉")

