#!/usr/bin/env python
# -*- coding: utf-8 -*-
import pygraphviz as pgv
import time

max_parallel_tasks = 4
tasklist = []
target = 'end'

PRIO_LOW = 1
PRIO_NORMAL = 0.5
PRIO_HIGH = 0.1

def t1_func():
    time.sleep(1)
def t2_func():
    time.sleep(2)
def t3_func():
    time.sleep(2)
def t4_func():
    time.sleep(1)
def t5_func():
    time.sleep(1)
def t6_func():
    time.sleep(1)
def t7_func():
    time.sleep(4)
def t8_func():
    time.sleep(0.1)
def t9_func():
    time.sleep(9)
def t10_func():
    time.sleep(0.1)
def t11_func():
    time.sleep(6)
def t12_func():
    time.sleep(0.1)

class Taskgroup:
    def run(self, executor):
        print('not done yet')

class Task:
    def __init__(self, name, dep_list, depman_list, target_list, prio, func):
        self.name = name
        self.dep_list = dep_list
        self.target_list = target_list
        self.depman_list = depman_list
        self.prio = prio
        self.duration = 0

    def set_duration(self, duration):
        self.duration = duration

def print_graph(start, end):
    #print edges and nodes
    g = pgv.AGraph(directed=True, strict=False, splines=True)
    for t in tasklist:
        if len(t.depman_list) > 0:
            for d in t.depman_list:
                g.add_edge(d.name, t.name, style='dashed', dir='none', color='grey')
        if len(t.dep_list) > 0:
            for d in t.dep_list:
                g.add_edge(d.name, t.name, style='solid')
        else:
            g.add_node(t.name)

        #show duration if set
        if t.duration > 0:
            n = g.get_node(t.name)
            n.attr['xlabel']=str(t.duration) + 's'

    # mark prio
    for t in tasklist:
        if t.prio == PRIO_HIGH:
            n = g.get_node(t.name)
            n.attr['style'] = 'bold'
        if t.prio == PRIO_LOW:
            n = g.get_node(t.name)
            n.attr['style'] = 'dashed'

    eNode = g.get_node(end.name)
    eNode.attr['color'] = 'green'

    sNode = g.get_node(start.name)
    sNode.attr['color'] = 'red'

    #print(g.string())
    g.layout(prog='dot')
    g.draw("depend.png")

def addTask(task):
    tasklist.append(task)
    return task

t0 = addTask(Task("start", [] , [], ["auto"], PRIO_NORMAL, None))
t1 = addTask(Task("power", [t0] , [t0], [], PRIO_NORMAL, t1_func))
t2 = addTask(Task("prog", [t1], [] , [], PRIO_NORMAL, t2_func))
t12 = addTask(Task("check version", [t2], [t1], [], PRIO_NORMAL, t12_func))
t3 = addTask(Task("io1", [t12], [], [], PRIO_NORMAL, t3_func))
t4 = addTask(Task("io2", [t3], [t1, t12],  [], PRIO_NORMAL, t4_func))
t5 = addTask(Task("adc1", [t12], [], [], PRIO_HIGH, t5_func))
t6 = addTask(Task("adc2", [t5], [t1, t12], [], PRIO_LOW, t6_func))
t7 = addTask(Task("adc3", [t6], [t1, t12], [], PRIO_NORMAL, t7_func))
t9 = addTask(Task("calibrate", [t5], [], [], PRIO_NORMAL, t9_func))
t8 = addTask(Task("write", [t9, t7], [], [], PRIO_NORMAL, t8_func))
t11 = addTask(Task("user action", [t12], [], [], PRIO_HIGH, t11_func))
t10 = addTask(Task("end", [t4, t8, t11], [], ["end"], PRIO_NORMAL, t10_func))

t5.set_duration(1)
t9.set_duration(3)
t11.set_duration(6)

#start tassk
print('Starting ' + str(len(tasklist)) + ' tasks')

#search for target
for t in tasklist:
    if t.name == target:
        target_o = t
        break

#search for start
for t in tasklist:
    for i in t.target_list:
        if i == "auto":
            start_o = t
            break

print_graph(start_o, target_o)

#print(target_element_nr)
print('done')
