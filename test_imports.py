# backend/test_imports.py
import unittest
import sys
import os

# Add the backend directory to Python path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

class TestImports(unittest.TestCase):
    def test_import_app(self):
        """Test that main app modules can be imported"""
        try:
            import app, models, config
            self.assertTrue(True)
        except ImportError as e:
            self.fail(f"Import failed: {e}")

    def test_postgresql_support(self):
        """Test that PostgreSQL driver is available"""
        try:
            import psycopg2
            self.assertTrue(True)
        except ImportError as e:
            self.fail(f"PostgreSQL driver not available: {e}")

    def test_config_postgresql(self):
        """Test that PostgreSQL configuration is properly set"""
        from config import config
        prod_config = config['production']
        self.assertIn('postgresql://', prod_config.SQLALCHEMY_DATABASE_URI)

if __name__ == '__main__':
    unittest.main()