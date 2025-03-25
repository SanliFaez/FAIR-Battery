"""
    ni6251.pi
    ---------
    Class for comunicating with the NI-6251 DAQ. It requires to have installed the DAQmx (provided by NI) and the pyDAQmx package (from pypy).
"""
import PyDAQmx as nidaq
import numpy as np
from PyDAQmx import *


class niDAQ():
    """Class for controlling a National Instruments NI-6251 DAQ.
    If using an expansion such as the SCC-68 it has to be properly configured through the NI-MAX software.
    """
    def __init__(self,device_number=1,model='6251',debug=0):
        self.read = int32()
        if debug == 1:
            print('Not implemented a debuggable version')
        else:
            self.adq = nidaq
        self.tasks = [] # Array to hold the tasks. Each element should be a dict
        self.deviceNumber = int(device_number)

    def addTask(self,task):
        """Adds a task to the list of tasks.
        task -- Dictionary containing name and TaskHandle of the task.
        """
        self.tasks.append(task)
        self.tasks[-1]['alive'] = 1
        return self.tasks.__len__()-1

    def getTask(self,number):
        """Retrieves the task based on the number.
        """
        number = int(number)
        return self.tasks[number]

    def acquire_analog(self,channel,points,accuracy,limits=(-10.0,10.0)):
        """Acquires an analog signal in the specified channel. The execution blocks the rest of the program.
        channel --  has to be defined as "Dev1/ai0", for example.
        points -- the total number of points to be acquired
        accuracy -- the time between acquisitions (in seconds)
        limits -- the limits of the expected values. A tuple of 2 values.
        Returns: numpy array of length points
        """
        taskAnalogNumber = self.addTask({'name':'TaskAnalog','TaskHandle':TaskHandle()})
        self.task_Analog = self.getTask(taskAnalogNumber)['TaskHandle']
        self.read = int32()
        points = int(points)
        data = np.zeros((points,), dtype=np.float64)
        channel = str.encode(channel)
        waiting_time = points*accuracy*1.05 # Adds a 5% waiting time in order to give enough time
        freq = 1/accuracy # Accuracy in seconds
        DAQmxCreateTask("",byref(self.task_Analog))
        DAQmxCreateAIVoltageChan(self.task_Analog,channel,"",DAQmx_Val_RSE,limits[0],limits[1],DAQmx_Val_Volts,None)
        DAQmxCfgSampClkTiming(self.task_Analog,"",freq,DAQmx_Val_Rising,DAQmx_Val_FiniteSamps,points)
        # DAQmx Start Code
        DAQmxStartTask(self.task_Analog)
        DAQmxReadAnalogF64(self.task_Analog,points,waiting_time,DAQmx_Val_GroupByChannel,data,points,byref(self.read),None)
        self.tasks[taskAnalogNumber]['alive'] = 0
        return data

    def analogSetup(self,taskNum,channel,points,accuracy,limits=(-10.0,10.0)):
        """Prepares the task for an analog measurement.
        taskNum -- the number of the task (an integer)
        channel --  has to be defined as 1 or as [1,2], for example, meaning ai1, ai2, etc.
        points -- the total number of points to be acquired
        accuracy -- the time between acquisitions (in seconds)
        limits -- the limits of the expected values. A tuple of 2 values.
        """
        taskAnalogNumber = self.addTask({'name':'TaskAnalog','TaskHandle':TaskHandle(taskNum)})
        self.task_Analog = self.getTask(taskAnalogNumber)['TaskHandle']
        points = int(points)
        dev = 'Dev%s'%self.deviceNumber
        if type(channel) != type([]):
            channel = [channel]
        channels = []
        for c in channel:
            newChannel = '%s/ai%s'%(dev,int(c))
            channels.append(newChannel)
        channels = ', '.join(channels)
        channels = str.encode(channels)
        freq = 1/accuracy # Accuracy in seconds
        DAQmxCreateTask("",byref(self.task_Analog))
        DAQmxCreateAIVoltageChan(self.task_Analog,channels,None,DAQmx_Val_RSE,limits[0],limits[1],DAQmx_Val_Volts,None)
        if points>0:
            DAQmxCfgSampClkTiming(self.task_Analog,"",freq,DAQmx_Val_Rising,,points)
        else:
            DAQmxCfgSampClkTiming(self.task_Analog,"",freq,DAQmx_Val_Rising,DAQmx_Val_ContSamps,points)
        return taskAnalogNumber

    def analogTrigger(self,taskNumber):
        """Triggers the analog measurement.
        """
        self.task_Analog = self.getTask(taskNumber)['TaskHandle']
        if type(self.task_Analog) != type(TaskHandle()):
            raise Exception('Triggering an analog measurement before defining it')
        else:
            # DAQmx Start Code
            DAQmxStartTask(self.task_Analog)

    def analogRead(self,taskNumber,points,waiting=1):
        """Reads a number of points from the analog task.
        Returns the total number of data points per channel acquired and a numpy array of length values*channels.
        """
        self.task_Analog = self.getTask(taskNumber)['TaskHandle']
        if type(self.task_Analog) != type(TaskHandle()):
            raise Exception('Reading an analog measurement before defining it')
        else:
            self.read = int32()
            points = int(points)
            if points>0:
                data = np.zeros((points,), dtype=np.float64)
                DAQmxReadAnalogF64(self.task_Analog,points,waiting,DAQmx_Val_GroupByChannel,data,points,byref(self.read),None)
            else:
                data = np.zeros((10000,), dtype=np.float64) # Defining a 10000 value that is completely arbitrary
                DAQmxReadAnalogF64(self.task_Analog,points,.2,DAQmx_Val_GroupByChannel,data,points,byref(self.read),None)
            values = self.read.value
            return values,data

    def clear(self,tasks):
        """Clears the specified task, releasing all the resources.
        task -- list of tasks to clear
        """
        if type(tasks) != type([]):
            tasks = [tasks]
        for task in tasks:
            self.adq.DAQmxClearTask(self.getTask(task)['TaskHandle'])

if __name__ == "__main__":
    import matplotlib.pyplot as plt
    from time import time, sleep
    adq = niDAQ()
    points = 10000
    accuracy = 0.001
    taskNu = adq.analogSetup(0,7,points,accuracy,limits=(-1.5,1.5))
    adq.analogTrigger(taskNu)
    t0=time()
    while time()-t0<points*accuracy/5:
        print('Waiting...\n')
        sleep(1)
    data = adq.analogRead(taskNu,-1) # Read all the points
    points = len(data)
    x = np.linspace(0,points*accuracy,points/10)
    plt.plot(x,data,'o')
    plt.show()
