import os
import numpy as np
import tensorflow as tf
from sklearn.decomposition import PCA
from sklearn.cluster import KMeans
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from matplotlib.offsetbox import OffsetImage, AnnotationBbox
import typer

def extract_features(image_path: str):
    image = tf.keras.preprocessing.image.load_img(image_path, target_size=(224, 224))
    image = tf.keras.preprocessing.image.img_to_array(image)
    image = np.expand_dims(image, axis=0)
    image = tf.keras.applications.vgg16.preprocess_input(image)
    model = tf.keras.applications.VGG16(weights='imagenet', include_top=False)
    features = model.predict(image)
    return features.flatten()

def main(image_folder: str, n_clusters: int = 5):
    image_files = [f for f in os.listdir(image_folder) if os.path.isfile(os.path.join(image_folder, f))]
    features_list = [extract_features(os.path.join(image_folder, f)) for f in image_files]

    pca = PCA(n_components=3)
    reduced_features = pca.fit_transform(features_list)

    kmeans = KMeans(n_clusters=n_clusters)
    kmeans.fit(reduced_features)

    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')

    for i in range(len(reduced_features)):
        x, y, z = reduced_features[i]
        img_path = os.path.join(image_folder, image_files[i])
        img = plt.imread(img_path)
        imagebox = OffsetImage(img, zoom=0.1)
        ab = AnnotationBbox(imagebox, (x, y, z), frameon=False, pad=0)
        ax.add_artist(ab)

    plt.show()

if __name__ == '__main__':
    typer.run(main)
