# CSV data viewer
Is a python and pyqt5 based UI to visualise csv data.

[![Python 3.10](https://img.shields.io/badge/python-3.10.10-red.svg)](https://www.python.org/downloads/release/python-31010/)
![PyQt5](https://img.shields.io/badge/pyqt-5.15.7-blue.svg)

## Installation
### Cloning the Repository
1. Navigate to the directory that you would like to clone the repository, using similar command/s:
  -  ```cd <path_to_desired_directory>``` : to change working directory
2. Clone the remote repository and create a local copy on your machine, using similar command/s:
  - ```git clone https://github.com/littleGex/csv_data_viewer.git```
  - ```git clone git@github.com:littleGex/csv_data_viewer.git```

### Create environment using yaml (assuming conda)
```conda env create -f environment.yml```

## Usage
The ui expects a csv file to be provided upon starting as a commandline argument.
Example:

```
python csvTableTest.py <filename>
```

If no argument is provided, the user will be prompted to select a csv file upon UI starting.

If too many arguments are provided the UI will not open, quoting an error in the number of arguments provided.

One can also use the `start_csv_viewer.sh` shell script to launch the UI.  
The shell script attempts to activate the conda environment and run the UI with/without arguments.

```
start_csv_viewer.sh <filename>
```

## History
Refer to [changelog](changelog.md)