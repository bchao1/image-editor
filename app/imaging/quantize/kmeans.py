import numpy as np 
from PIL import Image

def kmeans_plus_plus(img, K):
    img = np.array(img.convert('RGB')).astype(np.int)
    h, w, _ = img.shape
    img = img.reshape(-1, 3)  # h * w colors. One pixel is represented by an (R,G,B)

    # Find initial centroids of K-means (kmeans++)
    c0_idx = np.random.randint(img.shape[0])
    centroids = [img[c0_idx]]  # initial centroid
    D = np.zeros(img.shape[0])
    for i in range(K - 1):
        new_D = np.sum((img - centroids[-1])**2, axis=1)
        D = np.max(np.stack([D, new_D]), axis=0)
        p = D / np.sum(D)
        c_idx = np.random.choice(img.shape[0], p = p)
        centroids.append(img[c_idx])

    # Perform K-means
    error = np.inf
    while error > 1:
        D = np.stack([np.sum((img - c)**2, axis=1) for c in centroids])
        group = np.argmin(D, axis=0)
        new_centroids = []
        for i in range(K):
            pixel_indices = np.argwhere(group == i).ravel()
            colors = img[pixel_indices]
            c = np.mean(colors, axis=0)
            new_centroids.append(c)
        error = np.mean([np.sqrt(np.sum((new_c - c)**2)) for new_c, c in zip(new_centroids, centroids)])
        centroids = new_centroids
    # Assign colors
    D = np.stack([np.sum((img - c)**2, axis=1) for c in centroids])
    centroids = np.stack(centroids)
    group = np.argmin(D, axis=0)
    img = centroids[group].reshape(h, w, -1).astype(np.uint8)
    return Image.fromarray(img)
