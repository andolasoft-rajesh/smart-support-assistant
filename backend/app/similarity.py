import numpy as np


def cosine_similarity(vector1, vector2):
    """
    Returns cosine similarity between two vectors.
    """

    vector1 = np.array(vector1)
    vector2 = np.array(vector2)

    denominator = np.linalg.norm(vector1) * np.linalg.norm(vector2)

    if denominator == 0:
        return 0

    return np.dot(vector1, vector2) / denominator