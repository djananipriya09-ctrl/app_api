import unittest
from unittest.mock import patch, MagicMock
import json
import sys
import os

# Add the project root to the path
sys.path.insert(0, os.path.dirname(__file__))

from api_project import app, get_db_connection


class TestUserAPI(unittest.TestCase):
    """Test suite for User API endpoints"""
    
    def setUp(self):
        """Set up test client and app context"""
        self.app = app
        self.app.config['TESTING'] = True
        self.client = self.app.test_client()
    
    @patch('api_project.get_db_connection')
    def test_create_user_success(self, mock_db):
        """Test successful user creation"""
        # Mock database connection and cursor
        mock_cursor = MagicMock()
        mock_cursor.lastrowid = 1
        
        mock_conn = MagicMock()
        mock_conn.cursor.return_value = mock_cursor
        mock_db.return_value = mock_conn
        
        # Make request
        response = self.client.post(
            '/users',
            data=json.dumps({'name': 'John Doe', 'age': 30}),
            content_type='application/json'
        )
        
        # Assert response
        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.json['name'], 'John Doe')
        self.assertEqual(response.json['age'], 30)
        self.assertEqual(response.json['id'], 1)
        
        # Assert database was called
        mock_cursor.execute.assert_called_once()
        mock_conn.commit.assert_called_once()
    
    @patch('api_project.get_db_connection')
    def test_create_user_with_missing_data(self, mock_db):
        """Test user creation with missing data"""
        mock_cursor = MagicMock()
        mock_cursor.lastrowid = 2  # Set to integer
        mock_conn = MagicMock()
        mock_conn.cursor.return_value = mock_cursor
        mock_db.return_value = mock_conn
        
        # Make request with incomplete data
        response = self.client.post(
            '/users',
            data=json.dumps({'name': 'Jane Doe'}),
            content_type='application/json'
        )
        
        # Should still process with None for age
        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.json['name'], 'Jane Doe')
    
    @patch('api_project.get_db_connection')
    def test_get_all_users_success(self, mock_db):
        """Test retrieving all users"""
        mock_users = [
            {'id': 1, 'name': 'John Doe', 'age': 30},
            {'id': 2, 'name': 'Jane Doe', 'age': 28}
        ]
        
        mock_cursor = MagicMock()
        mock_cursor.fetchall.return_value = mock_users
        
        mock_conn = MagicMock()
        mock_conn.cursor.return_value = mock_cursor
        mock_db.return_value = mock_conn
        
        # Make request
        response = self.client.get('/users')
        
        # Assert response
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.json), 2)
        self.assertEqual(response.json[0]['name'], 'John Doe')
        self.assertEqual(response.json[1]['name'], 'Jane Doe')
    
    @patch('api_project.get_db_connection')
    def test_get_all_users_empty(self, mock_db):
        """Test retrieving users when none exist"""
        mock_cursor = MagicMock()
        mock_cursor.fetchall.return_value = []
        
        mock_conn = MagicMock()
        mock_conn.cursor.return_value = mock_cursor
        mock_db.return_value = mock_conn
        
        # Make request
        response = self.client.get('/users')
        
        # Assert response
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json, [])
    
    @patch('api_project.get_db_connection')
    def test_get_user_by_id_success(self, mock_db):
        """Test retrieving a specific user"""
        mock_user = {'id': 1, 'name': 'John Doe', 'age': 30}
        
        mock_cursor = MagicMock()
        mock_cursor.fetchone.return_value = mock_user
        
        mock_conn = MagicMock()
        mock_conn.cursor.return_value = mock_cursor
        mock_db.return_value = mock_conn
        
        # Make request
        response = self.client.get('/users/1')
        
        # Assert response
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json['id'], 1)
        self.assertEqual(response.json['name'], 'John Doe')
        self.assertEqual(response.json['age'], 30)
    
    @patch('api_project.get_db_connection')
    def test_get_user_by_id_not_found(self, mock_db):
        """Test retrieving a non-existent user"""
        mock_cursor = MagicMock()
        mock_cursor.fetchone.return_value = None
        
        mock_conn = MagicMock()
        mock_conn.cursor.return_value = mock_cursor
        mock_db.return_value = mock_conn
        
        # Make request
        response = self.client.get('/users/999')
        
        # Assert response
        self.assertEqual(response.status_code, 404)
        self.assertEqual(response.json['error'], 'User not found')
    
    @patch('api_project.get_db_connection')
    def test_update_user_success(self, mock_db):
        """Test successful user update"""
        mock_cursor = MagicMock()
        mock_cursor.rowcount = 1  # Indicates a row was updated
        
        mock_conn = MagicMock()
        mock_conn.cursor.return_value = mock_cursor
        mock_db.return_value = mock_conn
        
        # Make request
        response = self.client.put(
            '/users/1',
            data=json.dumps({'name': 'Jane Smith', 'age': 32}),
            content_type='application/json'
        )
        
        # Assert response
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json['message'], 'User updated')
        
        # Assert database was called correctly
        mock_cursor.execute.assert_called_once()
        mock_conn.commit.assert_called_once()
    
    @patch('api_project.get_db_connection')
    def test_update_user_not_found(self, mock_db):
        """Test updating a non-existent user"""
        mock_cursor = MagicMock()
        mock_cursor.rowcount = 0  # Indicates no rows were updated
        
        mock_conn = MagicMock()
        mock_conn.cursor.return_value = mock_cursor
        mock_db.return_value = mock_conn
        
        # Make request
        response = self.client.put(
            '/users/999',
            data=json.dumps({'name': 'Jane Smith', 'age': 32}),
            content_type='application/json'
        )
        
        # Assert response
        self.assertEqual(response.status_code, 404)
        self.assertEqual(response.json['error'], 'User not found')
    
    @patch('api_project.get_db_connection')
    def test_delete_user_success(self, mock_db):
        """Test successful user deletion"""
        mock_cursor = MagicMock()
        mock_cursor.rowcount = 1  # Indicates a row was deleted
        
        mock_conn = MagicMock()
        mock_conn.cursor.return_value = mock_cursor
        mock_db.return_value = mock_conn
        
        # Make request
        response = self.client.delete('/users/1')
        
        # Assert response
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json['message'], 'User deleted')
        
        # Assert database was called
        mock_cursor.execute.assert_called_once()
        mock_conn.commit.assert_called_once()
    
    @patch('api_project.get_db_connection')
    def test_delete_user_not_found(self, mock_db):
        """Test deleting a non-existent user"""
        mock_cursor = MagicMock()
        mock_cursor.rowcount = 0  # Indicates no rows were deleted
        
        mock_conn = MagicMock()
        mock_conn.cursor.return_value = mock_cursor
        mock_db.return_value = mock_conn
        
        # Make request
        response = self.client.delete('/users/999')
        
        # Assert response
        self.assertEqual(response.status_code, 404)
        self.assertEqual(response.json['error'], 'User not found')
    
    @patch('api_project.get_db_connection')
    def test_post_wrong_method(self, mock_db):
        """Test using correct method on POST endpoint"""
        mock_cursor = MagicMock()
        mock_cursor.lastrowid = 1
        mock_conn = MagicMock()
        mock_conn.cursor.return_value = mock_cursor
        mock_db.return_value = mock_conn
        
        # POST to /users is actually correct, test a wrong method instead
        response = self.client.patch('/users', data='{}', content_type='application/json')
        
        # PATCH method should not be allowed
        self.assertEqual(response.status_code, 405)
    
    def test_app_is_running(self):
        """Test that the app is properly initialized"""
        self.assertTrue(self.app is not None)
        self.assertTrue(self.app.config['TESTING'])


class TestAPIEdgeCases(unittest.TestCase):
    """Test edge cases and error handling"""
    
    def setUp(self):
        """Set up test client"""
        self.app = app
        self.app.config['TESTING'] = True
        self.client = self.app.test_client()
    
    @patch('api_project.get_db_connection')
    def test_create_user_with_special_characters(self, mock_db):
        """Test creating user with special characters in name"""
        mock_cursor = MagicMock()
        mock_cursor.lastrowid = 1
        
        mock_conn = MagicMock()
        mock_conn.cursor.return_value = mock_cursor
        mock_db.return_value = mock_conn
        
        response = self.client.post(
            '/users',
            data=json.dumps({'name': "O'Brien", 'age': 30}),
            content_type='application/json'
        )
        
        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.json['name'], "O'Brien")
    
    @patch('api_project.get_db_connection')
    def test_create_user_with_negative_age(self, mock_db):
        """Test creating user with negative age"""
        mock_cursor = MagicMock()
        mock_cursor.lastrowid = 1
        
        mock_conn = MagicMock()
        mock_conn.cursor.return_value = mock_cursor
        mock_db.return_value = mock_conn
        
        response = self.client.post(
            '/users',
            data=json.dumps({'name': 'John', 'age': -5}),
            content_type='application/json'
        )
        
        # API doesn't validate, so it should still process
        self.assertEqual(response.status_code, 201)
    
    @patch('api_project.get_db_connection')
    def test_get_user_with_invalid_id_format(self, mock_db):
        """Test getting user with non-integer ID"""
        response = self.client.get('/users/abc')
        
        # Should return 404 because URL doesn't match pattern
        self.assertEqual(response.status_code, 404)


if __name__ == '__main__':
    unittest.main()
