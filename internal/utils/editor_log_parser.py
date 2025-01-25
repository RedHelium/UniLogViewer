from dataclasses import dataclass
import re


@dataclass
class AssetInfo:
    size_mb: float
    percentage: float


@dataclass
class BuildReport:
    textures: AssetInfo = None
    meshes: AssetInfo = None
    animations: AssetInfo = None
    sounds: AssetInfo = None
    shaders: AssetInfo = None
    other_assets: AssetInfo = None
    levels: AssetInfo = None
    file_headers: AssetInfo = None
    total_user_assets_mb: float = 0
    complete_build_size_mb: float = 0
    status: str = ""
    time_seconds: int = 0
    time_ms: int = 0

    def __post_init__(self):
        self.textures = AssetInfo(0, 0)
        self.meshes = AssetInfo(0, 0)
        self.animations = AssetInfo(0, 0)
        self.sounds = AssetInfo(0, 0)
        self.shaders = AssetInfo(0, 0)
        self.other_assets = AssetInfo(0, 0)
        self.levels = AssetInfo(0, 0)
        self.file_headers = AssetInfo(0, 0)


class EditorLogParser:
    @staticmethod
    def parse_size_line(line: str) -> tuple[float, float]:
        """Парсит строку вида 'Textures   11.0 mb  76.5%'"""
        try:
            parts = [p for p in line.strip().split() if p]

            # Получаем размер
            size_str = parts[-3]  # Размер всегда третий с конца
            size = float(size_str)
            if "kb" in parts[-2].lower():  # Проверяем единицы измерения
                size = size / 1024

            # Получаем процент (всегда последний элемент)
            percentage = float(parts[-1].rstrip("%"))

            return size, percentage
        except Exception as e:
            print(f"Ошибка при парсинге строки '{line}': {str(e)}")
            return 0, 0

    @staticmethod
    def parse_size_only(line: str) -> float:
        """Парсит строку, содержащую только размер (для Total и Complete size)"""
        try:
            parts = [p for p in line.strip().split() if p]
            for i, part in enumerate(parts):
                if part.lower() == "mb":
                    return float(parts[i - 1])
            return 0
        except Exception:
            return 0

    @staticmethod
    def parse_build_report(content: str) -> BuildReport:
        report = BuildReport()

        try:
            # Парсим статус сборки
            status_match = re.search(r"Build Finished, Result: (\w+)", content)
            if status_match:
                report.status = status_match.group(1)

            # Парсим время сборки
            time_match = re.search(
                r"Build completed with a result of '[\w]+' in (\d+) seconds \((\d+) ms\)",
                content,
            )
            if time_match:
                report.time_seconds = int(time_match.group(1))
                report.time_ms = int(time_match.group(2))

            # Разбиваем на строки и фильтруем пустые
            lines = [line.strip() for line in content.split("\n") if line.strip()]

            # Словарь соответствия названий в логе и атрибутов класса
            asset_mapping = {
                "Textures": "textures",
                "Meshes": "meshes",
                "Animations": "animations",
                "Sounds": "sounds",
                "Shaders": "shaders",
                "Other Assets": "other_assets",
                "Levels": "levels",
                "File headers": "file_headers",
            }

            for line in lines:
                if "Total User Assets" in line:
                    report.total_user_assets_mb = EditorLogParser.parse_size_only(line)
                elif "Complete build size" in line:
                    report.complete_build_size_mb = EditorLogParser.parse_size_only(
                        line
                    )
                else:
                    # Проверяем, является ли строка описанием ассета
                    for asset_name, attr_name in asset_mapping.items():
                        if line.startswith(asset_name):
                            size, percentage = EditorLogParser.parse_size_line(line)
                            setattr(report, attr_name, AssetInfo(size, percentage))
                            break

        except Exception as e:
            print(f"Ошибка при парсинге Build Report: {str(e)}")

        return report
