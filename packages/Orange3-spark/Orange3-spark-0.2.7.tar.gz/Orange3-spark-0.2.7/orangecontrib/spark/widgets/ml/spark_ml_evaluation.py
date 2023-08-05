__author__ = 'jamh'

import random

from Orange.widgets import widget, gui
from PyQt4 import QtGui, QtCore
from pyspark.ml import evaluation

from orangecontrib.spark.base.spark_ml_transformer import OWSparkTransformer
from orangecontrib.spark.utils.ml_api_utils import get_evaluators


class OWSparkMLEvaluator(OWSparkTransformer, widget.OWWidget):
    priority = 8
    name = "Evaluation"
    description = "evaluation"
    icon = "../icons/Category-Evaluate.svg"

    module = evaluation
    module_name = 'Evaluation'
    box_text = "Spark Model Evaluator"
    get_modules = get_evaluators

    # outputs = [("DataFrame", pyspark.sql.DataFrame, widget.Dynamic)]

    def __init__(self):
        super().__init__()

        # Create place to show/set parameters of method
        self.values_box = gui.widgetBox(self.box, 'Evaluation:', addSpace = True)

        self.table = QtGui.QTableWidget(self.values_box)
        self.tableItem = QtGui.QTableWidgetItem()

        self.values_box.hide()

    def refresh_method(self, text):
        super().refresh_method(text)
        if hasattr(self, 'values_box'):
            self.values_box.hide()

    def apply(self):
        metric_names = self.gui_parameters['metricName'].doc_text.split('(')[-1].replace(')', '').split('|')
        values = { }
        method_instance = self.method()
        paramMap = self.build_param_map(method_instance)

        if self.in_df:
            for metric in metric_names:
                metricName = self.gui_parameters['metricName'].get_param_name()
                paramMap[metricName] = metric
                values[metric] = method_instance.apply(self.in_df, paramMap)
        else:
            for k in metric_names:
                values[k] = round(5 * random.random() - 2.5, 2)

        # self.send("DataFrame", self.out_df)
        self.table.clear()
        self.table.resize(500, 500)
        self.table.setRowCount(len(values))
        self.table.setColumnCount(2)

        # set label
        self.table.setHorizontalHeaderLabels(["Metric", "Value"])
        # self.table.setVerticalHeaderLabels(list(values))

        # set data
        for i, kv in enumerate(values.items()):
            k, v = kv
            it1 = QtGui.QTableWidgetItem(k)
            it2 = QtGui.QTableWidgetItem(str(v))
            self.table.setItem(i, 0, it1)
            self.table.setItem(i, 1, it2)
            it1.setFlags(QtCore.Qt.ItemIsEnabled)
            it2.setFlags(QtCore.Qt.ItemIsEnabled)

        # show table
        self.values_box.show()
