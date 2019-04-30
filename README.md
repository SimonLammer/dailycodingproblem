# [dailycodingproblem.com](https://dailycodingproblem.com/)

## Lessons

1. [How to solve a hard programming interview question](lessons/How_to_solve_hard_programming_interview_questions.md)

## My solutions

| Number | Title | Difficulty | Questioner | Description |
| ------:|:-----:|:----------:|:----------:|:----------- |
| 5 | [cons car cdr](src/0005-cons_car_cdr/cons_car_cdr.py) | Medium | Jane Street | cons(a, b) constructs a pair, and car(pair) and cdr(pair) returns the first and last element of that pair. For example, car(cons(3, 4)) returns 3, and cdr(cons(3, 4)) returns 4.<br/><br/>Given this implementation of cons:<br/><br/>def cons(a, b):<br/>  def pair(f):<br/>    return f(a, b)<br/>  return pair<br/><br/>Implement car and cdr.<br/> |
| 4 | [lowest positive integer not in array](src/0004-lowest_positive_integer_not_in_array/lowest_positive_integer_not_in_array.py) | Hard | Stripe | Given an array of integers, find the first missing positive integer in linear time and constant space. In other words, find the lowest positive integer that does not exist in the array. The array can contain duplicates and negative numbers as well.<br/><br/>For example, the input [3, 4, -1, 1] should give 2. The input [1, 2, 0] should give 3.<br/><br/>You can modify the input array in-place.<br/> |
| 3 | [binary tree serialization and deserialization](src/0003-binary_tree_serialization_and_deserialization/binary_tree_serialization_and_deserialization.py) | Medium | Google | Given the root to a binary tree, implement serialize(root), which serializes the tree into a string, and deserialize(s), which deserializes the string back into the tree.<br/><br/>For example, given the following Node class<br/><br/>class Node:<br/>    def __init__(self, val, left=None, right=None):<br/>        self.val = val<br/>        self.left = left<br/>        self.right = right<br/><br/>The following test should pass:<br/><br/>node = Node('root', Node('left', Node('left.left')), Node('right'))<br/>assert deserialize(serialize(node)).left.left.val == 'left.left'<br/> |
| 2 | [product of other array elements](src/0002-product_of_other_array_elements/product_of_other_array_elements.py) | Hard | Uber | Given an array of integers, return a new array such that each element at index i of the new array is the product of all the numbers in the original array except the one at i.<br/><br/>For example, if our input was [1, 2, 3, 4, 5], the expected output would be [120, 60, 40, 30, 24]. If our input was [3, 2, 1], the expected output would be [2, 3, 6].<br/><br/>Follow-up: what if you can't use division?<br/> |
| 1 | [is sum in array](src/0001-is_sum_in_array/is_sum_in_array.py) | Easy | Google | Given a list of numbers and a number k, return whether any two numbers from the list add up to k.<br/><br/>For example, given [10, 15, 3, 7] and k of 17, return true since 10 + 7 is 17.<br/><br/>Bonus: Can you do this in one pass?<br/> |
