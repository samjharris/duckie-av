# CICS 503 Fall 2019 DuckieTown Group 4
#
# path_planner.py:
# plans paths using BFS.

from config import TURN_L, TURN_R, TURN_S

#graph key: node 1 = n01, node 2 = n02, etc. 
#           "R" = right turn at intersection
#           "L" = left turn at intersection
#           "S" = straight at intersection
graph = { "n01" : [["n04",TURN_L],["n12",TURN_S]], #e.g.: from n01, we can go
          "n02" : [["n04",TURN_R],["n08",TURN_S]],     # 'L' to get to n04 or
          "n03" : [["n12",TURN_L],["n08",TURN_R]],     # 'S' to get to n12
          "n04" : [["n07",TURN_L],["n11",TURN_R]],
          "n05" : [["n03",TURN_L],["n07",TURN_S]],
          "n06" : [["n03",TURN_R],["n11",TURN_S]],
          "n07" : [["n10",TURN_S],["n01",TURN_L]],
          "n08" : [["n10",TURN_L],["n06",TURN_R]],
          "n09" : [["n01",TURN_R],["n06",TURN_S]],
          "n10" : [["n02",TURN_L],["n05",TURN_S]],
          "n11" : [["n02",TURN_R],["n09",TURN_S]],
          "n12" : [["n05",TURN_L],["n09",TURN_R]]
        }

#function input_helper
#
# takes:
#  "nodes", in whatever form Grupen provides
# returns
#   a list of nodes in proper format (e.g. ["n01","n02"])
#
#just a simple function to parse our input
def input_helper(nodes):
    #Assumes input such as the string: "1 2 3"
    nodes_list = ["n{:0>2}".format(x) for x in nodes.split(" ")]

    # #Currently assumes input such as the string: "n01 n02 n03"
    # nodes_list = nodes.split(" ")
    if(len(nodes_list) < 2):
        print("You have already arrived at your destination. Try adding a longer path")
        exit()
    return nodes_list

#function fill_steps:
#
# takes:
#   start node nA, end node nB
# returns:
#   stack of steps from nA to nB
#
#this function takes two nodes and finds
#a path across adjacent nodes from nA to
#nB. The returned stack is in reverse order
def fill_steps(nA,nB):
    steps = []
    explored = []
    frontier = [[nA,"START"]]
    #Just a BFS, nothing fancy to see here...
    while(frontier):
        cur = frontier.pop(0)
        if cur[0] == nB:
            #we found out goal, follow parents backward to
            #construct the path! Note we are just worried
            #about nodes & are ignoring instructions for now.
            explored.append(cur)
            while cur[1] != "START":
                steps.append(cur[0])
                for elem in explored:
                    if cur[1] == elem[0]:
                        cur = elem
                        break
            return steps
        found = False
        for node in explored:
            if(cur[0] == node[0]):
                found = True
        if not found:
            explored.append(cur)
            for adjacent in graph[cur[0]]:
                frontier.append([adjacent[0], cur[0]])
    return steps

#function plan_path:
#
# takes:
#   list of nodes
# returns:
#   stack of instructions followed by a full path (of nodes to visit)
#
#this function takes a list, made up
#of some start node, some end node, and
#some number of intermediate nodes. This
#function constructs a path from start to
#end, including all of the intermediate nodes
#as well as some extra nodes to fill in gaps.
#each instruction is defined as a turn through
#an intersection.
def plan_path(nodes):
    #parse the input...
    nodes_list = input_helper(nodes)

    #fill in the gaps...
    full_nodes_list = [nodes_list[0]]
    for i in range(0,len(nodes_list)-1):
        steps = fill_steps(nodes_list[i],nodes_list[i+1])
        while(steps):
            full_nodes_list.append(steps.pop(-1))

    #now we have a list of adjacent nodes, so we
    #can simply traverse it to get discrete instructions.
    #we do this separate from fill_steps for simplicity.
    instructions = []
    for i in range(0,len(full_nodes_list)-1):
        for elem in graph[full_nodes_list[i]]:
            if(elem[0] == full_nodes_list[i+1]):
                step = elem[1]
        instructions.append(step)

    return instructions, full_nodes_list

if __name__ == "__main__":
    # sample test paths:
    # path_string = "1 2 3"
    # path_string = "8 1 6 5 12 11 1 3 8"
    path_string = "10 12"

    p = ["n{:0>2}".format(int(x)) for x in path_string.split()]
    stack = plan_path(p)
    for elem in stack:
        print(elem," ")
