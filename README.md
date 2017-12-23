# K-means implemented for Image Segmentation

## Explanation:
- The K-means algorithm is a clustering method that selects K random points and forms clusters based on the proximity of pixels to the new centroids. The Silhouette method is used to determine the best K for clustering. For each pixel, the average distance of each pixel with other pixels in the same cluster is calculated. Then, the average distance of each pixel with the data in all other clusters except the cluster in which it is located is calculated, and the smallest one is selected. The value of s(i) is always between 1 and -1, and the closer this value is to 1, the more ideal it is. The obtained values are between 1 and -1, and being closer to 1 indicates the most suitable cluster. In this method, the K-means algorithm is executed for different K, and then the above average s(i) is executed for all the pixels and its average is calculated. That round of execution or K that yields the highest average s represents the best K.
- Silhouette method implemented to evaluate best K.

## Dataset
- just add your pictures under ./images/train directory