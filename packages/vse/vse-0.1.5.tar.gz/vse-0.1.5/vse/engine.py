"""vse - visual search engine

This module contains configurable visual search engine based on the OpenCV library.
Engine consists of bag of visual words and image index. Visual words are computed
on the basis of image descriptors and then clustered. Image index is a dictionary
of image path and histogram of particular visual words occurrences. Image
comparison consist in their histograms comparison.

"""

import cv2
from vse.index import InvertedIndex
from vse.ranker import SimpleRanker
from vse.comparator import Intersection
from vse.utils import load, save


def create_vse(vocabulary_path, recognized_visual_words=1000):
    """Create visual search engine with default configuration."""
    ranker = SimpleRanker(hist_comparator=Intersection())
    inverted_index = InvertedIndex(ranker=ranker, recognized_visual_words=recognized_visual_words)
    bag_of_visual_words = BagOfVisualWords(extractor=cv2.xfeatures2d.SURF_create(),
                                           matcher=cv2.BFMatcher(normType=cv2.NORM_L2),
                                           vocabulary=load(vocabulary_path))
    return VisualSearchEngine(inverted_index, bag_of_visual_words)


class VisualSearchEngine:
    def __init__(self, image_index, bag_of_visual_words):
        self.image_index = image_index
        self.bag_of_visual_words = bag_of_visual_words

    def add_to_index(self, image_id, image):
        """Adds image id and its histogram to index. Argument image contains binary image."""
        hist = self.bag_of_visual_words.generate_hist(image)
        self.image_index[image_id] = hist

    def remove_from_index(self, image_id):
        """Removes item with image_id."""
        del self.image_index[image_id]

    def find_similar(self, image, n=1):
        """Returns at most n similar images."""
        query_hist = self.bag_of_visual_words.generate_hist(image)
        return self.image_index.find(query_hist, n)


class BagOfVisualWords:
    def __init__(self, extractor, matcher, vocabulary):
        self.extractor = extractor
        self.extract_bow = cv2.BOWImgDescriptorExtractor(self.extractor, matcher)
        self.extract_bow.setVocabulary(vocabulary)

    def generate_hist(self, image):
        """Generates image visual words frequency histogram."""
        key_points = self.extractor.detect(image)
        hist = self.extract_bow.compute(image, key_points)[0]
        return hist


def cluster_vocabulary_from_img(images, extractor, recognized_visual_words=1000, filename=''):
    """Generates visual words vocabulary from images. Saves to file if filename given."""
    descriptors = [extractor.detectAndCompute(image, None)[1] for image in images]
    return cluster_vocabulary_from_descriptors(descriptors, recognized_visual_words, filename)


def cluster_vocabulary_from_descriptors(descriptors, recognized_visual_words=1000, filename=''):
    """Generates visual words vocabulary from images descriptors. Saves to file if filename given."""
    bow_kmeans_trainer = cv2.BOWKMeansTrainer(recognized_visual_words)
    for desc in descriptors:
        bow_kmeans_trainer.add(desc)
    vocabulary = bow_kmeans_trainer.cluster()
    if filename:
        save(filename, vocabulary)
    return vocabulary
