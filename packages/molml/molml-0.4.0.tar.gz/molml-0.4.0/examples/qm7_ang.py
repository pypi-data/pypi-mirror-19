from __future__ import print_function
import time

from sklearn.linear_model import Ridge
from sklearn.kernel_ridge import KernelRidge
from sklearn.metrics import mean_absolute_error as MAE

from molml.features import EncodedAngle

from utils import load_qm7


if __name__ == "__main__":
    for m in range(4):
        Xin_train, Xin_test, y_train, y_test = load_qm7()
        start = time.time()
        feat = EncodedAngle(n_jobs=-1,  max_depth=2,
                            slope=20., r_cut=6., form=m)
        X_train = feat.fit_transform(Xin_train)
        print(X_train.shape)
        X_test = feat.transform(Xin_test)
        print(time.time() - start)

        clfs = [
            Ridge(alpha=0.01),
            KernelRidge(alpha=1e-9, gamma=1e-5, kernel="rbf"),
        ]
        for clf in clfs:
            print(clf)
            start = time.time()
            clf.fit(X_train, y_train)
            train_error = MAE(clf.predict(X_train), y_train)
            test_error = MAE(clf.predict(X_test), y_test)
            string = "Train MAE: %.8f Test MAE: %.8f Time: %.2f"
            print(string % (train_error, test_error, time.time() - start))
            print()
