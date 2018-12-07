import time
import sys


class Node:
    # Constructor with a key parameter creates the Node object.
    def __init__(self, key):
        self.key = key
        self.parent = None
        self.left = None
        self.right = None
        self.height = 0

    # Calculate the current nodes' balance factor,
    # defined as height(left subtree) - height(right subtree)
    def get_balance(self):
        # Get current height of left subtree, or -1 if None
        left_height = -1
        if self.left is not None:
            left_height = self.left.height

        # Get current height of right subtree, or -1 if None
        right_height = -1
        if self.right is not None:
            right_height = self.right.height

        # Calculate the balance factor.
        return left_height - right_height

    # Recalculate the current height of the subtree rooted at
    # the node, usually called after a subtree has been
    # modified.
    def update_height(self):
        # Get current height of left subtree, or -1 if None
        left_height = -1
        if self.left is not None:
            left_height = self.left.height

        # Get current height of right subtree, or -1 if None
        right_height = -1
        if self.right is not None:
            right_height = self.right.height

        # Assign self.height with calculated node height.
        self.height = max(left_height, right_height) + 1

    # Assign either the left or right data member with a new
    # child. The parameter which_child is expected to be the
    # string "left" or the string "right". Returns True if
    # the new child is successfully assigned to this node, False
    # otherwise.
    def set_child(self, which_child, child):
        # Ensure which_child is properly assigned.
        if which_child != "left" and which_child != "right":
            return False

        # Assign the left or right data member.
        if which_child == "left":
            self.left = child
        else:
            self.right = child

        # Assign the parent data member of the new child,
        # if the child is not None.
        if child is not None:
            child.parent = self

        # Update the node's height, since the subtree's structure
        # may have changed.
        self.update_height()
        return True

    # Replace a current child with a new child. Determines if
    # the current child is on the left or right, and calls
    # set_child() with the new node appropriately.
    # Returns True if the new child is assigned, False otherwise.
    def replace_child(self, current_child, new_child):
        if self.left is current_child:
            return self.set_child("left", new_child)
        elif self.right is current_child:
            return self.set_child("right", new_child)

        # If neither of the above cases applied, then the new child
        # could not be attached to this node.
        return False


class AVLTree:
    # Constructor to create an empty AVLTree. There is only
    # one data member, the tree's root Node, and it starts
    # out as None.
    def __init__(self):
        self.root = None

    # Performs a left rotation at the given node. Returns the
    # new root of the subtree.
    def rotate_left(self, node):
        # Define a convenience pointer to the right child of the
        # left child.
        right_left_child = node.right.left

        # Step 1 - the right child moves up to the node's position.
        # This detaches node from the tree, but it will be reattached
        # later.
        if node.parent is not None:
            node.parent.replace_child(node, node.right)
        else:  # node is root
            self.root = node.right
            self.root.parent = None

        # Step 2 - the node becomes the left child of what used
        # to be its right child, but is now its parent. This will
        # detach right_left_child from the tree.
        node.right.set_child('left', node)

        # Step 3 - reattach right_left_child as the right child of node.
        node.set_child('right', right_left_child)

        return node.parent

    # Performs a right rotation at the given node. Returns the
    # subtree's new root.
    def rotate_right(self, node):
        # Define a convenience pointer to the left child of the
        # right child.
        left_right_child = node.left.right

        # Step 1 - the left child moves up to the node's position.
        # This detaches node from the tree, but it will be reattached
        # later.
        if node.parent is not None:
            node.parent.replace_child(node, node.left)
        else:  # node is root
            self.root = node.left
            self.root.parent = None

        # Step 2 - the node becomes the right child of what used
        # to be its left child, but is now its parent. This will
        # detach left_right_child from the tree.
        node.left.set_child('right', node)

        # Step 3 - reattach left_right_child as the left child of node.
        node.set_child('left', left_right_child)

        return node.parent

    # Updates the given node's height and rebalances the subtree if
    # the balancing factor is now -2 or +2. Rebalancing is done by
    # performing a rotation. Returns the subtree's new root if
    # a rotation occurred, or the node if no rebalancing was required.
    def rebalance(self, node):

        # First update the height of this node.
        node.update_height()

        # Check for an imbalance.
        if node.get_balance() == -2:

            # The subtree is too big to the right.
            if node.right.get_balance() == 1:
                # Double rotation case. First do a right rotation
                # on the right child.
                self.rotate_right(node.right)

            # A left rotation will now make the subtree balanced.
            return self.rotate_left(node)

        elif node.get_balance() == 2:

            # The subtree is too big to the left
            if node.left.get_balance() == -1:
                # Double rotation case. First do a left rotation
                # on the left child.
                self.rotate_left(node.left)

            # A right rotation will now make the subtree balanced.
            return self.rotate_right(node)

        # No imbalance, so just return the original node.
        return node

    def insert(self, node):

        # Special case: if the tree is empty, just set the root to
        # the new node.
        if self.root is None:
            self.root = node
            node.parent = None

        else:
            # Step 1 - do a regular binary search tree insert.
            current_node = self.root
            while current_node is not None:
                # Choose to go left or right
                if node.key < current_node.key:
                    # Go left. If left child is None, insert the new
                    # node here.
                    if current_node.left is None:
                        current_node.left = node
                        node.parent = current_node
                        current_node = None
                    else:
                        # Go left and do the loop again.
                        current_node = current_node.left
                else:
                    # Go right. If the right child is None, insert the
                    # new node here.
                    if current_node.right is None:
                        current_node.right = node
                        node.parent = current_node
                        current_node = None
                    else:
                        # Go right and do the loop again.
                        current_node = current_node.right

            # Step 2 - Rebalance along a path from the new node's parent up
            # to the root.
            node = node.parent
            while node is not None:
                self.rebalance(node)
                node = node.parent


# RBTNode class - represents a node in a red-black tree
class RBTNode:
    def __init__(self, key, parent, is_red=False, left=None, right=None):
        self.key = key
        self.left = left
        self.right = right
        self.parent = parent

        if is_red:
            self.color = "red"
        else:
            self.color = "black"

    # Returns true if both child nodes are black. A child set to None is considered
    # to be black.
    def are_both_children_black(self):
        if self.left != None and self.left.is_red():
            return False
        if self.right != None and self.right.is_red():
            return False
        return True

    def count(self):
        count = 1
        if self.left != None:
            count = count + self.left.count()
        if self.right != None:
            count = count + self.right.count()
        return count

    # Returns the grandparent of this node
    def get_grandparent(self):
        if self.parent is None:
            return None
        return self.parent.parent

    # Gets this node's predecessor from the left child subtree
    # Precondition: This node's left child is not None
    def get_predecessor(self):
        node = self.left
        while node.right is not None:
            node = node.right
        return node

    # Returns this node's sibling, or None if this node does not have a sibling
    def get_sibling(self):
        if self.parent is not None:
            if self is self.parent.left:
                return self.parent.right
            return self.parent.left
        return None

    # Returns the uncle of this node
    def get_uncle(self):
        grandparent = self.get_grandparent()
        if grandparent is None:
            return None
        if grandparent.left is self.parent:
            return grandparent.right
        return grandparent.left

    # Returns True if this node is black, False otherwise
    def is_black(self):
        return self.color == "black"

    # Returns True if this node is red, False otherwise
    def is_red(self):
        return self.color == "red"

    # Replaces one of this node's children with a new child
    def replace_child(self, current_child, new_child):
        if self.left is current_child:
            return self.set_child("left", new_child)
        elif self.right is current_child:
            return self.set_child("right", new_child)
        return False

    # Sets either the left or right child of this node
    def set_child(self, which_child, child):
        if which_child != "left" and which_child != "right":
            return False

        if which_child == "left":
            self.left = child
        else:
            self.right = child

        if child != None:
            child.parent = self

        return True


class RedBlackTree:
    def __init__(self):
        self.root = None

    def __len__(self):
        if self.root is None:
            return 0
        return self.root.count()

    def insert(self, key):
        new_node = RBTNode(key, None, True, None, None)
        self.insert_node(new_node)

    def insert_node(self, node):
        # Begin with normal BST insertion
        if self.root is None:
            # Special case for root
            self.root = node
        else:
            current_node = self.root
            while current_node is not None:
                if node.key < current_node.key:
                    if current_node.left is None:
                        current_node.set_child("left", node)
                        break
                    else:
                        current_node = current_node.left
                else:
                    if current_node.right is None:
                        current_node.set_child("right", node)
                        break
                    else:
                        current_node = current_node.right

        # Color the node red
        node.color = "red"

        # Balance
        self.insertion_balance(node)

    def insertion_balance(self, node):
        # If node is the tree's root, then color node black and return
        if node.parent is None:
            node.color = "black"
            return

        # If parent is black, then return without any alterations
        if node.parent.is_black():
            return

        # References to parent, grandparent, and uncle are needed for remaining operations
        parent = node.parent
        grandparent = node.get_grandparent()
        uncle = node.get_uncle()

        # If parent and uncle are both red, then color parent and uncle black, color grandparent
        # red, recursively balance  grandparent, then return
        if uncle is not None and uncle.is_red():
            parent.color = uncle.color = "black"
            grandparent.color = "red"
            self.insertion_balance(grandparent)
            return

        # If node is parent's right child and parent is grandparent's left child, then rotate left
        # at parent, update node and parent to point to parent and grandparent, respectively
        if node is parent.right and parent is grandparent.left:
            self.rotate_left(parent)
            node = parent
            parent = node.parent
        # Else if node is parent's left child and parent is grandparent's right child, then rotate
        # right at parent, update node and parent to point to parent and grandparent, respectively
        elif node is parent.left and parent is grandparent.right:
            self.rotate_right(parent)
            node = parent
            parent = node.parent

        # Color parent black and grandparent red
        parent.color = "black"
        grandparent.color = "red"

        # If node is parent's left child, then rotate right at grandparent, otherwise rotate left
        # at grandparent
        if node is parent.left:
            self.rotate_right(grandparent)
        else:
            self.rotate_left(grandparent)

    def rotate_left(self, node):
        right_left_child = node.right.left
        if node.parent != None:
            node.parent.replace_child(node, node.right)
        else:  # node is root
            self.root = node.right
            self.root.parent = None
        node.right.set_child("left", node)
        node.set_child("right", right_left_child)

    def rotate_right(self, node):
        left_right_child = node.left.right
        if node.parent != None:
            node.parent.replace_child(node, node.left)
        else:  # node is root
            self.root = node.left
            self.root.parent = None
        node.left.set_child("right", node)
        node.set_child("left", left_right_child)


# This uses the words in a file to create an AVL Tree
def avl_tree_creator(file):
    file_ = open(file)
    print("Please wait. AVL Tree is being created.")
    start_time = time.time()
    tree = AVLTree()  # Creates AVL Tree
    for line in file_:
        node = Node(line.strip())  # .strip removes spaces before and after each word
        tree.insert(node)  # Nodes are inserted into AVL Tree
    print("AVL Tree was created in %s seconds" % (time.time() - start_time))
    return tree


# This uses the words in a file to create a red-black tree
def red_black_tree_creator(file):
    file_ = open(file)
    print("Please wait. Red-Black Tree is being created.")
    start_time = time.time()
    red_black_tree = RedBlackTree()  # Created red-black tree
    for line in file_:
        red_black_tree.insert(line.strip())  # .strip removes spaces before and after each word
    print("Red-Black Tree was created in %s seconds" % (time.time() - start_time))
    return red_black_tree


# This returns the number of anagrams a word has by breaking the word apart
# and finding different anagrams through the tree
def count_anagrams(tree, key, prefix=""):
    # Base case
    if len(key) <= 1:
        string = prefix + key

        # This looks through the tree to find a word
        is_in_tree = False
        current = tree.root
        while current is not None:
            if current.key.lower() == string.lower():
                is_in_tree = True
                current = None  # This ends while loop by setting root to None

            elif string.lower() < current.key.lower():
                current = current.left
            else:
                current = current.right

        if is_in_tree:
            return 1
        else:
            return 0
    else:
        # Implementation of print_anagrams method provided
        for i in range(len(key)):
            cur = key[i: i + 1]
            before = key[0: i]  # letters before cur
            after = key[i + 1:]  # letters after cur
            if cur not in before:  # Check if permutations of cur have not been generated.
                return 1 + count_anagrams(tree, before + after, prefix + cur)


# Function that returns the word in a file that contains the most anagrams
# The function's parameters are the file with the words to compare and the tree with all the english words
def most_anagrams(file, tree):
    # File to get words from to make anagrams and compare how many each have to get the max
    file_ = open(file)
    max_anagrams = 0
    max_anagrams_word = ""
    # Traverse through the file's words and count the anagrams in each word and find the word with
    # the largest number of anagrams
    for line in file_:
        count = count_anagrams(tree, line)
        if count > max_anagrams:
            max_anagrams = count
        max_anagrams_word = line
    return max_anagrams_word


# This will allow the user to choose which tree they want to use.
def user_option_data_structure():
    print("Hello, which data structure do you wish to use? (Enter corresponding digit)")
    print("1.) AVL Tree")
    print("2.) Red-Black Tree")
    print("3.) Exit")


# This will allow the user to choose what they want to do with the chosen data structure
def user_option_action():
    print()
    print("What would you like to do with this data structure? (Enter corresponding digit)")
    print("1.) Find the number of anagrams for a word")
    print("2.) Find the word with the most anagrams in the file")
    print("3.) Exit")


def main():
    user_option_data_structure()
    user_response = input()

    # Checks for erroneous user input
    while user_response.isdigit() is False or (
            int(user_response) != 1 and int(user_response) != 2 and int(user_response) != 3):
        if not user_response.isdigit():
            user_response = input("Sorry, please enter the single digit that corresponds to desired answer. \n")
        else:
            user_response = input("Sorry, that is not one of the available choices. \n")

    # If user picks 1, create an AVL tree
    if int(user_response) == 1:
        tree = avl_tree_creator("words.txt")

        user_option_action()
        user_response = input()

        # Checks for erroneous user input
        while user_response.isdigit() is False or (
                int(user_response) != 1 and int(user_response) != 2 and int(user_response) != 3):
            if not user_response.isdigit():
                user_response = input("Sorry, please enter the single digit that corresponds to desired answer. \n")
            else:
                user_response = input("Sorry, that is not one of the available choices. \n")

        # Keeps repeating until exit
        while int(user_response) != 3:
            # Search for number of anagrams of a word
            if int(user_response) == 1:
                print("Enter the word you want to use")
                word_answer = input()

                while word_answer.isdigit():
                    word_answer = input("Oops. Check your input and try again.")

                start_time = int(round(time.time() * 1000))
                anagrams = count_anagrams(tree, word_answer)
                print(word_answer + " has " + str(anagrams) + " anagrams")
                print("Running time for this: %s milliseconds " % (start_time - time.time()))
            # If user picks 2, ask for the name of the file
            elif int(user_response) == 2:
                print("Enter the name of the file you want to use.(Make sure to add '.txt' at the end)")
                word_answer = input()

                try:
                    return_word = most_anagrams(word_answer, tree)
                    print("The word with the most anagrams is: " + return_word)
                except FileNotFoundError:
                    print("Sorry, the file could not be found")
                    sys.exit("The program will now exit.")

            user_option_action()
            user_response = input()

            # Checks for erroneous user input
            while user_response.isdigit() is False or (
                    int(user_response) != 1 and int(user_response) != 2 and int(user_response) != 3):
                if not user_response.isdigit():
                    user_response = input("Sorry, please enter the single digit that corresponds to desired answer. \n")
                else:
                    user_response = input("Sorry, that is not one of the available choices. \n")
        sys.exit("Program will now exit.")

    # If 2 create a Red-Black tree
    elif int(user_response) == 2:
        tree = red_black_tree_creator("words.txt")

        user_option_action()
        user_response = input()

        # Checks for erroneous user input
        while user_response.isdigit() is False or (
                int(user_response) != 1 and int(user_response) != 2 and int(user_response) != 3):
            if not user_response.isdigit():
                user_response = input("Sorry, please enter the single digit that corresponds to desired answer. \n")
            else:
                user_response = input("Sorry, that is not one of the available choices. \n")

        # Repeats until user exits
        while int(user_response) != 3:
            # If 1 ask for the word to find number of anagrams for
            if int(user_response) == 1:
                print("Enter the word you want to use")
                word_answer = input()

                while word_answer.isdigit():
                    word_answer = input("Oops. Check your input and try again.")

                start_time = int(round(time.time() * 1000))
                anagrams = count_anagrams(tree, word_answer)
                print(word_answer + " has " + str(anagrams) + " anagrams")
                print("Running time for this: %s milliseconds " % (start_time - time.time()))
            # If 2 ask for the name of the file
            elif int(user_response) == 2:
                print("Enter the name of the file you want to use.(Make sure to add '.txt' at the end)")
                word_answer = input()

                try:
                    return_word = most_anagrams(word_answer, tree)
                    print("The word with the most anagrams is: " + return_word)
                except FileNotFoundError:
                    print("Sorry, the file could not be found")
                    sys.exit("The program will now exit")

            user_option_action()
            user_response = input()

            # Checks for erroneous user input
            while user_response.isdigit() is False or (
                    int(user_response) != 1 and int(user_response) != 2 and int(user_response) != 3):
                if not user_response.isdigit():
                    user_response = input("Sorry, please enter the single digit that corresponds to desired answer. \n")
                else:
                    user_response = input("Sorry, that is not one of the available choices. \n")

    # If 3 exit the program
    elif int(user_response) == 3:
        sys.exit("Thank you, program will now exit.")


main()
