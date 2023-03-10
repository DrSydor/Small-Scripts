'''
This script allows for running another Python script numerous times in 
Powershell with different input parameters. In the script below, the 
Flow Denoising Gaussian Denoising script (flowdenoising.py) is run 
multiple times to screen different sigma, l, and w values, and save 
the subsequent output each time.
'''

import subprocess

# Values to be screened
sigma = [1, 1.5, 2, 2.5]
l_values = [0, 1, 2, 4]
w_values = [3, 5, 9, 17]

for s in sigma:
    for l in l_values:
        for w in w_values:
            # Construct the command to run the script with the above variables as an argument
            output_filename = "s" + str(s) + "_l" + str(l) + "_w" + str(w) + ".tif"
            variables = " -i " + "Denoising_Test_Sample.tif" + " -o " + output_filename + " -s " + str(s) + " " + str(s) + " " + str(s) + " -l " + str(l) + " -w " + str(w)
            command = "python flowdenoising.py" + variables

            subprocess.run(command, shell = True) # Run the command; shell = True allows for multiple variables to be input at once.
