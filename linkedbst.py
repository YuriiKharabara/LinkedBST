"""
File: linkedbst.py
Author: Ken Lambert
"""

from numpy import sort
from binary_search_tree.abstractcollection import AbstractCollection
from binary_search_tree.bstnode import BSTNode
from binary_search_tree.linkedstack import LinkedStack
from math import log
import time
import random
import sys
from tqdm import tqdm


class LinkedBST(AbstractCollection):
    """An link-based binary search tree implementation."""

    def __init__(self, sourceCollection=None):
        """Sets the initial state of self, which includes the
        contents of sourceCollection, if it's present."""
        self._root = None
        AbstractCollection.__init__(self, sourceCollection)

    # Accessor methods
    def __str__(self):
        """Returns a string representation with the tree rotated
        90 degrees counterclockwise."""

        def recurse(node, level):
            strng = ""
            if node != None:
                strng += recurse(node.right, level + 1)
                strng += "| " * level
                strng += str(node.data) + "\n"
                strng += recurse(node.left, level + 1)
            return strng

        return recurse(self._root, 0)

    def __iter__(self):
        """Supports a preorder traversal on a view of self."""
        if not self.isEmpty():
            stack = LinkedStack()
            stack.push(self._root)
            while not stack.isEmpty():
                node = stack.pop()
                yield node.data
                if node.right != None:
                    stack.push(node.right)
                if node.left != None:
                    stack.push(node.left)

    def preorder(self):
        """Supports a preorder traversal on a view of self."""
        return None

    def inorder(self):
        """Supports an inorder traversal on a view of self."""
        lyst = list()

        def recurse(node):
            if node != None:
                recurse(node.left)
                lyst.append(node.data)
                recurse(node.right)

        recurse(self._root)
        return iter(lyst)

    def postorder(self):
        """Supports a postorder traversal on a view of self."""
        return None

    def levelorder(self):
        """Supports a levelorder traversal on a view of self."""
        return None

    def __contains__(self, item):
        """Returns True if target is found or False otherwise."""
        return self.find(item) != None

    def find(self, item):
        """If item matches an item in self, returns the
        matched item, or None otherwise."""

        def recurse(node):
            if node is None:
                return None
            elif item == node.data:
                return node.data
            elif item < node.data:
                return recurse(node.left)
            else:
                return recurse(node.right)

        return recurse(self._root)

    # Mutator methods
    def clear(self):
        """Makes self become empty."""
        self._root = None
        self._size = 0

    def add(self, item):
        """Adds item to the tree."""

        # Helper function to search for item's position
        def recurse(node):
            # New item is less, go left until spot is found
            if item < node.data:
                if node.left == None:
                    node.left = BSTNode(item)
                else:
                    recurse(node.left)
            # New item is greater or equal,
            # go right until spot is found
            elif node.right == None:
                node.right = BSTNode(item)
            else:
                recurse(node.right)
                # End of recurse

        # Tree is empty, so new item goes at the root
        if self.isEmpty():
            self._root = BSTNode(item)
        # Otherwise, search for the item's spot
        else:
            recurse(self._root)
        self._size += 1

    def remove(self, item):
        """Precondition: item is in self.
        Raises: KeyError if item is not in self.
        postcondition: item is removed from self."""
        if not item in self:
            raise KeyError("Item not in tree.""")

        # Helper function to adjust placement of an item
        def lift_max_in_left_subtree_to_top(top):
            # Replace top's datum with the maximum datum in the left subtree
            # Pre:  top has a left child
            # Post: the maximum node in top's left subtree
            #       has been removed
            # Post: top.data = maximum value in top's left subtree
            parent = top
            current_node = top.left
            while not current_node.right == None:
                parent = current_node
                current_node = current_node.right
            top.data = current_node.data
            if parent == top:
                top.left = current_node.left
            else:
                parent.right = current_node.left

        # Begin main part of the method
        if self.isEmpty():
            return None

        # Attempt to locate the node containing the item
        item_removed = None
        pre_root = BSTNode(None)
        pre_root.left = self._root
        parent = pre_root
        direction = 'L'
        current_node = self._root
        while not current_node == None:
            if current_node.data == item:
                item_removed = current_node.data
                break
            parent = current_node
            if current_node.data > item:
                direction = 'L'
                current_node = current_node.left
            else:
                direction = 'R'
                current_node = current_node.right

        # Return None if the item is absent
        if item_removed == None:
            return None

        # The item is present, so remove its node

        # Case 1: The node has a left and a right child
        #         Replace the node's value with the maximum value in the
        #         left subtree
        #         Delete the maximium node in the left subtree
        if not current_node.left == None \
                and not current_node.right == None:
            lift_max_in_left_subtree_to_top(current_node)
        else:

            # Case 2: The node has no left child
            if current_node.left == None:
                new_child = current_node.right

                # Case 3: The node has no right child
            else:
                new_child = current_node.left

                # Case 2 & 3: Tie the parent to the new child
            if direction == 'L':
                parent.left = new_child
            else:
                parent.right = new_child

        # All cases: Reset the root (if it hasn't changed no harm done)
        #            Decrement the collection's size counter
        #            Return the item
        self._size -= 1
        if self.isEmpty():
            self._root = None
        else:
            self._root = pre_root.left
        return item_removed

    def replace(self, item, new_item):
        """
        If item is in self, replaces it with newItem and
        returns the old item, or returns None otherwise."""
        probe = self._root
        while probe != None:
            if probe.data == item:
                old_data = probe.data
                probe.data = new_item
                return old_data
            elif probe.data > item:
                probe = probe.left
            else:
                probe = probe.right
        return None

    def height(self):
        '''
        Return the height of tree
        :return: intif p.next is not None:
            return False
        return True
        '''
        def height1(top):
            '''
            Helper function
            :param top:
            :return:
            '''
            if top.left is None and top.right is None:
                return 0
            left_sum = 0
            right_sum = 0
            if top.left is not None:
                left_sum = height1(top.left)
            if top.right is not None:
                right_sum = height1(top.right)

            return max(left_sum, right_sum) + 1
        return height1(self._root)

    def is_balanced(self):
        '''
        Return True if tree is balanced
        :return:
        '''
        return self.height() < 2 * log(self._size + 1) - 1

    def range_find(self, low, high):
        '''
        Returns a list of the items in the tree, where low <= item <= high."""
        :param low:
        :param high:
        :return:
        '''
        lst = []
        for element in range(low, high + 1):
            if self.find(element):
                lst.append(element)
        return lst

    def rebalance(self):
        '''
        Rebalances the tree.
        :return:
        '''
        def rebalance1(elements):
            if len(elements) == 0:
                return None
            mid = len(elements)//2
            node = BSTNode(elements[mid])
            node.left = rebalance1(elements[:mid])
            node.right = rebalance1(elements[mid+1:])
            return node
        self._root = rebalance1(list(self.inorder()))

    def successor(self, item):
        """
        Returns the smallest item that is larger than
        item, or None if there is no such item.
        :param item:
        :type item:
        :return:
        :rtype:
        """
        smallest = None
        for i in self.inorder():
            if smallest is None and i > item:
                smallest = i
            elif smallest is not None and smallest > i > item:
                smallest = i
        return smallest

    def predecessor(self, item):
        """
        Returns the largest item that is smaller than
        item, or None if there is no such item.
        :param item:
        :type item:
        :return:
        :rtype:
        """
        biggest = None
        for i in self.inorder():
            if biggest is None and i < item:
                biggest = i
            elif biggest is not None and biggest < i < item:
                biggest = i
        return biggest

    def read_file(self, path):
        """Reads dictionary

        Args:
            path (str): path to dictionary

        Returns:
            list: dictionary in list
        """
        with open(path, 'r') as file:
            data = file.read()
        data = data.split('\n')
        return data[:-1]

    def find_in_list(self, lst, element):
        """finds word in list

        Args:
            lst (list): all dictionary
            element (str): element to find

        Returns:
            int: index of finded element
        """
        return lst.index(element)

    def find_in_sorted(self, sorted_tree, elemenent):
        """finds word in sorted tree

        Args:
            sorted_tree (LinkedBST): all dictionary
            element (str): element to find

        Returns:
            int: index of finded element
        """
        return sorted_tree.find(elemenent)

    def find_in_unsorted(self, unsorted_tree, element):
        """finds word in unsorted tree

        Args:
            sorted_tree (LinkedBST): all dictionary
            element (str): element to find

        Returns:
            int: index of finded element
        """
        return unsorted_tree.find(element)

    def find_in_balanced(self, balanced_tree, element):
        """finds word in balanced tree

        Args:
            sorted_tree (LinkedBST): all dictionary
            element (str): element to find

        Returns:
            int: index of finded element
        """
        return balanced_tree.find(element)

    def demo_bst(self, path):
        """
        Demonstration of efficiency binary search tree for the search tasks.
        :param path:
        :type path:
        :return:
        :rtype:
        """
        sys.setrecursionlimit(1000000)
        # Initialization
        data_lst = self.read_file(path)
        words_to_find = random.choices(data_lst, k=10000)
        # End init
        time_start = time.time()
        for i in tqdm(range(len(words_to_find))):
            self.find_in_list(data_lst, words_to_find[i])
        print(
            f'10000 random words finded in list with {len(data_lst)} words in\
 {time.time()-time_start} seconds.\n')

        sorted_tree = LinkedBST()
        # dictionary was decreased 'cause python is not able to do this with more than 21000 words
        for i in data_lst[:20000]:
            sorted_tree.add(i)
        words_to_find_in_sorted = random.choices(data_lst[:20000], k=10000)
        time_start = time.time()
        for i in tqdm(range(len(words_to_find_in_sorted))):
            self.find_in_sorted(sorted_tree, words_to_find_in_sorted[i])
        print(
            f'10000 random words finded in sorted tree with {len(data_lst[0:20000])} words\
 in {time.time()-time_start} seconds.\n')

        unsorted_tree = LinkedBST()
        unsorted = random.choices(data_lst, k=len(data_lst))
        for i in unsorted:
            unsorted_tree.add(i)
        time_start = time.time()
        for i in tqdm(range(len(words_to_find))):
            self.find_in_unsorted(unsorted_tree, words_to_find[i])
        print(
            f'10000 random words finded in unsorted tree with {len(data_lst)} words in\
 {time.time()-time_start} seconds.\n')

        unsorted_tree.rebalance()
        balanced_tree = unsorted_tree
        time_start = time.time()
        for i in tqdm(range(len(words_to_find))):
            self.find_in_balanced(balanced_tree, words_to_find[i])
        print(
            f'10000 random words finded in balanced tree with {len(data_lst)} words\
 in {time.time()-time_start} seconds.\n')


if __name__ == '__main__':
    tree = LinkedBST()
    tree.demo_bst('words.txt')
