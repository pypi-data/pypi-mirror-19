import unittest
from gentests import gentests, vals

from uniquepwd import uniquePrefix, uniquePrefixMulti, uniqueListTree

@gentests
class TestUniquepwd(unittest.TestCase):
    @vals([
        ["a", "b", "a"],
        ["a", "", "a"],
        ["", "", ""],
        ["", "a", ""],
        ["ab", "ac", "ab"],
        ["ab", "abc", "ab"],
        ["abc", "ab", "abc"]
    ])
    def test_uniquePrefix(self, path, compare_path, result):
        self.assertEqual(uniquePrefix(path, compare_path), result)

    @vals([
        ['a', [], 'a'],
        ['a', ['ab'], 'a'],
        ['ab', ['a'], 'ab'],
        ['ab', ['a', 'abc'], 'ab'],
        ['abcd', ['ab', 'a', 'de', 'abc'], 'abcd']
    ])
    def test_uniquePrefixMulti(self, path, compare_paths, result):
        self.assertEqual(uniquePrefixMulti(path, compare_paths), result)

    @vals([
        [[],
         [],
         []],

        [['a', 'a', 'a'],
         [['ab', 'abc'],
          ['ab', 'abc'],
          ['ab', 'abc']],
         ['a', 'a', 'a']],

        [['a', 'b', 'c'],
         [['ab', 'abc'],
          ['bc', 'bcd'],
          ['cd', 'cde']],
         ['a', 'b', 'c']],

        [['abc', 'de', 'fghi'],
         [['ac', 'abd'],
          ['f', 'e'],
          ['fg', 'hi']],
         ['abc', 'd', 'fgh']]
    ])
    def test_uniqueListTree(self, path, others, result):
        self.assertEqual(uniqueListTree(path, others), result)

if __name__ == '__main__':
    unittest.main()
