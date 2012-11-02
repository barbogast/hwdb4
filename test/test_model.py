from unittest import TestCase

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



class Test_DB(_Init_DB_Mixin, TestCase):
    def test_Parts(self):
        """
        Create multiple parts
        Create multiple subparts
        Create a Standard (must not change the result)
        Check each association
        Test unique constraints?
        """
        def _objects():
            # 1 child
            parent_part_1 = M.Part(name='parent_part_1', note='lalala')
            child_part_1_1 = M.Part(name='child_part_1_1', parent_part=parent_part_1)

            # 2 children (one child with subchild)
            parent_part_2 = M.Part(name='parent_part_2', note='lalala')
            child_part_2_1 = M.Part(name='child_part_2_1', parent_part=parent_part_2)
            child_part_2_2 = M.Part(name='child_part_2_2', parent_part=parent_part_2)
            subchild_2_2_1 = M.Part(name='subchild_part_2_2_1', parent_part=child_part_2_2)

            # No children
            parent_part_3 = M.Part(name='parent_part_3', note='lalala')
            return locals()

        M.db_session.add_all(_objects().values())
        M.db_session.flush()

        # Check connection from parent to child with 1 child
        p1 = M.db_session.query(M.Part).filter(M.Part.name=='parent_part_1').first()
        self.assertIsNotNone(p1)
        self.assertEqual(1, len(p1.children))
        self.assertEqual('child_part_1_1', p1.children[0].name)

        # Check connection from child to parent
        c1 = M.db_session.query(M.Part).filter(M.Part.name=='child_part_1_1').first()
        self.assertIsNotNone(c1)
        self.assertIsNotNone(c1.parent_part)
        self.assertEqual('parent_part_1', c1.parent_part.name)

        # Check connection from parent to child with multiple children
        p2 = M.db_session.query(M.Part).filter(M.Part.name=='parent_part_2').first()
        self.assertIsNotNone(p2)
        self.assertEqual(2, len(p2.children))
        names = [c.name for c in p2.children]
        self.assertIn('child_part_2_1', names)
        self.assertIn('child_part_2_2', names)

        # Check connection from child to subchild
        c2 = M.db_session.query(M.Part).filter(M.Part.name=='child_part_2_2').first()
        self.assertIsNotNone(p2)
        self.assertEqual(1, len(c2.children))
        self.assertEqual('subchild_part_2_2_1', c2.children[0].name)


    def test_Standards(self):
        """
        Create multiple standard groups
        Create multiple standards associated with different groups
        Create a Part (must not change the result)
        Associate them with different parts
        Check each association
        Test unique constraints?
        """
        raise

    def test_AttrTypes_with_units(self):
        """
        Create multiple Units
        Create multiple Parts
        Create multiple AttrTypes
        Associate AttrTypes with Units and Parts
        Check each association
        Test unique constraints?
        """
        raise

    def test_Attr(self):
        """
        Create multiple AttrTypes
        Create multiple Parts
        Create multiple Attrs
        Associate Attrs with AttrTypes and Parts
        Check each association
        Test unique constraints?
        """
        raise

    def test_Collection(self):
        """
        Create multiple Parts
        Create multiple Collections
        TODO
        """
        raise