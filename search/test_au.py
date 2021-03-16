import unittest
import ai_util as au

class TestAiMethods(unittest.TestCase):
    def test_data_to_path(self):
        data = {"upper": [["r", 0, 0],["r", 0, 1]],
            "lower": [["s", 1, -1]],
            "block": [["", 1, 0]]}
        friendly_list, enemy_list, block_list = au.data_to_path(data)
        self.assertEqual(friendly_list, [['r', [(0, 0)]], ['r', [(0, 1)]]])
        self.assertEqual(enemy_list, [['s', (1, -1),-1]])
        self.assertEqual(block_list, [(1,0)])

    def test_can_defeat(self):
        self.assertEqual(au.can_defeat('p','r'), 1)
        self.assertEqual(au.can_defeat('r','r'), 0)
        self.assertEqual(au.can_defeat('s','r'), -1)


    def test_potential_target(self):
        token = ('r', [(0, 0)])
        enemy_list1 = [('s', (3, -3))]
        enemy_list2 = [('r', (2, 2)), ('s', (3, -3)), ('p', (1,3)), ('s', (-2, 0))]
        self.assertEqual(au.potential_target(token, enemy_list1), [(3 , -3)])
        self.assertEqual(au.potential_target(token, enemy_list2), [(3, -3), (-2, 0)])
    def test_potential_slide(self):
        cur = (0,0)
        b = [(1,0),(1,-1),(-1,0),(0,-1),(-1,1),(0,1)]
        self.assertEqual(au.potential_slide(cur,b),[])

    def test_potential_move(self):
        cur = (0,0)
        token = ('r',(0,0))
        b = []
        e = [('r',(0,1)),('s',(0,-1)),('p',(1,0))]
        p = [(1,0),(1,-1),(-1,0),(0,-1),(-1,1),(0,1)]
        self.assertEqual(au.potential_move(cur,token,1,p,e,b),[])

if __name__ == '__main__':
    unittest.main()