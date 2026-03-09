import numpy as np
import matplotlib.pyplot as plt
import heapq
import random

np.random.seed(42)
random.seed(42)

print("=" * 60)
print("ALGORITHM 1: A* (A-STAR) SEARCH ALGORITHM")

class Node:
    def __init__(self, position, parent=None):
        self.position = position
        self.parent = parent
        self.g = 0
        self.h = 0
        self.f = 0
    
    def __eq__(self, other):
        return self.position == other.position
    
    def __lt__(self, other):
        return self.f < other.f
    
    def __hash__(self):
        return hash(self.position)

def heuristic(a, b):
    return abs(a[0] - b[0]) + abs(a[1] - b[1])

def astar(grid, start, goal):
    rows, cols = len(grid), len(grid[0])
    
    if start == goal:
        return [start], 1
    
    if not (0 <= start[0] < rows and 0 <= start[1] < cols and grid[start[0]][start[1]] == 0):
        return None, 0
    if not (0 <= goal[0] < rows and 0 <= goal[1] < cols and grid[goal[0]][goal[1]] == 0):
        return None, 0
    
    open_list = []
    closed_set = set()
    
    start_node = Node(start)
    goal_node = Node(goal)
    
    heapq.heappush(open_list, (0, start_node))
    
    nodes_explored = 0
    
    while open_list:
        current_node = heapq.heappop(open_list)[1]
        nodes_explored += 1
        
        if current_node == goal_node:
            path = []
            current = current_node
            while current is not None:
                path.append(current.position)
                current = current.parent
            return path[::-1], nodes_explored
        
        closed_set.add(current_node.position)
        
        for dx, dy in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
            new_pos = (current_node.position[0] + dx, current_node.position[1] + dy)
            
            if (0 <= new_pos[0] < rows and 0 <= new_pos[1] < cols and 
                grid[new_pos[0]][new_pos[1]] == 0 and new_pos not in closed_set):
                
                neighbor = Node(new_pos, current_node)
                neighbor.g = current_node.g + 1
                neighbor.h = heuristic(new_pos, goal)
                neighbor.f = neighbor.g + neighbor.h
                
                in_open = False
                for _, node in open_list:
                    if node == neighbor and node.g <= neighbor.g:
                        in_open = True
                        break
                
                if not in_open:
                    heapq.heappush(open_list, (neighbor.f, neighbor))
    
    return None, nodes_explored

def visualize_astar(grid, path, start, goal, title, filename):
    plt.figure(figsize=(10, 8))
    
    grid_display = np.array(grid)
    plt.imshow(grid_display, cmap='binary', alpha=0.3)
    
    if path:
        path_x = [p[1] for p in path]
        path_y = [p[0] for p in path]
        plt.plot(path_x, path_y, 'b-', linewidth=3, label='A* Path')
        plt.scatter(path_x, path_y, c='blue', s=100, zorder=5)
    
    plt.scatter(start[1], start[0], c='green', s=300, marker='o', label='Start', edgecolors='black', zorder=6)
    plt.scatter(goal[1], goal[0], c='red', s=300, marker='X', label='Goal', edgecolors='black', zorder=6)
    
    plt.title(title, fontsize=14, fontweight='bold')
    plt.legend()
    plt.grid(True, alpha=0.3)
    plt.xticks(range(len(grid[0])))
    plt.yticks(range(len(grid)))
    
    plt.savefig(filename, dpi=150, bbox_inches='tight')
    plt.show()
    print(f"Saved: {filename}")

print("\n" + "="*50)
print("EXAMPLE 1: Robot Navigation")
print("="*50)

warehouse_grid = [
    [0, 0, 0, 0, 1, 0, 0, 0, 0, 0],
    [0, 1, 1, 0, 1, 0, 1, 1, 1, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 1, 0],
    [0, 1, 0, 1, 1, 1, 1, 0, 1, 0],
    [0, 1, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 1, 1, 1, 1, 0, 1, 1, 1, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [1, 1, 1, 0, 1, 1, 1, 0, 1, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 1, 0],
    [0, 1, 1, 1, 1, 1, 1, 0, 0, 0]
]

start1 = (0, 0)
goal1 = (9, 9)

path1, explored1 = astar(warehouse_grid, start1, goal1)
print(f"Path found: {len(path1)} steps")
print(f"Nodes explored: {explored1}")

visualize_astar(warehouse_grid, path1, start1, goal1, 
                "A* Algorithm - Example 1: Robot Navigation", 
                "astar_example1.png")

tree = {
    'A': [('B', 1), ('C', 3)],
    'B': [('A', 1), ('D', 3), ('E', 1)],
    'C': [('A', 3), ('F', 2)],
    'D': [('B', 3), ('G', 2)],
    'E': [('B', 1), ('G', 1), ('H', 4)],
    'F': [('C', 2), ('I', 3)],
    'G': [('D', 2), ('E', 1), ('J', 2)],
    'H': [('E', 4), ('J', 2)],
    'I': [('F', 3), ('K', 2)],
    'J': [('G', 2), ('H', 2), ('K', 3)],
    'K': [('I', 2), ('J', 3)]
}

h = {'A': 5, 'B': 4, 'C': 4, 'D': 3, 'E': 2, 'F': 3, 'G': 2, 'H': 2, 'I': 2, 'J': 1, 'K': 0}

def astar_tree(start, goal):
    open_list = []
    closed_set = set()
    
    start_node = Node(start)
    heapq.heappush(open_list, (0, start_node))
    
    nodes_explored = 0
    
    while open_list:
        current_node = heapq.heappop(open_list)[1]
        nodes_explored += 1
        
        if current_node.position == goal:
            path = []
            current = current_node
            while current is not None:
                path.append(current.position)
                current = current.parent
            return path[::-1], nodes_explored
        
        closed_set.add(current_node.position)
        
        for neighbor, cost in tree.get(current_node.position, []):
            if neighbor not in closed_set:
                neighbor_node = Node(neighbor, current_node)
                neighbor_node.g = current_node.g + cost
                neighbor_node.h = h[neighbor]
                neighbor_node.f = neighbor_node.g + neighbor_node.h
                
                in_open = False
                for _, node in open_list:
                    if node.position == neighbor and node.g <= neighbor_node.g:
                        in_open = True
                        break
                
                if not in_open:
                    heapq.heappush(open_list, (neighbor_node.f, neighbor_node))
    
    return None, nodes_explored

def visualize_tree(path, title, filename):
    plt.figure(figsize=(12, 8))
    
    pos = {
        'A': (0, 3), 'B': (1, 4), 'C': (1, 2), 'D': (2, 5), 'E': (2, 3),
        'F': (2, 1), 'G': (3, 4), 'H': (3, 2), 'I': (4, 3), 'J': (4, 1), 'K': (5, 2)
    }
    
    for node, edges in tree.items():
        x1, y1 = pos[node]
        for neighbor, cost in edges:
            x2, y2 = pos[neighbor]
            plt.plot([x1, x2], [y1, y2], 'k-', linewidth=1, alpha=0.3)
    
    if path:
        for i in range(len(path) - 1):
            x1, y1 = pos[path[i]]
            x2, y2 = pos[path[i+1]]
            plt.plot([x1, x2], [y1, y2], 'b-', linewidth=4, alpha=0.8)
    
    for node, (x, y) in pos.items():
        color = 'green' if node == 'A' else ('red' if node == 'K' else ('blue' if path and node in path else 'lightblue'))
        plt.scatter(x, y, s=800, c=color, edgecolors='black', zorder=5)
        plt.annotate(f"{node}\n({h[node]})", (x, y), ha='center', va='center', fontsize=8, zorder=6)
    
    plt.title(title, fontsize=14, fontweight='bold')
    plt.xlim(-1, 7)
    plt.ylim(-1, 7)
    plt.axis('off')
    
    plt.savefig(filename, dpi=150, bbox_inches='tight')
    plt.show()
    print(f"Saved: {filename}")

print("\n" + "="*50)
print("EXAMPLE 2: Tree Search")
print("="*50)

start2 = 'A'
goal2 = 'K'

path2, explored2 = astar_tree(start2, goal2)
print(f"Path: {' -> '.join(path2)}")
print(f"Nodes explored: {explored2}")

visualize_tree(path2, "A* Algorithm - Example 2: Tree Search", "astar_example2.png")
