# -*- coding: utf-8 -*-
# Stalker a Production Asset Management System
# Copyright (C) 2009-2016 Erkan Ozgur Yilmaz
#
# This file is part of Stalker.
#
# Stalker is free software: you can redistribute it and/or modify
# it under the terms of the Lesser GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License.
#
# Stalker is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# Lesser GNU General Public License for more details.
#
# You should have received a copy of the Lesser GNU General Public License
# along with Stalker.  If not, see <http://www.gnu.org/licenses/>

import copy
import datetime
import logging
import tempfile

import unittest

from stalker.exceptions import CircularDependencyError
from stalker.db import DBSession
from stalker import (db, defaults, Entity, Project, Repository, StatusList,
                     Status, Task, Type, User, TimeLog, FilenameTemplate,
                     Structure)
from stalker.models.task import CONSTRAIN_END, CONSTRAIN_BOTH

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)


class TaskTestCase(unittest.TestCase):
    """Tests the stalker.models.task.Task class
    """

    config = {
        'sqlalchemy.url': 'sqlite://',
        'sqlalchemy.echo': False
    }

    @classmethod
    def setUpClass(cls):
        """run once
        """
        defaults.timing_resolution = datetime.timedelta(hours=1)

        # create a new session
        db.setup(cls.config)
        db.init()

        cls.status_wfd = Status.query.filter_by(code="WFD").first()
        cls.status_rts = Status.query.filter_by(code="RTS").first()
        cls.status_wip = Status.query.filter_by(code="WIP").first()
        cls.status_prev = Status.query.filter_by(code="PREV").first()
        cls.status_hrev = Status.query.filter_by(code="HREV").first()
        cls.status_drev = Status.query.filter_by(code="DREV").first()
        cls.status_oh = Status.query.filter_by(code="OH").first()
        cls.status_stop = Status.query.filter_by(code="STOP").first()
        cls.status_cmpl = Status.query.filter_by(code="CMPL").first()

        cls.task_status_list = StatusList.query\
            .filter_by(target_entity_type='Task').first()

        cls.test_project_status_list = StatusList(
            name="Project Statuses",
            statuses=[cls.status_wip,
                      cls.status_prev,
                      cls.status_cmpl],
            target_entity_type=Project,
        )

        cls.test_movie_project_type = Type(
            name="Movie Project",
            code='movie',
            target_entity_type=Project,
        )

        cls.test_repository_type = Type(
            name="Test Repository Type",
            code='test',
            target_entity_type=Repository,
        )

        cls.test_repository = Repository(
            name="Test Repository",
            type=cls.test_repository_type,
            linux_path=tempfile.mkdtemp(),
            windows_path=tempfile.mkdtemp(),
            osx_path=tempfile.mkdtemp()
        )

        cls.test_user1 = User(
            name="User1",
            login="user1",
            email="user1@user1.com",
            password="1234"
        )

        cls.test_user2 = User(
            name="User2",
            login="user2",
            email="user2@user2.com",
            password="1234"
        )

        cls.test_user3 = User(
            name="User3",
            login="user3",
            email="user3@user3.com",
            password="1234"
        )

        cls.test_user4 = User(
            name="User4",
            login="user4",
            email="user4@user4.com",
            password="1234"
        )

        cls.test_user5 = User(
            name="User5",
            login="user5",
            email="user5@user5.com",
            password="1234"
        )

        cls.test_project1 = Project(
            name="Test Project1",
            code='tp1',
            type=cls.test_movie_project_type,
            status_list=cls.test_project_status_list,
            repositories=[cls.test_repository]
        )

        cls.test_dependent_task1 = Task(
            name="Dependent Task1",
            project=cls.test_project1,
            status_list=cls.task_status_list,
            responsible=[cls.test_user1]
        )

        cls.test_dependent_task2 = Task(
            name="Dependent Task2",
            project=cls.test_project1,
            status_list=cls.task_status_list,
            responsible=[cls.test_user1]
        )

        cls.kwargs = {
            'name': 'Modeling',
            'description': 'A Modeling Task',
            'project': cls.test_project1,
            'priority': 500,
            'responsible': [cls.test_user1],
            'resources': [cls.test_user1, cls.test_user2],
            'alternative_resources': [cls.test_user3, cls.test_user4,
                                      cls.test_user5],
            'allocation_strategy': 'minloaded',
            'persistent_allocation': True,
            'watchers': [cls.test_user3],
            'bid_timing': 4,
            'bid_unit': 'd',
            'schedule_timing': 1,
            'schedule_unit': 'd',
            'start': datetime.datetime(2013, 4, 8, 13, 0),
            'end': datetime.datetime(2013, 4, 8, 18, 0),
            'depends': [cls.test_dependent_task1,
                        cls.test_dependent_task2],
            'time_logs': [],
            'versions': [],
            'is_milestone': False,
            'status': 0,
            'status_list': cls.task_status_list,
        }

        # create a test Task
        DBSession.add_all([
            cls.test_project_status_list, cls.test_movie_project_type,
            cls.test_repository_type, cls.test_repository, cls.test_user1,
            cls.test_user2, cls.test_user3, cls.test_user4,
            cls.test_user5, cls.test_project1, cls.test_dependent_task1,
            cls.test_dependent_task2,
        ])
        DBSession.commit()

    def setUp(self):
        """setup test
        """
        self.data_created = []

    def tearDown(self):
        """run after every test and clean up
        """
        for data in self.data_created:
            if data in DBSession:
                DBSession.delete(data)
        DBSession.commit()

    @classmethod
    def tearDownClass(cls):
        """run only once
        """
        DBSession.remove()
        defaults.timing_resolution = datetime.timedelta(hours=1)

    def test___auto_name__class_attribute_is_set_to_False(self):
        """testing if the __auto_name__ class attribute is set to False for
        Task class
        """
        self.assertFalse(Task.__auto_name__)

    def test_priority_argument_is_skipped_defaults_to_task_priority(self):
        """testing if skipping the priority argument will default the priority
        attribute to task_priority.
        """
        kwargs = copy.copy(self.kwargs)
        kwargs.pop("priority")
        new_task = Task(**kwargs)
        self.assertEqual(new_task.priority, defaults.task_priority)

    def test_priority_argument_is_given_as_None_will_default_to_task_priority(self):
        """testing if the priority argument is given as None will default the
        priority attribute to task_priority.
        """
        kwargs = copy.copy(self.kwargs)
        kwargs["priority"] = None
        new_task = Task(**kwargs)
        self.assertEqual(new_task.priority, defaults.task_priority)

    def test_priority_attribute_is_given_as_None_will_default_to_task_priority(self):
        """testing if the priority attribute is given as None will default the
        priority attribute to task_priority.
        """
        new_task = Task(**self.kwargs)
        new_task.priority = None
        self.assertEqual(new_task.priority, defaults.task_priority)

    def test_priority_argument_any_given_other_value_then_integer_will_default_to_task_priority(self):
        """testing if a TypeError will be raised if the priority argument value
        is not an integer
        """
        test_values = ["a324", []]
        kwargs = copy.copy(self.kwargs)

        for test_value in test_values:
            kwargs["priority"] = test_value
            with self.assertRaises(TypeError):
                Task(**kwargs)

    def test_priority_attribute_is_not_an_integer(self):
        """testing if any other value then an positive integer for priority
        attribute will raise a TypeError.
        """
        test_values = ["a324", []]
        new_task = Task(**self.kwargs)

        for test_value in test_values:
            with self.assertRaises(TypeError):
                new_task.priority = test_value

    def test_priority_argument_is_negative(self):
        """testing if the priority argument is given as a negative value will
        set the priority attribute to zero.
        """
        kwargs = copy.copy(self.kwargs)
        kwargs["priority"] = -1
        new_task = Task(**kwargs)
        self.assertEqual(new_task.priority, 0)

    def test_priority_attribute_is_negative(self):
        """testing if the priority attribute is given as a negative value will
        set the priority attribute to zero.
        """
        new_task = Task(**self.kwargs)
        new_task.priority = -1
        self.assertEqual(new_task.priority, 0)

    def test_priority_argument_is_too_big(self):
        """testing if the priority argument is given bigger then 1000 will
        clamp the priority attribute value to 1000
        """
        kwargs = copy.copy(self.kwargs)
        kwargs["priority"] = 1001
        new_task = Task(**kwargs)
        self.assertEqual(new_task.priority, 1000)

    def test_priority_attribute_is_too_big(self):
        """testing if the priority attribute is set to a value bigger than 1000
        will clamp the value to 1000
        """
        new_task = Task(**self.kwargs)
        new_task.priority = 1001
        self.assertEqual(new_task.priority, 1000)

    def test_priority_argument_is_float(self):
        """testing if float numbers for priority argument will be converted to
        integer
        """
        kwargs = copy.copy(self.kwargs)
        test_values = [500.1, 334.23]
        for test_value in test_values:
            kwargs["priority"] = test_value
            new_task = Task(**kwargs)
            self.assertEqual(new_task.priority, int(test_value))

    def test_priority_attribute_is_float(self):
        """testing if float numbers for priority attribute will be converted to
        integer
        """
        new_task = Task(**self.kwargs)
        test_values = [500.1, 334.23]
        for test_value in test_values:
            new_task.priority = test_value
            self.assertEqual(new_task.priority, int(test_value))

    def test_priority_attribute_is_working_properly(self):
        """testing if the priority attribute is working properly
        """
        new_task = Task(**self.kwargs)
        test_value = 234
        new_task.priority = test_value
        self.assertEqual(new_task.priority, test_value)

    def test_resources_argument_is_skipped(self):
        """testing if the resources attribute will be an empty list when the
        resources argument is skipped
        """
        kwargs = copy.copy(self.kwargs)
        kwargs.pop("resources")
        new_task = Task(**kwargs)
        self.assertEqual(new_task.resources, [])

    def test_resources_argument_is_None(self):
        """testing if the resources attribute will be an empty list when the
        resources argument is None
        """
        kwargs = copy.copy(self.kwargs)
        kwargs["resources"] = None
        new_task = Task(**kwargs)
        self.assertEqual(new_task.resources, [])

    def test_resources_attribute_is_None(self):
        """testing if a TypeError will be raised whe the resources attribute
        is set to None
        """
        new_task = Task(**self.kwargs)
        self.assertRaises(TypeError, setattr, new_task, "resources", None)

    def test_resources_argument_is_not_list(self):
        """testing if a TypeError will be raised when the resources argument is
        not a list
        """
        kwargs = copy.copy(self.kwargs)
        kwargs["resources"] = "a resource"
        self.assertRaises(TypeError, Task, **kwargs)

    def test_resources_attribute_is_not_list(self):
        """testing if a TypeError will be raised when the resources attribute
        is set to any other value then a list
        """
        new_task = Task(**self.kwargs)
        self.assertRaises(
            TypeError, setattr, new_task, "resources", "a resource"
        )

    def test_resources_argument_is_set_to_a_list_of_other_values_then_User(self):
        """testing if a TypeError will be raised when the resources argument is
        set to a list of other values then a User
        """
        kwargs = copy.copy(self.kwargs)
        kwargs["resources"] = ["a", "list", "of", "resources", self.test_user1]
        self.assertRaises(TypeError, Task, **kwargs)

    def test_resources_attribute_is_set_to_a_list_of_other_values_then_User(self):
        """testing if a TypeError will be raised when the resources attribute
        is set to a list of other values then a User
        """
        new_task = Task(**self.kwargs)
        with self.assertRaises(TypeError):
            new_task.resources = \
                ["a", "list", "of", "resources", self.test_user1]

    def test_resources_attribute_is_working_properly(self):
        """testing if the resources attribute is working properly
        """
        new_task = Task(**self.kwargs)
        test_value = [self.test_user1]
        new_task.resources = test_value
        self.assertEqual(new_task.resources, test_value)

    def test_resources_argument_backreferences_to_User(self):
        """testing if the User instances passed with the resources argument
        will have the current task in their User.tasks attribute
        """
        # create a couple of new users
        new_user1 = User(
            name="test1",
            login="test1",
            email="test1@test.com",
            password="test1"
        )
        DBSession.add(new_user1)
        DBSession.commit()
        self.data_created.append(new_user1)

        new_user2 = User(
            name="test2",
            login="test2",
            email="test2@test.com",
            password="test2"
        )
        DBSession.add(new_user2)
        DBSession.commit()
        self.data_created.append(new_user1)

        # assign it to a newly created task
        kwargs = copy.copy(self.kwargs)
        kwargs["resources"] = [new_user1]
        new_task = Task(**kwargs)
        DBSession.add(new_task)
        DBSession.commit()
        self.data_created.append(new_task)

        # now check if the user has the task in its tasks list
        self.assertTrue(new_task in new_user1.tasks)

        # now change the resources list
        new_task.resources = [new_user2]
        self.assertTrue(new_task in new_user2.tasks)
        self.assertFalse(new_task in new_user1.tasks)

        # now append the new resource
        new_task.resources.append(new_user1)
        self.assertTrue(new_task in new_user1.tasks)

        # clean up test
        new_task.resources = []

    def test_resources_attribute_backreferences_to_User(self):
        """testing if the User instances passed with the resources argument
        will have the current task in their User.tasks attribute
        """
        # create a new user
        new_user = User(
            name="Test User",
            login="testuser",
            email="testuser@test.com",
            password="testpass"
        )

        # assign it to a newly created task
        #self.kwargs["resources"] = [new_user]
        kwargs = copy.copy(self.kwargs)
        new_task = Task(**kwargs)
        new_task.resources = [new_user]

        # now check if the user has the task in its tasks list
        self.assertTrue(new_task in new_user.tasks)

    def test_resources_attribute_will_clear_itself_from_the_previous_Users(self):
        """testing if the resources attribute is updated will clear itself from
        the current resources tasks attribute.
        """
        # create a couple of new users
        new_user1 = User(
            name="Test User1",
            login="testuser1",
            email="testuser1@test.com",
            password="testpass"
        )

        new_user2 = User(
            name="Test User2",
            login="testuser2",
            email="testuser2@test.com",
            password="testpass"
        )

        new_user3 = User(
            name="Test User3",
            login="testuser3",
            email="testuser3@test.com",
            password="testpass"
        )

        new_user4 = User(
            name="Test User4",
            login="testuser4",
            email="testuser4@test.com",
            password="testpass"
        )
        DBSession.add_all([new_user1, new_user2, new_user3, new_user4])
        DBSession.commit()
        self.data_created.extend([new_user1, new_user2, new_user3, new_user4])

        # now add the 1 and 2 to the resources with the resources argument
        # assign it to a newly created task
        kwargs = copy.copy(self.kwargs)
        kwargs["resources"] = [new_user1, new_user2]
        new_task = Task(**kwargs)
        DBSession.add(new_task)
        DBSession.commit()
        self.data_created.append(new_task)

        # now check if the user has the task in its tasks list
        self.assertTrue(new_task in new_user1.tasks)
        self.assertTrue(new_task in new_user2.tasks)

        # now update the resources list
        new_task.resources = [new_user3, new_user4]

        # now check if the new resources has the task in their tasks attribute
        self.assertTrue(new_task in new_user3.tasks)
        self.assertTrue(new_task in new_user4.tasks)

        # and if it is not in the previous users tasks
        self.assertFalse(new_task in new_user1.tasks)
        self.assertFalse(new_task in new_user2.tasks)

    def test_watchers_argument_is_skipped(self):
        """testing if the watchers attribute will be an empty list when the
        watchers argument is skipped
        """
        kwargs = copy.copy(self.kwargs)
        kwargs.pop("watchers")
        new_task = Task(**kwargs)
        DBSession.add(new_task)
        DBSession.commit()
        self.data_created.append(new_task)
        self.assertEqual(new_task.watchers, [])

    def test_watchers_argument_is_None(self):
        """testing if the watchers attribute will be an empty list when the
        watchers argument is None
        """
        kwargs = copy.copy(self.kwargs)
        kwargs["watchers"] = None
        new_task = Task(**kwargs)
        DBSession.add(new_task)
        DBSession.commit()
        self.data_created.append(new_task)
        self.assertEqual(new_task.watchers, [])

    def test_watchers_attribute_is_None(self):
        """testing if a TypeError will be raised whe the watchers attribute
        is set to None
        """
        new_task = Task(**self.kwargs)
        DBSession.add(new_task)
        DBSession.commit()
        self.data_created.append(new_task)
        self.assertRaises(TypeError, setattr, new_task, "watchers", None)

    def test_watchers_argument_is_not_list(self):
        """testing if a TypeError will be raised when the watchers argument is
        not a list
        """
        kwargs = copy.copy(self.kwargs)
        kwargs["watchers"] = "a resource"
        self.assertRaises(TypeError, Task, **kwargs)

    def test_watchers_attribute_is_not_list(self):
        """testing if a TypeError will be raised when the watchers attribute
        is set to any other value then a list
        """
        new_task = Task(**self.kwargs)
        DBSession.add(new_task)
        DBSession.commit()
        self.data_created.append(new_task)
        self.assertRaises(
            TypeError, setattr, new_task, "watchers", "a resource"
        )

    def test_watchers_argument_is_set_to_a_list_of_other_values_then_User(self):
        """testing if a TypeError will be raised when the watchers argument is
        set to a list of other values then a User
        """
        kwargs = copy.copy(self.kwargs)
        kwargs["watchers"] = ["a", "list", "of", "watchers", self.test_user1]
        self.assertRaises(TypeError, Task, **kwargs)

    def test_watchers_attribute_is_set_to_a_list_of_other_values_then_User(self):
        """testing if a TypeError will be raised when the watchers attribute
        is set to a list of other values then a User
        """
        new_task = Task(**self.kwargs)
        DBSession.add(new_task)
        DBSession.commit()
        self.data_created.append(new_task)

        test_values = ["a", "list", "of", "watchers", self.test_user1]

        with self.assertRaises(TypeError):
            new_task.watchers = test_values

    def test_watchers_attribute_is_working_properly(self):
        """testing if the watchers attribute is working properly
        """
        new_task = Task(**self.kwargs)
        DBSession.add(new_task)
        DBSession.commit()
        self.data_created.append(new_task)

        test_value = [self.test_user1]

        new_task.watchers = test_value
        self.assertEqual(new_task.watchers, test_value)

    def test_watchers_argument_back_references_to_User(self):
        """testing if the User instances passed with the watchers argument
        will have the current task in their User.watching attribute
        """
        # create a couple of new users
        new_user1 = User(
            name="new_user1",
            login="new_user1",
            email="new_user1@test.com",
            password="new_user1"
        )
        DBSession.add(new_user1)
        DBSession.commit()
        self.data_created.append(new_user1)

        new_user2 = User(
            name="new_user2",
            login="new_user2",
            email="new_user2@test.com",
            password="new_user2"
        )
        DBSession.add(new_user2)
        DBSession.commit()
        self.data_created.append(new_user2)

        # assign it to a newly created task
        kwargs = copy.copy(self.kwargs)
        kwargs["watchers"] = [new_user1]
        new_task = Task(**kwargs)
        DBSession.add(new_task)
        DBSession.commit()
        self.data_created.append(new_task)

        # now check if the user has the task in its tasks list
        self.assertTrue(new_task in new_user1.watching)

        # now change the watchers list
        new_task.watchers = [new_user2]
        self.assertTrue(new_task in new_user2.watching)
        self.assertFalse(new_task in new_user1.watching)

        # now append the new user
        new_task.watchers.append(new_user1)
        self.assertTrue(new_task in new_user1.watching)

    def test_watchers_attribute_back_references_to_User(self):
        """testing if the User instances passed with the watchers argument will
        have the current task in their User.watching attribute
        """
        # create a new user
        new_user = User(
            name="new_user",
            login="new_user",
            email="new_user@test.com",
            password="new_user"
        )
        DBSession.add(new_user)
        DBSession.commit()
        self.data_created.append(new_user)

        # assign it to a newly created task
        kwargs = copy.copy(self.kwargs)
        new_task = Task(**kwargs)
        new_task.watchers = [new_user]
        DBSession.add(new_task)
        DBSession.commit()
        self.data_created.append(new_task)

        # now check if the user has the task in its watching list
        self.assertTrue(new_task in new_user.watching)

    def test_watchers_attribute_will_clear_itself_from_the_previous_Users(self):
        """testing if the watchers attribute is updated will clear itself from
        the current watchers watching attribute.
        """
        # create a couple of new users
        new_user1 = User(
            name="new_user1",
            login="new_user1",
            email="new_user1@test.com",
            password="new_user1"
        )
        DBSession.add(new_user1)
        DBSession.commit()
        self.data_created.append(new_user1)

        new_user2 = User(
            name="new_user2",
            login="new_user2",
            email="new_user2@test.com",
            password="new_user2"
        )
        DBSession.add(new_user2)
        DBSession.commit()
        self.data_created.append(new_user2)

        new_user3 = User(
            name="new_user3",
            login="new_user3",
            email="new_user3@test.com",
            password="new_user3"
        )
        DBSession.add(new_user3)
        DBSession.commit()
        self.data_created.append(new_user3)

        new_user4 = User(
            name="new_user4",
            login="new_user4",
            email="new_user4@test.com",
            password="new_user4"
        )
        DBSession.add(new_user4)
        DBSession.commit()
        self.data_created.append(new_user4)

        # now add the 1 and 2 to the watchers with the watchers argument
        # assign it to a newly created task
        kwargs = copy.copy(self.kwargs)
        kwargs["watchers"] = [new_user1, new_user2]
        new_task = Task(**kwargs)
        DBSession.add(new_task)
        DBSession.commit()
        self.data_created.append(new_task)

        # now check if the user has the task in its watching list
        self.assertTrue(new_task in new_user1.watching)
        self.assertTrue(new_task in new_user2.watching)

        # now update the watchers list
        new_task.watchers = [new_user3, new_user4]

        # now check if the new watchers has the task in their watching
        # attribute
        self.assertTrue(new_task in new_user3.watching)
        self.assertTrue(new_task in new_user4.watching)

        # and if it is not in the previous users watching list
        self.assertFalse(new_task in new_user1.watching)
        self.assertFalse(new_task in new_user2.watching)

    def test_depends_argument_is_skipped_depends_attribute_is_empty_list(self):
        """testing if the depends attribute is an empty list when the depends
        argument is skipped
        """
        kwargs = copy.copy(self.kwargs)
        kwargs.pop("depends")
        new_task = Task(**kwargs)
        self.assertEqual(new_task.depends, [])

    def test_depends_argument_is_none_depends_attribute_is_empty_list(self):
        """testing if the depends attribute is an empty list when the depends
        argument is None
        """
        kwargs = copy.copy(self.kwargs)
        kwargs["depends"] = None
        new_task = Task(**kwargs)
        self.assertEqual(new_task.depends, [])

    def test_depends_argument_is_not_a_list(self):
        """testing if a TypeError will be raised when the depends argument is
        not a list
        """
        kwargs = copy.copy(self.kwargs)
        kwargs["depends"] = self.test_dependent_task1
        self.assertRaises(TypeError, Task, **kwargs)

    def test_depends_attribute_is_not_a_list(self):
        """testing if a TypeError will be raised when the depends attribute is
        set to something else then a list
        """
        kwargs = copy.copy(self.kwargs)
        new_task = Task(**kwargs)
        self.assertRaises(TypeError, setattr, new_task, "depends",
                          self.test_dependent_task1)

    def test_depends_argument_is_a_list_of_other_objects_than_a_Task(self):
        """testing if a AttributeError will be raised when the depends argument is
        a list of other typed objects than Task
        """
        test_value = ["a", "dependent", "task", 1, 1.2]
        kwargs = copy.copy(self.kwargs)
        kwargs["depends"] = test_value
        self.assertRaises(TypeError, Task, **kwargs)

    def test_depends_attribute_is_a_list_of_other_objects_than_a_Task(self):
        """testing if a AttributeError will be raised when the depends
        attribute is set to a list of other typed objects than Task
        """
        test_value = ["a", "dependent", "task", 1, 1.2]
        kwargs = copy.copy(self.kwargs)
        new_task = Task(**kwargs)
        self.assertRaises(TypeError, setattr, new_task, "depends", test_value)

    def test_depends_attribute_doesnt_allow_simple_cyclic_dependencies(self):
        """testing if a CircularDependencyError will be raised when the depends
        attribute has a simple circular dependency in dependencies
        """
        # create two new tasks A, B
        # make B dependent to A
        # and make A dependent to B
        # and expect a CircularDependencyError
        kwargs = copy.copy(self.kwargs)
        kwargs["depends"] = None

        task_a = Task(**kwargs)
        task_b = Task(**kwargs)

        task_b.depends = [task_a]

        self.assertRaises(CircularDependencyError, setattr, task_a, "depends",
                          [task_b])
        DBSession.rollback()

    def test_depends_attribute_doesnt_allow_cyclic_dependencies(self):
        """testing if a CircularDependencyError will be raised when the depends
        attribute has a circular dependency in dependencies
        """
        # create three new tasks A, B, C
        # make B dependent to A
        # make C dependent to B
        # and make A dependent to C
        # and expect a CircularDependencyError
        kwargs = copy.copy(self.kwargs)
        kwargs["depends"] = None

        kwargs["name"] = "taskA"
        task_a = Task(**kwargs)

        kwargs["name"] = "taskB"
        task_b = Task(**kwargs)

        kwargs["name"] = "taskC"
        task_c = Task(**kwargs)

        task_b.depends = [task_a]
        task_c.depends = [task_b]

        self.assertRaises(CircularDependencyError, setattr, task_a, "depends",
                          [task_c])
        DBSession.rollback()

    def test_depends_attribute_doesnt_allow_more_deeper_cyclic_dependencies(self):
        """testing if a CircularDependencyError will be raised when the depends
        attribute has a deeper circular dependency in dependencies
        """
        # create new tasks A, B, C, D
        # make B dependent to A
        # make C dependent to B
        # make D dependent to C
        # and make A dependent to D
        # and expect a CircularDependencyError
        kwargs = copy.copy(self.kwargs)
        kwargs["depends"] = None

        kwargs["name"] = "taskA"
        task_a = Task(**kwargs)

        kwargs["name"] = "taskB"
        task_b = Task(**kwargs)

        kwargs["name"] = "taskC"
        task_c = Task(**kwargs)

        kwargs["name"] = "taskD"
        task_d = Task(**kwargs)

        task_b.depends = [task_a]
        task_c.depends = [task_b]
        task_d.depends = [task_c]

        self.assertRaises(CircularDependencyError, setattr, task_a, "depends",
                          [task_d])
        DBSession.rollback()

    def test_depends_argument_cyclic_dependency_bug_2(self):
        """testing if a CircularDependencyError will be raised in the following
        case:
          T1 is parent of T2
          T3 depends to T1
          T2 depends to T3
        """
        kwargs = copy.copy(self.kwargs)
        kwargs['depends'] = None
        kwargs['name'] = 'T1'
        t1 = Task(**kwargs)
        self.data_created.append(t1)

        kwargs['name'] = 'T3'
        t3 = Task(**kwargs)
        self.data_created.append(t3)

        t3.depends.append(t1)
        DBSession.commit()

        kwargs['name'] = 'T2'
        kwargs['parent'] = t1
        kwargs['depends'] = [t3]

        # the following should generate the CircularDependencyError
        with self.assertRaises(CircularDependencyError):
            new_task = Task(**kwargs)

        DBSession.rollback()

    def test_depends_argument_doesnt_allow_one_of_the_parents_of_the_task(self):
        """testing if a CircularDependencyError will be raised when the depends
        attribute has one of the parents of this task
        """
        # create two new tasks A, B
        # make A parent to B
        # and make B dependent to A
        # and expect a CircularDependencyError
        kwargs = copy.copy(self.kwargs)
        kwargs["depends"] = None

        task_a = Task(**kwargs)
        task_b = Task(**kwargs)
        task_c = Task(**kwargs)

        task_b.parent = task_a
        task_a.parent = task_c

        self.assertTrue(task_b in task_a.children)
        self.assertTrue(task_a in task_c.children)

        self.assertRaises(CircularDependencyError, setattr, task_b, 'depends',
                          [task_a])
        self.assertRaises(CircularDependencyError, setattr, task_b, 'depends',
                          [task_c])

        DBSession.rollback()

    def test_depends_argument_is_working_properly(self):
        """testing if the depends argument is working properly
        """
        kwargs = copy.copy(self.kwargs)
        kwargs['depends'] = None
        task_a = Task(**kwargs)
        task_b = Task(**kwargs)

        kwargs['depends'] = [task_a, task_b]
        task_c = Task(**kwargs)

        self.assertTrue(task_a in task_c.depends)
        self.assertTrue(task_b in task_c.depends)
        self.assertEqual(len(task_c.depends), 2)

    def test_depends_attribute_is_working_properly(self):
        """testing if the depends attribute is working properly
        """
        kwargs = copy.copy(self.kwargs)
        kwargs['depends'] = None

        task_a = Task(**kwargs)
        task_b = Task(**kwargs)
        task_c = Task(**kwargs)
        #self.data_created.extend([task_a, task_b, task_c])

        task_a.depends = [task_b]
        task_a.depends.append(task_c)

        self.assertTrue(task_b in task_a.depends)
        self.assertTrue(task_c in task_a.depends)

    def test_percent_complete_attribute_is_read_only(self):
        """testing if the percent_complete attribute is a read-only attribute
        """
        kwargs = copy.copy(self.kwargs)
        new_task = Task(**kwargs)

        self.assertRaises(AttributeError, setattr, new_task,
                          'percent_complete', 32)

    def test_percent_complete_attribute_is_working_properly_for_a_leaf_task(self):
        """testing if the percent_complete attribute is working properly for a
        leaf task
        """
        kwargs = copy.copy(self.kwargs)
        kwargs['depends'] = []

        new_task = Task(**kwargs)
        DBSession.add(new_task)
        DBSession.commit()
        self.data_created.append(new_task)

        dt = datetime.datetime
        td = datetime.timedelta
        now = dt.now()

        new_task.time_logs = []
        tlog1 = TimeLog(
            task=new_task,
            resource=new_task.resources[0],
            start=now,
            end=now + td(hours=8)
        )
        DBSession.add(tlog1)
        DBSession.commit()
        self.data_created.append(tlog1)

        self.assertTrue(tlog1 in new_task.time_logs)

        tlog2 = TimeLog(
            task=new_task,
            resource=new_task.resources[1],
            start=now,
            end=now + td(hours=12)
        )
        DBSession.add(tlog2)
        DBSession.commit()
        self.data_created.append(tlog2)

        self.assertTrue(tlog2 in new_task.time_logs)
        self.assertEqual(new_task.total_logged_seconds, 20 * 3600)
        self.assertEqual(new_task.percent_complete, 20.0 / 9.0 * 100.0)
        DBSession.commit()

    def test_percent_complete_attribute_is_working_properly_for_a_duration_based_leaf_task_1(self):
        """testing if the percent_complete attribute is working properly for a
        duration based leaf task

          #########
                     ^
                     |
                    now
        """
        kwargs = copy.copy(self.kwargs)
        kwargs['depends'] = []
        kwargs['schedule_model'] = 'duration'

        dt = datetime.datetime
        td = datetime.timedelta
        now = dt.now()

        new_task = Task(**kwargs)

        new_task.computed_start = now - td(days=2)
        new_task.computed_end = now - td(days=1)

        DBSession.add(new_task)
        DBSession.commit()
        self.data_created.append(new_task)

        self.assertEqual(new_task.percent_complete, 100)
        DBSession.commit()

    def test_percent_complete_attribute_is_working_properly_for_a_duration_based_leaf_task_2(self):
        """testing if the percent_complete attribute is working properly for a
        duration based leaf task

          #########
                  ^
                  |
                 now
        """
        kwargs = copy.copy(self.kwargs)
        kwargs['depends'] = []
        kwargs['schedule_model'] = 'duration'

        dt = datetime.datetime
        td = datetime.timedelta
        now = dt.now()

        new_task = Task(**kwargs)
        new_task.start = now - td(days=1, hours=1)
        new_task.end = now - td(hours=1)

        DBSession.add(new_task)
        DBSession.commit()
        self.data_created.append(new_task)

        self.assertEqual(new_task.percent_complete, 100)
        DBSession.commit()

    def test_percent_complete_attribute_is_working_properly_for_a_duration_based_leaf_task_3(self):
        """testing if the percent_complete attribute is working properly for a
        duration based leaf task

          #########
              ^
              |
             now
        """
        kwargs = copy.copy(self.kwargs)
        kwargs['depends'] = []
        kwargs['schedule_model'] = 'duration'

        dt = datetime.datetime
        td = datetime.timedelta
        now = dt.now()

        new_task = Task(**kwargs)
        new_task.start = now - td(hours=12)
        new_task.end = now + td(hours=12)

        DBSession.add(new_task)
        DBSession.commit()
        self.data_created.append(new_task)

        # it should be somewhere around 50%
        # due to the timing resolution we can not know it exactly
        # and I don't want to patch datetime.datetime.now()
        # this is a very simple test
        self.assertAlmostEqual(
            new_task.percent_complete,
            50,
            delta=5
        )
        DBSession.commit()

    def test_percent_complete_attribute_is_working_properly_for_a_duration_based_leaf_task_4(self):
        """testing if the percent_complete attribute is working properly for a
        duration based leaf task

              #########
              ^
              |
             now
        """
        kwargs = copy.copy(self.kwargs)
        kwargs['depends'] = []
        kwargs['schedule_model'] = 'duration'

        dt = datetime.datetime
        td = datetime.timedelta
        now = dt.now()

        new_task = Task(**kwargs)
        new_task.computed_start = now
        new_task.computed_end = now + td(days=1)

        DBSession.add(new_task)
        DBSession.commit()
        self.data_created.append(new_task)

        self.assertAlmostEqual(
            new_task.percent_complete,
            0,
            delta=5
        )
        DBSession.commit()

    def test_percent_complete_attribute_is_working_properly_for_a_duration_based_leaf_task_5(self):
        """testing if the percent_complete attribute is working properly for a
        duration based leaf task

             #########
           ^
           |
          now
        """
        kwargs = copy.copy(self.kwargs)
        kwargs['depends'] = []
        kwargs['schedule_model'] = 'duration'

        dt = datetime.datetime
        td = datetime.timedelta
        now = dt.now()

        new_task = Task(**kwargs)
        new_task.computed_start = now + td(days=1)
        new_task.computed_end = now + td(days=2)

        DBSession.add(new_task)
        DBSession.commit()
        self.data_created.append(new_task)

        self.assertEqual(new_task.percent_complete, 0)
        DBSession.commit()

    def test_percent_complete_attribute_is_not_using_any_time_logs_for_a_duration_task(self):
        """testing if the percent_complete attribute does not use any time log
        information if the task is a duration based task
        """
        kwargs = copy.copy(self.kwargs)
        kwargs['depends'] = []
        kwargs['schedule_model'] = 'duration'

        dt = datetime.datetime
        td = datetime.timedelta
        now = dt.now()

        new_task = Task(**kwargs)
        new_task.computed_start = now + td(days=1)
        new_task.computed_end = now + td(days=2)

        DBSession.add(new_task)
        DBSession.commit()
        self.data_created.append(new_task)

        tlog1 = TimeLog(
            task=new_task,
            resource=new_task.resources[0],
            start=now + td(days=1),
            end=now + td(days=2)
        )
        DBSession.add(tlog1)
        DBSession.commit()
        self.data_created.append(tlog1)

        self.assertEqual(new_task.percent_complete, 0)
        DBSession.commit()

    def test_percent_complete_attribute_is_working_properly_for_a_container_task(self):
        """testing if the percent complete attribute is working properly for a
        container task
        """
        kwargs = copy.copy(self.kwargs)
        kwargs['depends'] = []  # remove dependencies just to make it
                                # easy to create time logs after stalker
                                # v0.2.6.1

        new_task = Task(**kwargs)
        new_task.status = self.status_rts
        DBSession.add(new_task)
        DBSession.commit()
        self.data_created.append(new_task)

        dt = datetime.datetime
        td = datetime.timedelta
        now = dt.now()

        defaults.timing_resolution = td(hours=1)
        defaults.daily_working_hours = 9

        parent_task = Task(**kwargs)

        new_task.time_logs = []
        tlog1 = TimeLog(
            task=new_task,
            resource=new_task.resources[0],
            start=now - td(hours=4),
            end=now - td(hours=2)
        )
        DBSession.add(tlog1)
        DBSession.commit()
        self.data_created.append(tlog1)

        self.assertTrue(tlog1 in new_task.time_logs)

        tlog2 = TimeLog(
            task=new_task,
            resource=new_task.resources[1],
            start=now - td(hours=4),
            end=now + td(hours=1)
        )
        DBSession.add(tlog2)
        DBSession.commit()
        self.data_created.append(tlog2)

        new_task.parent = parent_task

        self.assertTrue(tlog2 in new_task.time_logs)
        self.assertEqual(new_task.total_logged_seconds, 7 * 3600)
        self.assertEqual(new_task.schedule_seconds, 9 * 3600)
        self.assertAlmostEqual(
            new_task.percent_complete,
            77.7777778,
            delta=0.01
        )
        self.assertAlmostEqual(
            parent_task.percent_complete,
            77.7777778,
            delta=0.01
        )

    def test_is_milestone_argument_is_skipped(self):
        """testing if the default value of the is_milestone attribute is going
        to be False when the is_milestone argument is skipped
        """
        kwargs = copy.copy(self.kwargs)
        kwargs.pop("is_milestone")
        new_task = Task(**kwargs)
        self.assertEqual(new_task.is_milestone, False)

    def test_is_milestone_argument_is_None(self):
        """testing if the is_milestone attribute will be set to False when the
        is_milestone argument is given as None
        """
        kwargs = copy.copy(self.kwargs)
        kwargs["is_milestone"] = None
        new_task = Task(**kwargs)
        self.assertEqual(new_task.is_milestone, False)

    def test_is_milestone_attribute_is_None(self):
        """testing if the is_milestone attribute will be False when set to None
        """
        kwargs = copy.copy(self.kwargs)
        new_task = Task(**kwargs)

        new_task.is_milestone = None
        self.assertEqual(new_task.is_milestone, False)

    def test_is_milestone_argument_is_not_a_bool(self):
        """testing if a TypeError will be raised when the is_milestone argument
        is anything other than a bool
        """
        kwargs = copy.copy(self.kwargs)
        test_values = [1, 0, 1.2, "A string", "", [], [1]]

        for i, test_value in enumerate(test_values):
            kwargs["name"] = "test" + str(i)
            kwargs["is_milestone"] = test_value
            with self.assertRaises(TypeError):
                new_task = Task(**kwargs)

    def test_is_milestone_attribute_is_not_a_bool(self):
        """testing if a TypeError will be raised when the is_milestone
        attribute is set to anything other than a bool value
        """
        kwargs = copy.copy(self.kwargs)
        new_task = Task(**kwargs)

        test_values = [1, 0, 1.2, "A string", "", [], [1]]
        for test_value in test_values:
            with self.assertRaises(TypeError):
                new_task.is_milestone = test_value

    def test_is_milestone_argument_makes_the_resources_list_an_empty_list(self):
        """testing if the resources will be an empty list when the is_milestone
        argument is given as True
        """
        kwargs = copy.copy(self.kwargs)
        kwargs["is_milestone"] = True
        kwargs["resources"] = [self.test_user1, self.test_user2]
        new_task = Task(**kwargs)
        self.data_created.append(new_task)
        DBSession.commit()

        self.assertEqual(new_task.resources, [])

    def test_is_milestone_attribute_makes_the_resource_list_an_empty_list(self):
        """testing if the resources will be an empty list when the is_milestone
        attribute is given as True
        """
        kwargs = copy.copy(self.kwargs)
        new_task = Task(**kwargs)
        self.data_created.append(new_task)
        DBSession.add(new_task)
        DBSession.commit()

        new_task.resources = [self.test_user1, self.test_user2]
        new_task.is_milestone = True
        self.assertEqual(new_task.resources, [])

    def test_time_logs_attribute_is_None(self):
        """testing if a TypeError will be raised when the time_logs attribute
        is set to None
        """
        new_task = Task(**self.kwargs)
        self.assertRaises(
            TypeError, setattr, new_task, "time_logs", None
        )

    def test_time_logs_attribute_is_not_a_list(self):
        """testing if a TypeError will be raised when the time_logs attribute
        is not set to a list
        """
        new_task = Task(**self.kwargs)
        self.assertRaises(TypeError, setattr, new_task, "time_logs", 123)

    def test_time_logs_attribute_is_not_a_list_of_TimeLog_instances(self):
        """testing if a TypeError will be raised when the time_logs attribute
        is not a list of TimeLog instances
        """
        new_task = Task(**self.kwargs)
        self.assertRaises(TypeError, setattr, new_task, "time_logs",
                          [1, "1", 1.2, "a time_log", []])

    def test_time_logs_attribute_is_working_properly(self):
        """testing if the time_log attribute is working properly
        """
        kwargs = copy.copy(self.kwargs)
        kwargs['depends'] = []
        new_task1 = Task(**kwargs)

        DBSession.add(new_task1)
        DBSession.commit()
        self.data_created.append(new_task1)
        self.assertEqual(new_task1.depends, [])

        now = datetime.datetime.now()
        dt = datetime.timedelta

        new_time_log1 = TimeLog(
            task=new_task1,
            resource=new_task1.resources[0],
            start=now + dt(100),
            end=now + dt(101)
        )
        self.data_created.append(new_time_log1)

        new_time_log2 = TimeLog(
            task=new_task1,
            resource=new_task1.resources[0],
            start=now + dt(101),
            end=now + dt(102)
        )
        self.data_created.append(new_time_log2)

        # create a new task
        kwargs['name'] = 'New Task'
        new_task2 = Task(**kwargs)
        DBSession.add(new_task2)
        DBSession.commit()
        self.data_created.append(new_task2)

        # create a new TimeLog for that task
        new_time_log3 = TimeLog(
            task=new_task2,
            resource=new_task2.resources[0],
            start=now + dt(102),
            end=now + dt(103)
        )
        self.data_created.append(new_time_log3)
        logger.debug('Task.query.get(37): %s' % Task.query.get(37))

        self.assertEqual(new_task2.depends, [])

        logger.debug('new_task.id : %s' % new_task2.id)

        DBSession.add_all([new_time_log1, new_time_log2, new_time_log3])
        DBSession.commit()

        # check if everything is in place
        self.assertTrue(new_time_log1 in new_task1.time_logs)
        self.assertTrue(new_time_log2 in new_task1.time_logs)
        self.assertTrue(new_time_log3 in new_task2.time_logs)

        # now move the time_log to test_task1
        new_task1.time_logs.append(new_time_log3)

        # check if new_time_log3 is in test_task1
        self.assertTrue(new_time_log3 in new_task1.time_logs)

        # there needs to be a database session commit to remove the time_log
        # from the previous tasks time_logs attribute

        DBSession.commit()

        self.assertTrue(new_time_log3 in new_task1.time_logs)
        self.assertFalse(new_time_log3 in new_task2.time_logs)

    def test_total_logged_seconds_is_the_sum_of_all_time_logs(self):
        """testing if the total_logged_seconds is the sum of all time_logs in
        hours
        """
        kwargs = copy.copy(self.kwargs)
        kwargs['depends'] = []

        new_task = Task(**kwargs)
        DBSession.add(new_task)
        DBSession.commit()
        self.data_created.append(new_task)

        new_task.depends = []

        dt = datetime.datetime
        td = datetime.timedelta
        now = dt.now()

        new_task.time_logs = []
        tlog1 = TimeLog(
            task=new_task,
            resource=new_task.resources[0],
            start=now,
            end=now + td(hours=8)
        )
        DBSession.add(tlog1)
        DBSession.commit()
        self.data_created.append(tlog1)

        self.assertTrue(tlog1 in new_task.time_logs)

        tlog2 = TimeLog(
            task=new_task,
            resource=new_task.resources[1],
            start=now,
            end=now + td(hours=12)
        )
        DBSession.add(tlog2)
        DBSession.commit()
        self.data_created.append(tlog2)

        self.assertTrue(tlog2 in new_task.time_logs)
        self.assertEqual(new_task.total_logged_seconds, 20 * 3600)

    def test_total_logged_seconds_is_the_sum_of_all_time_logs_of_children_for_a_container_task(self):
        """testing if the total_logged_seconds is the sum of all time_logs of
        the child tasks for a container task
        """
        kwargs = copy.copy(self.kwargs)
        kwargs['depends'] = []

        new_task = Task(**kwargs)
        DBSession.add(new_task)
        DBSession.commit()
        self.data_created.append(new_task)

        dt = datetime.datetime
        td = datetime.timedelta
        now = dt.now()

        kwargs.pop('schedule_timing')
        kwargs.pop('schedule_unit')
        parent_task = Task(**kwargs)
        DBSession.add(parent_task)
        DBSession.commit()
        self.data_created.append(parent_task)

        new_task.parent = parent_task

        new_task.time_logs = []
        tlog1 = TimeLog(
            task=new_task,
            resource=new_task.resources[0],
            start=now,
            end=now + td(hours=8)
        )
        DBSession.add(tlog1)
        DBSession.commit()
        self.data_created.append(tlog1)

        self.assertTrue(tlog1 in new_task.time_logs)

        tlog2 = TimeLog(
            task=new_task,
            resource=new_task.resources[1],
            start=now,
            end=now + td(hours=12)
        )
        DBSession.add(tlog2)
        DBSession.commit()
        self.data_created.append(tlog2)

        self.assertTrue(tlog2 in new_task.time_logs)
        self.assertEqual(new_task.total_logged_seconds, 20 * 3600)
        self.assertEqual(parent_task.total_logged_seconds, 20 * 3600)

    def test_total_logged_seconds_is_the_sum_of_all_time_logs_of_children_for_a_container_task_deeper(self):
        """testing if the total_logged_seconds is the sum of all time_logs of
        the child tasks for a container task (test deeper)
        """
        kwargs = copy.copy(self.kwargs)
        kwargs['depends'] = []

        new_task = Task(**kwargs)
        DBSession.add(new_task)
        DBSession.commit()
        self.data_created.append(new_task)

        dt = datetime.datetime
        td = datetime.timedelta
        now = dt.now()

        kwargs.pop('schedule_timing')
        kwargs.pop('schedule_unit')

        parent_task1 = Task(**kwargs)
        DBSession.add(parent_task1)
        DBSession.commit()
        self.data_created.append(parent_task1)
        self.assertEqual(parent_task1.total_logged_seconds, 0)

        parent_task2 = Task(**kwargs)
        DBSession.add(parent_task2)
        DBSession.commit()
        self.data_created.append(parent_task2)
        self.assertEqual(parent_task2.total_logged_seconds, 0)

        # create some other child
        child = Task(**kwargs)
        DBSession.add(child)
        DBSession.commit()
        self.data_created.append(child)

        self.assertEqual(child.total_logged_seconds, 0)
        # create a TimeLog for that child
        tlog1 = TimeLog(
            task=child,
            resource=child.resources[0],
            start=now - td(hours=50),
            end=now - td(hours=40)
        )
        DBSession.add(tlog1)
        DBSession.commit()
        self.data_created.append(tlog1)

        self.assertEqual(child.total_logged_seconds, 10 * 3600)
        parent_task2.children.append(child)
        self.assertEqual(parent_task2.total_logged_seconds, 10 * 3600)

        # self.test_task1.parent = parent_task
        parent_task1.children.append(new_task)
        self.assertEqual(parent_task1.total_logged_seconds, 0)

        parent_task1.parent = parent_task2
        self.assertEqual(parent_task2.total_logged_seconds, 10 * 3600)

        new_task.time_logs = []
        tlog2 = TimeLog(
            task=new_task,
            resource=new_task.resources[0],
            start=now,
            end=now + td(hours=8)
        )
        DBSession.add(tlog2)
        DBSession.commit()
        self.data_created.append(tlog2)

        self.assertTrue(tlog2 in new_task.time_logs)
        self.assertEqual(new_task.total_logged_seconds, 8 * 3600)
        self.assertEqual(parent_task1.total_logged_seconds, 8 * 3600)
        self.assertEqual(parent_task2.total_logged_seconds, 18 * 3600)

        tlog3 = TimeLog(
            task=new_task,
            resource=new_task.resources[1],
            start=now,
            end=now + td(hours=12)
        )
        DBSession.add(tlog3)
        DBSession.commit()
        self.data_created.append(tlog3)

        self.assertEqual(new_task.total_logged_seconds, 20 * 3600)
        self.assertEqual(parent_task1.total_logged_seconds, 20 * 3600)
        self.assertEqual(parent_task2.total_logged_seconds, 30 * 3600)

    def test_total_logged_seconds_attribute_is_working_properly_for_a_container_task_when_the_time_log_of_child_is_changed(self):
        """testing if the total_logged_seconds attribute is working properly
        for a container task when one of the time logs of one of the children
        of the task is changed
        """
        kwargs = copy.copy(self.kwargs)
        kwargs['depends'] = []
        new_task = Task(**kwargs)
        DBSession.add(new_task)
        DBSession.commit()
        self.data_created.append(new_task)

        dt = datetime.datetime
        td = datetime.timedelta
        now = dt.now()

        parent_task = Task(**kwargs)
        DBSession.add(parent_task)
        DBSession.commit()
        self.data_created.append(parent_task)

        child_task = Task(**kwargs)
        DBSession.add(child_task)
        DBSession.commit()
        self.data_created.append(child_task)

        parent_task.children.append(child_task)

        tlog1 = TimeLog(
            task=child_task,
            resource=child_task.resources[0],
            start=now,
            end=now + td(hours=8)
        )
        DBSession.add(tlog1)
        DBSession.commit()
        self.data_created.append(tlog1)

        self.assertEqual(
            parent_task.total_logged_seconds, 8 * 60 * 60
        )

        # now update the time log
        tlog1.end = now + td(hours=16)
        self.assertEqual(
            parent_task.total_logged_seconds, 16 * 60 * 60
        )

    def test_schedule_seconds_is_working_properly_for_an_effort_based_task_no_studio(self):
        """testing if schedule_seconds attribute is working properly for a
        effort based task on an environment where there are no studio
        """
        # no studio, using defaults
        kwargs = copy.copy(self.kwargs)
        kwargs['schedule_model'] = 'effort'

        kwargs['schedule_timing'] = 10
        kwargs['schedule_unit'] = 'h'
        new_task = Task(**kwargs)
        DBSession.add(new_task)
        DBSession.commit()
        self.data_created.append(new_task)

        self.assertEqual(new_task.schedule_seconds, 10 * 3600)

        kwargs['schedule_timing'] = 23
        kwargs['schedule_unit'] = 'd'
        new_task = Task(**kwargs)
        DBSession.add(new_task)
        DBSession.commit()
        self.data_created.append(new_task)

        self.assertEqual(
            new_task.schedule_seconds,
            23 * defaults.daily_working_hours * 3600
        )

        kwargs['schedule_timing'] = 2
        kwargs['schedule_unit'] = 'w'
        new_task = Task(**kwargs)
        DBSession.add(new_task)
        DBSession.commit()
        self.data_created.append(new_task)

        self.assertEqual(
            new_task.schedule_seconds,
            2 * defaults.weekly_working_hours * 3600
        )

        kwargs['schedule_timing'] = 2.5
        kwargs['schedule_unit'] = 'm'
        new_task = Task(**kwargs)
        DBSession.add(new_task)
        DBSession.commit()
        self.data_created.append(new_task)

        self.assertEqual(
            new_task.schedule_seconds,
            2.5 * 4 * defaults.weekly_working_hours * 3600
        )

        kwargs['schedule_timing'] = 3.1
        kwargs['schedule_unit'] = 'y'
        new_task = Task(**kwargs)
        DBSession.add(new_task)
        DBSession.commit()
        self.data_created.append(new_task)

        self.assertAlmostEqual(
            new_task.schedule_seconds,
            3.1 * defaults.yearly_working_days *
            defaults.daily_working_hours * 3600,
            3
        )

    def test_schedule_seconds_is_working_properly_for_an_effort_based_task_with_studio(self):
        """testing if schedule_seconds attribute is working properly for a
        effort based task where there is a studio present
        """
        kwargs = copy.copy(self.kwargs)
        # no studio, using defaults
        from stalker import Studio

        defaults.timing_resolution = datetime.timedelta(hours=1)

        studio = Studio(
            name='Test Studio',
            timing_resolution=datetime.timedelta(hours=1)
        )
        DBSession.add(studio)
        DBSession.commit()
        self.data_created.append(studio)

        kwargs['schedule_model'] = 'effort'

        kwargs['schedule_timing'] = 10
        kwargs['schedule_unit'] = 'h'
        new_task = Task(**kwargs)
        DBSession.add(new_task)
        DBSession.commit()
        self.data_created.append(new_task)

        self.assertEqual(new_task.schedule_seconds, 10 * 3600)

        kwargs['schedule_timing'] = 23
        kwargs['schedule_unit'] = 'd'
        new_task = Task(**kwargs)
        DBSession.add(new_task)
        DBSession.commit()
        self.data_created.append(new_task)

        self.assertEqual(
            new_task.schedule_seconds,
            23 * studio.daily_working_hours * 3600
        )

        kwargs['schedule_timing'] = 2
        kwargs['schedule_unit'] = 'w'
        new_task = Task(**kwargs)
        DBSession.add(new_task)
        DBSession.commit()
        self.data_created.append(new_task)

        self.assertEqual(
            new_task.schedule_seconds,
            2 * studio.weekly_working_hours * 3600
        )

        kwargs['schedule_timing'] = 2.5
        kwargs['schedule_unit'] = 'm'
        new_task = Task(**kwargs)
        DBSession.add(new_task)
        DBSession.commit()
        self.data_created.append(new_task)

        self.assertEqual(
            new_task.schedule_seconds,
            2.5 * 4 * studio.weekly_working_hours * 3600
        )

        kwargs['schedule_timing'] = 3.1
        kwargs['schedule_unit'] = 'y'
        new_task = Task(**kwargs)
        DBSession.add(new_task)
        DBSession.commit()
        self.data_created.append(new_task)

        self.assertAlmostEqual(
            new_task.schedule_seconds,
            3.1 * studio.yearly_working_days * studio.daily_working_hours *
            3600,
            3
        )

    def test_schedule_seconds_is_working_properly_for_a_container_task(self):
        """testing if schedule_seconds attribute is working properly for a
        container task
        """
        # no studio, using defaults
        kwargs = copy.copy(self.kwargs)
        parent_task = Task(**kwargs)
        DBSession.add(parent_task)
        DBSession.commit()
        self.data_created.append(parent_task)

        kwargs['schedule_model'] = 'effort'

        kwargs['schedule_timing'] = 10
        kwargs['schedule_unit'] = 'h'
        new_task = Task(**kwargs)
        DBSession.add(new_task)
        DBSession.commit()
        self.data_created.append(new_task)

        self.assertEqual(new_task.schedule_seconds, 10 * 3600)
        new_task.parent = parent_task
        self.assertEqual(parent_task.schedule_seconds, 10 * 3600)

        kwargs['schedule_timing'] = 23
        kwargs['schedule_unit'] = 'd'
        new_task = Task(**kwargs)
        DBSession.add(new_task)
        DBSession.commit()
        self.data_created.append(new_task)

        self.assertEqual(
            new_task.schedule_seconds,
            23 * defaults.daily_working_hours * 3600
        )
        new_task.parent = parent_task
        self.assertEqual(
            parent_task.schedule_seconds,
            10 * 3600 + 23 * defaults.daily_working_hours * 3600
        )

        kwargs['schedule_timing'] = 2
        kwargs['schedule_unit'] = 'w'
        new_task = Task(**kwargs)
        DBSession.add(new_task)
        DBSession.commit()
        self.data_created.append(new_task)

        self.assertEqual(
            new_task.schedule_seconds,
            2 * defaults.weekly_working_hours * 3600
        )
        new_task.parent = parent_task
        self.assertEqual(
            parent_task.schedule_seconds,
            10 * 3600 + 23 * defaults.daily_working_hours * 3600 +
            2 * defaults.weekly_working_hours * 3600
        )

        kwargs['schedule_timing'] = 2.5
        kwargs['schedule_unit'] = 'm'
        new_task = Task(**kwargs)
        DBSession.add(new_task)
        DBSession.commit()
        self.data_created.append(new_task)

        self.assertEqual(
            new_task.schedule_seconds,
            2.5 * 4 * defaults.weekly_working_hours * 3600
        )
        new_task.parent = parent_task
        self.assertEqual(
            parent_task.schedule_seconds,
            10 * 3600 + 23 * defaults.daily_working_hours * 3600 +
            2 * defaults.weekly_working_hours * 3600 +
            2.5 * 4 * defaults.weekly_working_hours * 3600
        )

        kwargs['schedule_timing'] = 3.1
        kwargs['schedule_unit'] = 'y'
        new_task = Task(**kwargs)
        DBSession.add(new_task)
        DBSession.commit()
        self.data_created.append(new_task)

        self.assertAlmostEqual(
            new_task.schedule_seconds,
            3.1 * defaults.yearly_working_days * defaults.daily_working_hours *
            3600, 3
        )
        new_task.parent = parent_task
        self.assertAlmostEqual(
            parent_task.schedule_seconds,
            10 * 3600 + 23 * defaults.daily_working_hours * 3600 +
            2 * defaults.weekly_working_hours * 3600 +
            2.5 * 4 * defaults.weekly_working_hours * 3600 +
            3.1 * defaults.yearly_working_days *
            defaults.daily_working_hours * 3600,
            3
        )

    def test_schedule_seconds_is_working_properly_for_a_container_task_when_the_child_is_updated(self):
        """testing if schedule_seconds attribute is working properly for a
        container task
        """
        kwargs = copy.copy(self.kwargs)
        # no studio, using defaults
        parent_task = Task(**kwargs)
        DBSession.add(parent_task)
        DBSession.commit()
        self.data_created.append(parent_task)

        kwargs['schedule_model'] = 'effort'

        kwargs['schedule_timing'] = 10
        kwargs['schedule_unit'] = 'h'
        new_task = Task(**kwargs)
        DBSession.add(new_task)
        DBSession.commit()
        self.data_created.append(new_task)

        self.assertEqual(new_task.schedule_seconds, 10 * 3600)
        new_task.parent = parent_task
        self.assertEqual(parent_task.schedule_seconds, 10 * 3600)

        # update the schedule_timing of the child
        new_task.schedule_timing = 5
        self.assertEqual(new_task.schedule_seconds, 5 * 3600)
        new_task.parent = parent_task
        self.assertEqual(parent_task.schedule_seconds, 5 * 3600)

        # update it back to 10 hours
        new_task.schedule_timing = 10
        self.assertEqual(new_task.schedule_seconds, 10 * 3600)
        new_task.parent = parent_task
        self.assertEqual(parent_task.schedule_seconds, 10 * 3600)

        kwargs['schedule_timing'] = 23
        kwargs['schedule_unit'] = 'd'
        new_task = Task(**kwargs)
        DBSession.add(new_task)
        DBSession.commit()
        self.data_created.append(new_task)

        self.assertEqual(
            new_task.schedule_seconds,
            23 * defaults.daily_working_hours * 3600
        )
        new_task.parent = parent_task
        self.assertEqual(
            parent_task.schedule_seconds,
            10 * 3600 + 23 * defaults.daily_working_hours * 3600
        )

        kwargs['schedule_timing'] = 2
        kwargs['schedule_unit'] = 'w'
        new_task = Task(**kwargs)
        DBSession.add(new_task)
        DBSession.commit()
        self.data_created.append(new_task)

        self.assertEqual(
            new_task.schedule_seconds,
            2 * defaults.weekly_working_hours * 3600
        )
        new_task.parent = parent_task
        self.assertEqual(
            parent_task.schedule_seconds,
            10 * 3600 + 23 * defaults.daily_working_hours * 3600 +
            2 * defaults.weekly_working_hours * 3600
        )

        kwargs['schedule_timing'] = 2.5
        kwargs['schedule_unit'] = 'm'
        new_task = Task(**kwargs)
        DBSession.add(new_task)
        DBSession.commit()
        self.data_created.append(new_task)

        self.assertEqual(
            new_task.schedule_seconds,
            2.5 * 4 * defaults.weekly_working_hours * 3600
        )
        new_task.parent = parent_task
        self.assertEqual(
            parent_task.schedule_seconds,
            10 * 3600 + 23 * defaults.daily_working_hours * 3600 +
            2 * defaults.weekly_working_hours * 3600 +
            2.5 * 4 * defaults.weekly_working_hours * 3600
        )

        kwargs['schedule_timing'] = 3.1
        kwargs['schedule_unit'] = 'y'
        new_task = Task(**kwargs)
        DBSession.add(new_task)
        DBSession.commit()
        self.data_created.append(new_task)

        self.assertAlmostEqual(
            new_task.schedule_seconds,
            3.1 * defaults.yearly_working_days * defaults.daily_working_hours *
            3600
        )
        new_task.parent = parent_task
        self.assertAlmostEqual(
            parent_task.schedule_seconds,
            10 * 3600 + 23 * defaults.daily_working_hours * 3600 +
            2 * defaults.weekly_working_hours * 3600 +
            2.5 * 4 * defaults.weekly_working_hours * 3600 +
            3.1 * defaults.yearly_working_days *
            defaults.daily_working_hours * 3600,
            3
        )

    def test_schedule_seconds_is_working_properly_for_a_container_task_when_the_child_is_updated_deeper(self):
        """testing if schedule_seconds attribute is working properly for a
        container task
        """
        kwargs = copy.copy(self.kwargs)
        defaults.timing_resolution = datetime.timedelta(hours=1)
        defaults.daily_working_hours = 9

        # no studio, using defaults
        parent_task1 = Task(**kwargs)
        DBSession.add(parent_task1)
        DBSession.commit()
        self.data_created.append(parent_task1)

        self.assertEqual(parent_task1.schedule_seconds, 9 * 3600)

        parent_task2 = Task(**kwargs)
        DBSession.add(parent_task2)
        DBSession.commit()
        self.data_created.append(parent_task2)

        self.assertEqual(parent_task2.schedule_seconds, 9 * 3600)
        parent_task2.schedule_timing = 5
        self.assertEqual(parent_task2.schedule_seconds, 5 * 9 * 3600)
        parent_task2.schedule_unit = 'h'
        self.assertEqual(parent_task2.schedule_seconds, 5 * 3600)

        parent_task1.parent = parent_task2
        self.assertEqual(parent_task2.schedule_seconds, 9 * 3600)

        # create another child task for parent_task2
        child_task = Task(**kwargs)
        DBSession.add(child_task)
        DBSession.commit()
        self.data_created.append(child_task)

        child_task.schedule_timing = 10
        child_task.schedule_unit = 'h'
        self.assertEqual(child_task.schedule_seconds, 10 * 3600)

        parent_task2.children.append(child_task)
        self.assertEqual(parent_task2.schedule_seconds, 10 * 3600 + 9 * 3600)

        kwargs['schedule_model'] = 'effort'
        kwargs['schedule_timing'] = 10
        kwargs['schedule_unit'] = 'h'
        new_task = Task(**kwargs)
        DBSession.add(new_task)
        DBSession.commit()
        self.data_created.append(new_task)

        self.assertEqual(new_task.schedule_seconds, 10 * 3600)
        new_task.parent = parent_task1
        self.assertEqual(parent_task1.schedule_seconds, 10 * 3600)
        self.assertEqual(parent_task2.schedule_seconds, 10 * 3600 + 10 * 3600)

        # update the schedule_timing of the child
        new_task.schedule_timing = 5
        self.assertEqual(new_task.schedule_seconds, 5 * 3600)
        new_task.parent = parent_task1
        self.assertEqual(parent_task1.schedule_seconds, 5 * 3600)
        self.assertEqual(parent_task2.schedule_seconds, 5 * 3600 + 10 * 3600)

        # update it back to 10 hours
        new_task.schedule_timing = 10
        self.assertEqual(new_task.schedule_seconds, 10 * 3600)
        new_task.parent = parent_task1
        self.assertEqual(parent_task1.schedule_seconds, 10 * 3600)
        self.assertEqual(parent_task2.schedule_seconds, 10 * 3600 + 10 * 3600)

        kwargs['schedule_timing'] = 23
        kwargs['schedule_unit'] = 'd'
        new_task = Task(**kwargs)
        DBSession.add(new_task)
        DBSession.commit()
        self.data_created.append(new_task)

        self.assertEqual(
            new_task.schedule_seconds,
            23 * defaults.daily_working_hours * 3600
        )
        new_task.parent = parent_task1
        self.assertEqual(
            parent_task1.schedule_seconds,
            10 * 3600 + 23 * defaults.daily_working_hours * 3600
        )
        self.assertEqual(
            parent_task2.schedule_seconds,
            10 * 3600 + 23 * defaults.daily_working_hours * 3600 +
            10 * 3600
        )

        kwargs['schedule_timing'] = 2
        kwargs['schedule_unit'] = 'w'
        new_task = Task(**kwargs)
        DBSession.add(new_task)
        DBSession.commit()
        self.data_created.append(new_task)

        self.assertEqual(
            new_task.schedule_seconds,
            2 * defaults.weekly_working_hours * 3600
        )
        new_task.parent = parent_task1
        self.assertEqual(
            parent_task1.schedule_seconds,
            10 * 3600 + 23 * defaults.daily_working_hours * 3600 +
            2 * defaults.weekly_working_hours * 3600
        )

        # update it to 1 week
        new_task.schedule_timing = 1
        self.assertEqual(
            parent_task1.schedule_seconds,
            10 * 3600 + 23 * defaults.daily_working_hours * 3600 +
            1 * defaults.weekly_working_hours * 3600
        )
        self.assertEqual(
            parent_task2.schedule_seconds,
            10 * 3600 + 23 * defaults.daily_working_hours * 3600 +
            1 * defaults.weekly_working_hours * 3600 + 10 * 3600
        )

        kwargs['schedule_timing'] = 2.5
        kwargs['schedule_unit'] = 'm'
        new_task = Task(**kwargs)
        DBSession.add(new_task)
        DBSession.commit()
        self.data_created.append(new_task)

        self.assertEqual(
            new_task.schedule_seconds,
            2.5 * 4 * defaults.weekly_working_hours * 3600
        )
        new_task.parent = parent_task1
        self.assertEqual(
            parent_task1.schedule_seconds,
            10 * 3600 + 23 * defaults.daily_working_hours * 3600 +
            1 * defaults.weekly_working_hours * 3600 +
            2.5 * 4 * defaults.weekly_working_hours * 3600
        )
        self.assertEqual(
            parent_task2.schedule_seconds,
            10 * 3600 + 23 * defaults.daily_working_hours * 3600 +
            1 * defaults.weekly_working_hours * 3600 +
            2.5 * 4 * defaults.weekly_working_hours * 3600 +
            10 * 3600
        )

        kwargs['schedule_timing'] = 3.1
        kwargs['schedule_unit'] = 'y'
        new_task = Task(**kwargs)
        DBSession.add(new_task)
        DBSession.commit()
        self.data_created.append(new_task)

        self.assertAlmostEqual(
            new_task.schedule_seconds,
            3.1 * defaults.yearly_working_days * defaults.daily_working_hours *
            3600,
            3
        )
        new_task.parent = parent_task1
        self.assertAlmostEqual(
            parent_task1.schedule_seconds,
            10 * 3600 + 23 * defaults.daily_working_hours * 3600 +
            1 * defaults.weekly_working_hours * 3600 +
            2.5 * 4 * defaults.weekly_working_hours * 3600 +
            3.1 * defaults.yearly_working_days *
            defaults.daily_working_hours * 3600,
            3
        )
        self.assertAlmostEqual(
            parent_task2.schedule_seconds,
            10 * 3600 + 23 * defaults.daily_working_hours * 3600 +
            1 * defaults.weekly_working_hours * 3600 +
            2.5 * 4 * defaults.weekly_working_hours * 3600 +
            3.1 * defaults.yearly_working_days *
            defaults.daily_working_hours * 3600 + 10 * 3600,
            3
        )

    def test_remaining_seconds_attribute_is_a_read_only_attribute(self):
        """testing if the remaining hours is a read only attribute
        """
        new_task = Task(**self.kwargs)
        with self.assertRaises(AttributeError):
            setattr(new_task, 'remaining_seconds', 2342)

    def test_remaining_seconds_is_working_properly(self):
        """testing if the remaining hours is working properly
        """
        kwargs = copy.copy(self.kwargs)
        kwargs['depends'] = []

        dt = datetime.datetime
        td = datetime.timedelta
        now = dt(2013, 4, 19, 10, 0)

        kwargs['schedule_model'] = 'effort'

        # -------------- HOURS --------------
        kwargs['schedule_timing'] = 10
        kwargs['schedule_unit'] = 'h'
        new_task = Task(**kwargs)
        DBSession.add(new_task)
        DBSession.commit()
        self.data_created.append(new_task)

        # create a time_log of 2 hours
        tlog1 = TimeLog(
            task=new_task,
            start=now,
            duration=td(hours=2),
            resource=new_task.resources[0]
        )
        DBSession.add(tlog1)
        DBSession.commit()
        self.data_created.append(tlog1)

        # check
        self.assertEqual(
            new_task.remaining_seconds,
            new_task.schedule_seconds - new_task.total_logged_seconds
        )

        # -------------- DAYS --------------
        kwargs['schedule_timing'] = 23
        kwargs['schedule_unit'] = 'd'
        new_task = Task(**kwargs)
        DBSession.add(new_task)
        DBSession.commit()
        self.data_created.append(new_task)

        # create a time_log of 5 days
        tlog2 = TimeLog(
            task=new_task,
            start=now + td(hours=2),
            end=now + td(days=5),
            resource=new_task.resources[0]
        )
        DBSession.add(tlog2)
        DBSession.commit()
        self.data_created.append(tlog2)

        # check
        self.assertEqual(
            new_task.remaining_seconds,
            new_task.schedule_seconds - new_task.total_logged_seconds
        )

        # add another 2 hours
        tlog3 = TimeLog(
            task=new_task,
            start=now + td(days=5),
            duration=td(hours=2),
            resource=new_task.resources[0]
        )
        DBSession.add(tlog3)
        DBSession.commit()
        self.data_created.append(tlog3)

        self.assertEqual(
            new_task.remaining_seconds,
            new_task.schedule_seconds - new_task.total_logged_seconds
        )

        # ------------------- WEEKS ------------------
        kwargs['schedule_timing'] = 2
        kwargs['schedule_unit'] = 'w'
        new_task = Task(**kwargs)
        DBSession.add(new_task)
        DBSession.commit()
        self.data_created.append(new_task)

        # create a time_log of 2 hours
        tlog4 = TimeLog(
            task=new_task,
            start=now + td(days=6),
            duration=td(hours=2),
            resource=new_task.resources[0]
        )
        DBSession.add(tlog4)
        DBSession.commit()
        self.data_created.append(tlog4)
        new_task.time_logs.append(tlog4)

        # check
        self.assertEqual(
            new_task.remaining_seconds,
            new_task.schedule_seconds - new_task.total_logged_seconds
        )

        # create a time_log of 1 week
        tlog5 = TimeLog(
            task=new_task,
            start=now + td(days=7),
            duration=td(weeks=1),
            resource=new_task.resources[0]
        )
        DBSession.add(tlog5)
        DBSession.commit()
        self.data_created.append(tlog5)
        new_task.time_logs.append(tlog5)

        # check
        self.assertEqual(
            new_task.remaining_seconds,
            new_task.schedule_seconds - new_task.total_logged_seconds
        )

        # ------------------ MONTH -------------------
        kwargs['schedule_timing'] = 2.5
        kwargs['schedule_unit'] = 'm'
        new_task = Task(**kwargs)
        DBSession.add(new_task)
        DBSession.commit()
        self.data_created.append(new_task)

        # create a time_log of 1 months or 30 days, remaining_seconds can be
        # negative
        tlog6 = TimeLog(
            task=new_task,
            start=now + td(days=15),
            duration=td(days=30),
            resource=new_task.resources[0]
        )
        DBSession.add(tlog6)
        DBSession.commit()
        self.data_created.append(tlog6)
        new_task.time_logs.append(tlog6)

        # check
        self.assertEqual(
            new_task.remaining_seconds,
            new_task.schedule_seconds - new_task.total_logged_seconds
        )

        # ------------------ YEARS ---------------------
        kwargs['schedule_timing'] = 3.1
        kwargs['schedule_unit'] = 'y'
        new_task = Task(**kwargs)
        DBSession.add(new_task)
        DBSession.commit()
        self.data_created.append(new_task)

        # create a time_log of 1 months or 30 days, remaining_seconds can be
        # negative
        tlog8 = TimeLog(
            task=new_task,
            start=now + td(days=55),
            duration=td(days=30),
            resource=new_task.resources[0]
        )
        DBSession.add(tlog8)
        DBSession.commit()
        self.data_created.append(tlog8)

        new_task.time_logs.append(tlog8)

        # check
        self.assertEqual(
            new_task.remaining_seconds,
            new_task.schedule_seconds - new_task.total_logged_seconds
        )

    def test_versions_attribute_is_None(self):
        """testing if a TypeError will be raised when the versions attribute
        is set to None
        """
        new_task = Task(**self.kwargs)
        with self.assertRaises(TypeError):
            new_task.versions = None

    def test_versions_attribute_is_not_a_list(self):
        """testing if a TypeError will be raised when the versions attribute is
        set to a value other than a list
        """
        new_task = Task(**self.kwargs)
        with self.assertRaises(TypeError):
            new_task.versions = 1

    def test_versions_attribute_is_not_a_list_of_Version_instances(self):
        """testing if a TypeError will be raised when the versions attribute is
        set to a list of other objects than Version instances
        """
        new_task = Task(**self.kwargs)
        with self.assertRaises(TypeError):
            new_task.versions = [1, 1.2, "a version"]

    def test_equality(self):
        """testing the equality operator
        """
        kwargs = copy.copy(self.kwargs)
        new_task = Task(**kwargs)

        entity1 = Entity(**kwargs)
        task0 = Task(**kwargs)
        task1 = Task(**kwargs)
        task2 = Task(**kwargs)
        task3 = Task(**kwargs)
        task4 = Task(**kwargs)
        task5 = Task(**kwargs)
        task6 = Task(**kwargs)

        task1.depends = [task2]
        task2.parent = task3
        task3.parent = task4
        task5.children = [task6]
        task6.depends = [task2]

        self.assertFalse(new_task == entity1)
        self.assertTrue(new_task == task0)
        self.assertFalse(new_task == task1)
        self.assertFalse(new_task == task5)

        self.assertFalse(task1 == task2)
        self.assertFalse(task1 == task3)
        self.assertFalse(task1 == task4)

        self.assertFalse(task2 == task3)
        self.assertFalse(task2 == task4)

        self.assertFalse(task3 == task4)

        self.assertFalse(task5 == task6)

        # check task with same names but different projects

    def test_inequality(self):
        """testing the inequality operator
        """
        kwargs = copy.copy(self.kwargs)
        new_task = Task(**kwargs)

        new_entity1 = Entity(**kwargs)
        new_task2 = Task(**kwargs)

        entity1 = Entity(**kwargs)
        task0 = Task(**kwargs)
        task1 = Task(**kwargs)
        task2 = Task(**kwargs)
        task3 = Task(**kwargs)
        task4 = Task(**kwargs)
        task5 = Task(**kwargs)
        task6 = Task(**kwargs)

        task1.depends = [task2]
        task2.parent = task3
        task3.parent = task4
        task5.children = [task6]

        self.assertTrue(new_task != entity1)
        self.assertFalse(new_task != task0)
        self.assertTrue(new_task != task1)
        self.assertTrue(new_task != task5)

        self.assertTrue(task1 != task2)
        self.assertTrue(task1 != task3)
        self.assertTrue(task1 != task4)

        self.assertTrue(task2 != task3)
        self.assertTrue(task2 != task4)

        self.assertTrue(task3 != task4)

        self.assertTrue(task5 != task6)

    def test_parent_argument_is_skipped_there_is_a_project_arg(self):
        """testing if the Task is still be able to be created without a parent
        if a Project is supplied with the project argument
        """
        kwargs = copy.copy(self.kwargs)
        try:
            kwargs.pop('parent')
        except KeyError:
            pass

        kwargs['project'] = self.test_project1
        new_task = Task(**kwargs)
        self.assertEqual(new_task.project, self.test_project1)

    # parent arg there but project skipped already tested
    # both skipped already tested

    def test_parent_argument_is_None_but_there_is_a_project_arg(self):
        """testing if the task is still be able to be created without a parent
        if a Project is supplied with the project argument
        """
        kwargs = copy.copy(self.kwargs)
        kwargs['parent'] = None
        kwargs['project'] = self.test_project1
        new_task = Task(**kwargs)
        self.assertEqual(new_task.project, self.test_project1)

    def test_parent_attribute_is_set_to_None(self):
        """testing if the parent of a task can be set to None
        """
        kwargs = copy.copy(self.kwargs)
        new_task1 = Task(**kwargs)

        kwargs['parent'] = new_task1
        new_task2 = Task(**kwargs)
        self.assertEqual(new_task2.parent, new_task1)
        db.DBSession.add_all([new_task1, new_task2])
        db.DBSession.commit()
        self.data_created.extend([new_task1, new_task2])

        # store the id to be used later
        id_ = new_task2.id
        self.assertTrue(id_ is not None)

        new_task2.parent = None
        self.assertTrue(new_task2.parent is None)
        db.DBSession.commit()

        # we still should have this task
        t = Task.query.get(id_)
        self.assertTrue(t is not None)
        self.assertEqual(t.name, kwargs['name'])

    def test_parent_argument_is_not_a_Task_instance(self):
        """testing if a TypeError will be raised when the parent argument is
        not a Task instance
        """
        kwargs = copy.copy(self.kwargs)
        kwargs['parent'] = 'not a task'
        self.assertRaises(TypeError, Task, **kwargs)

    def test_parent_attribute_is_not_a_Task_instance(self):
        """testing if a TypeError will be raised when the parent attribute is
        not a Task instance
        """
        kwargs = copy.copy(self.kwargs)
        new_task = Task(**kwargs)

        self.assertRaises(TypeError, new_task.parent, 'not a task')

        # there is no way to generate a CycleError by using the parent argument
        # cause the Task is just created, it is not in relationship with other

        # Tasks, there is no parent nor child.

    def test_parent_attribute_creates_a_cycle(self):
        """testing if a CycleError will be raised if a child is tried to be set
        as the parent.
        """
        kwargs = copy.copy(self.kwargs)
        new_task1 = Task(**kwargs)

        kwargs['name'] = 'New Task'
        kwargs['parent'] = new_task1
        new_task2 = Task(**kwargs)

        self.assertRaises(
            CircularDependencyError, setattr, new_task1, 'parent', new_task2
        )

        # more deeper test
        kwargs['parent'] = new_task2
        new_task3 = Task(**kwargs)

        self.assertRaises(
            CircularDependencyError, setattr, new_task1, 'parent', new_task3
        )

    def test_parent_argument_is_working_properly(self):
        """testing if the parent argument is working properly
        """
        kwargs = copy.copy(self.kwargs)
        new_task1 = Task(**kwargs)

        kwargs['parent'] = new_task1
        new_task2 = Task(**kwargs)
        self.assertEqual(new_task2.parent, new_task1)

    def test_parent_attribute_is_working_properly(self):
        """testing if the parent attribute is working properly
        """
        kwargs = copy.copy(self.kwargs)
        new_task1 = Task(**kwargs)

        kwargs['parent'] = new_task1
        kwargs['name'] = 'New Task'
        new_task = Task(**kwargs)

        kwargs['name'] = 'New Task 2'
        new_task2 = Task(**kwargs)

        self.assertNotEqual(new_task.parent, new_task2)

        new_task.parent = new_task2
        self.assertEqual(new_task.parent, new_task2)

    def test_parent_argument_will_not_allow_a_dependent_task_to_be_parent(self):
        """testing if a CircularDependencyError will be raised when one of the
        dependencies assigned also as the parent
        """
        kwargs = copy.copy(self.kwargs)

        kwargs['depends'] = None
        task_a = Task(**kwargs)
        task_b = Task(**kwargs)
        task_c = Task(**kwargs)
        DBSession.add_all([task_a, task_b, task_c])
        DBSession.commit()
        self.data_created.extend([task_a, task_b, task_c])

        kwargs['depends'] = [task_a, task_b, task_c]
        kwargs['parent'] = task_a
        self.assertRaises(CircularDependencyError, Task, **kwargs)

        DBSession.rollback()

    def test_parent_attribute_will_not_allow_a_dependent_task_to_be_parent(self):
        """testing if a CircularDependencyError will be raised when one of the
        dependent tasks are assigned as the parent
        """
        kwargs = copy.copy(self.kwargs)
        kwargs['depends'] = None
        task_a = Task(**kwargs)
        task_b = Task(**kwargs)
        task_c = Task(**kwargs)
        task_d = Task(**kwargs)
        DBSession.add_all([task_a, task_b, task_c])
        DBSession.commit()
        self.data_created.extend([task_a, task_b, task_c, task_d])

        task_d.depends = [task_a, task_b, task_c]

        with self.assertRaises(CircularDependencyError):
            task_d.parent = task_a

        DBSession.rollback()

    def test_children_attribute_is_empty_list_by_default(self):
        """testing if the children attribute is an empty list by default
        """
        new_task = Task(**self.kwargs)
        self.data_created.append(new_task)
        self.assertEqual(new_task.children, [])

    def test_children_attribute_is_set_to_None(self):
        """testing if a TypeError will be raised when the children attribute is
        set to None
        """
        new_task = Task(**self.kwargs)
        self.data_created.append(new_task)
        self.assertRaises(TypeError, setattr, new_task, 'children', None)

    def test_children_attribute_accepts_Tasks_only(self):
        """testing if a TypeError will be raised when the item assigned to the
        children attribute is not a Task instance
        """
        new_task = Task(**self.kwargs)
        self.data_created.append(new_task)
        self.assertRaises(TypeError, setattr, new_task, 'children',
                          'no task')

    def test_children_attribute_is_working_properly(self):
        """testing if the children attribute is working properly
        """
        kwargs = copy.copy(self.kwargs)
        new_task = Task(**kwargs)
        DBSession.add(new_task)
        DBSession.commit()
        self.data_created.append(new_task)

        kwargs['parent'] = new_task
        kwargs['name'] = 'Task 1'
        task1 = Task(**kwargs)
        DBSession.add(task1)
        DBSession.commit()
        self.data_created.append(task1)

        kwargs['name'] = 'Task 2'
        task2 = Task(**kwargs)
        DBSession.add(task2)
        DBSession.commit()
        self.data_created.append(task2)

        kwargs['name'] = 'Task 3'
        task3 = Task(**kwargs)
        DBSession.add(task3)
        DBSession.commit()
        self.data_created.append(task3)

        self.assertFalse(task2 in task1.children)
        self.assertFalse(task3 in task1.children)

        task1.children.append(task2)
        self.assertTrue(task2 in task1.children)

        task3.parent = task1
        self.assertTrue(task3 in task1.children)

    def test_is_leaf_attribute_is_read_only(self):
        """testing if the is_leaf attribute is a read only attribute
        """
        kwargs = copy.copy(self.kwargs)
        new_task = Task(**kwargs)
        self.data_created.append(new_task)
        DBSession.commit()
        self.assertRaises(AttributeError, setattr, new_task, 'is_leaf', True)

    def test_is_leaf_attribute_is_working_properly(self):
        """testing if the is_leaf attribute is True for a Task without a child
        Task and False for Task with at least one child Task
        """
        kwargs = copy.copy(self.kwargs)
        new_task = Task(**kwargs)
        self.data_created.append(new_task)

        kwargs['parent'] = new_task
        kwargs['name'] = 'Task 1'
        task1 = Task(**kwargs)
        self.data_created.append(task1)

        kwargs['name'] = 'Task 2'
        task2 = Task(**kwargs)
        self.data_created.append(task2)

        kwargs['name'] = 'Task 3'
        task3 = Task(**kwargs)
        self.data_created.append(task3)

        task2.parent = task1
        task3.parent = task1

        # we need to commit the Session
        DBSession.add_all([task1, task2, task3])
        DBSession.commit()

        self.assertTrue(task2.is_leaf)
        self.assertTrue(task3.is_leaf)
        self.assertFalse(task1.is_leaf)

    def test_is_root_attribute_is_read_only(self):
        """testing if the is_root attribute is a read only attribute
        """
        kwargs = copy.copy(self.kwargs)
        new_task = Task(**kwargs)
        DBSession.add(new_task)
        DBSession.commit()
        self.data_created.append(new_task)

        self.assertRaises(AttributeError, setattr, new_task, 'is_root',
                          True)

    def test_is_root_attribute_is_working_properly(self):
        """testing if the is_root attribute is True for a Task without a parent
        Task and False for Task with a parent Task
        """
        kwargs = copy.copy(self.kwargs)
        new_task = Task(**kwargs)
        self.data_created.append(new_task)

        kwargs['parent'] = new_task
        kwargs['name'] = 'Task 1'
        task1 = Task(**kwargs)
        self.data_created.append(task1)

        kwargs['name'] = 'Task 2'
        task2 = Task(**kwargs)
        self.data_created.append(task2)

        kwargs['name'] = 'Task 3'
        task3 = Task(**kwargs)
        self.data_created.append(task3)

        task2.parent = task1
        task3.parent = task1

        # we need to commit the Session
        DBSession.add_all([task1, task2, task3])
        DBSession.commit()

        self.assertFalse(task2.is_root)
        self.assertFalse(task3.is_root)
        self.assertFalse(task1.is_root)
        self.assertTrue(new_task.is_root)

    def test_is_container_attribute_is_read_only(self):
        """testing if the is_container attribute is a read only attribute
        """
        kwargs = copy.copy(self.kwargs)
        new_task = Task(**kwargs)
        DBSession.add(new_task)
        DBSession.commit()
        self.data_created.append(new_task)

        self.assertRaises(
            AttributeError, setattr, new_task, 'is_container', False
        )

    def test_is_container_attribute_working_properly(self):
        """testing if the is_container attribute is True for a Task with at
        least one child Task and False for a Task with no child Task
        """
        kwargs = copy.copy(self.kwargs)
        new_task = Task(**kwargs)
        self.data_created.append(new_task)

        kwargs['parent'] = new_task
        kwargs['name'] = 'Task 1'
        task1 = Task(**kwargs)
        self.data_created.append(task1)

        kwargs['name'] = 'Task 2'
        task2 = Task(**kwargs)
        self.data_created.append(task2)

        kwargs['name'] = 'Task 3'
        task3 = Task(**kwargs)
        self.data_created.append(task3)

        # we need to commit the Session
        DBSession.add_all([task1, task2, task3])
        DBSession.commit()

        task2.parent = task1
        task3.parent = task1

        DBSession.commit()

        self.assertFalse(task2.is_container)
        self.assertFalse(task3.is_container)
        self.assertTrue(task1.is_container)

    def test_project_and_parent_args_are_skipped(self):
        """testing if a TypeError will be raised when there is no project nor a
        parent task is given with the project and parent arguments respectively
        """
        kwargs = copy.copy(self.kwargs)
        kwargs.pop('project')

        try:
            kwargs.pop('parent')
        except KeyError:
            pass

        self.assertRaises(TypeError, Task, **kwargs)

    def test_project_arg_is_skipped_but_there_is_a_parent_arg(self):
        """testing if there is no problem creating a Task without a Project
        instance when there is a Task given in parent argument
        """
        kwargs = copy.copy(self.kwargs)
        new_task = Task(**kwargs)

        kwargs.pop('project')
        kwargs['parent'] = new_task

        new_task2 = Task(**kwargs)
        self.assertEqual(new_task2.project, self.test_project1)

    def test_project_argument_is_not_a_Project_instance(self):
        """testing if a TypeError will be raised if the given value for the
        project argument is not a stalker.models.project.Project instance
        """
        kwargs = copy.copy(self.kwargs)
        kwargs['name'] = 'New Task 1'
        kwargs['project'] = 'Not a Project instance'
        self.assertRaises(TypeError, Task, **kwargs)

    def test_project_attribute_is_a_read_only_attribute(self):
        """testing if the project attribute is a read only attribute
        """
        kwargs = copy.copy(self.kwargs)
        new_task = Task(**kwargs)
        self.assertRaises(
            AttributeError, setattr, new_task, 'project', self.test_project1
        )

    def test_project_argument_is_not_matching_the_given_parent_argument(self):
        """testing if a RuntimeWarning will be raised when the given project
        and parent is not matching, that is, the project of the given parent is
        different than the supplied Project with the project argument
        """
        kwargs = copy.copy(self.kwargs)
        new_task = Task(**kwargs)

        kwargs['name'] = 'New Task'
        kwargs['parent'] = new_task
        kwargs['project'] = Project(
            name='Some Other Project',
            code='SOP',
            status_list=self.test_project_status_list,
            repository=self.test_repository
        )
        # catching warnings are different then catching exceptions
        #self.assertRaises(RuntimeWarning, Task, **self.kwargs)
        import warnings
        warnings.simplefilter("always")

        with warnings.catch_warnings(record=True) as w:
            Task(**kwargs)
            self.assertTrue(
                issubclass(w[-1].category, RuntimeWarning)
            )

    def test_project_argument_is_not_matching_the_given_parent_argument_new_task_will_use_parents_project(self):
        """testing if the new task will use the parents project when the given
        project is not matching the given parent
        """
        kwargs = copy.copy(self.kwargs)
        new_task = Task(**kwargs)

        kwargs['name'] = 'New Task'
        kwargs['parent'] = new_task
        kwargs['project'] = Project(
            name='Some Other Project',
            code='SOP',
            status_list=self.test_project_status_list,
            repository=self.test_repository
        )
        new_task2 = Task(**kwargs)
        self.assertEqual(new_task2.project, new_task.project)

    def test_start_and_end_attribute_values_of_a_container_task_are_defined_by_its_child_tasks(self):
        """testing if the start and end attribute values is defined by the
        earliest start and the latest end date values of the children Tasks for
        a container Task
        """
        kwargs = copy.copy(self.kwargs)

        # remove effort and duration. Why?
        kwargs.pop('schedule_timing')
        kwargs.pop('schedule_unit')
        kwargs['schedule_constraint'] = CONSTRAIN_BOTH

        now = datetime.datetime(2013, 3, 22, 15, 0)
        dt = datetime.timedelta

        # task1
        kwargs['name'] = 'Task1'
        kwargs['start'] = now
        kwargs['end'] = now + dt(3)
        task1 = Task(**kwargs)

        logger.debug('now                   : %s' % now)
        logger.debug('now + dt(3)           : %s' % (now + dt(3)))
        logger.debug('now + dt(3) - now     : %s' % (now + dt(3) - now))
        logger.debug('task1.start           : %s' % task1.start)
        logger.debug('task1.end             : %s' % task1.end)
        logger.debug('task1.schedule_timing : %s' % task1.schedule_timing)
        logger.debug('task1.schedule_unit   : %s' % task1.schedule_unit)
        logger.debug('task1.is_leaf         : %s' % task1.is_leaf)

        # task2
        kwargs['name'] = 'Task2'
        kwargs['start'] = now + dt(1)
        kwargs['end'] = now + dt(5)
        task2 = Task(**kwargs)

        # task3
        kwargs['name'] = 'Task3'
        kwargs['start'] = now + dt(3)
        kwargs['end'] = now + dt(8)
        task3 = Task(**kwargs)

        # check start conditions
        logger.debug('task1.start: %s' % task1.start)
        logger.debug('task1.end  : %s' % task1.end)
        self.assertEqual(task1.start, now)
        self.assertEqual(task1.end, now + dt(3))

        # now parent the task2 and task3 to task1
        task2.parent = task1
        task1.children.append(task3)

        # check if the start is not `now` anymore
        self.assertNotEqual(task1.start, now)
        self.assertNotEqual(task1.end, now + dt(3))

        # but
        self.assertEqual(task1.start, now + dt(1))
        self.assertEqual(task1.end, now + dt(8))

        kwargs['name'] = 'Task4'
        kwargs['start'] = now + dt(15)
        kwargs['end'] = now + dt(16)
        task4 = Task(**kwargs)
        task3.parent = task4
        self.assertEqual(task4.start, task3.start)
        self.assertEqual(task4.end, task3.end)
        self.assertEqual(task1.start, task2.start)
        self.assertEqual(task1.end, task2.end)
        # TODO: with SQLAlchemy 0.9 please also check if removing the last
        #       child from a parent will update the parents start and end date
        #       values

    def test_end_value_is_calculated_with_the_schedule_timing_and_schedule_unit(self):
        """testing for a newly created task the end attribute value will be
        calculated using the schedule_timing and schedule_unit
        """
        kwargs = copy.copy(self.kwargs)

        kwargs['start'] = datetime.datetime(2013, 4, 17, 0, 0)
        kwargs.pop('end')
        kwargs['schedule_timing'] = 10
        kwargs['schedule_unit'] = 'h'

        new_task = Task(**kwargs)
        self.assertEqual(
            new_task.end,
            datetime.datetime(2013, 4, 17, 10, 0)
        )

        kwargs['schedule_timing'] = 5
        kwargs['schedule_unit'] = 'd'
        new_task = Task(**kwargs)
        self.assertEqual(
            new_task.end,
            datetime.datetime(2013, 4, 22, 0, 0)
        )

    def test_start_value_is_calculated_with_the_schedule_timing_and_schedule_unit_if_schedule_constraint_is_set_to_end(self):
        """testing if the start date value will be recalculated from the
        schedule_timing and schedule_unit if the schedule_constraint is set to
        end
        """
        kwargs = copy.copy(self.kwargs)

        kwargs['start'] = datetime.datetime(2013, 4, 17, 0, 0)
        kwargs['end'] = datetime.datetime(2013, 4, 18, 0, 0)
        kwargs['schedule_constraint'] = CONSTRAIN_END
        kwargs['schedule_timing'] = 10
        kwargs['schedule_unit'] = 'd'

        new_task = Task(**kwargs)
        self.assertEqual(
            new_task.end,
            datetime.datetime(2013, 4, 18, 0, 0)
        )
        self.assertEqual(
            new_task.start,
            datetime.datetime(2013, 4, 8, 0, 0)
        )

    def test_start_and_end_values_are_not_touched_if_the_schedule_constraint_is_set_to_both(self):
        """testing if the start and end date values are not touched if the
        schedule constraint is set to both
        """
        kwargs = copy.copy(self.kwargs)
        new_task = Task(**kwargs)

        kwargs['start'] = datetime.datetime(2013, 4, 17, 0, 0)
        kwargs['end'] = datetime.datetime(2013, 4, 27, 0, 0)
        kwargs['schedule_constraint'] = CONSTRAIN_BOTH
        kwargs['schedule_timing'] = 100
        kwargs['schedule_unit'] = 'd'

        new_task = Task(**kwargs)
        self.assertEqual(
            new_task.start,
            datetime.datetime(2013, 4, 17, 0, 0)
        )
        self.assertEqual(
            new_task.end,
            datetime.datetime(2013, 4, 27, 0, 0)
        )

    def test_level_attribute_is_a_read_only_property(self):
        """testing if the level attribute is a read only property
        """
        kwargs = copy.copy(self.kwargs)
        new_task = Task(**kwargs)

        self.assertRaises(AttributeError, setattr, new_task, 'level', 0)

    def test_level_attribute_returns_the_hierarchical_level_of_this_task(self):
        """testing if the level attribute returns the hierarchical level of
        this task
        """
        kwargs = copy.copy(self.kwargs)
        new_task = Task(**kwargs)

        kwargs['name'] = 'T1'
        test_task1 = Task(**kwargs)
        self.assertEqual(test_task1.level, 1)

        kwargs['name'] = 'T2'
        test_task2 = Task(**kwargs)
        test_task2.parent = test_task1
        self.assertEqual(test_task2.level, 2)

        kwargs['name'] = 'T3'
        test_task3 = Task(**kwargs)
        test_task3.parent = test_task2
        self.assertEqual(test_task3.level, 3)

    def test__check_circular_dependency_causes_recursion(self):
        """Bug ID: None

        Try to create one parent and three child tasks, second and third child
        are dependent to the first child. This was causing a recursion.
        """

        task1 = Task(
            project=self.test_project1,
            name='Cekimler',
            start=datetime.datetime(2013, 4, 1),
            end=datetime.datetime(2013, 5, 6),
            status_list=self.task_status_list,
            responsible=[self.test_user1]
        )

        task2 = Task(
            parent=task1,
            name='Supervising Shootings Part1',
            start=datetime.datetime(2013, 4, 1),
            end=datetime.datetime(2013, 4, 11),
            status_list=self.task_status_list
        )

        task3 = Task(
            parent=task1,
            name='Supervising Shootings Part2',
            depends=[task2],
            start=datetime.datetime(2013, 4, 12),
            end=datetime.datetime(2013, 4, 16),
            status_list=self.task_status_list
        )

        task4 = Task(
            parent=task1,
            name='Supervising Shootings Part3',
            depends=[task3],
            start=datetime.datetime(2013, 4, 12),
            end=datetime.datetime(2013, 4, 17),
            status_list=self.task_status_list
        )

        self.data_created.extend([task1, task2, task3, task4])

        DBSession.add_all([task1, task2, task3, task4])
        DBSession.commit()

        # move task4 dependency to task2
        task4.depends = [task2]
        DBSession.commit()

    def test_parent_attribute_checks_cycle_on_self(self):
        """Bug ID: None

        Check if a CircularDependency Error will be raised if the parent
        attribute is pointing itself
        """
        task1 = Task(
            project=self.test_project1,
            name='Cekimler',
            start=datetime.datetime(2013, 4, 1),
            end=datetime.datetime(2013, 5, 6),
            status_list=self.task_status_list,
            responsible=[self.test_user1]
        )
        DBSession.add(task1)
        DBSession.commit()

        with self.assertRaises(CircularDependencyError):
            task1.parent = task1

        DBSession.rollback()

    def test_bid_timing_argument_is_skipped(self):
        """testing if the bid_timing attribute value will be equal to
        schedule_timing attribute value if the bid_timing argument is skipped
        """
        kwargs = copy.copy(self.kwargs)
        kwargs['schedule_timing'] = 155
        kwargs.pop('bid_timing')
        new_task = Task(**kwargs)
        self.assertEqual(new_task.schedule_timing, kwargs['schedule_timing'])
        self.assertEqual(new_task.bid_timing, new_task.schedule_timing)

    def test_bid_timing_argument_is_None(self):
        """testing if the bid_timing attribute value will be equal to
        schedule_timing attribute value if the bid_timing argument is None
        """
        kwargs = copy.copy(self.kwargs)
        kwargs['bid_timing'] = None
        kwargs['schedule_timing'] = 1342
        new_task = Task(**kwargs)
        self.assertEqual(new_task.schedule_timing, kwargs['schedule_timing'])
        self.assertEqual(new_task.bid_timing, new_task.schedule_timing)

    def test_bid_timing_attribute_is_set_to_None(self):
        """testing if the bid_timing attribute can be set to None
        """
        new_task = Task(**self.kwargs)
        self.data_created.append(new_task)
        new_task.bid_timing = None
        self.assertTrue(new_task.bid_timing is None)

    def test_bid_timing_argument_is_not_an_integer_or_float(self):
        """testing if a TypeError will be raised when the bid_timing argument
        is not an integer or float
        """
        kwargs = copy.copy(self.kwargs)
        kwargs['bid_timing'] = '10d'
        self.assertRaises(TypeError, Task, **kwargs)

    def test_bid_timing_attribute_is_not_an_integer_or_float(self):
        """testing if a TypeError will be raised when the bid_timing attribute
        is set to a value which is not an integer or float
        """
        new_task = Task(**self.kwargs)
        self.data_created.append(new_task)
        self.assertRaises(TypeError, setattr, new_task, 'bid_timing', '10d')

    def test_bid_timing_argument_is_working_properly(self):
        """testing if the bid_timing argument is working properly
        """
        kwargs = copy.copy(self.kwargs)
        kwargs['bid_timing'] = 23
        new_task = Task(**kwargs)
        self.assertEqual(new_task.bid_timing, kwargs['bid_timing'])

    def test_bid_timing_attribute_is_working_properly(self):
        """testing if the bid_timning attribute is working properly
        """
        new_task = Task(**self.kwargs)
        self.data_created.append(new_task)
        test_value = 23
        new_task.bid_timing = test_value
        self.assertEqual(new_task.bid_timing, test_value)

    def test_bid_unit_argument_is_skipped(self):
        """testing if the bid_unit attribute value will be equal to
        schedule_unit attribute value if the bid_unit argument is skipped
        """
        kwargs = copy.copy(self.kwargs)
        kwargs['schedule_unit'] = 'd'
        kwargs.pop('bid_unit')
        new_task = Task(**kwargs)
        self.data_created.append(new_task)
        self.assertEqual(new_task.schedule_unit, kwargs['schedule_unit'])
        self.assertEqual(new_task.bid_unit, new_task.schedule_unit)

    def test_bid_unit_argument_is_None(self):
        """testing if the bid_unit attribute value will be equal to
        schedule_unit attribute value if the bid_unit argument is None
        """
        kwargs = copy.copy(self.kwargs)
        kwargs['bid_unit'] = None
        kwargs['schedule_unit'] = 'min'
        new_task = Task(**kwargs)
        self.assertEqual(new_task.schedule_unit, kwargs['schedule_unit'])
        self.assertEqual(new_task.bid_unit, new_task.schedule_unit)

    def test_bid_unit_attribute_is_set_to_None(self):
        """testing if the bid_unit attribute can be set to default value of 'h'
        """
        new_task = Task(**self.kwargs)
        self.data_created.append(new_task)
        new_task.bid_unit = None
        self.assertEqual(new_task.bid_unit, 'h')

    def test_bid_unit_argument_is_not_a_string(self):
        """testing if a TypeError will be raised when the bid_hour argument is
        not a string
        """
        kwargs = copy.copy(self.kwargs)
        kwargs['bid_unit'] = 10
        self.assertRaises(TypeError, Task, **kwargs)

    def test_bid_unit_attribute_is_not_a_string(self):
        """testing if a TypeError will be raised when the bid_unit attribute is
        set to a value which is not an integer
        """
        new_task = Task(**self.kwargs)
        self.data_created.append(new_task)
        self.assertRaises(TypeError, setattr, new_task, 'bid_unit', 10)

    def test_bid_unit_argument_is_working_properly(self):
        """testing if the bid_unit argument is working properly
        """
        kwargs = copy.copy(self.kwargs)
        kwargs['bid_unit'] = 'h'
        new_task = Task(**kwargs)
        self.data_created.append(new_task)
        self.assertEqual(new_task.bid_unit, kwargs['bid_unit'])

    def test_bid_unit_attribute_is_working_properly(self):
        """testing if the bid_unit attribute is working properly
        """
        test_value = 'h'
        new_task = Task(**self.kwargs)
        self.data_created.append(new_task)
        new_task.bid_unit = test_value
        self.assertEqual(new_task.bid_unit, test_value)

    def test_bid_unit_argument_value_not_in_defaults_datetime_units(self):
        """testing if a ValueError will be raised when the given unit value is
        not in the stalker.config.Config.datetime_units
        """
        kwargs = copy.copy(self.kwargs)
        kwargs['bid_unit'] = 'os'
        self.assertRaises(ValueError, Task, **kwargs)

    def test_bid_unit_attribute_value_not_in_defaults_datetime_units(self):
        """testing if a ValueError will be raised when the bid_unit value is
        set to a value which is not in stalker.config.Config.datetime_units.
        """
        new_task = Task(**self.kwargs)
        DBSession.add(new_task)
        DBSession.commit()
        self.data_created.append(new_task)
        self.assertRaises(ValueError, setattr, new_task, 'bid_unit', 'sys')

    def test_tjp_id_is_a_read_only_attribute(self):
        """testing if the tjp_id attribute is a read only attribute
        """
        new_task = Task(**self.kwargs)
        DBSession.add(new_task)
        DBSession.commit()
        self.data_created.append(new_task)
        self.assertRaises(AttributeError, setattr, new_task, 'tjp_id',
                          'some value')

    def test_tjp_abs_id_is_a_read_only_attribute(self):
        """testing if the tjp_abs_id attribute is a read only attribute
        """
        new_task = Task(**self.kwargs)
        self.assertRaises(AttributeError, setattr, new_task,
                          'tjp_abs_id', 'some_value')

    def test_tjp_id_attribute_is_working_properly_for_a_root_task(self):
        """testing if the tjp_id is working properly for a root task
        """
        kwargs = copy.copy(self.kwargs)
        kwargs['parent'] = None
        new_task = Task(**kwargs)
        self.assertEqual(new_task.tjp_id, 'Task_%s' % new_task.id)

    def test_tjp_id_attribute_is_working_properly_for_a_leaf_task(self):
        """testing if the tjp_id is working properly for a leaf task
        """
        kwargs = copy.copy(self.kwargs)
        new_task1 = Task(**kwargs)

        kwargs['parent'] = new_task1
        kwargs['depends'] = None
        new_task2 = Task(**kwargs)
        self.assertEqual(new_task2.tjp_id, 'Task_%s' % new_task2.id)

    def test_tjp_abs_id_attribute_is_working_properly_for_a_root_task(self):
        """testing if the tjp_abs_id is working properly for a root task
        """
        kwargs = copy.copy(self.kwargs)

        kwargs['parent'] = None
        new_task = Task(**kwargs)
        self.assertEqual(
            new_task.tjp_abs_id,
            'Project_%s.Task_%s' % (kwargs['project'].id, new_task.id))

    def test_tjp_abs_id_attribute_is_working_properly_for_a_leaf_task(self):
        """testing if the tjp_abs_id is working properly for a leaf task
        """
        kwargs = copy.copy(self.kwargs)
        kwargs['parent'] = None

        t1 = Task(**kwargs)
        t2 = Task(**kwargs)
        t3 = Task(**kwargs)

        t2.parent = t1
        t3.parent = t2
        DBSession.add_all([t1, t2, t3])
        DBSession.commit()
        self.data_created.extend([t1, t2, t3])

        self.assertEqual(
            t3.tjp_abs_id,
            'Project_%s.Task_%s.Task_%s.Task_%s' % (
                kwargs['project'].id,
                t1.id, t2.id, t3.id
            )
        )

    def test_to_tjp_attribute_is_working_properly_for_a_root_task(self):
        """testing if the to_tjp attribute is working properly for a root task
        """
        kwargs = copy.copy(self.kwargs)

        kwargs['parent'] = None
        kwargs['schedule_timing'] = 10
        kwargs['schedule_unit'] = 'd'
        kwargs['schedule_model'] = 'effort'
        kwargs['depends'] = []
        kwargs['resources'] = [self.test_user1, self.test_user2]

        dep_t1 = Task(**kwargs)
        dep_t2 = Task(**kwargs)
        DBSession.add_all([dep_t1, dep_t2])
        DBSession.commit()
        self.data_created.extend([dep_t1, dep_t2])

        kwargs['depends'] = [dep_t1, dep_t2]
        kwargs['name'] = 'Modeling'

        t1 = Task(**kwargs)
        DBSession.add(t1)
        DBSession.commit()
        self.data_created.append(t1)

        expected_tjp = """
task Task_%(t1_id)s "Task_%(t1_id)s" {

    
            depends Project_%(project1_id)s.Task_%(dep_t1_id)s {onend}, Project_%(project1_id)s.Task_%(dep_t2_id)s {onend}        
            
            effort 10.0d
            allocate User_%(user1_id)s {
                    alternative
                    User_%(user3_id)s, User_%(user4_id)s, User_%(user5_id)s select minloaded
                    persistent
                }, User_%(user2_id)s {
                    alternative
                    User_%(user3_id)s, User_%(user4_id)s, User_%(user5_id)s select minloaded
                    persistent
                }            
}""" % {
            'project1_id': self.test_project1.id,

            't1_id': t1.id,

            'dep_t1_id': dep_t1.id,
            'dep_t2_id': dep_t2.id,

            'user1_id': self.test_user1.id,
            'user2_id': self.test_user2.id,
            'user3_id': self.test_user3.id,
            'user4_id': self.test_user4.id,
            'user5_id': self.test_user5.id,
        }
        # print(t1.to_tjp)
        # print('---------------------------------')
        # print(expected_tjp)
        self.assertEqual(t1.to_tjp, expected_tjp)

    def test_to_tjp_attribute_is_working_properly_for_a_leaf_task(self):
        """testing if the to_tjp attribute is working properly for a leaf task
        """
        kwargs = copy.copy(self.kwargs)
        new_task = Task(**kwargs)
        DBSession.add(new_task)
        DBSession.commit()
        self.data_created.append(new_task)

        kwargs['parent'] = new_task
        kwargs['depends'] = []

        dep_task1 = Task(**kwargs)
        DBSession.add(dep_task1)
        DBSession.commit()
        self.data_created.append(dep_task1)

        dep_task2 = Task(**kwargs)
        DBSession.add(dep_task2)
        DBSession.commit()
        self.data_created.append(dep_task2)

        kwargs['name'] = 'Modeling'
        kwargs['schedule_timing'] = 1003
        kwargs['schedule_unit'] = 'h'
        kwargs['schedule_model'] = 'effort'
        kwargs['depends'] = [dep_task1, dep_task2]

        kwargs['resources'] = [self.test_user1, self.test_user2]

        new_task2 = Task(**kwargs)
        DBSession.add(new_task2)
        DBSession.commit()
        self.data_created.append(new_task2)

        # self.maxDiff = None
        expected_tjp = """
task Task_%(new_task2_id)s "Task_%(new_task2_id)s" {

    
            depends Project_%(project1_id)s.Task_%(new_task_id)s.Task_%(dep_task1_id)s {onend}, Project_%(project1_id)s.Task_%(new_task_id)s.Task_%(dep_task2_id)s {onend}        
            
            effort 1003.0h
            allocate User_%(user1_id)s {
                    alternative
                    User_%(user3_id)s, User_%(user4_id)s, User_%(user5_id)s select minloaded
                    persistent
                }, User_%(user2_id)s {
                    alternative
                    User_%(user3_id)s, User_%(user4_id)s, User_%(user5_id)s select minloaded
                    persistent
                }            
}""" % {
            'project1_id': self.test_project1.id,

            'new_task_id': new_task.id,
            'new_task2_id': new_task2.id,

            'dep_task1_id': dep_task1.id,
            'dep_task2_id': dep_task2.id,
            'user1_id': self.test_user1.id,
            'user2_id': self.test_user2.id,
            'user3_id': self.test_user3.id,
            'user4_id': self.test_user4.id,
            'user5_id': self.test_user5.id,
        }
        # print(new_task2.to_tjp)
        # print('---------------------------------')
        # print(expected_tjp)
        self.assertEqual(new_task2.to_tjp, expected_tjp)

    def test_to_tjp_attribute_is_working_properly_for_a_leaf_task_with_dependency_details(self):
        """testing if the to_tjp attribute is working properly for a leaf task
        """
        kwargs = copy.copy(self.kwargs)
        new_task = Task(**kwargs)
        DBSession.add(new_task)
        DBSession.commit()
        self.data_created.append(new_task)

        kwargs['parent'] = new_task
        kwargs['depends'] = []

        dep_task1 = Task(**kwargs)
        DBSession.add(dep_task1)
        DBSession.commit()
        self.data_created.append(dep_task1)

        dep_task2 = Task(**kwargs)
        DBSession.add(dep_task2)
        DBSession.commit()
        self.data_created.append(dep_task2)

        kwargs['name'] = 'Modeling'
        kwargs['schedule_timing'] = 1003
        kwargs['schedule_unit'] = 'h'
        kwargs['schedule_model'] = 'effort'
        kwargs['depends'] = [dep_task1, dep_task2]
        kwargs['resources'] = [self.test_user1, self.test_user2]

        new_task2 = Task(**kwargs)
        DBSession.add(new_task2)
        DBSession.commit()
        self.data_created.append(new_task2)

        # modify dependency attributes
        tdep1 = new_task2.task_depends_to[0]
        tdep1.dependency_target = 'onstart'
        tdep1.gap_timing = 2
        tdep1.gap_unit = 'd'
        tdep1.gap_model = 'length'

        tdep2 = new_task2.task_depends_to[1]
        tdep1.dependency_target = 'onstart'
        tdep2.gap_timing = 4
        tdep2.gap_unit = 'd'
        tdep2.gap_model = 'duration'

        expected_tjp = """
task Task_%(new_task2_id)s "Task_%(new_task2_id)s" {

    
            depends Project_%(project1_id)s.Task_%(new_task_id)s.Task_%(dep_task1_id)s {onstart gaplength 2d}, Project_%(project1_id)s.Task_%(new_task_id)s.Task_%(dep_task2_id)s {onend gapduration 4d}        
            
            effort 1003.0h
            allocate User_%(user1_id)s {
                    alternative
                    User_%(user3_id)s, User_%(user4_id)s, User_%(user5_id)s select minloaded
                    persistent
                }, User_%(user2_id)s {
                    alternative
                    User_%(user3_id)s, User_%(user4_id)s, User_%(user5_id)s select minloaded
                    persistent
                }            
}""" % {
            'project1_id': self.test_project1.id,

            'new_task_id': new_task.id,
            'new_task2_id': new_task2.id,

            'dep_task1_id': dep_task1.id,
            'dep_task2_id': dep_task2.id,
            'user1_id': self.test_user1.id,
            'user2_id': self.test_user2.id,
            'user3_id': self.test_user3.id,
            'user4_id': self.test_user4.id,
            'user5_id': self.test_user5.id,
        }
        # print new_task.to_tjp
        # print '---------------------------------'
        # print expected_tjp
        self.assertEqual(new_task2.to_tjp, expected_tjp)

    def test_to_tjp_attribute_is_working_properly_for_a_leaf_task_with_custom_allocation_strategy(self):
        """testing if the to_tjp attribute is working properly for a leaf task
        with custom allocation_strategy value
        """
        kwargs = copy.copy(self.kwargs)
        new_task1 = Task(**kwargs)
        DBSession.add(new_task1)
        DBSession.commit()
        self.data_created.append(new_task1)

        kwargs['parent'] = new_task1
        kwargs['depends'] = []

        dep_task1 = Task(**kwargs)
        DBSession.add(dep_task1)
        DBSession.commit()
        self.data_created.append(dep_task1)

        dep_task2 = Task(**kwargs)
        DBSession.add(dep_task2)
        DBSession.commit()
        self.data_created.append(dep_task2)

        kwargs['name'] = 'Modeling'
        kwargs['schedule_timing'] = 1003
        kwargs['schedule_unit'] = 'h'
        kwargs['schedule_model'] = 'effort'
        kwargs['depends'] = [dep_task1, dep_task2]

        kwargs['resources'] = [self.test_user1, self.test_user2]

        kwargs['alternative_resources'] = [self.test_user3]
        kwargs['allocation_strategy'] = 'minloaded'

        new_task2 = Task(**kwargs)
        DBSession.add(new_task2)
        DBSession.commit()
        self.data_created.append(new_task2)

        # modify dependency attributes
        tdep1 = new_task2.task_depends_to[0]
        tdep1.dependency_target = 'onstart'
        tdep1.gap_timing = 2
        tdep1.gap_unit = 'd'
        tdep1.gap_model = 'length'

        tdep2 = new_task2.task_depends_to[1]
        tdep1.dependency_target = 'onstart'
        tdep2.gap_timing = 4
        tdep2.gap_unit = 'd'
        tdep2.gap_model = 'duration'

        expected_tjp = """
task Task_%(new_task2_id)s "Task_%(new_task2_id)s" {

    
            depends Project_%(project1_id)s.Task_%(new_task1_id)s.Task_%(dep_task1_id)s {onstart gaplength 2d}, Project_%(project1_id)s.Task_%(new_task1_id)s.Task_%(dep_task2_id)s {onend gapduration 4d}        
            
            effort 1003.0h
            allocate User_%(user1_id)s {
                    alternative
                    User_%(user3_id)s select minloaded
                    persistent
                }, User_%(user2_id)s {
                    alternative
                    User_%(user3_id)s select minloaded
                    persistent
                }            
}""" % {
            'project1_id': self.test_project1.id,

            'new_task1_id': new_task1.id,
            'new_task2_id': new_task2.id,

            'dep_task1_id': dep_task1.id,
            'dep_task2_id': dep_task2.id,

            'user1_id': self.test_user1.id,
            'user2_id': self.test_user2.id,
            'user3_id': self.test_user3.id,
            'user4_id': self.test_user4.id,
            'user5_id': self.test_user5.id,
        }
        # print(new_task2.to_tjp)
        # print('---------------------------------')
        # print(expected_tjp)
        self.assertEqual(new_task2.to_tjp, expected_tjp)

    def test_to_tjp_attribute_is_working_properly_for_a_container_task(self):
        """testing if the to_tjp attribute is working properly for a container
        task
        """
        kwargs = copy.copy(self.kwargs)

        kwargs['parent'] = None
        kwargs['depends'] = []

        t1 = Task(**kwargs)
        DBSession.add(t1)
        DBSession.commit()
        self.data_created.append(t1)

        kwargs['parent'] = t1

        dep_task1 = Task(**kwargs)
        DBSession.add(dep_task1)
        DBSession.commit()
        self.data_created.append(dep_task1)

        dep_task2 = Task(**kwargs)
        DBSession.add(dep_task2)
        DBSession.commit()
        self.data_created.append(dep_task2)

        kwargs['name'] = 'Modeling'
        kwargs['schedule_timing'] = 1
        kwargs['schedule_unit'] = 'd'
        kwargs['schedule_model'] = 'effort'
        kwargs['depends'] = [dep_task1, dep_task2]

        kwargs['resources'] = [self.test_user1, self.test_user2]

        t2 = Task(**kwargs)
        DBSession.add(t2)
        DBSession.commit()
        self.data_created.append(t2)

        expected_tjp = """
task Task_%(t1_id)s "Task_%(t1_id)s" {

    
    
task Task_%(dep_task1_id)s "Task_%(dep_task1_id)s" {

    
            
            
            effort 1.0d
            allocate User_%(user1_id)s {
                    alternative
                    User_%(user3_id)s, User_%(user4_id)s, User_%(user5_id)s select minloaded
                    persistent
                }, User_%(user2_id)s {
                    alternative
                    User_%(user3_id)s, User_%(user4_id)s, User_%(user5_id)s select minloaded
                    persistent
                }            
}
task Task_%(dep_task2_id)s "Task_%(dep_task2_id)s" {

    
            
            
            effort 1.0d
            allocate User_%(user1_id)s {
                    alternative
                    User_%(user3_id)s, User_%(user4_id)s, User_%(user5_id)s select minloaded
                    persistent
                }, User_%(user2_id)s {
                    alternative
                    User_%(user3_id)s, User_%(user4_id)s, User_%(user5_id)s select minloaded
                    persistent
                }            
}
task Task_%(t2_id)s "Task_%(t2_id)s" {

    
            depends Project_%(project1_id)s.Task_%(t1_id)s.Task_%(dep_task1_id)s {onend}, Project_%(project1_id)s.Task_%(t1_id)s.Task_%(dep_task2_id)s {onend}        
            
            effort 1.0d
            allocate User_%(user1_id)s {
                    alternative
                    User_%(user3_id)s, User_%(user4_id)s, User_%(user5_id)s select minloaded
                    persistent
                }, User_%(user2_id)s {
                    alternative
                    User_%(user3_id)s, User_%(user4_id)s, User_%(user5_id)s select minloaded
                    persistent
                }            
}
}""" % {
            'user1_id': self.test_user1.id,
            'user2_id': self.test_user2.id,
            'user3_id': self.test_user3.id,
            'user4_id': self.test_user4.id,
            'user5_id': self.test_user5.id,

            'project1_id': self.test_project1.id,

            't1_id': t1.id,
            't2_id': t2.id,
            'dep_task1_id': dep_task1.id,
            'dep_task2_id': dep_task2.id,
        }
        # print(t1.to_tjp)
        # print('---------------------------------')
        # print(expected_tjp)
        self.assertEqual(t1.to_tjp, expected_tjp)

    def test_to_tjp_attribute_is_working_properly_for_a_container_task_with_dependency(self):
        """testing if the to_tjp attribute is working properly for a container
        task which has dependency
        """
        kwargs = copy.copy(self.kwargs)

        # kwargs['project'].id = 87987
        kwargs['parent'] = None
        kwargs['depends'] = []
        kwargs['name'] = 'Random Task Name 1'

        t0 = Task(**kwargs)
        DBSession.add(t0)
        DBSession.commit()
        self.data_created.append(t0)

        kwargs['depends'] = [t0]
        kwargs['name'] = 'Modeling'

        t1 = Task(**kwargs)
        t1.priority = 888
        DBSession.add(t1)
        DBSession.commit()
        self.data_created.append(t1)

        kwargs['parent'] = t1
        kwargs['depends'] = []

        dep_task1 = Task(**kwargs)
        dep_task1.depends = []
        DBSession.add(dep_task1)
        DBSession.commit()
        self.data_created.append(dep_task1)

        dep_task2 = Task(**kwargs)
        dep_task1.depends = []
        DBSession.add(dep_task2)
        DBSession.commit()
        self.data_created.append(dep_task2)

        kwargs['name'] = 'Modeling'
        kwargs['schedule_timing'] = 1
        kwargs['schedule_unit'] = 'd'
        kwargs['schedule_model'] = 'effort'
        kwargs['depends'] = [dep_task1, dep_task2]

        self.test_user1.name = 'Test User 1'
        self.test_user1.login = 'testuser1'
        # self.test_user1.id = 1231

        self.test_user2.name = 'Test User 2'
        self.test_user2.login = 'testuser2'
        # self.test_user2.id = 1232

        kwargs['resources'] = [self.test_user1, self.test_user2]

        t2 = Task(**kwargs)
        DBSession.add(t2)
        DBSession.commit()
        self.data_created.append(t2)

        expected_tjp = """
task Task_%(t1_id)s "Task_%(t1_id)s" {

    priority 888
            depends Project_%(project1_id)s.Task_%(t0_id)s {onend}
task Task_%(dep_task1_id)s "Task_%(dep_task1_id)s" {

    
            
            
            effort 1.0d
            allocate User_%(user1_id)s {
                    alternative
                    User_%(user3_id)s, User_%(user4_id)s, User_%(user5_id)s select minloaded
                    persistent
                }, User_%(user2_id)s {
                    alternative
                    User_%(user3_id)s, User_%(user4_id)s, User_%(user5_id)s select minloaded
                    persistent
                }            
}
task Task_%(dep_task2_id)s "Task_%(dep_task2_id)s" {

    
            
            
            effort 1.0d
            allocate User_%(user1_id)s {
                    alternative
                    User_%(user3_id)s, User_%(user4_id)s, User_%(user5_id)s select minloaded
                    persistent
                }, User_%(user2_id)s {
                    alternative
                    User_%(user3_id)s, User_%(user4_id)s, User_%(user5_id)s select minloaded
                    persistent
                }            
}
task Task_%(t2_id)s "Task_%(t2_id)s" {

    
            depends Project_%(project1_id)s.Task_%(t1_id)s.Task_%(dep_task1_id)s {onend}, Project_%(project1_id)s.Task_%(t1_id)s.Task_%(dep_task2_id)s {onend}        
            
            effort 1.0d
            allocate User_%(user1_id)s {
                    alternative
                    User_%(user3_id)s, User_%(user4_id)s, User_%(user5_id)s select minloaded
                    persistent
                }, User_%(user2_id)s {
                    alternative
                    User_%(user3_id)s, User_%(user4_id)s, User_%(user5_id)s select minloaded
                    persistent
                }            
}
}""" % {
            'user1_id': self.test_user1.id,
            'user2_id': self.test_user2.id,
            'user3_id': self.test_user3.id,
            'user4_id': self.test_user4.id,
            'user5_id': self.test_user5.id,

            'project1_id': self.test_project1.id,

            't0_id': t0.id,
            't1_id': t1.id,
            't2_id': t2.id,
            'dep_task1_id': dep_task1.id,
            'dep_task2_id': dep_task2.id
        }
        # print(t1.to_tjp)
        # print('---------------------------------')
        # print(expected_tjp)
        self.assertEqual(t1.to_tjp, expected_tjp)

    def test_to_tjp_schedule_constraint_is_reflected_in_tjp_file(self):
        """testing if the schedule_constraint is reflected in the tjp file
        """
        kwargs = copy.copy(self.kwargs)

        # kwargs['project'].id = 87987
        kwargs['parent'] = None
        kwargs['depends'] = []

        t1 = Task(**kwargs)
        DBSession.add(t1)
        DBSession.commit()
        self.data_created.append(t1)

        kwargs['parent'] = t1

        dep_task1 = Task(**kwargs)
        DBSession.add(dep_task1)
        DBSession.commit()
        self.data_created.append(dep_task1)

        dep_task2 = Task(**kwargs)
        DBSession.add(dep_task2)
        DBSession.commit()
        self.data_created.append(dep_task2)

        kwargs['name'] = 'Modeling'
        kwargs['schedule_timing'] = 1
        kwargs['schedule_unit'] = 'd'
        kwargs['schedule_model'] = 'effort'
        kwargs['depends'] = [dep_task1, dep_task2]
        kwargs['schedule_constraint'] = 3
        kwargs['start'] = datetime.datetime(2013, 5, 3, 14, 0)
        kwargs['end'] = datetime.datetime(2013, 5, 4, 14, 0)

        self.test_user1.name = 'Test User 1'
        self.test_user1.login = 'testuser1'
        # self.test_user1.id = 1231

        self.test_user2.name = 'Test User 2'
        self.test_user2.login = 'testuser2'
        # self.test_user2.id = 1232

        kwargs['resources'] = [self.test_user1, self.test_user2]

        t2 = Task(**kwargs)
        DBSession.add(t2)
        DBSession.commit()
        self.data_created.append(t2)

        expected_tjp = """
task Task_%(t1_id)s "Task_%(t1_id)s" {

    
    
task Task_%(dep_task1_id)s "Task_%(dep_task1_id)s" {

    
            
            
            effort 1.0d
            allocate User_%(user1_id)s {
                    alternative
                    User_%(user3_id)s, User_%(user4_id)s, User_%(user5_id)s select minloaded
                    persistent
                }, User_%(user2_id)s {
                    alternative
                    User_%(user3_id)s, User_%(user4_id)s, User_%(user5_id)s select minloaded
                    persistent
                }            
}
task Task_%(dep_task2_id)s "Task_%(dep_task2_id)s" {

    
            
            
            effort 1.0d
            allocate User_%(user1_id)s {
                    alternative
                    User_%(user3_id)s, User_%(user4_id)s, User_%(user5_id)s select minloaded
                    persistent
                }, User_%(user2_id)s {
                    alternative
                    User_%(user3_id)s, User_%(user4_id)s, User_%(user5_id)s select minloaded
                    persistent
                }            
}
task Task_%(t2_id)s "Task_%(t2_id)s" {

    
            depends Project_%(project1_id)s.Task_%(t1_id)s.Task_%(dep_task1_id)s {onend}, Project_%(project1_id)s.Task_%(t1_id)s.Task_%(dep_task2_id)s {onend}        
                                                start 2013-05-03-14:00
                                end 2013-05-04-14:00
                            
            effort 1.0d
            allocate User_%(user1_id)s {
                    alternative
                    User_%(user3_id)s, User_%(user4_id)s, User_%(user5_id)s select minloaded
                    persistent
                }, User_%(user2_id)s {
                    alternative
                    User_%(user3_id)s, User_%(user4_id)s, User_%(user5_id)s select minloaded
                    persistent
                }            
}
}""" % {
            'user1_id': self.test_user1.id,
            'user2_id': self.test_user2.id,
            'user3_id': self.test_user3.id,
            'user4_id': self.test_user4.id,
            'user5_id': self.test_user5.id,

            'project1_id': self.test_project1.id,

            't1_id': t1.id,
            't2_id': t2.id,
            'dep_task1_id': dep_task1.id,
            'dep_task2_id': dep_task2.id
        }
        # print(t1.to_tjp)
        # print('-----------------------')
        # print(expected_tjp)
        self.maxDiff = None
        self.assertEqual(t1.to_tjp, expected_tjp)

    def test_is_scheduled_is_a_read_only_attribute(self):
        """testing if the is_scheduled is a read-only attribute
        """
        kwargs = copy.copy(self.kwargs)
        new_task = Task(**kwargs)
        DBSession.add(new_task)
        DBSession.commit()
        self.data_created.append(new_task)

        self.assertRaises(
            AttributeError, setattr, new_task, 'is_scheduled', True
        )

    def test_is_scheduled_is_true_if_the_computed_start_and_computed_end_is_not_None(self):
        """testing if the is_scheduled attribute value is True if the
        computed_start and computed_end has both valid values
        """
        kwargs = copy.copy(self.kwargs)
        new_task = Task(**kwargs)
        DBSession.add(new_task)
        DBSession.commit()
        self.data_created.append(new_task)

        new_task.computed_start = datetime.datetime.now()
        new_task.computed_end = \
            datetime.datetime.now() + datetime.timedelta(10)
        self.assertTrue(new_task.is_scheduled)

    def test_is_scheduled_is_false_if_one_of_computed_start_and_computed_end_is_None(self):
        """testing if the is_scheduled attribute value is False if one of the
        computed_start and computed_end values is None
        """
        kwargs = copy.copy(self.kwargs)
        new_task = Task(**kwargs)
        DBSession.add(new_task)
        DBSession.commit()
        self.data_created.append(new_task)

        new_task.computed_start = None
        new_task.computed_end = datetime.datetime.now()
        self.assertFalse(new_task.is_scheduled)

        new_task.computed_start = datetime.datetime.now()
        new_task.computed_end = None
        self.assertFalse(new_task.is_scheduled)

    def test_parents_attribute_is_read_only(self):
        """testing if the parents attribute is read only
        """
        kwargs = copy.copy(self.kwargs)
        new_task = Task(**kwargs)
        DBSession.add(new_task)
        DBSession.commit()
        self.data_created.append(new_task)

        self.assertRaises(
            AttributeError,
            setattr,
            new_task,
            'parents',
            self.test_dependent_task1
        )

    def test_parents_attribute_is_working_properly(self):
        """testing if the parents attribute is working properly
        """
        kwargs = copy.copy(self.kwargs)
        kwargs['parent'] = None

        t1 = Task(**kwargs)
        t2 = Task(**kwargs)
        t3 = Task(**kwargs)

        t2.parent = t1
        t3.parent = t2

        self.assertEqual(
            t3.parents,
            [t1, t2]
        )

    def test_responsible_argument_is_skipped_for_a_root_task(self):
        """testing if the responsible list will be an empty list if a root task
        have no responsible set
        """
        kwargs = copy.copy(self.kwargs)
        kwargs.pop('responsible')
        new_task = Task(**kwargs)

        self.assertEqual(new_task.responsible, [])

    def test_responsible_argument_is_skipped_for_a_non_root_task(self):
        """testing if the parent tasks responsible will be used if the
        responsible argument is skipped for a non-root task
        """
        kwargs = copy.copy(self.kwargs)
        kwargs['name'] = 'Root Task'
        root_task = Task(**kwargs)
        self.assertEqual(root_task.responsible, [self.test_user1])

        kwargs.pop('responsible')
        kwargs['parent'] = root_task
        kwargs['name'] = 'Child Task'

        new_task = Task(**kwargs)

        self.assertEqual(new_task.responsible, root_task.responsible)

    def test_responsible_argument_is_None_for_a_root_task(self):
        """testing if a RuntimeError will be raised if the responsible argument
        is None for a root task
        """
        kwargs = copy.copy(self.kwargs)
        kwargs['responsible'] = None
        new_task = Task(**kwargs)

        self.assertEqual(new_task.responsible, [])

    def test_responsible_argument_is_none_for_a_non_root_task(self):
        """testing if the parent tasks responsible will be used if the
        responsible argument is None for a non-root task
        """
        kwargs = copy.copy(self.kwargs)
        kwargs['name'] = 'Root Task'
        root_task = Task(**kwargs)
        self.assertEqual(root_task.responsible, [self.test_user1])

        kwargs['responsible'] = None
        kwargs['parent'] = root_task
        kwargs['name'] = 'Child Task'

        new_task = Task(**kwargs)

        self.assertEqual(new_task.responsible, root_task.responsible)

    def test_responsible_argument_not_a_list_instance(self):
        """testing if a TypeError will be raised when the responsible argument
        is not a List instance
        """
        kwargs = copy.copy(self.kwargs)
        kwargs['responsible'] = 'not a list'
        with self.assertRaises(TypeError) as cm:
            Task(**kwargs)

        self.assertEqual(
            str(cm.exception),
            'Incompatible collection type: str is not list-like'
        )

    def test_responsible_attribute_not_a_list_instance(self):
        """testing if a TypeError will be raised when the responsible attribute
        is set to a value other than a List of User instances
        """
        kwargs = copy.copy(self.kwargs)
        new_task = Task(**kwargs)

        with self.assertRaises(TypeError) as cm:
            new_task.responsible = 'not a list of users'

        self.assertEqual(
            str(cm.exception),
            'Incompatible collection type: str is not list-like'
        )

    def test_responsible_argument_is_not_a_list_of_User_instance(self):
        """testing if a TypeError will be raised if the responsible argument
        value is not a List of User instance
        """
        kwargs = copy.copy(self.kwargs)
        kwargs['responsible'] = ['not a user instance']

        with self.assertRaises(TypeError) as cm:
            Task(**kwargs)

        self.assertEqual(
            str(cm.exception),
            'Task.responsible should be a list of stalker.models.auth.User '
            'instances, not str'
        )

    def test_responsible_attribute_is_set_to_something_other_than_a_list_of_User_instance(self):
        """testing if a TypeError will be raised if the responsible attribute
        is set to something other than a list of User instance
        """
        kwargs = copy.copy(self.kwargs)
        new_task = Task(**kwargs)

        with self.assertRaises(TypeError) as cm:
            new_task.responsible = ['not a user instance']

        self.assertEqual(
            str(cm.exception),
            'Task.responsible should be a list of stalker.models.auth.User '
            'instances, not str'
        )

    def test_responsible_argument_is_None_or_skipped_responsible_attribute_comes_from_parents(self):
        """testing if the responsible argument is None or skipped then the
        responsible attribute value comes from parents
        """
        # create two new tasks
        kwargs = copy.copy(self.kwargs)
        new_task = Task(**kwargs)

        kwargs['responsible'] = None

        kwargs['parent'] = new_task
        new_task1 = Task(**kwargs)

        kwargs['parent'] = new_task1
        new_task2 = Task(**kwargs)

        kwargs['parent'] = new_task2
        new_task3 = Task(**kwargs)

        self.assertEqual(new_task1.responsible, [self.test_user1])
        self.assertEqual(new_task2.responsible, [self.test_user1])
        self.assertEqual(new_task3.responsible, [self.test_user1])

        new_task2.responsible = [self.test_user2]
        self.assertEqual(new_task1.responsible, [self.test_user1])
        self.assertEqual(new_task2.responsible, [self.test_user2])
        self.assertEqual(new_task3.responsible, [self.test_user2])

    def test_responsible_attribute_is_set_to_None_responsible_attribute_comes_from_parents(self):
        """testing if the responsible attribute is None or skipped then its
        value comes from parents
        """
        # create two new tasks
        kwargs = copy.copy(self.kwargs)
        new_task = Task(**kwargs)

        kwargs['parent'] = new_task
        new_task1 = Task(**kwargs)

        kwargs['parent'] = new_task1
        new_task2 = Task(**kwargs)

        kwargs['parent'] = new_task2
        new_task3 = Task(**kwargs)

        new_task1.responsible = []
        new_task2.responsible = []
        new_task3.responsible = []
        new_task.responsible = [self.test_user2]

        self.assertEqual(new_task1.responsible, [self.test_user2])
        self.assertEqual(new_task2.responsible, [self.test_user2])
        self.assertEqual(new_task3.responsible, [self.test_user2])

        new_task2.responsible = [self.test_user1]
        self.assertEqual(new_task1.responsible, [self.test_user2])
        self.assertEqual(new_task2.responsible, [self.test_user1])
        self.assertEqual(new_task3.responsible, [self.test_user1])

    def test_computed_start_also_sets_start(self):
        """testing if computed_start also sets the start value of the task
        """
        kwargs = copy.copy(self.kwargs)
        new_task1 = Task(**kwargs)
        test_value = datetime.datetime(2013, 8, 2, 13, 0)
        self.assertNotEqual(new_task1.start, test_value)
        new_task1.computed_start = test_value
        self.assertEqual(new_task1.computed_start, test_value)
        self.assertEqual(new_task1.start, test_value)

    def test_computed_end_also_sets_end(self):
        """testing if computed_end also sets the end value of the task
        """
        kwargs = copy.copy(self.kwargs)
        new_task = Task(**kwargs)

        new_task1 = Task(**kwargs)
        test_value = datetime.datetime(2013, 8, 2, 13, 0)
        self.assertNotEqual(new_task1.end, test_value)
        new_task1.computed_end = test_value
        self.assertEqual(new_task1.computed_end, test_value)
        self.assertEqual(new_task1.end, test_value)

    # TODO: please add tests for _total_logged_seconds for leaf tasks

    def test_tickets_attribute_is_a_read_only_property(self):
        """testing if the tickets attribute is a read-only property
        """
        kwargs = copy.copy(self.kwargs)
        new_task = Task(**kwargs)

        self.assertRaises(
            AttributeError, setattr, new_task, 'tickets', 'some value'
        )

    def test_tickets_attribute_is_working_properly(self):
        """testing if the tickets attribute is working properly
        """
        kwargs = copy.copy(self.kwargs)
        new_task = Task(**kwargs)
        DBSession.add(new_task)
        DBSession.commit()
        self.data_created.append(new_task)

        from stalker import Ticket
        # create ticket statuses
        #db.init()

        new_ticket1 = Ticket(
            project=new_task.project,
            links=[new_task]
        )
        DBSession.add(new_ticket1)
        DBSession.commit()
        self.data_created.append(new_ticket1)

        new_ticket2 = Ticket(
            project=new_task.project,
            links=[new_task]
        )
        DBSession.add(new_ticket2)
        DBSession.commit()
        self.data_created.append(new_ticket2)

        # add some other tickets
        new_ticket3 = Ticket(
            project=new_task.project,
            links=[]
        )
        DBSession.add(new_ticket3)
        DBSession.commit()
        self.data_created.append(new_ticket3)

        self.assertEqual(
            sorted(new_task.tickets, key=lambda x: x.name),
            sorted([new_ticket1, new_ticket2], key=lambda x: x.name)
        )

    def test_open_tickets_attribute_is_a_read_only_property(self):
        """testing if the open_tickets attribute is a read-only property
        """
        kwargs = copy.copy(self.kwargs)
        new_task = Task(**kwargs)

        self.assertRaises(
            AttributeError, setattr, new_task, 'open_tickets', 'some value'
        )

    def test_open_tickets_attribute_is_working_properly(self):
        """testing if the open_tickets attribute is working properly
        """
        kwargs = copy.copy(self.kwargs)
        new_task = Task(**kwargs)
        DBSession.add(new_task)
        DBSession.commit()
        self.data_created.append(new_task)

        from stalker import Ticket
        # create ticket statuses
        #db.init()

        new_ticket1 = Ticket(
            project=new_task.project,
            links=[new_task]
        )
        DBSession.add(new_ticket1)
        DBSession.commit()
        self.data_created.append(new_ticket1)

        new_ticket2 = Ticket(
            project=new_task.project,
            links=[new_task]
        )
        DBSession.add(new_ticket2)
        DBSession.commit()
        self.data_created.append(new_ticket2)

        # close this ticket
        new_ticket2.resolve(None, 'fixed')
        DBSession.commit()

        # add some other tickets
        new_ticket3 = Ticket(
            project=new_task.project,
            links=[]
        )
        DBSession.add(new_ticket3)
        DBSession.commit()
        self.data_created.append(new_ticket3)

        self.assertEqual(
            new_task.open_tickets,
            [new_ticket1]
        )

    def test_reviews_attribute_is_an_empty_list_by_default(self):
        """testing if the reviews attribute is an empty list by default
        """
        kwargs = copy.copy(self.kwargs)
        new_task = Task(**kwargs)
        self.assertEqual(new_task.reviews, [])

    def test_status_is_WFD_for_a_newly_created_task_with_dependencies(self):
        """testing if the status for a newly created task is WFD by default if
        there are dependencies
        """
        # try to trick it
        kwargs = copy.copy(self.kwargs)
        kwargs['status'] = self.status_cmpl  # this will be ignored
        new_task = Task(**kwargs)
        self.assertEqual(new_task.status, self.status_wfd)

    def test_status_is_RTS_for_a_newly_created_task_without_dependency(self):
        """testing if the status for a newly created task is RTS by default if
        there are no dependencies
        """
        # try to trick it
        kwargs = copy.copy(self.kwargs)
        kwargs['status'] = self.status_cmpl
        kwargs.pop('depends')
        new_task = Task(**kwargs)
        self.assertEqual(new_task.status, self.status_rts)

    def test_review_number_attribute_is_read_only(self):
        """testing if the review_number attribute is read-only
        """
        kwargs = copy.copy(self.kwargs)
        new_task = Task(**kwargs)

        with self.assertRaises(AttributeError):
            new_task.review_number = 12

    def test_review_number_attribute_initializes_with_0(self):
        """testing if the review_number attribute initializes to 0
        """
        kwargs = copy.copy(self.kwargs)
        new_task = Task(**kwargs)

        self.assertEqual(new_task.review_number, 0)

    def test_task_dependency_auto_generates_TaskDependency_object(self):
        """testing if a TaskDependency instance is automatically created when
        the association proxy is used
        """
        kwargs = copy.copy(self.kwargs)
        kwargs['depends'] = []
        new_task = Task(**kwargs)

        new_task.depends.append(self.test_dependent_task1)

        task_depends = new_task.task_depends_to[0]
        self.assertEqual(task_depends.task, new_task)
        self.assertEqual(task_depends.depends_to, self.test_dependent_task1)

    def test_alternative_resources_argument_is_skipped(self):
        """testing if the alternative_resources attribute will be an empty list
        when it is skipped
        """
        kwargs = copy.copy(self.kwargs)
        kwargs.pop('alternative_resources')
        new_task = Task(**kwargs)
        self.data_created.append(new_task)
        self.assertEqual(new_task.alternative_resources, [])

    def test_alternative_resources_argument_is_None(self):
        """testing if the alternative_resources attribute will be an empth list
        when the alternative_resources argument value is None
        """
        kwargs = copy.copy(self.kwargs)
        kwargs['alternative_resources'] = None
        new_task = Task(**kwargs)
        self.assertEqual(new_task.alternative_resources, [])

    def test_alternative_resources_attribute_is_set_to_None(self):
        """testing if a TypeError will be raised when the alternative_resources
        attribute is set to None
        """
        new_task = Task(**self.kwargs)
        self.data_created.append(new_task)
        self.assertRaises(TypeError, setattr, new_task,
                          'alternative_resources', None)

    def test_alternative_resources_argument_is_not_a_list(self):
        """testing if a TypeError will be raised when the alternative_resources
        argument value is not a list
        """
        kwargs = copy.copy(self.kwargs)
        kwargs['alternative_resources'] = self.test_user3
        self.assertRaises(TypeError, Task, **kwargs)

    def test_alternative_resources_attribute_is_not_a_list(self):
        """testing if a TypeError will be raised when the alternative_resources
        attribute is set to a value other than a list
        """
        new_task = Task(**self.kwargs)
        self.data_created.append(new_task)
        self.assertRaises(TypeError, setattr, new_task,
                          'alternative_resources', self.test_user3)

    def test_alternative_resources_argument_elements_are_not_User_instances(self):
        """testing if a TypeError will be raised when the elements in the
        alternative_resources argument are not all User instances
        """
        kwargs = copy.copy(self.kwargs)
        kwargs['alternative_resources'] = ['not', 1, 'user']
        self.assertRaises(TypeError, Task, **kwargs)

    def test_alternative_resources_attribute_elements_are_not_all_User_instances(self):
        """testing if a TypeError will be raised when the elements in the
        alternative_resources attribute are not all User instances
        """
        new_task = Task(**self.kwargs)
        self.data_created.append(new_task)
        self.assertRaises(TypeError, setattr, new_task,
                          'alternative_resources', ['not', 1, 'user'])

    def test_alternative_resources_argument_is_working_properly(self):
        """testing if the alternative_resources argument value is correctly
        passed to the alternative_resources attribute
        """
        new_task = Task(**self.kwargs)
        self.data_created.append(new_task)
        self.assertEqual(
            sorted([self.test_user3, self.test_user4, self.test_user5],
                   key=lambda x: x.name),
            sorted(new_task.alternative_resources, key=lambda x: x.name)
        )

    def test_alternative_resources_attribute_is_working_properly(self):
        """testing if the alternative_resources attribute value can be
        correctly set
        """
        new_task = Task(**self.kwargs)
        self.data_created.append(new_task)
        self.assertEqual(
            sorted(new_task.alternative_resources, key=lambda x: x.name),
            sorted([self.test_user3, self.test_user4, self.test_user5],
                   key=lambda x: x.name)
        )
        alternative_resources = [self.test_user4, self.test_user5]
        new_task.alternative_resources = alternative_resources
        self.assertEqual(
            sorted(alternative_resources, key=lambda x: x.name),
            sorted(new_task.alternative_resources, key=lambda x: x.name)
        )

    def test_allocation_strategy_argument_is_skipped(self):
        """testing if the default value will be used for allocation_strategy
        attribute if the allocation_strategy argument is skipped
        """
        kwargs = copy.copy(self.kwargs)
        kwargs.pop('allocation_strategy')
        new_task = Task(**kwargs)
        self.assertEqual(new_task.allocation_strategy,
                         defaults.allocation_strategy[0])

    def test_allocation_strategy_argument_is_none(self):
        """testing if the default value will be used for allocation_strategy
        attribute if the allocation_strategy argument is None
        """
        kwargs = copy.copy(self.kwargs)
        kwargs['allocation_strategy'] = None
        new_task = Task(**kwargs)
        self.assertEqual(new_task.allocation_strategy,
                         defaults.allocation_strategy[0])

    def test_allocation_strategy_attribute_is_set_to_None(self):
        """testing if the default value will be used for the
        allocation_strategy when it is set to None
        """
        new_task = Task(**self.kwargs)
        self.data_created.append(new_task)
        new_task.allocation_strategy = None
        self.assertEqual(new_task.allocation_strategy,
                         defaults.allocation_strategy[0])

    def test_allocation_strategy_argument_is_not_a_string(self):
        """testing if a TypeError will be raised when the allocation_strategy
        argument value is not a string
        """
        kwargs = copy.copy(self.kwargs)
        kwargs['allocation_strategy'] = 234
        self.assertRaises(TypeError, Task, **kwargs)

    def test_allocation_strategy_attribute_is_set_to_a_value_other_than_string(self):
        """testing if a TypeError will be used when the allocation_strategy
        attribute is set to a value other then a string
        """
        new_task = Task(**self.kwargs)
        self.data_created.append(new_task)
        self.assertRaises(TypeError, setattr, new_task,
                          'allocation_strategy', 234)

    def test_allocation_strategy_argument_value_is_not_correct(self):
        """testing if a ValueError will be raised when the allocation_strategy
        argument value is not one of [minallocated, maxloaded, minloaded,
        order, random]
        """
        kwargs = copy.copy(self.kwargs)
        kwargs['allocation_strategy'] = 'not in the list'
        self.assertRaises(ValueError, Task, **kwargs)

    def test_allocation_strategy_attribute_value_is_not_correct(self):
        """testing if a ValueError will be raised when the allocation_strategy
        attribute is set to a value which is not one of [minallocated,
        maxloaded, minloaded, order, random]
        """
        new_task = Task(**self.kwargs)
        self.data_created.append(new_task)
        self.assertRaises(ValueError, setattr, new_task,
                          'allocation_strategy', 'not in the list')

    def test_allocation_strategy_argument_is_working_properly(self):
        """testing if the allocation_strategy argument value is correctly
        passed to the allocation_strategy attribute
        """
        test_value = defaults.allocation_strategy[1]
        kwargs = copy.copy(self.kwargs)
        kwargs['allocation_strategy'] = test_value
        new_task = Task(**kwargs)
        self.assertEqual(test_value, new_task.allocation_strategy)

    def test_allocation_strategy_attribute_is_working_properly(self):
        """testing if the allocation_strategy attribute value can be correctly
        set
        """
        new_task = Task(**self.kwargs)
        self.data_created.append(new_task)

        test_value = defaults.allocation_strategy[1]
        self.assertNotEqual(new_task.allocation_strategy, test_value)

        new_task.allocation_strategy = test_value
        self.assertEqual(new_task.allocation_strategy, test_value)

    def test_computed_resources_attribute_value_is_equal_to_the_resources_attribute_for_a_new_task(self):
        """testing if the computed_resources attribute value is equal to the
        resources attribute when a task initialized.
        """
        kwargs = copy.copy(self.kwargs)
        new_task = Task(**kwargs)
        self.data_created.append(new_task)

        self.assertFalse(new_task.is_scheduled)
        self.assertEqual(new_task.resources, new_task.computed_resources)

    def test_computed_resources_attribute_value_will_be_updated_with_resources_attribute_if_is_scheduled_is_False_append(self):
        """testing if the computed_resources attribute will be updated with the
        resources attribute if the is_scheduled attribute is False
        """
        kwargs = copy.copy(self.kwargs)
        new_task = Task(**kwargs)
        self.data_created.append(new_task)

        self.assertFalse(new_task.is_scheduled)
        test_value = [self.test_user3, self.test_user5]
        self.assertNotEqual(new_task.resources, test_value)
        self.assertNotEqual(new_task.computed_resources, test_value)
        new_task.resources = test_value
        self.assertEqual(
            sorted(new_task.computed_resources, key=lambda x: x.name),
            sorted(test_value, key=lambda x: x.name)
        )

    def test_computed_resources_attribute_value_will_be_updated_with_resources_attribute_if_is_scheduled_is_False_remove(self):
        """testing if the computed_resources attribute will be updated with the
        resources attribute if the is_scheduled attribute is False in remove
        item action
        """
        kwargs = copy.copy(self.kwargs)
        new_task = Task(**kwargs)
        self.data_created.append(new_task)

        self.assertFalse(new_task.is_scheduled)
        test_value = [self.test_user3, self.test_user5]
        self.assertNotEqual(new_task.resources, test_value)
        self.assertNotEqual(new_task.computed_resources, test_value)
        new_task.resources = test_value
        self.assertEqual(
            sorted(new_task.computed_resources, key=lambda x: x.name),
            sorted(test_value, key=lambda x: x.name)
        )

    def test_computed_resources_attribute_value_will_not_be_updated_with_resources_attribute_if_is_scheduled_is_True(self):
        """testing if the computed_resources attribute will be not be updated
        with the resources attribute if the is_scheduled is True
        """
        kwargs = copy.copy(self.kwargs)
        new_task = Task(**kwargs)
        self.data_created.append(new_task)

        self.assertFalse(new_task.is_scheduled)
        test_value = [self.test_user3, self.test_user5]
        self.assertNotEqual(new_task.resources, test_value)
        self.assertNotEqual(new_task.computed_resources, test_value)

        # now set computed_start and computed_end to emulate a computation has
        # been done
        dt = datetime.datetime
        td = datetime.timedelta
        now = dt.now()

        self.assertFalse(new_task.is_scheduled)
        new_task.computed_start = now
        new_task.computed_end = now + td(hours=1)

        self.assertTrue(new_task.is_scheduled)

        new_task.resources = test_value
        self.assertNotEqual(new_task.computed_resources, test_value)

    def test_persistent_allocation_argument_is_skipped(self):
        """testing if the default value will be used for the
        persistent_allocation attribute value if the persistent_allocation
        argument is skipped
        """
        self.kwargs.pop('persistent_allocation')
        new_task = Task(**self.kwargs)
        self.assertTrue(new_task.persistent_allocation)

    def test_persistent_allocation_argument_is_None(self):
        """testing if the default value will be used for the
        persistent_allocation attribute value if the persistent_allocation
        argument is None
        """
        self.kwargs['persistent_allocation'] = None
        new_task = Task(**self.kwargs)
        self.assertTrue(new_task.persistent_allocation)

    def test_persistent_allocation_attribute_is_set_to_None(self):
        """testing if the default value will be used when for the
        persistent_allocation attribute if it is set to None
        """
        new_task = Task(**self.kwargs)
        new_task.persistent_allocation = None
        self.assertTrue(new_task.persistent_allocation)

    def test_persistent_allocation_argument_is_not_bool(self):
        """testing if the value will be converted to bool if the
        persistent_allocation argument value is not a bool value
        """
        kwargs = copy.copy(self.kwargs)

        test_value = 'not a bool'
        kwargs['persistent_allocation'] = test_value
        new_task1 = Task(**kwargs)
        self.assertEqual(bool(test_value), new_task1.persistent_allocation)

        test_value = 0
        kwargs['persistent_allocation'] = test_value
        new_task2 = Task(**kwargs)
        self.assertEqual(bool(test_value), new_task2.persistent_allocation)

    def test_persistent_allocation_attribute_is_not_bool(self):
        """testing if the persistent_allocation attribute value will be
        converted to a bool value when it is something other than a bool
        """
        new_task = Task(**self.kwargs)

        test_value = 'not a bool'
        new_task.persistent_allocation = test_value
        self.assertEqual(
            bool(test_value),
            new_task.persistent_allocation
        )

        test_value = 0
        new_task.persistent_allocation = test_value
        self.assertEqual(
            bool(test_value),
            new_task.persistent_allocation
        )

    def test_persistent_allocation_argument_is_working_properly(self):
        """testing if the persistent_allocation argument value is correctly
        passed to the persistent_allocation attribute
        """
        kwargs = copy.copy(self.kwargs)
        kwargs['persistent_allocation'] = False
        new_task = Task(**kwargs)
        self.assertEqual(new_task.persistent_allocation, False)

    def test_persistent_allocation_attribute_is_working_properly(self):
        """testing if the persistent_allocation attribute value can be
        correctly set
        """
        kwargs = copy.copy(self.kwargs)
        new_task = Task(**kwargs)

        new_task.persistent_allocation = False
        self.assertEqual(new_task.persistent_allocation, False)

    def test_path_attribute_is_read_only(self):
        """testing if the path attribute is read only
        """
        new_task = Task(**self.kwargs)
        with self.assertRaises(AttributeError):
            new_task.path = 'some_path'

    def test_path_attribute_raises_a_RuntimeError_if_no_FilenameTemplate_found(self):
        """testing if the path attribute raises a RuntimeError if there is no
        FilenameTemplate matching the entity_type
        """
        new_task = Task(**self.kwargs)
        with self.assertRaises(RuntimeError):
            new_task.path

    def test_path_attribute_raises_a_RuntimeError_if_no_matching_FilenameTemplate_found(self):
        """testing if the path attribute raises a RuntimeError if there is no
        matching FilenameTemplate matching the entity_type
        """
        new_task = Task(**self.kwargs)
        ft = FilenameTemplate(
            name='Asset Filename Template',
            target_entity_type='Asset',
            path='{{project.code}}/{%- for parent_task in parent_tasks -%}'
                 '{{parent_task.nice_name}}/{%- endfor -%}',
            filename='{{task.nice_name}}_{{version.take_name}}'
                     '_v{{"%03d"|format(version.version_number)}}{{extension}}'
        )
        structure = Structure(
            name='Movie Project Structure',
            templates=[ft]
        )
        self.test_project1.structure = structure
        with self.assertRaises(RuntimeError):
            new_task.path

        self.test_project1.structure = None

    def test_path_attribute_is_the_rendered_version_of_the_related_FilenameTemplate_object_in_the_related_project(self):
        """testing if the path attribute value is the rendered version of the
        FilenameTemplate matching the class entity_type
        """
        new_task = Task(**self.kwargs)
        DBSession.add(new_task)
        DBSession.commit()
        self.data_created.append(new_task)

        ft = FilenameTemplate(
            name='Task Filename Template',
            target_entity_type='Task',
            path='{{project.code}}/{%- for parent_task in parent_tasks -%}'
                 '{{parent_task.nice_name}}/{%- endfor -%}',
            filename='{{task.nice_name}}_{{version.take_name}}'
                     '_v{{"%03d"|format(version.version_number)}}{{extension}}'
        )
        DBSession.add(ft)
        DBSession.commit()
        self.data_created.append(ft)

        structure = Structure(
            name='Movie Project Structure',
            templates=[ft]
        )
        DBSession.add(structure)
        DBSession.commit()
        self.data_created.append(structure)

        self.test_project1.structure = structure

        self.assertEqual('tp1/Modeling', new_task.path)
        self.test_project1.structure = None

    def test_absolute_path_attribute_is_read_only(self):
        """testing if absolute_path is read only
        """
        new_task = Task(**self.kwargs)
        with self.assertRaises(AttributeError):
            setattr(new_task, 'absolute_path', 'some_path')

    def test_absolute_path_attribute_raises_a_RuntimeError_if_no_FilenameTemplate_found(self):
        """testing if the absolute_path attribute raises a RuntimeError if
        there is no FilenameTemplate matching the entity_type
        """
        new_task = Task(**self.kwargs)
        with self.assertRaises(RuntimeError):
            path = new_task.absolute_path

    def test_absolute_path_attribute_raises_a_RuntimeError_if_no_matching_FilenameTemplate_found(self):
        """testing if the absolute_path attribute raises a RuntimeError if
        there is no matching FilenameTemplate matching the entity_type
        """
        new_task = Task(**self.kwargs)
        DBSession.add(new_task)
        DBSession.commit()
        self.data_created.append(new_task)

        ft = FilenameTemplate(
            name='Asset Filename Template',
            target_entity_type='Asset',
            path='{{project.code}}/{%- for parent_task in parent_tasks -%}'
                 '{{parent_task.nice_name}}/{%- endfor -%}',
            filename='{{task.nice_name}}_{{version.take_name}}'
                     '_v{{"%03d"|format(version.version_number)}}{{extension}}'
        )
        DBSession.add(ft)
        DBSession.commit()
        self.data_created.append(ft)

        structure = Structure(
            name='Movie Project Structure',
            templates=[ft]
        )
        DBSession.add(structure)
        DBSession.commit()
        self.data_created.append(structure)

        self.test_project1.structure = structure
        with self.assertRaises(RuntimeError):
            path = new_task.path

        self.test_project1.structure = None

    def test_absolute_path_attribute_is_the_rendered_version_of_the_related_FilenameTemplate_object_in_the_related_project(self):
        """testing if the absolute_path attribute value is the rendered version
        of the FilenameTemplate matching the class entity_type
        """
        new_task = Task(**self.kwargs)
        DBSession.add(new_task)
        DBSession.commit()
        self.data_created.append(new_task)

        ft = FilenameTemplate(
            name='Task Filename Template',
            target_entity_type='Task',
            path='{{project.repository.path}}/{{project.code}}/'
                 '{%- for parent_task in parent_tasks -%}'
                 '{{parent_task.nice_name}}/'
                 '{%- endfor -%}',
            filename='{{task.nice_name}}_{{version.take_name}}'
                     '_v{{"%03d"|format(version.version_number)}}{{extension}}'
        )
        DBSession.add(ft)
        DBSession.commit()
        self.data_created.append(ft)

        structure = Structure(
            name='Movie Project Structure',
            templates=[ft]
        )
        DBSession.add(structure)
        DBSession.commit()
        self.data_created.append(structure)

        self.test_project1.structure = structure

        import os
        self.assertEqual(
            os.path.normpath(
                '%s/tp1/Modeling' % self.test_project1.repositories[0].path
            ).replace('\\', '/'),
            new_task.absolute_path
        )
        self.test_project1.structure = None

    def test_good_argument_is_skipped(self):
        """testing if the good attribute will be None if good argument is
        skipped
        """
        kwargs = copy.copy(self.kwargs)
        try:
            kwargs.pop('good')
        except KeyError:
            pass

        new_task = Task(**kwargs)
        self.data_created.append(new_task)
        db.DBSession.add(new_task)
        db.DBSession.commit()
        self.assertEqual(new_task.good, None)

    def test_good_argument_is_None(self):
        """testing if the good attribute will be None if good argument is None
        """
        kwargs = copy.copy(self.kwargs)
        kwargs['good'] = None
        new_task = Task(**kwargs)
        self.data_created.append(new_task)
        db.DBSession.add(new_task)
        db.DBSession.commit()
        self.assertEqual(new_task.good, None)

    def test_good_attribute_is_None(self):
        """testing if it is possible to set the good attribute to None
        """
        from stalker import Good
        kwargs = copy.copy(self.kwargs)
        kwargs['good'] = Good(name='Some Good')
        new_task = Task(**kwargs)
        self.data_created.append(new_task)
        self.data_created.append(kwargs['good'])
        db.DBSession.add(new_task)
        db.DBSession.commit()
        self.assertNotEqual(new_task.good, None)
        new_task.good = None
        self.assertEqual(new_task.good, None)

    def test_good_argument_is_not_a_good_instance(self):
        """testing if a TypeError will be raised when the good argument value
        is not a Good instance
        """
        kwargs = copy.copy(self.kwargs)
        kwargs['good'] = 'not a good instance'
        with self.assertRaises(TypeError) as cm:
            Task(**kwargs)

        self.assertEqual(
            str(cm.exception),
            'Task.good should be a stalker.models.budget.Good instance, not '
            'str'
        )

    def test_good_attribute_is_not_a_good_instance(self):
        """testing if a TypeError will be raised when the good attribute is not
        set to a Good instance
        """
        new_task = Task(**self.kwargs)
        with self.assertRaises(TypeError) as cm:
            new_task.good = 'not a good instance'

        self.assertEqual(
            str(cm.exception),
            'Task.good should be a stalker.models.budget.Good instance, not '
            'str'
        )

    def test_good_argument_is_working_properly(self):
        """testing if the good argument value is properly passed to the good
        attribute
        """
        kwargs = copy.copy(self.kwargs)
        from stalker import Good
        new_good = Good(name='Some Good')
        kwargs['good'] = new_good
        new_task = Task(**kwargs)
        self.assertEqual(new_task.good, new_good)

    def test_good_attribute_is_working_properly(self):
        """testing if the good attribute value can be correctly set
        """
        from stalker import Good
        new_good = Good(name='Some Good')
        new_task = Task(**self.kwargs)
        self.assertNotEqual(new_task.good, new_good)
        new_task.good = new_good
        self.assertEqual(new_task.good, new_good)


class TaskPostgreSQLTestCase(TaskTestCase):
    """tests the Task class with PostgreSQL database
    """

    config = {
        'sqlalchemy.url':
            'postgresql://stalker_admin:stalker@localhost/stalker_test',
        'sqlalchemy.echo': False
    }

    @classmethod
    def setUpClass(cls):
        """run once
        """
        defaults.timing_resolution = datetime.timedelta(hours=1)

        # # clean up test database
        db.setup(cls.config)
        #db.init()

        from stalker.db.declarative import Base
        Base.metadata.drop_all(DBSession.connection())

        DBSession.commit()
        super(TaskPostgreSQLTestCase, cls).setUpClass()

    @classmethod
    def tearDownClass(cls):
        """clean up the test
        """
        # clean up test database
        from stalker.db.declarative import Base
        Base.metadata.drop_all(db.DBSession.connection())
        DBSession.commit()
        DBSession.remove()

        defaults.timing_resolution = datetime.timedelta(hours=1)
