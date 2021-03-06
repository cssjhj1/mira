from Qt.QtWidgets import *
from Qt.QtCore import *
from Qt.QtGui import *
import hooks
reload(hooks)
from hooks import Hook


class Task(QWidget):
    def __init__(self, parent=None):
        super(Task, self).__init__(parent)
        main_layout = QVBoxLayout(self)
        self.entity_label = QLabel()
        self.list_view = QListView()
        self.list_view.setFocusPolicy(Qt.NoFocus)
        main_layout.addWidget(self.entity_label)
        main_layout.addWidget(self.list_view)

    def set_label(self, text):
        self.entity_label.setText(text)

    def set_model(self, model_data):
        if model_data:
            self.model = DetailModel(model_data)
        else:
            self.model = QStandardItemModel()
        self.list_view.setModel(self.model)

    def set_delegate(self):
        delegate = TaskDelegate(self)
        self.list_view.setItemDelegate(delegate)
        self.show_delegate()

    def show_delegate(self):
        for i in xrange(self.model.rowCount()):
            self.list_view.openPersistentEditor(self.model.index(i, 0))

    def close_delegate(self):
        for i in xrange(self.model.rowCount()):
            self.list_view.closePersistentEditor(self.model.index(i, 0))


class DetailModel(QAbstractListModel):
    def __init__(self, model_data=[], parent=None):
        super(DetailModel, self).__init__(parent)
        self.__model_data = model_data

    @property
    def model_data(self):
        return self.__model_data

    @model_data.setter
    def model_data(self, value):
        self.__model_data = value

    def rowCount(self, parent=QModelIndex()):
        return len(self.__model_data)

    def data(self, index, role=Qt.DisplayRole):
        if not index.isValid():
            return
        row = index.row()
        if role == Qt.DisplayRole:
            return self.__model_data[row]

    def flags(self, index):
        return Qt.ItemIsEnabled


class TaskDelegate(QItemDelegate):
    def __init__(self, parent=None):
        super(TaskDelegate, self).__init__(parent)

    def createEditor(self, parent, option, index):
        cell_widget = CellTaskWidget(parent)
        return cell_widget

    def setEditorData(self, editor, index):
        item = index.model().data(index, Qt.DisplayRole)
        if item:
            editor.set_image(item.pix_map)
            info = "<font size=4 face=Arial color=#fff><b>%s</b>  -  %s</font>" % (item.step, item.task)
            editor.set_info(info)
            editor.set_action(item.actions)
            editor.set_status(item.status_name, item.status_color)
            editor.item = item

    def sizeHint(self, option, index):
        return QSize(300, 90)


class CellTaskWidget(QWidget):
    def __init__(self, parent=None):
        super(CellTaskWidget, self).__init__(parent)
        self.item = None
        self.menu = QMenu()
        self.action_group = QActionGroup(self)
        main_layout = QHBoxLayout(self)
        main_layout.setContentsMargins(0, 0, 0, 3)
        group_box = QGroupBox()
        main_layout.addWidget(group_box)
        group_layout = QHBoxLayout(group_box)
        group_layout.setContentsMargins(0, 0, 0, 0)
        self.thumb_label = QLabel()

        info_layout = QVBoxLayout()
        self.info_label = QLabel()
        self.status_label = QLabel()
        info_layout.addWidget(self.info_label)
        info_layout.addWidget(self.status_label)
        info_layout.setAlignment(Qt.AlignVCenter)

        self.actions_btn = QPushButton("Actions")
        self.actions_btn.setStyleSheet("QPushButton{color: #00b4ff; font: bold;}QPushButton:hover{color:#ff8c00;}")
        group_layout.addWidget(self.thumb_label)
        group_layout.addLayout(info_layout)
        group_layout.addWidget(self.actions_btn)
        group_layout.setStretch(0, 3)
        group_layout.setStretch(1, 10)
        group_layout.setStretch(2, 1)
        group_layout.setStretchFactor(self.thumb_label, 0)
        group_layout.setStretchFactor(info_layout, 1)
        group_layout.setStretchFactor(self.actions_btn, 0)
        self.action_group.triggered.connect(self.__on_acton_triggered)

    def set_image(self, pix_map):
        self.thumb_label.setPixmap(pix_map)

    def set_info(self, info):
        self.info_label.setText(info)

    def set_status(self, status_name, status_color):
        self.status_label.setText("<font size=4 color=%s>%s</font>" % (status_color, status_name))

    def set_action(self, actions):
        self.menu.clear()
        for action in actions:
            task_action = self.action_group.addAction(action)
            self.menu.addAction(task_action)
        self.actions_btn.setMenu(self.menu)

    def __on_acton_triggered(self, action):
        project = self.item.project
        entity_type = self.item.entity_type
        asset_type_sequence = self.item.asset_type_sequence
        asset_shot_names = self.item.asset_name_shot
        step = self.item.step
        task = self.item.task
        action_name = action.text()
        hooker = Hook(project, entity_type, asset_type_sequence, asset_shot_names, step, task, action_name)
        hooker.execute()

