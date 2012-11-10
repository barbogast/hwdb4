from unittest import TestCase

#from hwdb.init_data import get_initial_objects, get_objects_computer_BA
import hwdb.model as M


TEST_DB_PATH = 'sqlite:///:memory:'


class _Init_DB_Mixin(object):
    def setUp(self):
        engine = M.get_engine(TEST_DB_PATH, False)
        M.create_all(engine)
        M.init_session(engine)


    def tearDown(self):
        M.db_session.rollback()
        M.db_session.close()



#class Test_init_data(_Init_DB_Mixin, TestCase):
    #def test_(self):
        #obj_dict = get_initial_objects()
        #self.assertIsNotNone(obj_dict)
        #M.db_session.add_all(obj_dict.values())
        #M.db_session.flush()

        #obj_dict2 = get_objects_computer_BA(obj_dict)
        #self.assertIsNotNone(obj_dict2)
        #M.db_session.add_all(obj_dict2.values())
        #M.db_session.flush()

        #M.db_session.commit()
