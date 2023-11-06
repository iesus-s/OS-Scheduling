import pandas as pd
import sys

# Press the green button in the gutter to run the script.
if __name__ == '__main__':

    # Reading Text File
    text_file = sys.argv[1]
    text_input = pd.read_csv(text_file, sep=" ", header=None)

    i_cpu_high = 1188
    i_cpu_mid_high = 918
    i_cpu_mid_low = 648
    i_cpu_low = 384
    i_cpu_idle = 84
    clock = 0
    # Accessing Values from Text File
    number_tasks = text_input.loc[0].at[0]
    system_execution = text_input.loc[0].at[1]
    cpu_high = text_input.loc[0].at[2]
    cpu_high_mid = text_input.loc[0].at[3]
    cpu_low_mid = text_input.loc[0].at[4]
    cpu_low = text_input.loc[0].at[5]
    cpu_idle = text_input.loc[0].at[6]
    cpu_values = [cpu_high, cpu_high_mid, cpu_low_mid, cpu_low, cpu_idle]

    if len(sys.argv) == 3:
        # Finding Earliest Deadline at maximum CPU Frequency #
        row_count = len(text_input)
        table = []
        min_table = []
        total_energy = [0, 0, 0, 0, 0]
        if sys.argv[2] == "EDF":
            for i in range(row_count-1):
                table.append(text_input.iloc[i+1])

            for i in range(len(table)):
                min_table = sorted(table, key=lambda x: x[1])

            # EDF Scheduler
            clock = 1
            print("Earliest Deadline at Maximum CPU Frequency: ")
            # Getting Total Energy Used and Total Execution
            for i in range(len(min_table)):
                total_energy[i] = cpu_high * min_table[i][2] * 0.001
            # Printing Schedule Results
            for i in range(len(min_table)):
                print(clock, min_table[i][0], i_cpu_high, min_table[i][2],
                      total_energy[i], "J")
                # Keeping track of the clock
                clock += min_table[i][2]

        print("Total Energy Consumption: ", sum(total_energy), "J")
        print("Percentage Time spent IDLE: 0 seconds")
        print("Total Execution Time: ", clock-1, "seconds")

    if len(sys.argv) == 4:
        # Finding Earliest Deadline and Energy Efficiency #
        row_count = len(text_input)
        table = []
        min_table = []
        total_energy = [0, 0, 0, 0, 0]
        if sys.argv[2] == "EDF" and sys.argv[3] == "EE":
            for i in range(row_count-1):
                table.append(text_input.iloc[i+1])

            for i in range(len(table)):
                min_table = sorted(table, key=lambda x: x[1])

            # EDF Scheduler with EE
            for i in range(len(table)-1):
                clock = 1
                print("Earliest Deadline at Maximum CPU Frequency: ")
                # Getting Total Energy Used and Total Execution
                for j in range(len(min_table)):
                    total_energy[j] = cpu_values[i] * min_table[j][2+i] * 0.001
                # Printing Schedule Results
                for k in range(len(min_table)):
                    print(k + clock, min_table[k][0], min_table[k][2+i],
                          total_energy[k], "J")
                    # Keeping track of the clock
                    clock += min_table[k][2+i]-1
                print("Total Energy Consumption: ", sum(total_energy), "J")

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

