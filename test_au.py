import unittest
import search.ai_util as au

class TestAiMethods(unittest.TestCase):
    def test_data_to_path(self):
        data = {"upper": [["r", 0, 0],["r", 0, 1]],
            "lower": [["s", 1, -1]],
            "block": [["", 1, 0]]}
        friendly_list, enemy_list, block_list = au.data_to_path(data)
        self.assertEqual(friendly_list, [{'path': [(0, 0)], 'type': 'r'}, {'path': [(0, 1)], 'type': 'r'}])
        self.assertEqual(enemy_list, [{'type':'s','cord':(1,-1),'death_round':-1}])
        self.assertEqual(block_list, [(1,0)])

    def test_can_defeat(self):
        self.assertEqual(au.can_defeat('p','r'), 1)
        self.assertEqual(au.can_defeat('r','r'), 0)
        self.assertEqual(au.can_defeat('s','r'), -1)


    def test_potential_target(self):
        token = {'type': 'r', 'path': [(0, 0)]}
        enemy_list1 = [{'type': 's','cord': (3, -3), 'death_round': -1}]
        enemy_list2 = [{'type': 'r', 'cord': (2, 2), 'death_round': -1}, {'type': 's', 'cord': (3, -3), 'death_round': -1}, 
        {'type': 'p', 'cord': (1, 3), 'death_round': -1}, {'type': 's', 'cord': (-2, 0), 'death_round': -1}]
        self.assertEqual(au.potential_target(token, enemy_list1), [(3 , -3)])
        self.assertEqual(au.potential_target(token, enemy_list2), [(3, -3), (-2, 0)])

    def test_out_bound(self):
        move_list = [(5,1),(1,0),(-5,1),(-4,4),(1,5)]
        au.remove_out_bound(move_list)
        self.assertEqual(move_list,[(1,0),(-4,4)])
    
    # one token used to swing at 0 round
    def test_potential_swing(self):
        cur = (0,0)
        cur_round = 1
        friendly_list = [{'path': [(0, 2),(0,1)], 'type': 'r'}, {'path': [(0, 2),(0,3)], 'type': 'r'}]
        out = [(-1, 1), (-1, 2), (0, 0), (0, 2), (1, 0), (1, 1)]
        potential_swing_list = au.potential_swing(cur, cur_round, friendly_list)
        print(potential_swing_list)
        for out_cord in out:
            self.assertIn(out_cord, potential_swing_list)

    def test_remove_enemy_kill(self):
        cur_round = 3
        potential_move_list = [(1,0),(1,-1),(-1,0),(0,-1),(-1,1),(0,1)]
        out = [(1,0),(1,-1),(-1,0),(0,-1),(-1,1),(0,1)]
        enemy_list = [{'type':'s','cord':(1,-1),'death_round':-1}]
        token = {'path': [(0, 0)], 'type': 'r'}
        p = au.remove_enemy_kill(token,cur_round,enemy_list,potential_move_list)
        self.assertEqual(p,out)

    # def test_potential_slide(self):
    #     cur = (0,0)
    #     b = [(1,0),(1,-1),(-1,0),(0,-1),(-1,1),(0,1)]
    #     self.assertEqual(au.potential_slide(cur,b),[])

    # def test_potential_move(self):
    #     cur = (0,0)
    #     token = ('r',(0,0))
    #     b = []
    #     e = [('r',(0,1)),('s',(0,-1)),('p',(1,0))]
    #     p = [(1,0),(1,-1),(-1,0),(0,-1),(-1,1),(0,1)]
    #     self.assertEqual(au.potential_move(cur,token,1,p,e,b),[])

if __name__ == '__main__':
    unittest.main()