#!/usr/bin/python3
# Questioner: Google
# Difficulty: Hard

"""
Suppose we represent our file system by a string in the following manner:

The string "dir\n\tsubdir1\n\tsubdir2\n\t\tfile.ext" represents:

dir
    subdir1
    subdir2
        file.ext

The directory dir contains an empty sub-directory subdir1 and a sub-directory subdir2 containing a file file.ext.

The string "dir\n\tsubdir1\n\t\tfile1.ext\n\t\tsubsubdir1\n\tsubdir2\n\t\tsubsubdir2\n\t\t\tfile2.ext" represents:

dir
    subdir1
        file1.ext
        subsubdir1
    subdir2
        subsubdir2
            file2.ext

The directory dir contains two sub-directories subdir1 and subdir2. subdir1 contains a file file1.ext and an empty second-level sub-directory subsubdir1. subdir2 contains a second-level sub-directory subsubdir2 containing a file file2.ext.

We are interested in finding the longest (number of characters) absolute path to a file within our file system. For example, in the second example above, the longest absolute path is "dir/subdir2/subsubdir2/file2.ext", and its length is 32 (not including the double quotes).

Given a string representing the file system in the above format, return the length of the longest absolute path to a file in the abstracted file system. If there is no file in the system, return 0.

Note:
The name of a file contains at least a period and an extension.
The name of a directory or sub-directory will not contain a period.
"""

# -----------------------------------------------------------------------------

from collections import deque
FILESYSTEM_ITEM_SEPARATOR = '\n'
FILESYSTEM_ITEM_INDENT = '\t'

def max_filepath_length(filesystem: str) -> int:
  max_filepath_len = 0
  parent_folder_lengths = deque()
  hierarchy_length = 0
  i = 0
  while i < len(filesystem):
    indentation_level = 0
    while filesystem[i] == FILESYSTEM_ITEM_INDENT:
      indentation_level += 1
      i += 1
    assert indentation_level <= len(parent_folder_lengths)

    while len(parent_folder_lengths) > indentation_level:
      hierarchy_length -= 1 + parent_folder_lengths.pop()

    name_length = 0
    is_file = False
    while i < len(filesystem):
      if filesystem[i] == '.':
        is_file = True
      if filesystem[i] == FILESYSTEM_ITEM_SEPARATOR:
        i += 1
        break
      name_length += 1
      i += 1

    if is_file:
      path_length = hierarchy_length + name_length
      if path_length > max_filepath_len:
        max_filepath_len = path_length
    else:
      hierarchy_length += 1 + name_length # +1 accounts for the '/'
      parent_folder_lengths.append(name_length)
  return max_filepath_len

# -----------------------------------------------------------------------------

if __name__ == '__main__':
  functions = (
    max_filepath_length,
  )

  tests = [
    (("dir\n\tsubdir1\n\tsubdir2\n\t\tfile.ext",), len("dir/subdir2/file.ext")),
    (("dir\n\tsubdir1\n\t\tfile1.ext\n\t\tsubsubdir1\n\tsubdir2\n\t\tsubsubdir2\n\t\t\tfile2.ext",), 32),
    (("",), 0),
    (("dir\n\tsubdir1\n\t\tfile1_ext\n\t\tsubsubdir1\n\tsubdir2\n\t\tsubsubdir2\n\t\t\tfile2_ext",), 0),
  ]

  for args, expectation in tests:
    print(f"{args=} {expectation=}")
    results = []
    for f in functions:
      res = f(*args)
      results.append(res)
      print(res, f)
    assert all([res == expectation for res in results])
  print("All tests passed")


"""
args=('dir\n\tsubdir1\n\tsubdir2\n\t\tfile.ext',) expectation=20
20 <function max_filepath_length at 0x7f2489ee60c0>
args=('dir\n\tsubdir1\n\t\tfile1.ext\n\t\tsubsubdir1\n\tsubdir2\n\t\tsubsubdir2\n\t\t\tfile2.ext',) expectation=32
32 <function max_filepath_length at 0x7f2489ee60c0>
args=('',) expectation=0
0 <function max_filepath_length at 0x7f2489ee60c0>
args=('dir\n\tsubdir1\n\t\tfile1_ext\n\t\tsubsubdir1\n\tsubdir2\n\t\tsubsubdir2\n\t\t\tfile2_ext',) expectation=0
0 <function max_filepath_length at 0x7f2489ee60c0>
All tests passed
"""
