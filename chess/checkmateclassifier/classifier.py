import sys
import os
import numpy as np
from sklearn.svm  import SVC
from sklearn.multiclass import OneVsRestClassifier
from sklearn import cross_validation
from sklearn.metrics import confusion_matrix
import pylab as plt
from sklearn.metrics import accuracy_score

import logging
import json
from collections import defaultdict
from sklearn.externals import joblib
import argparse


TOTAL_SIZE_OF_DATASET = 50000
TRAIN_SET_SIZE_PERCENTAGE = 80
TEST_SET_SIZE_PERCENTAGE = 20
CLASSIFICATION_PROBABILITY_THRESHOLD = 0.7
NUMBER_OF_CPUS_TO_USE = -1

logging.basicConfig()
logger = logging.getLogger()
logger.setLevel(logging.INFO)

class Bunch(dict):
    """Container object for datasets: dictionary-like object that
       exposes its keys as attributes."""

    def __init__(self, **kwargs):
        dict.__init__(self, kwargs)
        self.__dict__ = self


def load_dataset(dataset_file_paths):
    dataset = defaultdict(list)
    with open(dataset_file_paths, "r") as dataset_f:
        features_names = next(dataset_f).split("\t")[1:-3]
        for line in dataset_f:
            fields = line.strip().split("\t")
            fen, game_features, game_results = fields[0],fields[1:-3],fields[-2]
            
            dataset[game_results].append([fen, game_features])
    return (dataset, features_names)


def limit_dataset(dataset):
    new_dataset = defaultdict(list)
    samples_counter = 0
    sorted_classes_names = sorted(dataset, key=lambda k: len(dataset[k]))
    for indx, class_name in enumerate(sorted_classes_names):
        batch_size = (TOTAL_SIZE_OF_DATASET - samples_counter) / (len(sorted_classes_names) - indx)
        new_dataset[class_name] = dataset[class_name][:batch_size]
        samples_counter += len(new_dataset[class_name])
    return new_dataset


def split_dataset(dataset, n_feature):
    X_train = np.empty((0, n_feature), dtype=bool)
    X_test = np.empty((0, n_feature), dtype=bool)
    y_train = np.empty((0,), dtype=bool)
    y_test = np.empty((0,), dtype=bool)
    train_terms_name = np.empty((0,), dtype=bool)
    test_terms_name = np.empty((0,), dtype=bool)
    train_size = float(TRAIN_SET_SIZE_PERCENTAGE) / 100
    test_size = float(TEST_SET_SIZE_PERCENTAGE) / 100
    for k, v in dataset.iteritems():
        data = [sample[1] for sample in v]
        target = [k] * len(data)
        terms_name = [sample[0] for sample in v]
        #Split arrays or matrices into random train and test subsets
        splitted_lists = cross_validation.train_test_split(data, target, terms_name, train_size=train_size, test_size=test_size, random_state=None)

        X_train = np.append(X_train, splitted_lists[0], axis=0)
        X_test = np.append(X_test, splitted_lists[1], axis=0)
        y_train = np.append(y_train, splitted_lists[2], axis=0)
        y_test = np.append(y_test, splitted_lists[3], axis=0)
        train_terms_name = np.append(train_terms_name, splitted_lists[4], axis=0)
        test_terms_name = np.append(test_terms_name, splitted_lists[5], axis=0)
    return Bunch(X_train=X_train, X_test=X_test, y_train=y_train, y_test=y_test, \
                 train_terms_name=train_terms_name, test_terms_name=test_terms_name)


def validation(y_test, y_pred, y_pred_with_unknown_cls, y_pred_fictive, labels):
    cm = confusion_matrix(y_test, y_pred, labels)
    cm_with_unknown = confusion_matrix(y_test, y_pred_with_unknown_cls, labels)

    pred_counter = cm.sum()
    true_pred_counter = cm.diagonal().sum()
    false_pred_counter = pred_counter - true_pred_counter
    unknown_pred_counter = cm_with_unknown[:, -1].sum()

    logger.info("classifier accuracy score (without a probability threshold): %f" % (accuracy_score(y_test, y_pred)))
    logger.info("classifier accuracy score (with a probability threshold of %s): %f" %
                (CLASSIFICATION_PROBABILITY_THRESHOLD, accuracy_score(y_test, y_pred_fictive)))
    logger.info("unknown class / all tested data ratio: %.2f%%" % ((float(unknown_pred_counter) / pred_counter) * 100))
    logger.info("unknown class / false predictions ratio: %.2f%%" % ((float(unknown_pred_counter) / false_pred_counter) * 100))
    logger.info("unknown class / true predictions ratio: %.2f%%" % ((float(unknown_pred_counter) / true_pred_counter) * 100))


def plot_cm(cm, labels, file_name):
    plt.clf()
    fig = plt.figure()
    ax = fig.add_subplot(111)

    cax = ax.matshow(cm)
    fig.colorbar(cax)
    fig.set_size_inches(18.5, 10.5)
    ax.set_xticks(range(len(labels)))
    ax.set_yticks(range(len(labels)))
    ax.set_xticklabels(labels, rotation=45)
    ax.set_yticklabels(labels, rotation=0)
    plt.ylabel('True classes')
    plt.xlabel('Predicted classes')

    for i, row in enumerate(cm):
        for j, column in enumerate(row):
            ax.annotate(cm[i, j], xy=(j, i), va="center", ha="center")
    fig.savefig(file_name, dpi=100)


def plot_confusion_matrices(y_test, y_pred, labels, confusionMatricesDir, stage):
    cm = confusion_matrix(y_test, y_pred, labels)

    # plot with counters
    plot_cm(cm, labels, "%s/confusion_matrix_counters_%s.png" % (confusionMatricesDir, stage))

    # plot with probabilities
    np.set_printoptions(precision=2, suppress=True)
    probabilities_cm = np.empty((len(labels), len(labels)), dtype=float)
    for i, row in enumerate(cm):
        for j, column in enumerate(row):
            if sum(row):
                probabilities_cm[i, j] = "{0:.2f}".format(float(cm[i, j]) / sum(row))
            else:
                probabilities_cm[i, j] = 0.0

    plot_cm(probabilities_cm, labels, "%s/confusion_matrix_probabilities_%s.png" % (confusionMatricesDir, stage))


def produce_output(y_test, y_pred, y_probs, test_terms_name, false_predictions_f, unknown_predictions_f):
    with open(false_predictions_f, "w") as false_pred_f, open(unknown_predictions_f, "w") as unknown_pred_f:
        false_pred_f.write('index\tterm_name\torigin\tprediction\tprobability\n')
        unknown_pred_f.write('index\tterm_name\torigin\tprediction\tprobability\n')
        for i in range(len(y_pred)):
            if y_probs[i] < CLASSIFICATION_PROBABILITY_THRESHOLD:
                unknown_pred_f.write("%s\t%s\t%s\t%s\t%s\n" % (i, test_terms_name[i], y_test[i], y_pred[i], y_probs[i]))
                continue
            if y_pred[i] != y_test[i]:
                false_pred_f.write("%s\t%s\t%s\t%s\t%s\n" % (i, test_terms_name[i], y_test[i], y_pred[i], y_probs[i]))


def process_prediction_vector(y_test, y_pred, y_pred_probabilities):
    max_y_pred_probs = []
    y_pred_with_unknown_cls = []
    y_pred_fictive = []
    for i, cls in enumerate(y_pred):
        prob = max(y_pred_probabilities[i])
        max_y_pred_probs.append(prob)
        if prob < CLASSIFICATION_PROBABILITY_THRESHOLD:
            y_pred_with_unknown_cls.append("unknown")
            y_pred_fictive.append(y_test[i])
        else:
            y_pred_with_unknown_cls.append(y_pred[i])
            y_pred_fictive.append(y_pred[i])
    return (y_pred_with_unknown_cls, y_pred_fictive, max_y_pred_probs)


def ml_train(datasetFilePath, falsePredictionsFilePath, unknownPredictionsFilePath, confusionMatricesDir, classifierFilePath):
    logger.info("start of training and testing phase")

    classifier = OneVsRestClassifier(SVC(kernel='linear', probability=True), n_jobs=NUMBER_OF_CPUS_TO_USE)

    logger.info("loading data set")
    dataset, features_names = load_dataset(datasetFilePath)

    #limited_dataset = limit_dataset(dataset)
    limited_dataset = dataset
    
    ml_dataset = split_dataset(limited_dataset, len(features_names))

    logger.info("fitting training set X_train - %s, y_train - %s" % (ml_dataset.X_train.shape, ml_dataset.y_train.shape))
    classifier.fit(ml_dataset.X_train, ml_dataset.y_train)

    logger.info("predicting test set X_test - %s, y_test - %s" % (ml_dataset.X_test.shape, ml_dataset.y_test.shape))
    y_pred = classifier.predict(ml_dataset.X_test)

    y_pred_probabilities = classifier.predict_proba(ml_dataset.X_test)

    y_pred_with_unknown_cls, y_pred_fictive, max_y_pred_probs = process_prediction_vector(ml_dataset.y_test, y_pred, y_pred_probabilities)

    validation(ml_dataset.y_test, y_pred, y_pred_with_unknown_cls, y_pred_fictive, list(classifier.classes_) + ["unknown"])
    plot_confusion_matrices(ml_dataset.y_test, y_pred, list(classifier.classes_) + ["unknown"], confusionMatricesDir, "1")
    plot_confusion_matrices(ml_dataset.y_test, y_pred_with_unknown_cls, list(classifier.classes_) + ["unknown"], confusionMatricesDir, "2")
    plot_confusion_matrices(ml_dataset.y_test, y_pred_fictive, list(classifier.classes_) + ["unknown"], confusionMatricesDir, "3")

    produce_output(ml_dataset.y_test, y_pred, max_y_pred_probs, ml_dataset.test_terms_name, falsePredictionsFilePath, unknownPredictionsFilePath)

    logger.info("exporting classifier model")
    joblib.dump(classifier, classifierFilePath)

    logger.info("end of training and testing phase")


def parseOptions():
    parser = argparse.ArgumentParser()
    parser.add_argument("--dataset-f", required=True, dest="datasetFilePath", help="The full path for the dataset file (.tsv)")
    parser.add_argument("--false-predifction-f", required=True, dest="falsePredictionsFilePath", help="The full path for the false predictions output file (.tsv)")
    parser.add_argument("--unknown-predictions-f", required=True, dest="unknownPredictionsFilePath", help="The full path for the unknown predictions output file (.tsv)")
    parser.add_argument("--confusion-matrices-dir", required=True, dest="confusionMatricesDir", help="The full path for the confusion matrices directory")
    parser.add_argument("--classifier-f", required=True, dest="classifierFilePath", help="The full path for the classifier main dump file (.pkl)")
    return parser.parse_args()


def main():
    options = parseOptions()
    ml_train(options.datasetFilePath, options.falsePredictionsFilePath, options.unknownPredictionsFilePath, options.confusionMatricesDir, options.classifierFilePath)


if __name__ == '__main__':
    path = "/home/taykey/code/learningchess/data/results/checkmateclassifier/results6/"
    sys.argv.append("--dataset-f="+path+"input_10k_features.tsv")
    sys.argv.append("--false-predifction-f="+path+"false_predictions_f.tsv")
    sys.argv.append("--unknown-predictions-f="+path+"unknown_predictions_f.tsv")
    sys.argv.append("--confusion-matrices-dir="+path+"classifier")
    sys.argv.append("--classifier-f="+path+"classifier.pkl")
    main()