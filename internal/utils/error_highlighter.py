from PyQt6.QtGui import QSyntaxHighlighter, QTextCharFormat, QColor
import re


class ErrorHighlighter(QSyntaxHighlighter):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setup_formats()

    def setup_formats(self):
        self.error_format = QTextCharFormat()
        self.error_format.setForeground(QColor("#A4262C"))

        self.file_format = QTextCharFormat()
        self.file_format.setForeground(QColor("#0078D4"))

    def highlightBlock(self, text):
        patterns = {
            "error": (r"(\w+Exception:.*$)", self.error_format),
            "file": (
                r"(?:in\s+)?((?:[A-Z]:|\/)?(?:[\w\s-]+\/)*[\w-]+\.[a-zA-Z]+(?::\d+)?)",
                self.file_format,
            ),
        }

        for pattern, format in patterns.values():
            for match in re.finditer(pattern, text):
                self.setFormat(match.start(), match.end() - match.start(), format)
