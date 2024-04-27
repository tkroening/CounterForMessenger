from Main import MainPage
from Main import MultiSortPopup
from functools import cmp_to_key
import unittest

column_biases = {
        "name": "stringwise",
        "pep": "numberwise",
        "type": "stringwise",
        "msg": "numberwise",
        "call": "numberwise",
        "photos": "numberwise",
        "gifs": "numberwise",
        "videos": "numberwise",
        "files": "numberwise",
    }

columns_reversed = {
        "name": False,
        "pep": False,
        "type": False,
        "msg": False,
        "call": False,
        "photos": False,
        "gifs": False,
        "videos": False,
        "files": False,
    }

def apply_multi_sort(rows, sort_columns):
    """
    This function sorts the rows based on the ordering stored in
    `self.sort_columns`.

    To achieve this, the `compare` function tries to break ties based
    each successive column in the ordering, before giving up and declaring
    a tie.
    """
    def compare(a, b, ordering):
        # a and b are *rows* of data (dictionaries)
        if ordering == []:
            # We have nothing left to break ties on
            return 0

        # We will try to break the tie on this column
        column_name = ordering[0]
        bias = column_biases[column_name]
        reverse_multiplier = -1 if columns_reversed[column_name] else 1

        # Retrieve the appropriate column from each row
        a_value = a[column_name]
        b_value = b[column_name]

        if bias == "stringwise":
            if a_value < b_value: return -1 * reverse_multiplier
            elif a_value > b_value: return 1 * reverse_multiplier
        elif bias == "numberwise":
            a_value, b_value = int(a_value), int(b_value)
            if a_value < b_value: return -1 * reverse_multiplier
            elif a_value > b_value: return 1 * reverse_multiplier
        else:
            raise Exception(f"Undefined bias")

        """
        If we made it here, then the values are equal when compared
        on the current column value.

        We continue with the next column in the ordering.
        """
        return compare(a, b, ordering[1:])

    def compare_wrapper(a, b):
        (_, a) = a
        (_, b) = b

        return compare(a, b, sort_columns)

    rows.sort(key = cmp_to_key(compare_wrapper))

empty = []
sort_columns1 =  [
        "name",
        "pep",
        "type",
        "msg",
        "call",
        "photos",
        "gifs",
        "videos",
        "files",
    ]
apply_multi_sort(empty, sort_columns1)
assert (empty == [])

dicta = {
        "name": "1",
        "pep": "2",
        "type": "3",
        "msg": "4",
        "call": "5",
        "photos": "6",
        "gifs": "7",
        "videos": "8",
        "files": "9",
    }

dictb = {
        "name": "2",
        "pep": "1",
        "type": "3",
        "msg": "4",
        "call": "5",
        "photos": "6",
        "gifs": "7",
        "videos": "8",
        "files": "9",
    }

dictc = {
        "name": "9",
        "pep": "8",
        "type": "7",
        "msg": "6",
        "call": "5",
        "photos": "4",
        "gifs": "3",
        "videos": "2",
        "files": "1",
    }

emptydict = {
        "name": "",
        "pep": "",
        "type": "",
        "msg": "",
        "call": "",
        "photos": "",
        "gifs": "",
        "videos": "",
        "files": "",
    }

rows1 = [(0, dicta.copy())]
apply_multi_sort(rows1, sort_columns1)
(i1, _) = rows1[0]
test1 = 0
assert(i1 == test1)

rows2 = [(0, dicta.copy()), (1, dictb.copy())]
apply_multi_sort(rows2, sort_columns1)
(i1, _), (i2, _) = rows2[0], rows2[1]
test2 = (0,1)
assert(test2 == (i1, i2))

rows3 = [(0, dictb.copy()), (1, dicta.copy())]
apply_multi_sort(rows3, sort_columns1)
(i1, _), (i2, _) = rows3[0], rows3[1]
test3 = (1, 0)
assert(test3 == (i1, i2))

rows4 = [(0, dicta.copy()), (1, dicta.copy())]
apply_multi_sort(rows4, sort_columns1)
(i1, _), (i2, _) = rows4[0], rows4[1]
test4 = (0, 1)
assert(test4 == (i1, i2))

columns_reversed["name"] = True
rows5 = [(0, dicta.copy()), (1, dictb.copy())]
apply_multi_sort(rows5, sort_columns1)
(i1, _), (i2, _) = rows5[0], rows5[1]
test5 = (1, 0)
assert(test5 == (i1, i2))

rows6 = [(0, dictb.copy()), (1, dicta.copy())]
apply_multi_sort(rows6, sort_columns1)
(i1, _), (i2, _) = rows6[0], rows6[1]
test6 = (0, 1)
assert(test6 == (i1, i2))

columns_reversed["name"] = False
column_biases["name"] = "foo"
rows2 = [(0, dicta.copy()), (1, dictb.copy())]
caught = False
try:
    apply_multi_sort(rows2, sort_columns1)
except:
    caught = True
assert(caught)
column_biases["name"] = "stringwise"

sort_columns2 = sort_columns1.copy()
sort_columns2.pop(0)
sort_columns2.pop(0)
sort_columns2.append("name")
sort_columns2.append("pep")
rows7 = [(0, dicta.copy()), (1, dictb.copy()), (2, dictc.copy())]
apply_multi_sort(rows7, sort_columns2)
(i1, _), (i2, _), (i3, _) = rows7[0], rows7[1], rows7[2]
test7 = (0, 1, 2)
assert(test7 == (i1, i2, i3))

columns_reversed["type"] = True
rows8 = [(0, dicta.copy()), (1, dictb.copy()), (2, dictc.copy())]
apply_multi_sort(rows8, sort_columns2)
(i1, _), (i2, _), (i3, _) = rows8[0], rows8[1], rows8[2]
test8 = (2, 0, 1)
assert(test8 == (i1, i2, i3))

rows9 = [(0, dicta.copy()), (1, emptydict.copy())]
apply_multi_sort(rows9, sort_columns1)
(i1, _), (i2, _) = rows9[0], rows9[1]
test9 = (1, 0)
assert(test9 == (i1, i2))

print("All Tests Passed!")