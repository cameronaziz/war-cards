from typing import List, Tuple

import matplotlib.pyplot as plt
import numpy as np
import numpy.typing as npt
from sklearn import datasets
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import learning_curve


def graph(scores: npt.NDArray[np.float64]):
    train_sizes, _train_scores, _test_scores = learning_curve(
        RandomForestClassifier(),
        X,
        y,
        cv=10,
        scoring="accuracy",
        n_jobs=-1,
        train_sizes=np.linspace(0.01, 1.0, 50),
    )
    train_std = np.std(scores, axis=1)
    train_mean = np.mean(scores, axis=1)

    plt.subplots(1, figsize=(10, 10))
    plt.plot(train_sizes, train_mean, "--", color="#111111", label="Training score")
    # plt.plot(train_sizes, test_mean, color="#111111", label="Cross-validation score")

    plt.fill_between(
        train_sizes, train_mean - train_std, train_mean + train_std, color="#DDDDDD"
    )
    # plt.fill_between(train_sizes, test_mean - test_std, test_mean + test_std, color="#DDDDDD")

    plt.title("Learning Curve")
    plt.xlabel("Training Set Size"), plt.ylabel("Accuracy Score"), plt.legend(
        loc="best"
    )
    plt.tight_layout()
    plt.show()
