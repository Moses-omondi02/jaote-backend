#!/usr/bin/env python3
"""Test database operations to verify CRUD functionality"""

import unittest
import os
import sys
from datetime import datetime

# Add current directory to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from app import create_app
from models import db, NGO, User, Task, Signup


class TestDatabaseOperations(unittest.TestCase):
    def setUp(self):
        """Set up test database"""
        self.app = create_app('testing')
        self.app_context = self.app.app_context()
        self.app_context.push()
        db.create_all()

    def tearDown(self):
        """Clean up test database"""
        db.session.remove()
        db.drop_all()
        self.app_context.pop()

    def test_ngo_crud(self):
        """Test NGO Create, Read, Update, Delete operations"""
        # Create
        ngo = NGO(
            name="Test NGO",
            email="test@ngo.com",
            description="Test organization"
        )
        db.session.add(ngo)
        db.session.commit()

        # Read
        ngo_from_db = NGO.query.filter_by(email="test@ngo.com").first()
        self.assertIsNotNone(ngo_from_db)
        self.assertEqual(ngo_from_db.name, "Test NGO")

        # Update
        ngo_from_db.name = "Updated Test NGO"
        db.session.commit()

        updated_ngo = NGO.query.filter_by(email="test@ngo.com").first()
        self.assertEqual(updated_ngo.name, "Updated Test NGO")

        # Delete
        db.session.delete(updated_ngo)
        db.session.commit()

        deleted_ngo = NGO.query.filter_by(email="test@ngo.com").first()
        self.assertIsNone(deleted_ngo)

    def test_user_crud(self):
        """Test User Create, Read, Update, Delete operations"""
        # Create
        user = User(
            name="Test User",
            email="test@user.com",
            password="password123"
        )
        db.session.add(user)
        db.session.commit()

        # Read
        user_from_db = User.query.filter_by(email="test@user.com").first()
        self.assertIsNotNone(user_from_db)
        self.assertEqual(user_from_db.name, "Test User")

        # Update
        user_from_db.name = "Updated Test User"
        db.session.commit()

        updated_user = User.query.filter_by(email="test@user.com").first()
        self.assertEqual(updated_user.name, "Updated Test User")

        # Delete
        db.session.delete(updated_user)
        db.session.commit()

        deleted_user = User.query.filter_by(email="test@user.com").first()
        self.assertIsNone(deleted_user)

    def test_task_relationships(self):
        """Test Task creation with NGO and User relationships"""
        # Create NGO and User first
        ngo = NGO(name="Test NGO", email="test@ngo.com")
        user = User(name="Test User", email="test@user.com", password="pass123")

        db.session.add_all([ngo, user])
        db.session.commit()

        # Create Task
        task = Task(
            ngo_id=ngo.id,
            user_id=user.id,
            title="Test Task",
            description="Test task description",
            location="Test Location",
            hours=5
        )
        db.session.add(task)
        db.session.commit()

        # Verify relationships
        task_from_db = Task.query.filter_by(title="Test Task").first()
        self.assertIsNotNone(task_from_db)
        self.assertEqual(task_from_db.ngo.name, "Test NGO")
        self.assertEqual(task_from_db.user.name, "Test User")

    def test_signup_relationships(self):
        """Test Signup creation with Task and User relationships"""
        # Create NGO, User, and Task
        ngo = NGO(name="Test NGO", email="test@ngo.com")
        user = User(name="Test User", email="test@user.com", password="pass123")

        db.session.add_all([ngo, user])
        db.session.commit()

        task = Task(
            ngo_id=ngo.id,
            user_id=user.id,
            title="Test Task",
            location="Test Location",
            hours=5
        )
        db.session.add(task)
        db.session.commit()

        # Create Signup
        signup = Signup(
            task_id=task.id,
            user_id=user.id,
            message="I'm interested in this task"
        )
        db.session.add(signup)
        db.session.commit()

        # Verify relationships
        signup_from_db = Signup.query.filter_by(task_id=task.id).first()
        self.assertIsNotNone(signup_from_db)
        self.assertEqual(signup_from_db.task.title, "Test Task")
        self.assertEqual(signup_from_db.user.name, "Test User")

    def test_data_integrity(self):
        """Test database constraints and data integrity"""
        # Test unique constraint on User email
        user1 = User(name="User 1", email="unique@test.com", password="pass123")
        db.session.add(user1)
        db.session.commit()

        # Try to create user with same email (should fail)
        user2 = User(name="User 2", email="unique@test.com", password="pass456")
        db.session.add(user2)

        with self.assertRaises(Exception):  # Should raise IntegrityError
            db.session.commit()

        db.session.rollback()

    def test_query_operations(self):
        """Test various query operations"""
        # Create test data
        ngo = NGO(name="Query Test NGO", email="query@test.com")
        user = User(name="Query User", email="query@user.com", password="pass123")

        db.session.add_all([ngo, user])
        db.session.commit()

        task = Task(
            ngo_id=ngo.id,
            user_id=user.id,
            title="Query Test Task",
            location="Query Location",
            hours=3,
            status="open"
        )
        db.session.add(task)
        db.session.commit()

        # Test count
        self.assertEqual(Task.query.count(), 1)
        self.assertEqual(User.query.count(), 1)
        self.assertEqual(NGO.query.count(), 1)

        # Test filtering
        open_tasks = Task.query.filter_by(status="open").all()
        self.assertEqual(len(open_tasks), 1)

        # Test ordering
        tasks_by_hours = Task.query.order_by(Task.hours.desc()).all()
        self.assertEqual(len(tasks_by_hours), 1)


if __name__ == '__main__':
    unittest.main()