from Orange.widgets import gui
from PyQt4 import QtGui, QtCore


class GuiParam:
    widget = None

    def __init__(self, parent_widget, label = None, default_value = None, place_holder_text = None, list_values = None, callback_func = None, doc_text = None, **kwargs):
        """

        :param label: a text label for the GUI control
        :param default_value: a default value to asing to the value of the control in case of empty.
        :param place_holder_text: a text to show when the value of the control is empty, it can be used to avoid use of label.
        :param list_values: a closed list of the values that accepts this parameter, this should create a combobox like control.
        :param callback_func: a call back function when the value of the GUI control changes, e.g. combobox selection.
        :param doc_text: if want to add extra documentation for the parameter, it can be used for a tool tip for instance.
        :param kwargs: used to add extra parameters for future improvements and compatibility.
        :return: an instance of gui_param
        """
        dummy_func = lambda x: True

        self.default_value = default_value
        list_values = ['True', 'False'] if default_value in ('True', 'False') else list_values

        self.callback_func = callback_func
        self.parent_widget = parent_widget
        self.hbox = self.parent_widget
        layout = self.hbox.layout()
        if doc_text:
            self.doc_text = doc_text

        if list_values:
            self.list_values = list_values
            self.gui_type = 'multiple'
            callback_func = dummy_func if not callback_func else callback_func
            self.widget = create_auto_combobox(parent_widget, self.list_values, callback_func)
            self.widget.setStyleSheet("background-color: rgb(255, 255, 255);")
            if self.default_value:
                index = self.widget.findText(self.default_value, QtCore.Qt.MatchFixedString)
                if index >= 0:
                    self.widget.setCurrentIndex(index)

        else:
            self.gui_type = 'single'
            self.widget = QtGui.QLineEdit(parent_widget)
            self.widget.setStyleSheet("background-color: rgb(255, 255, 255);")
            self.widget.setPlaceholderText(str(place_holder_text))
            if self.default_value:
                self.widget.setText(str(self.default_value))

        if label:
            self.label = label + ":"
            self.widget_label = QtGui.QLabel(self.label, self.parent_widget)
            self.widget_label.setBuddy(self.widget)

            self.hbox = gui.widgetBox(self.hbox, orientation = 'horizontal', addSpace = True)
            layout = self.hbox.layout()
            layout.addWidget(self.widget_label)

        layout.addWidget(self.widget)

    def get_value(self):
        if self.gui_type == 'multiple':
            return self.widget.currentText()
        elif self.gui_type == 'single':
            return self.widget.text()
        else:
            return None

    def update(self, values):
        self.widget.clear()
        if self.gui_type == 'multiple':
            for val in values:
                self.widget.addItem(val)
        else:
            self.widget.setText(values)

    def get_usable_value(self):
        val = self.get_value().strip()
        if val == 'None' or val == '' or val is None:
            return None
        if val in ('True', 'False'):
            return True if val == 'True' else False
        try:
            try:
                if float(val) == int(val):
                    if "." in val:
                        return float(val)
                    return int(val)
            except ValueError:
                return float(val)

        except ValueError:
            return val


def create_auto_combobox(parent_widget, values, callback_func = None):
    combo = QtGui.QComboBox(parent_widget)
    for val in values:
        combo.addItem(val)

    combo.activated[str].connect(callback_func)
    return combo
