import os
import pwd

ROOT_PATH = os.path.realpath(os.path.join(os.path.dirname(__file__), '..'))
START = f"CSV data viewer session for user: {pwd.getpwuid(os.getuid())[0]}"
VERSION = "1.0.0"
