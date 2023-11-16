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
##########################################################################################################
                    ## copy this code in rm

                    # Checks for Execution End & Updates Ex table
                    if ex_table[index] == 0:
                        it_flag[index] = 1
                        iterations[index] += 1
                        edf_table[index] = 10000
                        ex_table[index] = table[index][2]
                        index = 10

                    # Check for Task Arrival
                    if clock in temp_table:
                        if it_flag[temp_table.index(clock)] == 1:
                            hold = temp_table.index(clock)
                            temp_table[hold] = iterations[hold] * table[hold][1]
                            edf_table[hold] = temp_table[hold]
                            it_flag[hold] = 0
                            index = 10
##########################################################################################################
                if state == 1:
                    print(ex_time, " ", end="")
                    print(round(i_cpu_idle * ex_time * 0.001, 2), "J")
                    total_energy += round(i_cpu_idle * ex_time * 0.001, 2)
                    total_idle += ex_time
                else:
                    print(ex_table[index_check], " ", end="")
                    print(round(i_cpu_high * ex_table[index_check] * 0.001, 2), "J")
                    total_energy += round(i_cpu_high * ex_time * 0.001, 2)
            print("Total Energy Consumption: ", total_energy, "J")
            print("Percentage Time spent IDLE: ", total_idle, "seconds")
            print("Total Execution Time: ", clock, "seconds")


        if sys.argv[2] == "RM":
            # Find RM at maximum CPU Frequency #
            row_count = len(text_input)
            table = []
            iterations = []
            it_flag = []
            rm_table = []
            index_table = []
            temp_table = []
            total_energy = 0
            total_idle = 0
            total_execution = 0
            ex_time = 0
            index = 0
            index_check = 0
            index_prev = 3
            clock = 1
            state = 0
            sorted_ex =[]
            sorted_task =[]
            task_list =["w1", "w2", "w3", "w4", "w5"]
            next_deadline =[10000, 10000, 10000, 10000, 10000]


            # Create RM Table
            for i in range(row_count - 1):
                table.append(text_input.iloc[i + 1])
            for i in range(len(table)):
                rm_table.append(table[i][1])
            for i in range(len(table)):
                ex_table.append(table[i][2])
            for i in range(len(table)):
                iterations.append(0)
            for i in range(len(table)):
                it_flag.append(1)

            sorted_rm = sorted(rm_table)

            ## sort the execution times and make a temp_table of executions
            for m in range(len(sorted_rm)):
                for j in range(len(sorted_rm)):
                    if sorted_rm[m] == rm_table[j]:
                        index_table.append(j)
                        sorted_ex.append(ex_table[j])
                        temp_table.append(ex_table[j])
                        sorted_task.append(task_list[j])

            # print("after sorting")
            # print(sorted_rm)
            # print(index_table)
            # print(sorted_ex)
            # print(sorted_task)
            # print(temp_table)

##########################################################################################################
            cpu_time = 0;
            clock_start =0;
            clock_end =0;
            clock_count =0;
            updated = 0;
            idle_count = 0

            while clock < 1000:


                for x in range(len(sorted_rm)):
                    if temp_table[x] > 0:
                        cpu_time = temp_table[x]
                        clock_start = clock

                        while clock_count < cpu_time:

                            temp_table[x] -= 1
                            clock_count = clock_count + 1
                            clock = clock +1

                            ## Check for new deadlines
                            for j in range(len(sorted_rm)):
                                if clock == next_deadline[j]:
                                    temp_table[j] = sorted_ex[j]
                                    temp_table[x] = cpu_time - clock_count
                                    run_time = clock_count
                                    updated =1

                            if updated ==1:
                                break
                        if temp_table[x] ==0:
                            iterations[x] += 1
                            next_deadline[x] = sorted_rm[x] * (iterations[x])

                        clock_end = clock -1
                        clock_count = 0

                        if updated ==1:
                            print(clock_start, sorted_task[x], i_cpu_high, run_time, round(i_cpu_high * run_time * 0.001, 2), "J")
                            clock_start = clock_end
                            total_energy += round(i_cpu_high * run_time * 0.001, 2)

                        else :
                            print(clock_start, sorted_task[x], i_cpu_high, cpu_time,round(i_cpu_high * cpu_time * 0.001, 2), "J")
                            clock_start = clock_end
                            total_energy += round(i_cpu_high * cpu_time * 0.001, 2)

                    elif sum(temp_table) == 0 :

                        ## make idle clock
                        while sum(temp_table) == 0:

                            idle_count = idle_count+1
                            clock_end = clock -1

                            clock =clock +1

                            ## Check for new deadlines
                            for j in range(len(sorted_rm)):
                                if clock == next_deadline[j]:
                                    temp_table[j] = sorted_ex[j]
                                    run_time = clock_count
                                    updated = 1

                        print(clock_start, "IDLE", "IDLE", idle_count,
                              round(i_cpu_high * idle_count * 0.001, 2), "J")
                        clock_start = clock_end
                        total_energy += round(i_cpu_high * idle_count * 0.001, 2)
                        total_idle = total_idle + idle_count
                        idle_count =0;

                    if updated == 1:
                        break

                updated = 0

            print("Total Energy Consumption: ", total_energy, "J")
            print("Percentage Time spent IDLE: ", total_idle, "seconds")
            print("Total Execution Time: ", clock, "seconds")
##########################################################################################################


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