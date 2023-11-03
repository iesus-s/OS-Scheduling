# This is a sample Python script.
import pandas as pd

# Press the green button in the gutter to run the script.
if __name__ == '__main__':

    # Reading Text File
    text_input = pd.read_csv("input1.txt", sep=" ", header=None)

    # Accessing Values from Text File
    number_tasks = text_input.loc[0].at[0]
    system_execution = text_input.loc[0].at[1]
    cpu_high = text_input.loc[0].at[2]
    cpu_high_mid = text_input.loc[0].at[3]
    cpu_low_mid = text_input.loc[0].at[4]
    cpu_low = text_input.loc[0].at[5]
    cpu_idle = text_input.loc[0].at[6]

    # For Testing
    """ 
    print(text_input)
    print("Number of Tasks: " + number_tasks)
    print("System Execution: " + system_execution.astype(str) + " sec")
    print("Active CPU Power @ 1188 MHz: " + cpu_high.astype(str))
    print("Active CPU Power @ 918 MHz: " + cpu_high_mid.astype(str))
    print("Active CPU Power @ 648 MHz: " + cpu_low_mid.astype(str))
    print("Active CPU Power @ 384 MHz: " + cpu_low.astype(str))
    print("Idle CPU Power @ Lowest Frequency: " + cpu_idle.astype(str))
    """