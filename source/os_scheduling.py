# This is a sample Python script.
import pandas as pd

# Press the green button in the gutter to run the script.
if __name__ == '__main__':

    # Reading Text File
    text_input = pd.read_csv("input1.txt", sep=" ", header=None)

    i_cpu_high = 1188
    i_cpu_mid_high = 918
    i_cpu_mid_low = 648
    i_cpu_low = 384
    i_cpu_idle = "IDLE"

    # Accessing Values from Text File
    number_tasks = text_input.loc[0].at[0]
    system_execution = text_input.loc[0].at[1]
    cpu_high = text_input.loc[0].at[2]
    cpu_high_mid = text_input.loc[0].at[3]
    cpu_low_mid = text_input.loc[0].at[4]
    cpu_low = text_input.loc[0].at[5]
    cpu_idle = text_input.loc[0].at[6]

    row_count = len(text_input)
    table = []
    min_table = []

    # Finding Earliest Deadline at maximum CPU Frequency #
    for i in range(row_count-1):
        table.append(text_input.iloc[i+1])

    for i in range(len(table)):
        min_table = sorted(table, key=lambda x: x[1])

    # print("Sorted: ", min_table)

    # Scheduler
    clock = 1
    for i in range(len(min_table)):
        print(i+clock, min_table[i][0], i_cpu_high, min_table[i][2],
              (cpu_high * min_table[i][1] * 0.001).astype(str)+"J")
        clock += min_table[i][2]-1

    # For Testing
    """
    print(text_input)
    print("Number of Tasks: " + number_tasks)
    print("System Execution: " + system_execution.astype(str) + " sec")
    print("Active CPU Power @ 1188 MHz: " + cpu_high.astype(str) + " mW")
    print("Active CPU Power @ 918 MHz: " + cpu_high_mid.astype(str) + " mW")
    print("Active CPU Power @ 648 MHz: " + cpu_low_mid.astype(str) + " mW")
    print("Active CPU Power @ 384 MHz: " + cpu_low.astype(str) + " mW")
    print("Idle CPU Power @ Lowest Frequency: " + cpu_idle.astype(str) + " mW")
    
    print(table)
    """

