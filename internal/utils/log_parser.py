import re


class LogParser:
    @staticmethod
    def parse_error(error_text):
        error_type = re.match(r"(\w+Exception)", error_text)
        error_type = error_type.group(1) if error_type else "Unknown"

        file_info = re.search(r"in (.*?):(\d+)", error_text)
        if file_info:
            file_path = file_info.group(1)
            line_number = file_info.group(2)
        else:
            file_path = "Unknown"
            line_number = "N/A"

        return error_type, file_path, line_number

    @staticmethod
    def extract_errors(content):
        error_pattern = r"(\w+Exception:.*?)(?=\n\n|\Z)"
        return list(re.finditer(error_pattern, content, re.DOTALL)) 