from PyQt6.QtWidgets import (
    QMainWindow,
    QTextEdit,
    QVBoxLayout,
    QHBoxLayout,
    QWidget,
    QPushButton,
    QTableWidget,
    QTableWidgetItem,
    QHeaderView,
    QFileDialog,
    QLabel,
    QTabWidget,
)
from PyQt6.QtCore import Qt
import os

from internal.utils.error_highlighter import ErrorHighlighter
from internal.utils.log_parser import LogParser
from internal.widgets.metrics_widget import MetricsWidget
from internal.utils.editor_log_parser import EditorLogParser
from internal.widgets.editor_metrics_widget import EditorMetricsWidget
from internal.utils.settings_manager import SettingsManager


class LogTab(QWidget):
    def __init__(self, tab_type="player", parent=None):
        super().__init__(parent)
        self.tab_type = tab_type
        self.settings = SettingsManager()
        self.setup_ui()
        self.errors_list = []

    def setup_ui(self):
        layout = QHBoxLayout(self)
        layout.setContentsMargins(16, 16, 16, 16)
        layout.setSpacing(16)

        if self.tab_type == "player":
            # Левая панель
            left_panel = self.setup_left_panel()
            layout.addWidget(left_panel, stretch=2)

            # Правая панель
            right_panel = self.setup_right_panel()
            layout.addWidget(right_panel, stretch=1)
        else:
            # Для Editor лога только метрики и кнопка загрузки
            editor_panel = QWidget()
            editor_layout = QVBoxLayout(editor_panel)
            editor_layout.setContentsMargins(0, 0, 0, 0)
            editor_layout.setSpacing(16)

            # Метрики для Editor лога
            self.metrics_widget = EditorMetricsWidget()
            editor_layout.addWidget(self.metrics_widget, stretch=1)

            # Кнопка загрузки для Editor лога
            button_container = QWidget()
            button_layout = QHBoxLayout(button_container)
            button_layout.setContentsMargins(0, 0, 0, 0)
            
            load_button = QPushButton("Select Editor Log File")
            load_button.clicked.connect(self.select_log_file)
            button_layout.addWidget(load_button)
            button_layout.addStretch()
            
            editor_layout.addWidget(button_container)
            layout.addWidget(editor_panel)

    def setup_left_panel(self):
        panel = QWidget()
        layout = QVBoxLayout(panel)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(8)

        # Таблица ошибок
        self.table = QTableWidget()
        self.table.setColumnCount(3)
        
        # Разные заголовки для разных типов логов
        if self.tab_type == "player":
            self.table.setHorizontalHeaderLabels(["Exception Type", "File", "Line"])
        else:
            self.table.setHorizontalHeaderLabels(["Category", "Size", "% of Total"])
        
        # Настройка размеров колонок
        header = self.table.horizontalHeader()
        header.setSectionResizeMode(0, QHeaderView.ResizeMode.Fixed)
        header.setSectionResizeMode(1, QHeaderView.ResizeMode.Stretch)
        header.setSectionResizeMode(2, QHeaderView.ResizeMode.Fixed)
        
        self.table.verticalHeader().setVisible(False)
        
        self.table.setColumnWidth(0, 200)
        self.table.setColumnWidth(2, 80)
        
        self.table.setSelectionBehavior(QTableWidget.SelectionBehavior.SelectRows)
        self.table.setAlternatingRowColors(True)
        self.table.itemClicked.connect(self.show_error_details)
        
        if self.tab_type == "editor":
            self.table.setProperty("editorLog", "true")
        
        layout.addWidget(self.table)

        # Кнопка загрузки
        load_button = QPushButton("Select Player Log File")
        load_button.clicked.connect(self.select_log_file)
        layout.addWidget(load_button)

        return panel

    def setup_right_panel(self):
        panel = QWidget()
        layout = QVBoxLayout(panel)
        layout.setSpacing(16)
        layout.setContentsMargins(0, 0, 0, 0)

        # Метрики только для Player лога
        if self.tab_type == "player":
            self.metrics_widget = MetricsWidget()
            layout.addWidget(self.metrics_widget)

            # Заголовок деталей ошибки
            error_details_title = QLabel("Exception Details")
            error_details_title.setProperty("class", "sectionTitle")  # Используем class вместо objectName

            layout.addWidget(error_details_title)

            # Детали ошибки
            self.text_edit = QTextEdit()
            self.text_edit.setReadOnly(True)
            self.highlighter = ErrorHighlighter(self.text_edit.document())
            layout.addWidget(self.text_edit)

        return panel

    def select_log_file(self):
        file_name, _ = QFileDialog.getOpenFileName(
            self,
            "Выберите лог-файл",
            "",
            "Log Files (*.log);;All Files (*.*)"
        )
        if file_name:
            self.settings.save_recent_file(self.tab_type, file_name)
            self.load_log(file_name)

    def load_log(self, file_path=None):
        try:
            if file_path is None:
                # Пробуем загрузить последний открытый файл
                file_path = self.settings.get_recent_file(self.tab_type)
                if not file_path or not os.path.exists(file_path):
                    # Если нет последнего файла, используем файл по умолчанию
                    file_path = f"unity_logs/{self.tab_type.capitalize()}.log"
                
            with open(file_path, "r", encoding="utf-8") as file:
                content = file.read()

            if self.tab_type == "player":
                self.load_player_log(content)
            else:
                self.load_editor_log(content)

            # Сохраняем путь к успешно загруженному файлу
            self.settings.save_recent_file(self.tab_type, file_path)

        except Exception as e:
            if self.tab_type == "player":
                self.text_edit.setText(f"Ошибка при чтении лога: {str(e)}")
            print(f"Ошибка при чтении лога: {str(e)}")

    def load_player_log(self, content):
        errors = LogParser.extract_errors(content)
        self.errors_list = []
        self.table.setRowCount(0)

        for error in errors:
            error_text = error.group(1)
            formatted_error = error_text.replace("  at ", "\n    at ")
            self.errors_list.append(formatted_error)

            error_type, file_path, line_number = LogParser.parse_error(error_text)
            self.add_error_to_table(error_type, file_path, line_number)

        self.metrics_widget.update_metrics(self.errors_list)
        self.table.resizeColumnsToContents()

    def load_editor_log(self, content):
        try:
            build_report = EditorLogParser.parse_build_report(content)
            self.metrics_widget.update_metrics(build_report)
        except Exception as e:
            print(f"Ошибка при обработке Editor лога: {str(e)}")

    @staticmethod
    def get_file_name(file_path: str) -> str:
        """Извлекает имя файла из полного пути."""
        return file_path.split('/')[-1].split('\\')[-1]

    def add_error_to_table(self, error_type, file_path, line_number):
        row_position = self.table.rowCount()
        self.table.insertRow(row_position)
        self.table.setItem(row_position, 0, QTableWidgetItem(error_type))
        # Показываем только имя файла без пути
        self.table.setItem(row_position, 1, QTableWidgetItem(self.get_file_name(file_path)))
        self.table.setItem(row_position, 2, QTableWidgetItem(line_number))

    def show_error_details(self, item):
        row = item.row()
        if row < len(self.errors_list):
            self.text_edit.setText(self.errors_list[row])


class LogViewer(QMainWindow):
    def __init__(self):
        super().__init__()
        self.settings = SettingsManager()
        self.setup_ui()
        self.load_recent_files()  # Добавляем загрузку последних файлов

    def setup_ui(self):
        self.setWindowTitle("UniLogViewer")
        self.setFixedSize(1200, 800)
        self.setWindowFlags(
            self.windowFlags() & ~Qt.WindowType.WindowMaximizeButtonHint
        )

        # Основной виджет с табами
        self.tabs = QTabWidget()
        self.tabs.setObjectName("mainTabs")
        self.setCentralWidget(self.tabs)

        # Создаем табы для разных логов
        self.player_tab = LogTab(tab_type="player")
        self.editor_tab = LogTab(tab_type="editor")

        self.tabs.addTab(self.player_tab, "Player Log")
        self.tabs.addTab(self.editor_tab, "Editor Log")

    def load_recent_files(self):
        # Загружаем последние открытые файлы
        player_log = self.settings.get_recent_file('player')
        editor_log = self.settings.get_recent_file('editor')

        # Загружаем файлы, если они существуют
        if player_log and os.path.exists(player_log):
            self.player_tab.load_log(player_log)
        else:
            print("Последний Player лог не найден")

        if editor_log and os.path.exists(editor_log):
            self.editor_tab.load_log(editor_log)
        else:
            print("Последний Editor лог не найден")
