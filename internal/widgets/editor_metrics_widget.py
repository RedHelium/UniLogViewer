from PyQt6.QtWidgets import (
    QFrame,
    QVBoxLayout,
    QHBoxLayout,
    QLabel,
    QWidget,
    QGridLayout,
)
from PyQt6.QtCore import Qt


class BuildMetricWidget(QWidget):
    def __init__(self, title, icon, parent=None):
        super().__init__(parent)
        self.setup_ui(title, icon)

    def setup_ui(self, title, icon):
        layout = QVBoxLayout(self)
        layout.setSpacing(4)
        layout.setContentsMargins(0, 0, 0, 0)

        # Создаем основной контейнер
        self.container = QFrame()
        self.container.setProperty("class", "buildMetric")
        container_layout = QVBoxLayout(self.container)
        container_layout.setContentsMargins(
            8, 8, 8, 8
        )  # Уменьшаем внутренние отступы с 16 до 8
        container_layout.setSpacing(2)  # Уменьшаем расстояние между элементами

        # Заголовок с иконкой
        header = QWidget()
        header_layout = QHBoxLayout(header)
        header_layout.setContentsMargins(0, 0, 0, 0)
        header_layout.setSpacing(4)  # Уменьшаем отступ между иконкой и текстом

        icon_label = QLabel(icon)
        title_label = QLabel(title)
        title_label.setProperty("class", "metricTitle")

        header_layout.addWidget(icon_label)
        header_layout.addWidget(title_label)
        header_layout.addStretch()

        # Значение
        self.value_label = QLabel("0")
        self.value_label.setProperty("class", "metricValue")
        self.value_label.setAlignment(Qt.AlignmentFlag.AlignLeft)
        self.value_label.setWordWrap(True)

        container_layout.addWidget(header)
        container_layout.addWidget(self.value_label)

        layout.addWidget(self.container)

    def set_value(self, value, unit=""):
        try:
            text = f"{value}{unit}"
            print(f"Setting value: {text}")
            self.value_label.setText(text)
            print(f"Value set successfully. Label text: {self.value_label.text()}")
        except Exception as e:
            print(f"Ошибка при установке значения: {str(e)}")


class EditorMetricsWidget(QFrame):
    def __init__(self):
        super().__init__()
        self.setObjectName("metricsFrame")
        self.setup_ui()

    def setup_ui(self):
        layout = QVBoxLayout(self)
        layout.setSpacing(12)  # Уменьшаем отступы между секциями
        layout.setContentsMargins(16, 16, 16, 16)  # Уменьшаем внешние отступы

        # Заголовок
        title = QLabel("Build Report")
        title.setObjectName("metricsTitle")
        layout.addWidget(title)

        # Статус сборки и основные метрики в одной строке
        top_metrics = QHBoxLayout()
        top_metrics.setSpacing(8)  # Уменьшаем отступы между элементами

        self.build_status = BuildMetricWidget("Build Status", "🎯")
        self.build_time = BuildMetricWidget("Build Time", "⏱️")
        self.total_build_size = BuildMetricWidget(
            "Build Size", "📦"
        )  # Сократили название
        self.total_assets_size = BuildMetricWidget(
            "Assets Size", "📊"
        )  # Сократили название

        top_metrics.addWidget(self.build_status)
        top_metrics.addWidget(self.build_time)
        top_metrics.addWidget(self.total_build_size)
        top_metrics.addWidget(self.total_assets_size)
        layout.addLayout(top_metrics)

        # Заголовок для ассетов
        assets_title = QLabel("Assets Usage")
        assets_title.setObjectName("metricsSubtitle")
        layout.addWidget(assets_title)

        # Метрики ассетов в компактной сетке
        assets_grid = QWidget()
        assets_layout = QGridLayout(assets_grid)
        assets_layout.setSpacing(8)  # Уменьшаем отступы между элементами
        assets_layout.setContentsMargins(0, 0, 0, 0)  # Убираем внешние отступы

        # Метрики ассетов с сокращенными названиями
        self.assets_metrics = {
            "textures": BuildMetricWidget("Textures", "🖼️"),
            "meshes": BuildMetricWidget("Meshes", "🔷"),
            "animations": BuildMetricWidget("Animations", "🎬"),
            "sounds": BuildMetricWidget("Sounds", "🔊"),
            "shaders": BuildMetricWidget("Shaders", "✨"),
            "other": BuildMetricWidget("Other Assets", "📁"),
            "levels": BuildMetricWidget("Levels", "🎮"),
            "headers": BuildMetricWidget("File Headers", "📑"),
        }

        # Размещаем метрики в сетке 4x2
        metrics_list = list(self.assets_metrics.values())
        for i in range(4):
            for j in range(2):
                idx = i * 2 + j
                if idx < len(metrics_list):
                    assets_layout.addWidget(metrics_list[idx], i, j)
                    assets_layout.setColumnStretch(j, 1)
                    # Уменьшаем минимальные размеры
                    assets_layout.setRowMinimumHeight(i, 75)  # Уменьшаем высоту
                    assets_layout.setColumnMinimumWidth(j, 180)  # Уменьшаем ширину

        layout.addWidget(assets_grid)
        layout.addStretch()

    def update_metrics(self, build_report):
        try:
            print("\n=== Обновление метрик Build Report ===")

            # Обновляем статус сборки
            if build_report.status:
                status_color = (
                    "#4CAF50" if build_report.status == "Success" else "#F44336"
                )
                self.build_status.set_value(build_report.status)
                self.build_status.value_label.setStyleSheet(f"color: {status_color}")

            # Обновляем время сборки
            if build_report.time_seconds > 0:
                minutes = build_report.time_seconds // 60
                seconds = build_report.time_seconds % 60
                time_text = f"{minutes}m {seconds}s" if minutes > 0 else f"{seconds}s"
                self.build_time.set_value(time_text)

            # Обновляем основные метрики
            print(f"Complete Build Size: {build_report.complete_build_size_mb:.1f} MB")
            print(f"Total User Assets: {build_report.total_user_assets_mb:.1f} MB")

            self.total_build_size.set_value(
                f"{build_report.complete_build_size_mb:.1f}", " MB"
            )
            self.total_assets_size.set_value(
                f"{build_report.total_user_assets_mb:.1f}", " MB"
            )

            # Обновляем метрики ассетов
            asset_data = {
                "textures": (build_report.textures, "Textures"),
                "meshes": (build_report.meshes, "Meshes"),
                "animations": (build_report.animations, "Animations"),
                "sounds": (build_report.sounds, "Sounds"),
                "shaders": (build_report.shaders, "Shaders"),
                "other": (build_report.other_assets, "Other"),
                "levels": (build_report.levels, "Levels"),
                "headers": (build_report.file_headers, "Headers"),
            }

            print("\nОбновление метрик ассетов:")
            for key, (asset_info, name) in asset_data.items():
                if asset_info is None:
                    print(f"Warning: {name} info is None")
                    continue

                print(
                    f"{name}: {asset_info.size_mb:.1f} MB ({asset_info.percentage:.1f}%)"
                )
                size_text = f"{asset_info.size_mb:.1f} MB"
                percentage_text = f" ({asset_info.percentage:.1f}%)"

                if key in self.assets_metrics:
                    self.assets_metrics[key].set_value(size_text + percentage_text)
                    print(
                        f"Обновлено значение для {key}: {size_text + percentage_text}"
                    )
                else:
                    print(f"Error: Метрика {key} не найдена в self.assets_metrics")

        except Exception as e:
            print(f"Ошибка при обновлении метрик: {str(e)}")
            import traceback

            traceback.print_exc()
