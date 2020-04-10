from numpy import mean
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import cross_val_score

LOGISTIC_REGRESSION_PARAMETERS = {'C': 0.1,
                                  'max_iter': 100}


def fit_classifier(X, y):
    y = y.values
    classifier = LogisticRegression(**LOGISTIC_REGRESSION_PARAMETERS)
    return classifier.fit(X, y)


def cross_val_score_classifier(X, y):
    classifier = LogisticRegression(**LOGISTIC_REGRESSION_PARAMETERS)
    cv_score = mean(cross_val_score(classifier, X, y, cv=3, scoring='roc_auc'))
    return cv_score


def compute_CV_score_for_each_class(X, y_full, labels):
    scores = []
    for label in labels:
        target = y_full[label].values
        cv_score = cross_val_score_classifier(X, target)
        scores.append(cv_score)
        print('CV score for class {} is {}'.format(label, cv_score))
    return scores


def fit_models(X, y_full, labels):
    classifiers = {}
    for idx, label in enumerate(labels):
        print('fit', label)
        target = y_full[label]
        classifier = fit_classifier(X, target)
        classifiers[label] = classifier
    return classifiers


def get_feature_importance_logistic_regression(labels, classifiers):
    feature_importance = []
    for idx, label in enumerate(labels):
        classifier = classifiers[idx]
        coefficients = classifier.coef_[0]
        coefficients = 100.0 * (coefficients / coefficients.max())
        feature_importance.append(coefficients)
    return feature_importance

