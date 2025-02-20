from skimage import morphology, measure
from sklearn.cluster import KMeans
import numpy as np
import SimpleITK as sitk
from utils import load_nifti_image, save_nifti_image
import os
def apply_kmeans_segmentation(image, n_clusters=2):
    """Apply K-Means clustering to segment the image."""
    values = image[image > 0].reshape(-1, 1)
    kmeans = KMeans(n_clusters=n_clusters, random_state=42)
    kmeans.fit(values)
    sorted_labels = np.argsort(kmeans.cluster_centers_.flatten())
    label_mapping = {sorted_labels[0]: 2, sorted_labels[1]: 1}
    segmented = np.zeros_like(image, dtype=np.uint8)
    segmented[image > 0] = [label_mapping[label] for label in kmeans.labels_]
    return segmented

def filter_and_process_cluster(segmented_image, target_label=2):
    """Filter clusters and process connected components."""
    filtered_image = (segmented_image == target_label).astype(np.uint8)
    closed_image = morphology.binary_closing(filtered_image, morphology.ball(2))
    labeled_image = measure.label(closed_image, connectivity=3)
    properties = measure.regionprops(labeled_image)
    valid_components = [prop for prop in properties if prop.area >= 5000]
    return labeled_image, valid_components

def keep_closest_component(labeled_image, properties, image_shape):
    """Keep the connected component closest to the image center."""
    center = np.array(image_shape) // 2
    components = [(prop.label, np.linalg.norm(np.array(prop.centroid) - center))
                  for prop in properties]
    closest_label = min(components, key=lambda x: x[1])[0]
    selected_mask = (labeled_image == closest_label).astype(np.uint8)
    return morphology.binary_closing(selected_mask, morphology.ball(5))

def segment_lungs(inhale_image_path, exhale_image_path, output_dir):
    """Perform full lung segmentation for both inhale and exhale images."""
    
    # Load images
    inhale_img, inhale_affine = load_nifti_image(inhale_image_path)
    exhale_img, exhale_affine = load_nifti_image(exhale_image_path)

    # Segment Inhale
    segmented_inhale = apply_kmeans_segmentation(inhale_img)
    labeled_inhale, properties_inhale = filter_and_process_cluster(segmented_inhale)
    inhale_lung_mask = keep_closest_component(labeled_inhale, properties_inhale, inhale_img.shape)
    inhale_lung_mask_path = os.path.join(output_dir, "inhale_lung_mask.nii")
    save_nifti_image(inhale_lung_mask, inhale_affine, inhale_lung_mask_path)

    # Segment Exhale
    segmented_exhale = apply_kmeans_segmentation(exhale_img)
    labeled_exhale, properties_exhale = filter_and_process_cluster(segmented_exhale)
    exhale_lung_mask = keep_closest_component(labeled_exhale, properties_exhale, exhale_img.shape)
    exhale_lung_mask_path = os.path.join(output_dir, "exhale_lung_mask.nii")
    save_nifti_image(exhale_lung_mask, exhale_affine, exhale_lung_mask_path)

    print("Lung segmentation completed.")
    return inhale_lung_mask_path, exhale_lung_mask_path

