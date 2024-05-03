import sys
sys.path.append(r"C:\Program Files (x86)\CST Studio Suite 2021\AMD64\python_cst_libraries")

import os
import cst.interface as ci
import cst.results as cr
import numpy as np

project_path = r"path-to-directory\design.cst"
out_dir = r'path-to-directory\name-of-the-output-file.csv'

def write_string_to_file(content, file_path):
    try:
        # Open the file in write mode
        mode = 'a' if os.path.exists(out_dir) else 'w'
        with open(file_path, mode) as file:
            # Write the content to the file
            file.write(content)
        
        print(f"Successfully wrote content to '{file_path}'")
    except IOError:
        print(f"Error: Unable to write content to '{file_path}'")

print("Setting up... (This might take a while)")
my_cst = ci.DesignEnvironment()    
active_instance = ci.DesignEnvironment.open_project(my_cst, project_path)

parameter_values = [
    {'param1': 50, 'param2': 40},
    {'param1': 52, 'param2': 45},
    {'param1': 53, 'param2': 41}
]

parameter_names = list(parameter_values[0].keys())

delete_results = 'Sub Main() \ndim objName as object \nset objName = Result1D("S−Parameters") \nDeleteAt("truemodelchange") \nEnd Sub()'
delete_sequence = 'Sub Main() \nParameterSweep.DeleteAllSequences() \nEnd Sub'            
solve = 'Sub Main () \nParameterSweep.Start \nEnd Sub'

for i in range(len(parameter_values)):
    print(f'Running simulation for index: {i}...')
    out_dir_exists = os.path.exists(out_dir)
    result_str = "" if out_dir_exists else 'Frequency,S(11),'+ ','.join(parameter_names)+ ",F11,F12,F21,F22,B.W1,B.W2" + '\r'
    change_param = 'Sub Main ()'

    for j in range(len(parameter_names)):
        key = parameter_names[j]
        value = parameter_values[i][key]
    
        change_param += '\nStoreParameter("' + key + '",' + str(value) + ')'
    
    change_param += '\nRebuildOnParametricChange(bfullRebuild, bShowErrorMsgBox) \nEnd Sub'
    
    active_instance.schematic.execute_vba_code(change_param, timeout=None)        
    
    active_instance.modeler.run_solver()
    
    project = cr.ProjectFile(project_path, allow_interactive=True)
    results = []

    try:
        results = project.get_3d().get_result_item(r"1D Results\S-Parameters\S1,1")
    except ValueError:
        print (f'Values at index {i} were skipped due to error in simulation')
        continue
        
    freqs = np.array(results.get_xdata())
    s_param_values = np.array(results.get_ydata())
    s_db = []
    
    dimensions = ','.join([str(val) for val in parameter_values[i].values()])
    f_bw = [0, 0, 0, 0]
    
    for k in range(len(s_param_values)):
        s_real = s_param_values[k].real
        s_imag = s_param_values[k].imag
        s = np.sqrt(s_real**2+s_imag**2)
        s_db_val = 20 * np.log10(s)
        
        s_real_next = 0 if k+1 == len(s_param_values) else s_param_values[k+1].real
        s_imag_next = 0 if k+1 == len(s_param_values) else s_param_values[k+1].imag
        s_next = np.sqrt(s_real_next**2+s_imag_next**2)
        s_db_val_next = 0 if k+1 == len(s_param_values) else 20 * np.log10(s_next)
        
        s_db.append(s_db_val)
        
        if s_db_val <= -10:
            if f_bw[0] == 0:
                f_bw[0] = freqs[k]
            elif f_bw[1] == 0 and s_db_val_next > -10:
                f_bw[1] = freqs[k]
            elif f_bw[2] == 0 and f_bw[1] != 0:
                f_bw[2] = freqs[k]
            elif f_bw[3] == 0 and s_db_val_next > -10:
                f_bw[3] = freqs[k]
    
    bw1 = f_bw[1] - f_bw[0]
    bw2 = f_bw[3] - f_bw[2]

    #Get results for each freq.point of interest from CST
    for k in range(len(s_param_values)):
        result_str += str(freqs[k]) + "," + str(s_db[k]) + "," + dimensions + "," + ",".join([str(val) for val in f_bw]) + "," + str(bw1) + "," + str(bw2) + "\r"
        
    # Return results
    print("Result: ", result_str)
    write_string_to_file(result_str, out_dir)
    print("=======================================================================================")