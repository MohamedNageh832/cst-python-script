# CST automation script

This a python script made to automate the simulation in CST studio suite

## Before you run the script

You need to make few changes to the `cst_script.py`

#### Update project directory

```python
project_path = r"path-to-directory\design.cst"
out_dir = r'path-to-directory\name-of-the-output-file.csv'
```

#### Update the parameters

```python
parameter_values = [
    {'param1': 50, 'param2': 40},
    {'param1': 52, 'param2': 45},
    {'param1': 53, 'param2': 41}
]
```

## Setup

1. Instal CST studio suite (2020 or 2021) version

2. install python 3.6

3. install spyder 4.1.5 (optional)

4. download the `"cst_script.py"` file

5. open the command prompt

6. Run this snippet to make sure you have the correct version of python `python --version`. It should output `Python 3.6.*`

   The `*` is to indicate that the exact number here doesn't really matter

7. Write ` Python <path-to-directory>\cst_script.py`
8. The script should run successfully, run the simulation and write the results to the output directory as a `csv` file

## Ouput example

```csv
Frequency,S(11),param1,param2,F11,F12,F21,F22,B.W1,B.W2
2.0007998943328857,-0.7026998650685952,50,40,2.2495999336242676,2.2992000579833984,0,0,0.04960012435913086,0
```

Feel free to edit the script as you like
