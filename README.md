# qman-pyqt

![License](https://img.shields.io/badge/license-MIT-blue.svg)
![Python Version](https://img.shields.io/badge/python-3.8%2B-blue.svg)
![PySide6](https://img.shields.io/badge/PySide6-6.4.0-green.svg)

qman-pyqt is a Python application built with PySide6 for managing queues at the Bialkow Observatory. It provides a user-friendly interface to handle various queue operations efficiently.

## Table of Contents

- [Features](#features)
- [Installation](#installation)
- [Usage](#usage)
- [Authors](#authors)
- [Contributing](#contributing)
- [License](#license)

## Features

- **Manage Queues:** Add, edit, and delete queues with ease.
- **Filtering:** Quickly filter queues by name to find specific entries.
- **Aladin Integration:** Preview object fields directly in Aladin for detailed analysis.
- **Coordinate Visualization:** View object coordinates and positions on an interactive map.

## Installation

Follow these steps to set up the application on your local machine:

### Prerequisites

- Python 3.8 or higher
- Git

### Steps

1. **Clone the Repository:**

    ```bash
    git clone https://github.com/kkotysz/qman-pyqt.git
    cd qman-pyqt
    ```

2. **Create a Virtual Environment (Optional but Recommended):**

    ```bash
    python -m venv venv
    source venv/bin/activate  # On Windows: venv\Scripts\activate
    ```

3. **Install the Required Dependencies:**

    ```bash
    pip install -r requirements.txt
    ```

## Usage

1. **Prepare the Required `ccdobs.lst` File:**

    Ensure that you have the `ccdobs.lst` file available, as it is necessary for the application to run.

2. **Run the Application:**

    ```bash
    python qman-pyqt.py <path_to_ccdobs.lst>
    ```

    Replace `<path_to_ccdobs.lst>` with the actual path to your `ccdobs.lst` file.

3. **Interact with the GUI:**

    Use the intuitive graphical interface to manage your queues, filter entries, and preview object details.

## Authors

- **Krzysztof Kotysz**  
  *Lead Developer*  
  [GitHub](https://github.com/kkotysz)

- **Przemysław Mikołajczyk**  
  *Developer*  
  [GitHub](https://github.com/astromiki)

## Contributing

Contributions are welcome! Whether you're fixing a bug, improving documentation, or suggesting new features, your help is greatly appreciated.

1. **Fork the Repository**

2. **Create a New Branch**

    ```bash
    git checkout -b feature/YourFeatureName
    ```

3. **Commit Your Changes**

    ```bash
    git commit -m "Add your detailed description"
    ```

4. **Push to the Branch**

    ```bash
    git push origin feature/YourFeatureName
    ```

5. **Open a Pull Request**

Please make sure to update tests as appropriate.

## License

This project is licensed under the [MIT License](LICENSE). You are free to use, modify, and distribute this software under the terms of the license.

---

&copy; 2024 Bialkow Observatory. All rights reserved.
