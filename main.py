import random
import xlwt
import time

# virtual machine request simulation: (id, start time, end time, capacity, weight)
# use random number to generate some virtual machine request
def creat_vir_request():
    vir_machine_requests = []
    for i in range(0, 100, 1):
        start = random.randint(0, 99)
        end = random.randint(start + 1, 100)
        capacity = random.randint(1, 100)
        weight = capacity * (end - start)
        vir_machine_requests.append([i, start, end, capacity, weight])
    return vir_machine_requests


# physical machine simulation
def creat_pm():
    PM = []
    for i in range(0, 101, 1):
        PM.append(100)
    return PM


# used to check the total available storage for each physical machine
def storage_leak(list):
    storage = []
    # loop for each physical machine
    for i in range(0, len(list), 1):
        storage.append([])
        # add all available storage together for each physical machine, then add the value to storage list
        storage_value = 0
        for o in range(0, len(list[i]), 1):
            storage_value = storage_value + list[i][o]
        storage[i] = storage_value
    return storage


# used to get total weight for each physical machine
def physical_weight(list):
    weight = []
    # loop for each physical machine
    for i in range(0, len(list), 1):
        weight.append([])

        # add all request weight allocated to this physical machine, then add the weight to weight list
        weight_value = 0
        for o in range(0, len(list[i]), 1):
            weight_value = weight_value + list[i][o][4]
        weight[i] = weight_value
    return weight


# tian sort algorithm
# sort the requests in non-increasing order
# efficient algorithm
def first_algorithm(request_list):
    a = sorted(request_list, key=lambda request: (request[4], request[1] - request[2]), reverse=True)
    return algorithm_common_part(a)


# this algorithm sort request list according to the start time
# greedy algorithm for minimize the number of machines
def second_algorithm(request_list):
    a = sorted(request_list, key=lambda request: request[1])
    # print(a)
    return algorithm_common_part(a)


# this algorithm sort request list according to the end time
# self defined algorithm, idea from Earliest Finish Time (EFT) algorithm
def third_algorithm(request_list):
    a = sorted(request_list, key=lambda request: request[2])
    return algorithm_common_part(a)


def algorithm_common_part(requests):
    # PM is physical machine list,
    # PM_alloc is the list used to store which request is allocated to which physical machine
    PM = []
    PM_alloc = []

    pm_num = 1
    PM.append(creat_pm())
    PM_alloc.append([])
    # loop for virtual machine request to check for each request
    for i in range(0, len(requests), 1):
        check = 0

        # loop for physical machine list to find a physical machine to deal with the request
        for pm in range(0, pm_num, 1):
            # check whether this physical machine can deal with this request
            for p in range(requests[i][1], requests[i][2] + 1, 1):
                # if this physical machine can not deal with the request, then let 'check' variable be '1'
                if PM[pm][p] < requests[i][3]:
                    check = 1
                    break
            # if the physical machine can deal with the request, then allocate the request to this physical machine
            # and loop next virtual machine request
            if check == 0:
                for p in range(requests[i][1], requests[i][2] + 1, 1):
                    PM[pm][p] = PM[pm][p] - requests[i][3]
                PM_alloc[pm].append(requests[i])
                break
            # if this physical machine cannot deal with the request
            # and this physical machine is not the last machine in the list,
            # then loop to next physical machine
            if check == 1 and pm != pm_num - 1:
                check = 0
                continue

        # check will be '1' only if all the physical machine cannot deal with the request,
        # then the following code will add a new physical machine in the physical machine list
        # and allocate the request to the new physical machine
        if check == 1:
            PM.append(creat_pm())
            PM_alloc.append([])
            pm_num = pm_num + 1

            # assign the virtual machine request to this physical machine
            for p in range(requests[i][1], requests[i][2] + 1, 1):
                PM[pm_num - 1][p] = PM[pm_num - 1][p] - requests[i][3]
            PM_alloc[pm_num - 1].append(requests[i])
    return PM_alloc, pm_num, PM


if __name__ == '__main__':
    workbook = xlwt.Workbook()
    worksheet = workbook.add_sheet('third year data')
    worksheet.write(0, 0, 'running time')
    worksheet.write(1, 0, 'self algorithm')
    worksheet.write(1, 2, 'greedy algorithm')
    worksheet.write(1, 4, 'effective algorithm')

    worksheet.write(0, 6, 'number of physical machine')
    worksheet.write(1, 6, 'self algorithm')
    worksheet.write(1, 8, 'greedy algorithm')
    worksheet.write(1, 10, 'effective algorithm')

    worksheet.write(0, 12, 'average weights for first five physical machines')
    worksheet.write(1, 12, 'self algorithm')
    worksheet.write(1, 14, 'greedy algorithm')
    worksheet.write(1, 16, 'effective algorithm')

    worksheet.write(0, 18, 'amount of memory not been allocated for all physical machine')
    worksheet.write(1, 18, 'self algorithm')
    worksheet.write(1, 20, 'greedy algorithm')
    worksheet.write(1, 22, 'effective algorithm')

    for i in range(0, 100, 1):
        vir_machine_requests = creat_vir_request()
        start_time_1 = time.time() * 1000
        b1, c1, d1 = first_algorithm(vir_machine_requests)
        end_time_1 = time.time() * 1000

        start_time_2 = time.time() * 1000
        b2, c2, d2 = second_algorithm(vir_machine_requests)
        end_time_2 = time.time() * 1000

        start_time_3 = time.time() * 1000
        b3, c3, d3 = third_algorithm(vir_machine_requests)
        end_time_3 = time.time() * 1000

        x1 = physical_weight(b1)
        x2 = physical_weight(b2)
        x3 = physical_weight(b3)
        x1_1 = (x1[0] + x1[1] + x1[2] + x1[3] + x1[4]) / 5
        x2_2 = (x2[0] + x2[1] + x2[2] + x2[3] + x2[4]) / 5
        x3_3 = (x3[0] + x3[1] + x3[2] + x3[3] + x3[4]) / 5

        z1 = storage_leak(d1)
        z2 = storage_leak(d2)
        z3 = storage_leak(d3)
        a1 = sorted(z1)
        a2 = sorted(z2)
        a3 = sorted(z3)
        memory1 = (a1[0] + a1[1] + a1[2] + a1[3] + a1[4]) / 5
        memory2 = (a2[0] + a2[1] + a2[2] + a2[3] + a2[4]) / 5
        memory3 = (a3[0] + a3[1] + a3[2] + a3[3] + a3[4]) / 5

        # running time part
        run_1 = (end_time_1 - start_time_1)
        run_2 = (end_time_2 - start_time_2)
        run_3 = (end_time_3 - start_time_3)
        worksheet.write(i+2, 0, str(run_3) + 'ms')
        worksheet.write(i+2, 2, str(run_2) + 'ms')
        worksheet.write(i+2, 4, str(run_1) + 'ms')

        # number of physical machine
        worksheet.write(i+2, 6, c3)
        worksheet.write(i+2, 8, c2)
        worksheet.write(i+2, 10, c1)

        # average weights for first five physical machines
        worksheet.write(i+2, 12, x3_3)
        worksheet.write(i+2, 14, x2_2)
        worksheet.write(i+2, 16, x1_1)

        # the average of the smallest five amount of memory not been allocated for all physical machine
        worksheet.write(i+2, 18, memory3)
        worksheet.write(i+2, 20, memory2)
        worksheet.write(i+2, 22, memory1)

    workbook.save('third_year_data.xls')
