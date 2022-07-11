import subprocess
import os
from trace import Trace

record_csv_path = r"F:\pycharmProjects\Attendance\database\Records.csv"
subprocess.Popen([record_csv_path],shell=True)
