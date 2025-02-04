'''Utility functions for the Embedding module.'''
import numpy as np

# Calculate cosine similarity between two vectors
def cosine_similarity(vec1, vec2):
    """
    Calculates the cosine similarity between two vectors.

    Parameters:
    vec1 (numpy.ndarray): The first vector.
    vec2 (numpy.ndarray): The second vector.

    Returns:
    float: The cosine similarity between vec1 and vec2.
    """
    dot_product = np.dot(vec1, vec2)
    norm_vec1 = np.linalg.norm(vec1)
    norm_vec2 = np.linalg.norm(vec2)
    return dot_product / (norm_vec1 * norm_vec2)
