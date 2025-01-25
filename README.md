# Unity Log Viewer

A desktop application for viewing and analyzing Unity log files with a modern Material Design interface.

## Features

- View and analyze Player and Editor logs
- Track error metrics and statistics
- Material Design dark theme
- Automatic loading of recently opened files
- Progress visualization for error types
- Detailed error information view
- Build report analysis for Editor logs

## Requirements

- Python 3.8+
- PyQt6
- PyQt6-Charts

## Installation

1. Clone the repository:
bash
git clone https://github.com/yourusername/unity-log-viewer.git

2. Install dependencies:
pip install -r requirements.txt

3. Run the application:
python main.py


## Usage

1. Launch the application
2. Switch between Player and Editor logs using tabs
3. Load log files using the "Select log file" button
4. View error details and metrics in the right panel
5. Track error statistics and build report information


## Settings

The application stores settings in `~/.unity_log_viewer/settings.json`, including:
- Recently opened files
- User preferences

## Contributing

1. Fork the repository
2. Create a feature branch
3. Commit your changes
4. Push to the branch
5. Create a Pull Request

## License

MIT License
