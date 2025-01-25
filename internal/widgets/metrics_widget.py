from PyQt6.QtWidgets import (
    QFrame,
    QVBoxLayout,
    QLabel,
    QProgressBar,
    QHBoxLayout,
    QWidget,
)


class MetricsWidget(QFrame):
    ERROR_TYPES = {
        "NullReferenceException": {
            "style_type": "nullref",
            "color": "#03DAC5",  # Бирюзовый
        },
        "ArgumentException": {"style_type": "argument", "color": "#CF6679"},  # Красный
        "IndexOutOfRangeException": {
            "style_type": "index",
            "color": "#FFB74D",  # Оранжевый
        },
        "MissingReferenceException": {
            "style_type": "missing",
            "color": "#4FC3F7",  # Голубой
        },
        "KeyNotFoundException": {"style_type": "key", "color": "#AED581"},  # Зеленый
    }

    def __init__(self):
        super().__init__()
        self.setObjectName("metricsFrame")
        self.setup_ui()

    def setup_ui(self):
        layout = QVBoxLayout(self)
        layout.setSpacing(12)  # Уменьшаем отступы между элементами
        layout.setContentsMargins(16, 16, 16, 16)

        # Заголовок
        title = QLabel("Metrics")
        title.setObjectName("metricsTitle")
        layout.addWidget(title)

        # Всего ошибок в одной строке с заголовком
        total_container = QHBoxLayout()
        total_errors = QLabel("Total Exceptions:")
        total_errors.setProperty("class", "errorMetricTitle")
        self.total_value = QLabel("0")
        self.total_value.setProperty("class", "errorMetricValue")
        self.total_value.setProperty("type", "total")  # Добавляем тип для стилизации
        total_container.addWidget(total_errors)
        total_container.addWidget(self.total_value)
        total_container.addStretch()
        layout.addLayout(total_container)

        # Создаем метрики для каждого типа ошибки
        for error_type, props in self.ERROR_TYPES.items():
            self.setup_error_type(
                error_type, props["style_type"], layout, props["color"]
            )

        layout.addStretch()

    def setup_error_type(self, error_type, style_type, layout, color):
        # Контейнер для каждого типа ошибки
        container = QWidget()
        error_layout = QVBoxLayout(container)
        error_layout.setSpacing(4)  # Минимальный отступ между элементами
        error_layout.setContentsMargins(0, 0, 0, 0)

        # Заголовок и значение в одной строке
        header = QHBoxLayout()
        label = QLabel(error_type)
        label.setProperty("class", "errorMetricTitle")
        value = QLabel("0")
        value.setProperty("class", "errorMetricValue")
        value.setProperty("type", style_type)  # Добавляем тип для стилизации
        header.addWidget(label)
        header.addWidget(value)
        header.addStretch()
        error_layout.addLayout(header)

        # Прогресс бар
        progress = QProgressBar()
        progress.setTextVisible(False)
        progress.setFixedHeight(4)  # Делаем прогресс бар тоньше
        progress.setStyleSheet(
            f"""
            QProgressBar::chunk {{
                background-color: {color};
                border-radius: 2px;
            }}
        """
        )
        error_layout.addWidget(progress)

        layout.addWidget(container)

        setattr(self, f"{error_type.lower()}_value", value)
        setattr(self, f"{error_type.lower()}_progress", progress)

    def update_metrics(self, errors_list):
        total_errors = len(errors_list)
        self.total_value.setText(str(total_errors))

        # Подсчет ошибок каждого типа
        error_counts = {error_type: 0 for error_type in self.ERROR_TYPES.keys()}

        for error in errors_list:
            for error_type in self.ERROR_TYPES.keys():
                if error_type in error:
                    error_counts[error_type] += 1

        # Обновление значений и прогресс-баров
        if total_errors > 0:
            for error_type, count in error_counts.items():
                value_widget = getattr(self, f"{error_type.lower()}_value")
                progress_widget = getattr(self, f"{error_type.lower()}_progress")

                value_widget.setText(str(count))
                percent = (count / total_errors) * 100
                progress_widget.setValue(int(percent))
        else:
            # Если ошибок нет, обнуляем все значения
            for error_type in self.ERROR_TYPES.keys():
                value_widget = getattr(self, f"{error_type.lower()}_value")
                progress_widget = getattr(self, f"{error_type.lower()}_progress")

                value_widget.setText("0")
                progress_widget.setValue(0)
