import pandas as pd
import sys

# Press the green button in the gutter to run the script.
if __name__ == '__main__':

    # Reading Text File
    text_file = sys.argv[1]
    text_input = pd.read_csv(text_file, sep=" ", header=None)

    i_cpu_high = 1188
    i_cpu_high_mid = 918
    i_cpu_low_mid = 648
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
    i_cpu_values = [i_cpu_high, i_cpu_high_mid, i_cpu_low_mid, i_cpu_low]

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
        windex = 10
        zoo = 0
        index_check = 0
        index_prev = 3
        clock = 1
        state = 0
        glock = 1
        duplicate = []
        ex_time = 0
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
            for clock in range(1000):
                clock += 1
                # Check for Earliest Deadline First
                min_table = []
                for i in edf_table:
                    min_table.append(i)

                index = min_table.index(min(min_table))
                index_check = index

                if windex == 10:
                    print(clock, " ", end="")
                    state = 0
                    if sum(edf_table) == 50000:
                        print("IDLE", " ", end="")
                        print(i_cpu_idle, " ", end="")
                        state = 1
                    else:
                        print(table[index][0], " ", end="")
                        print(i_cpu_high, " ", end="")
                    windex = 100

                # Updates counters
                # print("EDF TABLE ", edf_table)
                ex_time += 1
                if state == 0:
                    ex_table[index] -= 1
                    edf_table[index] -= 1

                # Checks for Execution End & Updates Ex table
                if ex_table[index] == 0:
                    it_flag[index] = 1
                    iterations[index] += 1
                    edf_table[index] = 10000
                    ex_table[index] = table[index][2]
                    windex = 10
                    # print("IT ", iterations)

                # Check for Task Arrival
                # print("CLOCK------------------------------------", clock)
                for z in temp_table:
                    if z == clock:
                        # print(temp_table)
                        # print(iterations)
                        # print("XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX", temp_table.index(clock))
                        ugh = temp_table.index(clock)
                        duplicate = []
                        for i, v in enumerate(temp_table):
                            if v == clock:
                                duplicate.append(i)
                        if duplicate:
                            for k in duplicate:
                                temp_table[k] = (iterations[k] * table[k][1])
                                edf_table[k] = temp_table[k]
                                # ex_table[index] = table[index][2]
                                it_flag[k] = 0
                        else:
                            temp_table[ugh] = (iterations[ugh] * table[ugh][1])
                            edf_table[ugh] = temp_table[ugh]
                            # ex_table[index] = table[index][2]
                            it_flag[ugh] = 0

                min_table = []
                for i in edf_table:
                    min_table.append(i)
                index = min_table.index(min(min_table))
                if index != index_check:
                    windex = 10

                if windex == 10:
                    if state == 1:
                        print(ex_time, " ", end="")
                        print(round(i_cpu_idle * ex_time * 0.001, 2), "J")
                        total_energy += round(i_cpu_idle * ex_time * 0.001, 2)
                        total_idle += ex_time
                    else:
                        print(ex_time, " ", end="")
                        print(round(i_cpu_high * ex_time * 0.001, 2), "J")
                        total_energy += round(i_cpu_high * ex_time * 0.001, 2)
                    ex_time = 0

                    # print("EDF TABLE ", edf_table)
                    # print("TEMP", temp_table)
                    # print(duplicate)
                    # print("IT ", iterations)
                    # print(it_flag)
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
            ex_table = []
            sorted_ex = []
            sorted_task = []
            task_list = ["w1", "w2", "w3", "w4", "w5"]
            next_deadline = [10000, 10000, 10000, 10000, 10000]

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

            cpu_time = 0
            clock_start = 0
            clock_end = 0
            clock_count = 0
            updated = 0
            idle_count = 0

            while clock < 1000:

                for x in range(len(sorted_rm)):
                    if temp_table[x] > 0:
                        cpu_time = temp_table[x]
                        clock_start = clock

                        while clock_count < cpu_time:

                            temp_table[x] -= 1
                            clock_count = clock_count + 1
                            clock = clock + 1

                            # Check for new deadlines
                            for j in range(len(sorted_rm)):
                                if clock == next_deadline[j]:
                                    temp_table[j] = sorted_ex[j]
                                    temp_table[x] = cpu_time - clock_count
                                    run_time = clock_count
                                    updated = 1

                            if updated == 1:
                                break
                        if temp_table[x] == 0:
                            iterations[x] += 1
                            next_deadline[x] = sorted_rm[x] * (iterations[x])

                        clock_end = clock - 1
                        clock_count = 0

                        if updated == 1:
                            print(clock_start, sorted_task[x], i_cpu_high, run_time,
                                  round(i_cpu_high * run_time * 0.001, 2), "J")
                            clock_start = clock_end
                            total_energy += round(i_cpu_high * run_time * 0.001, 2)

                        else:
                            print(clock_start, sorted_task[x], i_cpu_high, cpu_time,
                                  round(i_cpu_high * cpu_time * 0.001, 2), "J")
                            clock_start = clock_end
                            total_energy += round(i_cpu_high * cpu_time * 0.001, 2)

                    elif sum(temp_table) == 0:
                        # make idle clock
                        while sum(temp_table) == 0:
                            idle_count = idle_count + 1
                            # clock_start = clock
                            clock_end = clock - 1
                            clock = clock + 1

                            # Check for new deadlines
                            for j in range(len(sorted_rm)):
                                if clock == next_deadline[j]:
                                    temp_table[j] = sorted_ex[j]
                                    run_time = clock_count
                                    updated = 1

                        print(clock_start, "IDLE", "IDLE", idle_count,
                              round(i_cpu_idle * idle_count * 0.001, 2), "J")
                        clock_start = clock_end
                        total_energy += round(i_cpu_idle * idle_count * 0.001, 2)
                        total_idle = total_idle + idle_count
                        idle_count = 0

                    if updated == 1:
                        break

                updated = 0

            print("Total Energy Consumption: ", total_energy, "J")
            print("Percentage Time spent IDLE: ", total_idle, "seconds")
            print("Total Execution Time: ", clock, "seconds")

    if len(sys.argv) == 4:
        if sys.argv[2] == "EDF" and sys.argv[3] == "EE":
            for best_power in i_cpu_values:
                # Finding Earliest Deadline First at maximum CPU Frequency #
                cpu_execution = i_cpu_values.index(best_power)
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
                windex = 10
                zoo = 0
                index_check = 0
                index_prev = 3
                clock = 1
                state = 0
                glock = 1
                duplicate = []
                deadline_miss = []
                missed_tasks = []
                ex_time = 0
                # Create EDF Table
                for i in range(row_count - 1):
                    table.append(text_input.iloc[i + 1])
                for i in range(len(table)):
                    edf_table.append(table[i][1])
                for i in range(len(table)):
                    ex_table.append(table[i][cpu_execution + 2])
                for i in range(len(table)):
                    iterations.append(1)
                for i in range(len(table)):
                    temp_table.append(table[i][1])
                for i in range(len(table)):
                    it_flag.append(1)

                # EDF Scheduler
                for clock in range(1000):

                    clock += 1
                    # Check for Earliest Deadline First
                    min_table = []
                    for i in edf_table:
                        min_table.append(i)

                    index = min_table.index(min(min_table))
                    index_check = index

                    if windex == 10:
                        print(clock, " ", end="")
                        state = 0
                        if sum(edf_table) == 50000:
                            print("IDLE", " ", end="")
                            print(i_cpu_idle, " ", end="")
                            state = 1
                        else:
                            print(table[index][0], " ", end="")
                            print(best_power, " ", end="")
                        windex = 100

                    # Updates counters
                    # print("EDF TABLE ", edf_table)
                    ex_time += 1
                    if state == 0:
                        ex_table[index] -= 1
                        edf_table[index] -= 1

                    # Checks for Execution End & Updates Ex table
                    if ex_table[index] == 0:
                        it_flag[index] = 1
                        iterations[index] += 1
                        edf_table[index] = 10000
                        ex_table[index] = table[index][2]
                        windex = 10
                        # print("IT ", iterations)

                    # Check for Task Arrival
                    # print("CLOCK------------------------------------", clock)
                    for z in temp_table:
                        if z == clock:
                            # print(temp_table)
                            # print(iterations)
                            # print("XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX", temp_table.index(clock))
                            ugh = temp_table.index(clock)
                            duplicate = []
                            for i, v in enumerate(temp_table):
                                if v == clock:
                                    duplicate.append(i)
                            if duplicate:
                                for k in duplicate:
                                    temp_table[k] = (iterations[k] * table[k][1])
                                    edf_table[k] = temp_table[k]
                                    # ex_table[index] = table[index][2]
                                    it_flag[k] = 0
                            else:
                                temp_table[ugh] = (iterations[ugh] * table[ugh][1])
                                edf_table[ugh] = temp_table[ugh]
                                # ex_table[index] = table[index][2]
                                it_flag[ugh] = 0

                    min_table = []
                    for i in edf_table:
                        min_table.append(i)
                    index = min_table.index(min(min_table))
                    if index != index_check:
                        windex = 10

                    if windex == 10:
                        if state == 1:
                            print(ex_time, " ", end="")
                            print(round(i_cpu_idle * ex_time * 0.001, 2), "J")
                            total_energy += round(i_cpu_idle * ex_time * 0.001, 2)
                            total_idle += ex_time
                        else:
                            print(ex_time, " ", end="")
                            print(round(best_power * ex_time * 0.001, 2), "J")
                            total_energy += round(best_power * ex_time * 0.001, 2)
                        ex_time = 0
                print("Total Energy Consumption: ", total_energy, "J")
                print("Percentage Time spent IDLE: ", total_idle, "seconds")
                print("Total Execution Time: ", clock, "seconds")

        if sys.argv[2] == "RM" and sys.argv[3] == "EE":
            pick_cpu = []
            for best_power in i_cpu_values:
                cpu_execution = i_cpu_values.index(best_power)
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
                windex = 10
                zoo = 0
                index_check = 0
                index_prev = 3
                clock = 1
                state = 0
                glock = 1
                duplicate = []
                deadline_miss = []
                missed_tasks = []
                ex_time = 0
                utilization = []
                # Create EDF Table
                for i in range(row_count - 1):
                    table.append(text_input.iloc[i + 1])
                for i in range(len(table)):
                    edf_table.append(table[i][1])
                for i in range(len(table)):
                    ex_table.append(table[i][cpu_execution + 2])
                for i in range(len(table)):
                    iterations.append(1)
                for i in range(len(table)):
                    temp_table.append(table[i][1])
                for i in range(len(table)):
                    it_flag.append(1)

                for ex in ex_table:
                    utilization.append(ex / edf_table[ex_table.index(ex)])

                print("Utilization @", best_power, ":", sum(utilization))

                if sum(utilization) < 1:
                    pick_cpu.append(sum(utilization))

            print("Picked CPU :", max(pick_cpu))