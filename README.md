# qupath_2_haloai
Script to transfer qupath annotation to haloai annotation directly. 


# Requirements

---
Tested with Python 3.7.10

Requires:
1. Python 
2. pip

And the following additional python package:
1. argparse

2. paquo.project

3. os

4. xml.dom
 
Since argparse/os/xml.dom are standard libraries already installed, you only need to install paquo library by using:

```
pip3 install paquo
```

### Run

Go to the github repository. Download or simply git-cloned, using the following typical command line for running the script like.

```python
 python3 qupath_2_haloai_using_paquo.py {The directory containing the qupath project files.} {The directory for the output annotation files.} {The category for the primitive (e.g. tubule/cortex)}.
```

