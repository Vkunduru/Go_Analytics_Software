from MonteCarlo import MonteCarloNode

def print_Tree(root):
    root.printNode()
    for i in range(root.next_moves.length):
        print_Tree(root.next_moves[i])

    print ")"


root = MonteCarloNode()

root.node_level = 0
root.move = 0
child1 = root.add_next_move(p_move=1)

print_Tree(root)
