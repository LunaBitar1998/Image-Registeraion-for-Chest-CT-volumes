import nibabel as nib
import numpy as np

def load_nifti_image(image_path):
    """Load a NIfTI image and return the image data and affine."""
    image = nib.load(image_path)
    return image.get_fdata(), image.affine


def save_nifti_image(image, affine, output_path):
    """Save a NIfTI image to the specified path."""
    nifti_image = nib.Nifti1Image(image.astype(np.uint8), affine)
    nib.save(nifti_image, output_path)
    
