import re
from subprocess import Popen, PIPE
import heapq

global kb
kb=set()

global next_move
next_move=set()

global rules
rules=set()
def prove(x,y):
    kb.difference({element for element in kb if f'({x},{y})' in element})
    a=1
    #Wumpus
    rules.add(f"S({x},{y-1})&S({x+1},{y})&S({x},{y+1})&S({x-1},{y})->W({x},{y}).")
    rules.add(f"S({x},{y-1})&S({x+1},{y})&S({x},{y+1})&S({x-1},{y})&MW({x},{y})->W({x},{y}).")
    #Maybe Wumpus
    rules.add(f"S({x},{y-1})|S({x+1},{y})|S({x},{y+1})|S({x-1},{y})->MW({x},{y}).")
    #Pit
    rules.add(f"B({x},{y-1})&B({x+1},{y})&B({x},{y+1})&B({x-1},{y})->P({x},{y}).")
    rules.add(f"B({x},{y-1})&B({x+1},{y})&B({x},{y+1})&B({x-1},{y})&MP({x},{y})->P({x},{y}).")
    #Maybe Pit
    rules.add(f"B({x},{y-1})|B({x+1},{y})|B({x},{y+1})|B({x-1},{y})->MP({x},{y}).")
    #Safe
    rules.add(f"W({x},{y})|P({x},{y})->-Safe({x},{y}).")
    rules.add(f"-MW({x},{y})&-MP({x},{y})->Safe({x},{y}).")

    f = open("prove.in","w")    
    f.write("formulas(sos).\n")
    for k in kb:
        f.write(k+"\n")
    f.write("end_of_list.\n")
    f.write("formulas(assumptions).\n")
    for r in rules:
        f.write(r+"\n")
    f.write("end_of_list.\n")
    f.write("formulas(goals).\n")
    f.write(f"MW({x},{y}).\n")
    f.write("end_of_list.")
    f.close()
    p = Popen(["./LADR-2009-11A/bin/prover9","-f","prove.in"],stdout=PIPE, stderr=PIPE)
    stdout=p.stdout.read()
    retW = re.search(re.compile(rb"PROOF"),stdout)
    if retW is not None:
        kb.add(f'MW({x},{y}).')
    else:
        kb.add(f'-MW({x},{y}).')

    
    f = open("prove.in","w")    
    f.write("formulas(sos).\n")
    for k in kb:
        f.write(k+"\n")
    f.write("end_of_list.\n")
    f.write("formulas(assumptions).\n")
    for r in rules:
        f.write(r+"\n")
    f.write("end_of_list.\n")
    f.write("formulas(goals).\n")
    f.write(f"MP({x},{y}).\n")
    f.write("end_of_list.")
    f.close()
    p = Popen(["./LADR-2009-11A/bin/prover9","-f","prove.in"],stdout=PIPE, stderr=PIPE)
    stdout=p.stdout.read()
    retP = re.search(re.compile(rb"PROOF"),stdout)
    if retP is not None:
        kb.add(f'MP({x},{y}).')
    else:
        kb.add(f'-MP({x},{y}).')

    
    f = open("prove.in","w")    
    f.write("formulas(sos).\n")
    for k in kb:
        f.write(k+"\n")
    f.write("end_of_list.\n")
    f.write("formulas(assumptions).\n")
    for r in rules:
        f.write(r+"\n")
    f.write("end_of_list.\n")
    f.write("formulas(goals).\n")
    f.write(f"Safe({x},{y}).\n")
    f.write("end_of_list.")
    f.close()
    p = Popen(["./LADR-2009-11A/bin/prover9","-f","prove.in"],stdout=PIPE, stderr=PIPE)
    stdout=p.stdout.read()
    ret = re.search(re.compile(rb"PROOF"),stdout)
    if ret is not None:
        kb.add(f'Safe({x},{y}).')
    else:
        kb.add(f'-Safe({x},{y}).')
    if f'MP({x},{y}).' in kb:
        if f'Safe({x},{y}).'in kb:
            kb.remove(f'Safe({x},{y}).')
            kb.add(f'-Safe({x},{y}).')

    if f'MW({x},{y}).' in kb:
        if f'Safe({x},{y}).'in kb:
            kb.remove(f'Safe({x},{y}).')
            kb.add(f'-Safe({x},{y}).')
    return a

def add_kb(map, agent):
    
    x,y = agent
    kb.difference({element for element in kb if f'({x},{y})' in element})
    objects=set(map[x][y].split(","))-{""}
    if "Breeze" in objects:
        kb.add(f'B({x},{y}).')
    else:
        kb.add(f"-B({x},{y}).")
    if "Smell" in objects:
        kb.add(f"S({x},{y}).")
    else:
        kb.add(f"-S({x},{y}).")
    if "Gold" in objects:
        kb.add(f"G({x},{y}).")
    else:
        kb.add(f"-G({x},{y}).")
    if "Pit" in objects:
        kb.add(f"P({x},{y}).")
    else:
        kb.add(f"-P({x},{y}).")
    if "Wumpus" in objects:
        kb.add(f"W({x},{y}).")
    else:
        kb.add(f"-W({x},{y}).")
    if "Wumpus" in objects or "Pit" in objects:
        kb.add(f"-Safe({x},{y}).")
    else:
        kb.add(f"Safe({x},{y}).")
    
def add_next_move(point,visited):
    x,y=point
    if x+1<len(visited):
        if not visited[x+1][y]:
            next_move.add((x+1,y))
    if y+1<len(visited[x]):
        if not visited[x][y+1]:
            next_move.add((x,y+1))
    if x-1>=0:
        if not visited[x-1][y]:
            next_move.add((x-1,y))

    if y-1>=0:
        if not visited[x][y-1]:
            next_move.add((x,y-1))




def pars(input_file):
    object_in_map = set(input_file.split("\n"))-{""}
    m = next(obj for obj in object_in_map if obj.startswith("M"))
    object_in_map = object_in_map -{m}
    x = int(m[1])
    y = int(m[2])

    map = []
    for i in range(y):
        map.append([""for j in range(x)])
    vistied = []
    for i in range(y):
        vistied.append([False for j in range(x)])

    a = next(obj for obj in object_in_map if obj.startswith("A"))
    object_in_map = object_in_map -{a}
    ax = int(a[1])-1
    ay = int(a[2])-1

    go = next(obj for obj in object_in_map if obj.startswith("GO"))
    object_in_map = object_in_map -{go}
    gox = int(go[2])-1
    goy = int(go[3])-1
    map[gox][goy] = map[gox][goy] + "Goal,"
    global exit_map
    exit_map=(gox,goy)
    g = next(obj for obj in object_in_map if obj.startswith("G"))
    object_in_map = object_in_map -{g}
    gx = int(g[1])-1
    gy = int(g[2])-1
    map[gx][gy] = map[gx][gy] + "Gold,"
    
    for obj in object_in_map:
        ox = int(obj[1])-1
        oy = int(obj[2])-1
        match obj[0]:
            case "B":
                map[ox][oy] = map[ox][oy] + "Breeze,"
            case "S":
                map[ox][oy] = map[ox][oy] + "Smell,"
            case "P":
                map[ox][oy] = map[ox][oy] + "Pit,"
            case "W":
                map[ox][oy] = map[ox][oy] + "Wumpus,"
        object_in_map = object_in_map-{obj}
    return (vistied,map,(ax,ay))
def print_map(visited, map):
    n = len(map)
    for i in range(n):
        for j in range(len(map[n-1-i])):
            if visited[n-1-i][j]:
                if map[n-1-i][j]=="":
                    print("x",end="\t")
                else:
                    print(map[n-1-i][j],end="\t")
            else:
                print("0",end="\t")
        print()

def find_route(start,orentation, cilj,visited_map):
    #Iskanje poti med dvema točkoma A*, BFS v preiskani jami(mapi)
    ret =0
    #Hevristika= Dx+Dy
    heap = []
    x,y =start
    match orentation:
        case "N":
            if x+1 <len(visited_map):
                if visited_map[x+1][y]:
                    heapq.heappush(heap,(1 + abs(cilj[0]-(x+1))+ abs(cilj[1]-y),(x+1,y),"N",1))
            if y-1 >=0:
                if visited_map[x][y-1]:
                    heapq.heappush(heap,(2 + abs(cilj[0]-x) + abs(cilj[1]-(y-1)),(x,y-1),"W",2))
            if x-1 >=0:
                if visited_map[x-1][y]:
                    heapq.heappush(heap,(3 + abs(cilj[0]-(x-1))+ abs(cilj[1]-y),(x-1,y),"S",3))
            if y+1 <len(visited_map[x]):
                if visited_map[x][y+1]:
                    heapq.heappush(heap,(4 + abs(cilj[0]-x)+1 + abs(cilj[1]-(y+1)),(x,y+1),"E",4))
            
        case "E":
            if x+1 <len(visited_map):
                if visited_map[x+1][y]:
                    heapq.heappush(heap,(2 + abs(cilj[0]-(x+1))+ abs(cilj[1]-y),(x+1,y),"N",2))
            if y-1 >=0:
                if visited_map[x][y-1]:
                    heapq.heappush(heap,(3 + abs(cilj[0]-x) + abs(cilj[1]-(y-1)),(x,y-1),"W",3))
            if x-1 >=0:
                if visited_map[x-1][y]:
                    heapq.heappush(heap,(4 + abs(cilj[0]-(x-1))+ abs(cilj[1]-y),(x-1,y),"S",4))
            if y+1 <len(visited_map[x]):
                if visited_map[x][y+1]:
                    heapq.heappush(heap,(1 + abs(cilj[0]-x)+1 + abs(cilj[1]-(y+1)),(x,y+1),"E",1))
        case "S":
            if x+1 <len(visited_map):
                if visited_map[x+1][y]:
                    heapq.heappush(heap,(3 + abs(cilj[0]-(x+1))+ abs(cilj[1]-y),(x+1,y),"N",3))
            if y-1 >=0:
                if visited_map[x][y-1]:
                    heapq.heappush(heap,(4 + abs(cilj[0]-x) + abs(cilj[1]-(y-1)),(x,y-1),"W",4))
            if x-1 >=0:
                if visited_map[x-1][y]:
                    heapq.heappush(heap,(1 + abs(cilj[0]-(x-1))+ abs(cilj[1]-y),(x-1,y),"S",1))
            if y+1 <len(visited_map[x]):
                if visited_map[x][y+1]:
                    heapq.heappush(heap,(2 + abs(cilj[0]-x)+1 + abs(cilj[1]-(y+1)),(x,y+1),"E",2))
        case "W":
            if x+1 <len(visited_map):
                if visited_map[x+1][y]:
                    heapq.heappush(heap,(4 + abs(cilj[0]-(x+1))+ abs(cilj[1]-y),(x+1,y),"N",4))
            if y-1 >=0:
                if visited_map[x][y-1]:
                    heapq.heappush(heap,(1 + abs(cilj[0]-x) + abs(cilj[1]-(y-1)),(x,y-1),"W",1))
            if x-1 >=0:
                if visited_map[x-1][y]:
                    heapq.heappush(heap,(2 + abs(cilj[0]-(x-1))+ abs(cilj[1]-y),(x-1,y),"S",2))
            if y+1 <len(visited_map[x]):
                if visited_map[x][y+1]:
                    heapq.heappush(heap,(3 + abs(cilj[0]-x)+ abs(cilj[1]-(y+1)),(x,y+1),"E",4))
        
    while len(heap) !=0:
        _,state,orentation,dist = heapq.heappop(heap)
        if state == cilj:
            return (dist,state,orentation)
        x,y=state
        match orentation:
            case "N":
                if x+1 <len(visited_map):
                    if visited_map[x+1][y]:
                        heapq.heappush(heap,(dist + 1 + abs(cilj[0]-(x+1))+ abs(cilj[1]-y),(x+1,y),"N",1))
                if y-1 >=0:
                    if visited_map[x][y-1]:
                        heapq.heappush(heap,(dist + 2 + abs(cilj[0]-x) + abs(cilj[1]-(y-1)),(x,y-1),"W",2))
                if x-1 >=0:
                    if visited_map[x-1][y]:
                        heapq.heappush(heap,(dist + 3 + abs(cilj[0]-(x-1))+ abs(cilj[1]-y),(x-1,y),"S",3))
                if y+1 <len(visited_map[x]):
                    if visited_map[x][y+1]:
                        heapq.heappush(heap,(dist + 4 + abs(cilj[0]-x)+1 + abs(cilj[1]-(y+1)),(x,y+1),"E",4))
                
            case "E":
                if x+1 <len(visited_map):
                    if visited_map[x+1][y]:
                        heapq.heappush(heap,(dist + 2 + abs(cilj[0]-(x+1))+ abs(cilj[1]-y),(x+1,y),"N",2))
                if y-1 >=0:
                    if visited_map[x][y-1]:
                        heapq.heappush(heap,(dist + 3 + abs(cilj[0]-x) + abs(cilj[1]-(y-1)),(x,y-1),"W",3))
                if x-1 >=0:
                    if visited_map[x-1][y]:
                        heapq.heappush(heap,(dist + 4 + abs(cilj[0]-(x-1))+ abs(cilj[1]-y),(x-1,y),"S",4))
                if y+1 <len(visited_map[x]):
                    if visited_map[x][y+1]:
                        heapq.heappush(heap,(dist + 1 + abs(cilj[0]-x)+1 + abs(cilj[1]-(y+1)),(x,y+1),"E",1))
            case "S":
                if x+1 <len(visited_map):
                    if visited_map[x+1][y]:
                        heapq.heappush(heap,(dist + 3 + abs(cilj[0]-(x+1))+ abs(cilj[1]-y),(x+1,y),"N",3))
                if y-1 >=0:
                    if visited_map[x][y-1]:
                        heapq.heappush(heap,(dist + 4 + abs(cilj[0]-x) + abs(cilj[1]-(y-1)),(x,y-1),"W",4))
                if x-1 >=0:
                    if visited_map[x-1][y]:
                        heapq.heappush(heap,(dist + 1 + abs(cilj[0]-(x-1))+ abs(cilj[1]-y),(x-1,y),"S",1))
                if y+1 <len(visited_map[x]):
                    if visited_map[x][y+1]:
                        heapq.heappush(heap,(dist + 2 + abs(cilj[0]-x)+1 + abs(cilj[1]-(y+1)),(x,y+1),"E",2))
            case "W":
                if x+1 <len(visited_map):
                    if visited_map[x+1][y]:
                        heapq.heappush(heap,(dist + 4 + abs(cilj[0]-(x+1))+ abs(cilj[1]-y),(x+1,y),"N",4))
                if y-1 >=0:
                    if visited_map[x][y-1]:
                        heapq.heappush(heap,(dist + 1 + abs(cilj[0]-x) + abs(cilj[1]-(y-1)),(x,y-1),"W",1))
                if x-1 >=0:
                    if visited_map[x-1][y]:
                        heapq.heappush(heap,(dist + 2 + abs(cilj[0]-(x-1))+ abs(cilj[1]-y),(x-1,y),"S",2))
                if y+1 <len(visited_map[x]):
                    if visited_map[x][y+1]:
                        heapq.heappush(heap,(dist + 3 + abs(cilj[0]-x)+ abs(cilj[1]-(y+1)),(x,y+1),"E",4))
    return None


def main():
    score =0
    file = open("svet_wumpusa3.txt","r").read(-1)
    visited_map, world_map, agent= pars(file)
    agent_facing="E"
    visited_map[agent[0]][agent[1]]= True
    add_next_move(agent,visited_map)
    add_kb(world_map,agent)
    gold = False
    if "Gold" in world_map[agent[0]][agent[1]]:
        score= score +1000
        gold=True
    while not gold:
        x,y=(-1,-1)
        i=0
        find=False
        for move in next_move:
            i = i+1
            x,y=move
            prove(x,y)
            if f"Safe({x},{y})." in kb:
                find=True
                break
            kb.difference({element for element in kb if f'({x},{y})' in element})

        if(x,y) != (-1,-1) and find:
            next_move.remove((x,y))
            visited_map[x][y]= True
            scr,agent,agent_facing=find_route(agent,agent_facing,(x,y),visited_map)
            score =score -scr*10
            print(f"Agent je na polj: ({x+1},{y+1})\n Pregledana mapa:")
            print_map(visited_map,world_map)
            add_next_move(agent,visited_map)
            add_kb(world_map,agent)
            print(f"Agent pozna: {kb}")
            
            if "Wumpus" in world_map[x][y]:
                print("Dead by Wumpus")
                print_map(visited_map,world_map)
                print(f"Score: {score}")
                print(f"Knowlage base: {kb}")
                print(f"Rules: {rules}")
                return -2
            if "Pit" in world_map[x][y]:
                print("Dead by Pit")
                print_map(visited_map,world_map)
                print(f"Score: {score}")
                print(f"Knowlage base: {kb}")
                print(f"Rules: {rules}")
                return -2
            if "Gold" in world_map[x][y]:
                score= score +1000
                gold=True                

        else:
            scr,agent,agent_facing=find_route(agent,agent_facing,(0,0),visited_map)
            score =score -scr*10
            print("No gold win")
            print_map(visited_map,world_map)
            print(f"Score: {score}")
            print(f"Knowlage base: {kb}")
            print(f"Rules: {rules}")
            return -1
    scr,agent,agent_facing=find_route(agent,agent_facing,(0,0),visited_map)
    score =score -scr*10
    print("Win")
    print_map(visited_map,world_map)
    print(f"Score: {score}")
    print(f"Knowlage base: {kb}")
    print(f"Rules: {rules}")

if __name__ == "__main__":
    main()
