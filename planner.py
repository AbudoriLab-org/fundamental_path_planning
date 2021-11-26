#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import matplotlib.pyplot as plt
import argparse
import queue

class Mapper():

    def __init__(self, start, goal):
        print("Initializing map...")
        self.width=10
        self.height=10
        self.obstacles=[[3,0,5],[6,4,9]]
        self.start=start
        self.goal=goal
        self.grid=[[0]*self.width for i in range(self.height)]
        self.visited=[[False]*self.width for i in range(self.height)]
        self.init_grid()
        self.prev=[[-100, -100]*self.width for i in range(self.height)]
        print("Start is {}".format(self.start))
        print("Goal is {}".format(self.goal))
    
    def init_grid(self):
        for i in range(10):
            for j in range(10):
                self.grid[i][j]=0
        for i in range(len(self.obstacles)):
            obs=self.obstacles[i]
            x=obs[0]
            y1=obs[1]
            y2=obs[2]
            for j in range(y1, y2+1):
                self.grid[x][j]=1

    def adj(self, v):
            x=v[0]
            y=v[1]
            result=[]
            for i in range(max(0, x-1), min(10, x+2)):
                for j in range(max(0, y-1), min(10, y+2)):
                    if self.grid[i][j]==0:
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

               
def obstacles_plot(map, ax):
    for i in range(len(map.obstacles)):
        tmp=map.obstacles[i]
        ax.axvspan(tmp[0], tmp[0]+1, float(tmp[1])/map.height, float(tmp[2]+1)/map.height, color = "black")
        ax.axvspan(tmp[0], tmp[0]+1, float(tmp[1])/map.height, float(tmp[2]+1)/map.height, color = "black")

        

def visit_plot(map, ax, u, plot_color):
    x=u[0]
    y=float(u[1])
    ax.axvspan(x, x+1, y/map.height, (y+1)/map.height, color = plot_color)
    plt.pause(0.01)

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





def width_first(map, ax):
    print("finding a path by width first search...")
    Q=queue.Queue()
    Q.put(map.start)
    visit_plot(map, ax, map.start, "blue")
    map.visited[map.start[0]][map.start[1]]=True
    goal_flag=False
    while not Q.empty():
        if goal_flag==True:
            break
        v=Q.get()
        adj_list=map.adj(v)
        for u in adj_list:
            if map.visited[u[0]][u[1]]==False:
                map.visited[u[0]][u[1]]=True
                visit_plot(map, ax, u, "blue")
                map.prev[u[0]][u[1]]=v
                if u==map.goal:
                    print("goal!")
                    goal_flag=True
                    path_plot(map, ax)
                    break

                Q.put(u)


def depth_first(map, ax):
    print("finding a path by depth first search...")
    S=[]
    S.append(map.start)
    while len(S)!=0:
        v=S.pop()
        if map.visited[v[0]][v[1]]==False:
            map.visited[v[0]][v[1]]=True
            visit_plot(map, ax, v, "blue")
            if v==map.goal:
                print("goal!")
                visit_plot(map, ax, v, "blue")
                path_plot(map, ax)
                break
            adj_list=map.adj(v)
            for u in adj_list:
                if map.visited[u[0]][u[1]]==False:
                    S.append(u)
                    map.prev[u[0]][u[1]]=v


def main():
    parser = argparse.ArgumentParser(description='Sample code of width-first and depth-first path planning on a grid map')
    parser.add_argument('-p', '--planner', default='width', type=str, choices=['width', 'depth'], help='width-first and depth-first')

    args=parser.parse_args()

    map = Mapper(start=[0,0], goal=[9,9])
    plt.figure(figsize=(7, 7))
    ax = plt.gca()

    map_plot(map, ax)

    if args.planner=='width':
        width_first(map, ax)
    if args.planner=='depth':
        depth_first(map, ax)
    else:
        pass

    plt.show()


if __name__=="__main__":
    main()