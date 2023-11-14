import pandas as pd
import sys
from sys import exit

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
        # Finding Earliest Deadline First at maximum CPU Frequency #
        row_count = len(text_input)
        table = []
        iterations = []
        it_flag = []
        edf_table = []
        ex_table = []
        current_execute = 0
        temp_table = []
        total_energy = 0
        total_idle = 0
        total_execution = 0
        ex_time = 0
        index = 0
        index_check = 0
        index_prev = 3
        clock = 0
        state = 0
        duplicate = []
        if sys.argv[2] == "EDF":
            # Create EDF Table
            for i in range(row_count - 1):
                table.append(text_input.iloc[i + 1])
            for i in range(len(table)):
                edf_table.append(table[i][1])
            for i in range(len(table)):
                ex_table.append(table[i][2])
            for i in range(len(table)):
                iterations.append(1)
            for i in range(len(table)):
                temp_table.append(table[i][1])
            for i in range(len(table)):
                it_flag.append(1)

            # EDF Scheduler
            while clock < 1000:
                # Check for Earliest Deadline First
                min_table = []
                for i in edf_table:
                    min_table.append(i - clock)
                index = min_table.index(min(min_table))
                index_check = index
                print(clock+1, " ", end="")
                state = 0
                if sum(edf_table) == 50000:
                    print("IDLE", " ", end="")
                    print(i_cpu_idle, " ", end="")
                    state = 1
                else:
                    print(table[index][0], " ", end="")
                    print(i_cpu_high, " ", end="")

                # Executing
                ex_time = 0
                while index == index_check:
                    ex_time += 1

                    # Updates counters
                    edf_table[index] -= 1
                    if state == 0:
                        ex_table[index] -= 1
                    clock += 1

                    # Checks for Execution End & Updates Ex table
                    if ex_table[index] == 0:
                        it_flag[index] = 1
                        iterations[index] += 1
                        edf_table[index] = 10000
                        ex_table[index] = table[index][2]
                        index = 10

                    # Check for Task Arrival
                    if clock in temp_table:
                        # print("CLOCK------------------------------------", clock)
                        duplicate = []
                        for i, v in enumerate(temp_table):
                            if v == clock:
                                duplicate.append(i)
                        # print("DUP", duplicate)
                        if it_flag[temp_table.index(clock)] == 1:
                            hold = temp_table.index(clock)
                            if duplicate:
                                for k in duplicate:
                                    temp_table[k] = iterations[k] * table[k][1]
                                    edf_table[k] = temp_table[k]
                                    # ex_table[index] = table[index][2]
                                    it_flag[k] = 0
                                    index = 10
                                    # print("XXXXXXXXXXX")
                            else:
                                temp_table[hold] = iterations[hold] * table[hold][1]
                                edf_table[hold] = temp_table[hold]
                                # ex_table[index] = table[index][2]
                                it_flag[hold] = 0
                                index = 10

                if state == 1:
                    print(ex_time, " ", end="")
                    print(round(i_cpu_idle * ex_time * 0.001, 2), "J")
                    total_energy += round(i_cpu_idle * ex_time * 0.001, 2)
                    total_idle += ex_time
                else:
                    print(ex_time, " ", end="")
                    print(round(i_cpu_high * ex_time * 0.001, 2), "J")
                    total_energy += round(i_cpu_high * ex_time * 0.001, 2)
                    # print(edf_table)
                    # print("TEMP", temp_table)
                    # print(duplicate)
                    # print(iterations)
                    # print(it_flag)
            print("Total Energy Consumption: ", total_energy, "J")
            print("Percentage Time spent IDLE: ", total_idle, "seconds")
            print("Total Execution Time: ", clock, "seconds")

    if sys.argv[2] == "RM":
        # Finding Earliest Deadline First at maximum CPU Frequency #
        row_count = len(text_input)
        table = []
        iterations = []
        it_flag = []
        rm_table = []
        ex_table = []
        temp_table = []
        total_energy = 0
        total_idle = 0
        total_execution = 0
        ex_time = 0
        index = 0
        index_check = 0
        index_prev = 3
        clock = 0
        state = 0

        # Create EDF Table
        for i in range(row_count - 1):
            table.append(text_input.iloc[i + 1])
        for i in range(len(table)):
            rm_table.append(table[i][1])
        for i in range(len(table)):
            ex_table.append(table[i][2])
        for i in range(len(table)):
            iterations.append(1)
        for i in range(len(table)):
            temp_table.append(table[i][1])
        for i in range(len(table)):
            it_flag.append(1)

        # EDF Scheduler
        while clock < 1000:

            state = 0
            print(clock + 1, " ", end="")
            if sum(temp_table) == 50000:
                print("IDLE", " ", end="")
                print(i_cpu_idle, " ", end="")
                state = 1

            index = rm_table.index(min(rm_table))
            print(table[index][0], " ", end="")
            print(rm_table[0])
            exit()

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