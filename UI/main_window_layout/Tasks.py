# UI/Tasks.py
from PySide6.QtWidgets import QGroupBox, QVBoxLayout, QListWidget, QListWidgetItem
from PySide6.QtCore import Qt


class TaskPane:
    """
    Encapsulates the task list pane: layout + logic.
    Exposes the QWidget and provides methods to populate the list.
    """

    def __init__(self):
        self.group_box = QGroupBox("Tasks")
        layout = QVBoxLayout(self.group_box)

        self.list_widget = QListWidget()
        layout.addWidget(self.list_widget)

    def widget(self):
        return self.group_box

    def populate_tasks(self, tasks):
        """
        tasks: list of Task objects
        """
        self.list_widget.clear()
        for task in tasks:
            item = QListWidgetItem(task.name)
            item.setData(Qt.UserRole, task)
            self.list_widget.addItem(item)

    def get_selected_task(self):
        """Return the currently selected Task object."""
        selected_items = self.list_widget.selectedItems()
        if not selected_items:
            return None
        return selected_items[0].data(Qt.UserRole)
