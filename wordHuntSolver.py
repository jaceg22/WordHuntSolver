import tkinter as tk
'''
#remove all words with >16 letters
file_path='words.txt'
with open(file_path, 'r') as file:
    words=file.readlines()
filtered_words=[word for word in words if len(word.strip())<17]
with open(file_path, 'w') as file:
    file.writelines(filtered_words)
print("Filtered words have been written to", file_path)
'''
def load_words(file_path):
    with open(file_path, 'r') as file:
        words=set(line.strip() for line in file if 1<=len(line.strip())<=16)
    return words

class Node:
    def __init__(self, value):
        self.value=value
        self.top=None
        self.bottom=None
        self.left=None
        self.right=None
        self.top_left=None
        self.top_right=None
        self.bottom_left=None
        self.bottom_right=None

def create_grid_linked_list(grid):
    rows=len(grid)
    cols=len(grid[0])
    nodes=[[Node(grid[r][c]) for c in range(cols)] for r in range(rows)]
    for r in range(rows):
        for c in range(cols):
            if r>0:
                nodes[r][c].top=nodes[r-1][c]
                if c>0:
                    nodes[r][c].top_left=nodes[r-1][c-1]
                if c<cols-1:
                    nodes[r][c].top_right=nodes[r-1][c+1]
            if r<rows-1:
                nodes[r][c].bottom=nodes[r+1][c]
                if c>0:
                    nodes[r][c].bottom_left=nodes[r+1][c-1]
                if c<cols-1:
                    nodes[r][c].bottom_right=nodes[r+1][c+1]
            if c>0:
                nodes[r][c].left=nodes[r][c-1]
            if c<cols-1:
                nodes[r][c].right=nodes[r][c+1]
    return nodes

def dfs(node, current_word, visited, results, words, max_length):
    if len(current_word)>max_length:
        return
    if len(current_word)>=3 and current_word in words:
        results.add(current_word)
    visited.add(node)
    for neighbor in [node.top, node.bottom, node.left, node.right, node.top_left, node.top_right, node.bottom_left, node.bottom_right]:
        if neighbor and neighbor not in visited:
            dfs(neighbor, current_word+neighbor.value, visited, results, words, max_length)
    visited.remove(node)

def find_all_words(grid, words):
    results=set()
    for row in grid:
        for node in row:
            dfs(node, node.value, set(), results, words, 16)
    return results

def show_organized(linked_grid, words, guess_text):
    found_words=find_all_words(linked_grid, words)
    organized_words={i: [] for i in range(16, 2, -1)}
    for word in found_words:
        word_length=len(word)
        if 3<=word_length<=16:
            organized_words[word_length].append(word)
    guess_text.delete("1.0", tk.END)
    for length in range(16, 2, -1):
        if organized_words[length]:
            guess_text.insert(tk.END, f"{length}: ({', '.join(organized_words[length])})\n")

def button(guess_entries, guess_text):
    words=load_words('words.txt')
    grid=[
    [entry.get() for entry in guess_entries[0:4]],
    [entry.get() for entry in guess_entries[4:8]],
    [entry.get() for entry in guess_entries[8:12]],
    [entry.get() for entry in guess_entries[12:16]]
    ]
    linked_grid=create_grid_linked_list(grid)
    show_organized(linked_grid, words, guess_text)
    
def go_next_guess_entry(event, entries, current_index):
    if len(entries[current_index].get())==1:
        if current_index+1<len(entries):
            entries[current_index+1].focus()

def clear(guess_entries, guess_text):
    for entry in guess_entries:
        entry.delete(0, tk.END)
    guess_text.delete("1.0", tk.END) 
    guess_entries[0].focus()

def wordHuntSolver():
    root=tk.Tk()
    root.geometry("1500x900")
    root.title("Word Hunt Solver")

    guess_entries=[]
    entry_vars=[]
    positions = [(600, 100), (660, 100), (720, 100), (780, 100),
                 (600, 160), (660, 160), (720, 160), (780, 160),
                 (600, 220), (660, 220), (720, 220), (780, 220),
                 (600, 280), (660, 280), (720, 280), (780, 280)]
    
    for i, (x, y) in enumerate(positions):
        entry_var=tk.StringVar()
        entry_var.trace_add("write", lambda *args: entry_var.set(entry_var.get()[:1]))
        entry=tk.Entry(root, font=("Helvetica", 30), textvariable=entry_var, width=2)
        entry.place(x=x, y=y)
        entry.bind("<KeyRelease>", lambda event, idx=i: go_next_guess_entry(event, guess_entries, idx))
        guess_entries.append(entry)
        entry_vars.append(entry_var)
    
    guess_text=tk.Text(root, wrap=tk.WORD, font=("Helvetica", 20))
    guess_text.place(width=1100, height=400, x=300, y=440)
    enter_button=tk.Button(root, text="Enter", command=lambda: button(guess_entries, guess_text))
    enter_button.place(width=100, height=50, x=600, y=340)
    clear_button=tk.Button(root, text="Clear", command=lambda: clear(guess_entries, guess_text))
    clear_button.place(width=100, height=50, x=725, y=340)
    root.mainloop()

wordHuntSolver()
