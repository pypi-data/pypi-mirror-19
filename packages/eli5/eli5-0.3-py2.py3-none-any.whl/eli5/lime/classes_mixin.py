# # -*- coding: utf-8 -*-
# from __future__ import absolute_import
#
# from sklearn.preprocessing import LabelEncoder
#
# from .utils import fix_multiclass_predict_proba
#
#
# class ClassesMeta(type):
#     def __call__(cls, *args, **kwargs):
#         classes = kwargs.pop("classes", None)
#         obj = type.__call__(cls, *args, **kwargs)
#         obj.classes = classes
#         return obj
#
#
# class ClassesMixin(object):
#     def get_params(self, deep=True):
#         params = super(ClassesMixin, self).get_params(deep=deep)
#         params['classes'] = self.classes
#         return params
#
#     def set_params(self, params):
#         self.classes = params.pop('classes', None)
#         return super(ClassesMixin, self).set_params(params)
#
#     def fit(self, X, y):
#         self._private_le = LabelEncoder().fit(self.classes)
#         return super(ClassesMixin, self).fit(X, self._private_le.transform(y))
#
#     def predict(self, X):
#         y_pred = super(ClassesMixin, self).predict(X)
#         return self._private_le.inverse_transform(y_pred)
#
#     def predict_proba(self, X):
#         probs = super(ClassesMixin, self).predict_proba(X)
#         return fix_multiclass_predict_proba(probs, self.classes_,
#                                             self._private_le.classes_)
#
#
# def add_classes_wrapper(cls):
#     """
#     >>> from sklearn.linear_model import LogisticRegression
#     >>> from sklearn.datasets import load_iris
#     >>> LogisticRegressionWithClasses = add_classes_wrapper(LogisticRegression)
#     >>> clf = LogisticRegressionWithClasses(classes=[0, 1, 2, 4])
#     >>> iris = load_iris()
#     >>> clf = clf.fit(iris.data, iris.target)
#     >>> clf.predict_proba(iris.data).shape
#     (150, 4)
#     >>> clf.classes_
#     """
#     return ClassesMeta(cls.__name__ + "WithClasses", (ClassesMixin, cls), {})
