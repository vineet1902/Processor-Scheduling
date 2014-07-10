#!/usr/bin/python

import random
import matplotlib.pyplot as plt
#this function generates the random subtask slots in the gen_data.txt file
def generate_file(str_processorsNumF, taskNumF):
   # print "func0"
    gen_dataFile = open("gen_data.txt", "w")
    gen_dataFile.write(str_processorsNumF + "\n")                   #store number of processors and number of tasks in this file
    gen_dataFile.write(str(taskNumF) + "\n")
    count_subTaskF = 0
    while (count_subTaskF < taskNumF):                              #generate random numbers for each subtask representing time slots
        rand_num = random.randint(199,500)                          #and write into the file  #change                  
        gen_dataFile.write(str(rand_num) + "\n")
        count_subTaskF = count_subTaskF + 1
    gen_dataFile.close()

#this function reads the data from the gen_data.txt file
def read_gen_file(total_timeC):
    #print "func1"
    read_file = open("gen_data.txt", "r")
    sub_taskSlots = []
    sub_taskSum = 0                                                 #to store sum of all the time slots
    for val in read_file.read().split():
        sub_taskSlots.append(int(val))                              #read timeslots and store them into a list    
        sub_taskSum = sub_taskSum + int(val) 
    read_file.close()                                               
    i = 2
    newsub_taskSlots = [0]*len(sub_taskSlots)                       #store newly scaled list into a new list
    sub_taskSum = sub_taskSum - sub_taskSlots[0] - sub_taskSlots[1]     #remove first two values of the list as those are number of processors and tasks resp.
    while i < len(sub_taskSlots):
       newsub_taskSlots[i] = float(float(sub_taskSlots[i]*total_timeC)/float(sub_taskSum))     #scale down the time slots for each subtask
       i = i + 1
    return sub_taskSlots,newsub_taskSlots,total_timeC

#this function defines the round robin scheduling algorithm
def round_robin(newtask_Slots,task_Slots, total_timeR, processorsNum):
    cmp_tasks=[]
    for i in range(len(newtask_Slots)):
        cmp_tasks.append(0)
    j=0
    miss=0
    t=0
    for i in range(1,total_timeR/processorsNum+1):
        count=0
        queue = []
        while(count<processorsNum):
            if t==total_timeR:
                break
            if(newtask_Slots[j%len(newtask_Slots)]!=cmp_tasks[j%len(newtask_Slots)]):
                queue.append(j%len(newtask_Slots))
                count = count+1
                cmp_tasks[j%len(newtask_Slots)] = cmp_tasks[j%len(newtask_Slots)] +1
                j=j+1
                t = t+1
            else:
                j=j+1
        for q in range(len(newtask_Slots)):
            lag = ((newtask_Slots[q]*i*processorsNum)/total_timeR)-cmp_tasks[q]
            if int(lag)>=1:
                miss = miss + int(lag) 
        del queue[:]
    return miss


    
#this is the main function which takes in the input
if __name__ == '__main__':
    str_processorsNum = raw_input("Enter the number of processors: ")
    #str_taskNum = raw_input("Enter the number of tasks: ")
    file_name = 'gen_data.txt'
    taskNum = 10                         #change
    test = []
    simulation_time = 1000
    listt = []
    task = []
    repeat=0
    totalmiss=0
    total_time = 1000*int(str_processorsNum)
    while (taskNum < 101):
        totalmiss=0
        repeat=0
        while(repeat<20):
            generate_file(str_processorsNum, taskNum)
            old_subtask, subtask,time = read_gen_file(total_time)
            old1 = old_subtask[2:]
            new1 = subtask[2:]
            tt=0
            for i in old1:
                tt = tt + int(i)
            miss = round_robin(old1, new1,tt, int(str_processorsNum))
            totalmiss=totalmiss+miss
            repeat=repeat+1
        listt.append(totalmiss/20)
        task.append(taskNum)
        taskNum = taskNum + 10
        print "Number of misses: ",totalmiss/20        
    plt.plot(task,listt)
    plt.show()







        