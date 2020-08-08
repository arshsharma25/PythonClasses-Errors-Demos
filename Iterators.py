def _is_perfect_length(sequence):
    """True if sequence has length 2^n -1, otherwise False"""
    n = len(sequence)
    return ((n+1)&n==0) and (n != 0)

class LevelOrderIterator:

    def __init__(self, sequence):
        if not _is_perfect_length(sequence):
            raise ValueError(
                f"Sequence of length {len(sequence)} does not represent"
                "a perfect binary tree with length 2^n - 1"
                )
        self._sequence = sequence
        self._index = 0

    def __next__(self):
        if self._index >= len(self._sequence):
            raise StopIteration
        result = self._sequence[self._index]
        self._index += 1
        return result

    def __iter__(self):
        return self

    def _left_child(index):
        return 2 * index + 1

    def _right_child(index):
        return 2 * index + 2


class PreOrderIterator:

    def __init__(self, sequence):
        if not _is_perfect_length(sequence):
            raise ValueError(
                f"Sequence of length {len(sequence)} does not represent"
                "a perfect binary tree with length 2^n - 1"
                )
            self._sequence = sequence
            self._stack = [0]

    def __next__(self):
        if len(self._stack) == 0:
            raise StopIteration

        index = self._stack.pop()
        result = self._sequence[index]


        # Pre-order: Push right child first so left child is
        # popped processed first. Last-in, first-out
        right_child_index = _right_child(index)
        if right_child_index < len(self._sequence):
            self._stack.append(right_child_index)

        left_child_index = _left_child(index)
        if left_child_index < len(self._sequence):
            self._stack.append(left_child_index)

        return result

    def __iter__(self):
        return self

# level order iterator
level_expr_tree = ["*","+","-","a","b","c","d"]
level_order_iterator = LevelOrderIterator(level_expr_tree)

# pre order iterator
pre_order_expr_tree = "* + - a b c d".split()
pre_order_iterator = PreOrderIterator(pre_order_iterator)
final_pre_order_iterator = " ".join(pre_order_iterator)
print(final_pre_order_iterator)
