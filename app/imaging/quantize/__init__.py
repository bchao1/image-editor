from .kmeans import kmeans_plus_plus
from .median_cut import median_cut

quantize_dict = {
    'quantize-kmeans': kmeans_plus_plus,
    'quantize-median': median_cut
}