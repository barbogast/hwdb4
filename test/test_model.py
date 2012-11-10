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


class Test_PartConnection(_Init_DB_Mixin, TestCase):
    def test_tODO():
        """
        A part which is a connection parent may not be a container of a
        parent_less (=fixed) connection
        """

    def test_(self):
        """
        Add Standards as distractions:
        create part S1
        create part S2: S1=>S2

        create part A1 as systemA parent
        create part A2 as systemA A1=>A2 (add a 1st part contained by the system parent)
        create part A3 as systemA A1=>A3 (add a 2nd part contained by the system parent)
        create part A4 as systemA A2=>A4 (add a 1st part contained by a contained part)
        create part A5 as systemA A2=>A5 (add a 2nd part contained by a contained part)

        Add 2 parts not belonging to a system, each containing system A
        create part B1 without system parent B1=>A1
        create part C1 without system parent C1=>A1

        A part belonging to a foreign system contains system A
        create part D1 as systemD parent
        add connection: systemD D1=>A1

        A sub part belonging to a foreign system contains systemA
        create part E1 as systemE parent
        create part E2 as systemE E1=>E2
        add connection: systemD E2=>A1

        Multiple parts of the same systems contain systemA
        create part F1 as systemF parent
        create part F2 as systemF F1=>F2
        create part F3 as systemF F2=>F3
        add connection: systemF F1=>A1
        add connection: systemF F2=>A1
        add connection: systemF F3=>A1
        """


    def test_max_one_container_part_per_system_parent(self):
        """
        # In the same system: a part may contain multiple other parts but
        # may only be contained by one part
        create part A1 as systemA parent
        create part A2 as systemA A1=>A2 (add a 1st part contained by the system parent)
        create part A3 as systemA A1=>A3 (add a 2nd part contained by the system parent)
        create part A4 as systemA A2=>A4 (add a 1st part contained by a contained part)
        create part A5 as systemA A2=>A5 (add a 2nd part contained by a contained part)
        add connection: systemA A1=>A4 ===> Error: A4 is already contained by A2 for this system parent

        # Assert that part A4 (which is already contained by part A2 in
        # systemA) may be contained by A2 a second time in a
        # different system
        create part B1 as systemB parent
        add connection: systemB A1=>A4 ===> No error!
        """

    def test_missing_link_to_system_parent(self):
        """
        # The chain of containedPart=>containerPart must always end with the
        # system parent part
        create part A1 as systemA parent
        create part B1 as systemA parent
        create part A2

        add connection: systemB A1=A2 (add a corrent chain for a foreign system to distract the next test)
        nt connection)
        create part A3 as systemA A2=>A3 ===> Error: A2 is not connected with systemA parent
        """

    def test_add_the_system_parent_as_contained_part_in_the_same_system(self):
        """
        # A part which is system parent may not be contained by another
        # part within the same system
        create part A1 as systemA parent
        create part A2
        create part A3 as systemA A2=>A3

        # foreign system which contains systemA as distraction
        create part B1 as systemB parent
        add connection: systemB B1=>A1

        # connect part with system parent
        add connection: systemA A2=>A1   ====> Error

        # connect subpart with system parent
        add connection: systemA A3=>A1   ====> Error
        """



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