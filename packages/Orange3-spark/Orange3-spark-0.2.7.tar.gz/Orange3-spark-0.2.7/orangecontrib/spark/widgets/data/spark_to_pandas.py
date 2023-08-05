__author__ = 'jamh'

import pandas
import pyspark
from Orange.widgets import widget, gui, settings
from PyQt4.QtGui import QSizePolicy


class OWSparkToPandas(widget.OWWidget):
    priority = 10
    name = "to Pandas"
    description = "Convert Spark dataframe to Pandas"
    icon = "../icons/spark.png"

    inputs = [("DataFrame", pyspark.sql.DataFrame, "get_input", widget.Default)]
    outputs = [("Dataframe", pandas.DataFrame, widget.Dynamic)]
    settingsHandler = settings.DomainContextHandler()

    def __init__(self):
        super().__init__()
        gui.label(self.controlArea, self, "Spark->Pandas:")
        self.setSizePolicy(QSizePolicy.Maximum, QSizePolicy.Maximum)

    def get_input(self, obj):
        self.send("Dataframe", obj.toPandas())
