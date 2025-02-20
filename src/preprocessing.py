import os
import SimpleITK as sitk
import numpy as np

def histogram_matching(fixed_image_path, moving_image_path):
    """Perform histogram matching to align intensity distributions."""
    fixed_image = sitk.ReadImage(fixed_image_path)
    moving_image = sitk.ReadImage(moving_image_path)
    
    matcher = sitk.HistogramMatchingImageFilter()
    matcher.SetNumberOfHistogramLevels(256)
    matcher.SetNumberOfMatchPoints(10)
    matcher.ThresholdAtMeanIntensityOn() 
    
    matched_image = matcher.Execute(moving_image, fixed_image)
    return matched_image

def normalize_intensity(image):
    """Normalize image intensities to [0, 255]."""
    image_array = sitk.GetArrayFromImage(image)
    min_intensity = image_array.min()
    max_intensity = image_array.max()
    image_array = (image_array - min_intensity) / (max_intensity - min_intensity)
    image_array *= 255
    normalized_image = sitk.GetImageFromArray(image_array.astype(np.float32))
    normalized_image.CopyInformation(image)
    return normalized_image

def preprocess_image(input_nifti_path, fixed_image_path, output_path):
    """
    Perform full preprocessing:
    1. Apply histogram matching.
    2. Normalize intensity.
    """
    print("\n Step 1: Performing Histogram Matching...")
    matched_image = histogram_matching(fixed_image_path, input_nifti_path)

    print("\n Step 2: Normalizing Image Intensity...")
    normalized_image = normalize_intensity(matched_image)

    # Save the final preprocessed image
    sitk.WriteImage(normalized_image, output_path)
    print(f"Preprocessed Image Saved at: {output_path}")

    return output_path


