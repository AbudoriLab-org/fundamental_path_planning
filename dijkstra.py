# Copyright 2021 Abudori Lab.
#
#    Licensed under the Apache License, Version 2.0 (the "License");
#    you may not use this file except in compliance with the License.
#    You may obtain a copy of the License at
#
#        http://www.apache.org/licenses/LICENSE-2.0
#
#    Unless required by applicable law or agreed to in writing, software
#    distributed under the License is distributed on an "AS IS" BASIS,
#    WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#    See the License for the specific language governing permissions and
#    limitations under the License.
#


#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import heapq
import matplotlib.pyplot as plt
import argparse
import queue
import random
random.seed(3)
import heapq
import numpy as np

class Mapper():

    def __init__(self, start, goal):
        print("Initializing map...")
        self.width=10
        self.height=10
        self.obstacles=[[3,0,5],[6,4,9]]
        self.start=start
        self.goal=goal
        self.grid=[[0]*self.width for i in range(self.height)]
        self.visited=np.array([[False]*self.width for i in range(self.height)])
        self.distance=np.array([[1000]*self.width for i in range(self.height)])
        self.init_grid()
        self.prev=[[-100, -100]*self.width for i in range(self.height)]
        print("Start is {}".format(self.start))
        print("Goal is {}".format(self.goal))
    
    def init_grid(self):
        for i in range(self.height):
            for j in range(self.width):
                if (i==0 and j==0) or (i==9 and j==9):
                    self.grid[i][j]=0
                else:
                    self.grid[i][j]=random.randint(1, 9)
        for i in range(len(self.obstacles)):
            obs=self.obstacles[i]
            x=obs[0]
            y1=obs[1]
            y2=obs[2]
            for j in range(y1, y2+1):
                self.grid[x][j]=100

    def adj(self, v):
            x=v[0]
            y=v[1]
            result=[]
            for i in range(max(0, x-1), min(10, x+2)):
                for j in range(max(0, y-1), min(10, y+2)):
                    if self.grid[i][j]!=100:
                        if (not (i==x and j==y)) and (abs(x+y-i-j)==1):
                            result.append([i, j])
            return result

def map_plot(map, ax):
    string_plot(ax, map.start, 'START')
    string_plot(ax, map.goal, 'GOAL')

    for i in range(map.width):
        ax.plot([i, i], [0, map.height], color='black', linewidth=1)

    for i in range(map.height):
        ax.plot([0, map.width], [i, i], color='black', linewidth=1)

    ax.set_xlim(0, map.width)
    ax.set_ylim(0, map.height)
    ax.tick_params(axis='both', which='both', bottom='off', top='off',
                    labelbottom='off', right='off', left='off', labelleft='off')

    obstacles_plot(map, ax)

    for i in range(map.height):
        for j in range(map.width):
                if map.grid[i][j]!=100:
                    ax.axvspan(i, i+1, j/map.height, (j+1)/map.height, color="green", alpha=map.grid[i][j]/10.0)





               
def obstacles_plot(map, ax):
    for i in range(len(map.obstacles)):
        tmp=map.obstacles[i]
        ax.axvspan(tmp[0], tmp[0]+1, float(tmp[1])/map.height, float(tmp[2]+1)/map.height, color = "black")
        ax.axvspan(tmp[0], tmp[0]+1, float(tmp[1])/map.height, float(tmp[2]+1)/map.height, color = "black")

        

def visit_plot(map, ax, u, plot_color):
    x=u[0]
    y=float(u[1])
    ax.axvspan(x, x+1, y/map.height, (y+1)/map.height, color = plot_color)
    plt.pause(0.05)

def path_plot(map, ax):
    print("Plotting path...")
    v=map.goal
    while v!=map.start:
        visit_plot(map, ax, v, "red")
        dif_x=v[0]-map.prev[v[0]][v[1]][0]
        dif_y=v[1]-map.prev[v[0]][v[1]][1]
        dif_vec=[dif_x, dif_y]
        if dif_vec==[0,1]:
            string_plot(ax, map.prev[v[0]][v[1]], "↑")
        elif dif_vec==[1,0]:
            string_plot(ax, map.prev[v[0]][v[1]], "→")
        elif dif_vec==[0,-1]:
            string_plot(ax, map.prev[v[0]][v[1]], "↓")
        elif dif_vec==[-1,0]:
            string_plot(ax, map.prev[v[0]][v[1]], "←")
        else:
            pass
        v=map.prev[v[0]][v[1]]


    visit_plot(map, ax, map.start, "red")

def string_plot(ax, v, plot_string):
    if plot_string=='START':
        plt.text(v[0]+0.5, v[1]+0.7, plot_string, ha='center')
    else:
        plt.text(v[0]+0.5, v[1]+0.4, plot_string, ha='center')


def dijkstra(map, ax):
    print("finding a path by dijkstra search...")

    map.distance[map.start[0]][map.start[1]]=0
    
    while np.all(map.visited)!=True:

        min_dst=np.min(map.distance[np.where(map.visited==False)])
        arg_list=np.where(map.distance==min_dst)
        
        for i in range(len(arg_list[0])):
            if map.visited[arg_list[0][i]][arg_list[1][i]]==False:
                v=[arg_list[0][i], arg_list[1][i]]
                break
            else:
                pass

        
        if v==map.goal:
            print("goal!, the total distance is {}.".format(min_dst))
            path_plot(map, ax)
            break

        if map.visited[v[0]][v[1]]==False:
            map.visited[v[0]][v[1]]=True
            visit_plot(map, ax, v, "blue")
            adj_list=map.adj(v)
            for u in adj_list:
                if map.distance[u[0]][u[1]]>map.distance[v[0]][v[1]]+map.grid[u[0]][u[1]]:
                    map.distance[u[0]][u[1]]=map.distance[v[0]][v[1]]+map.grid[u[0]][u[1]]
                    map.prev[u[0]][u[1]]=v
        else:
            pass






def main():
    map = Mapper(start=[0,0], goal=[9,9])
    plt.figure(figsize=(7, 7))
    ax = plt.gca()

    map_plot(map, ax)

    plt.savefig("map.png", format="png", dpi=300)

    dijkstra(map, ax)

    plt.savefig("path.png", format="png", dpi=300)

    plt.show()


if __name__=="__main__":
    main()