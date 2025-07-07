from datetime import datetime
from flask_mysqldb import MySQL
from typing import Optional, List, Dict, Any
import logging

logger = logging.getLogger(__name__)

class DatabaseManager:
    """Database connection manager"""
    
    def __init__(self, mysql: MySQL):
        self.mysql = mysql
    
    def get_cursor(self):
        """Get database cursor with error handling"""
        try:
            return self.mysql.connection.cursor()
        except Exception as e:
            logger.error(f"Database connection error: {e}")
            raise DatabaseError("Unable to connect to database")
    
    def commit(self):
        """Commit database transaction"""
        try:
            self.mysql.connection.commit()
        except Exception as e:
            logger.error(f"Database commit error: {e}")
            raise DatabaseError("Database commit failed")

class DatabaseError(Exception):
    """Custom database exception"""
    pass

class User:
    """User model"""
    
    def __init__(self, db_manager: DatabaseManager):
        self.db = db_manager
    
    def create(self, name: str, email: str, username: str, password_hash: str) -> bool:
        """Create a new user"""
        try:
            cursor = self.db.get_cursor()
            query = "INSERT INTO user (name, email, uname, pwd, status) VALUES (%s, %s, %s, %s, %s)"
            cursor.execute(query, (name, email, username, password_hash, 0))
            self.db.commit()
            cursor.close()
            return True
        except Exception as e:
            logger.error(f"Error creating user: {e}")
            return False
    
    def get_by_username(self, username: str) -> Optional[Dict[str, Any]]:
        """Get user by username"""
        try:
            cursor = self.db.get_cursor()
            query = "SELECT * FROM user WHERE uname = %s"
            result = cursor.execute(query, (username,))
            user = cursor.fetchone() if result > 0 else None
            cursor.close()
            return user
        except Exception as e:
            logger.error(f"Error getting user by username: {e}")
            return None
    
    def get_by_id(self, user_id: int) -> Optional[Dict[str, Any]]:
        """Get user by ID"""
        try:
            cursor = self.db.get_cursor()
            query = "SELECT * FROM user WHERE id = %s"
            result = cursor.execute(query, (user_id,))
            user = cursor.fetchone() if result > 0 else None
            cursor.close()
            return user
        except Exception as e:
            logger.error(f"Error getting user by ID: {e}")
            return None
    
    def get_all(self) -> List[Dict[str, Any]]:
        """Get all users"""
        try:
            cursor = self.db.get_cursor()
            query = "SELECT * FROM user"
            result = cursor.execute(query)
            users = cursor.fetchall() if result > 0 else []
            cursor.close()
            return users
        except Exception as e:
            logger.error(f"Error getting all users: {e}")
            return []
    
    def update_status(self, user_id: int, status: int) -> bool:
        """Update user status"""
        try:
            cursor = self.db.get_cursor()
            query = "UPDATE user SET status = %s WHERE id = %s"
            cursor.execute(query, (status, user_id))
            self.db.commit()
            cursor.close()
            return True
        except Exception as e:
            logger.error(f"Error updating user status: {e}")
            return False
    
    def username_exists(self, username: str) -> bool:
        """Check if username exists"""
        try:
            cursor = self.db.get_cursor()
            query = "SELECT COUNT(*) as count FROM user WHERE uname = %s"
            cursor.execute(query, (username,))
            result = cursor.fetchone()
            cursor.close()
            return result['count'] > 0
        except Exception as e:
            logger.error(f"Error checking username existence: {e}")
            return False

class Article:
    """Article model"""
    
    def __init__(self, db_manager: DatabaseManager):
        self.db = db_manager
    
    def create(self, title: str, author: str, content: str, keywords: str) -> bool:
        """Create a new article"""
        try:
            cursor = self.db.get_cursor()
            query = "INSERT INTO articles (title, author, content, keywords) VALUES (%s, %s, %s, %s)"
            cursor.execute(query, (title, author, content, keywords))
            self.db.commit()
            cursor.close()
            return True
        except Exception as e:
            logger.error(f"Error creating article: {e}")
            return False
    
    def get_all(self) -> List[Dict[str, Any]]:
        """Get all articles"""
        try:
            cursor = self.db.get_cursor()
            query = "SELECT * FROM articles ORDER BY created_date DESC"
            result = cursor.execute(query)
            articles = cursor.fetchall() if result > 0 else []
            cursor.close()
            return articles
        except Exception as e:
            logger.error(f"Error getting all articles: {e}")
            return []
    
    def get_by_id(self, article_id: int) -> Optional[Dict[str, Any]]:
        """Get article by ID"""
        try:
            cursor = self.db.get_cursor()
            query = "SELECT * FROM articles WHERE id = %s"
            result = cursor.execute(query, (article_id,))
            article = cursor.fetchone() if result > 0 else None
            cursor.close()
            return article
        except Exception as e:
            logger.error(f"Error getting article by ID: {e}")
            return None
    
    def update(self, article_id: int, title: str, content: str, keywords: str) -> bool:
        """Update article"""
        try:
            cursor = self.db.get_cursor()
            query = "UPDATE articles SET title = %s, content = %s, keywords = %s WHERE id = %s"
            cursor.execute(query, (title, content, keywords, article_id))
            self.db.commit()
            cursor.close()
            return True
        except Exception as e:
            logger.error(f"Error updating article: {e}")
            return False
    
    def delete(self, article_id: int) -> bool:
        """Delete article"""
        try:
            cursor = self.db.get_cursor()
            query = "DELETE FROM articles WHERE id = %s"
            cursor.execute(query, (article_id,))
            self.db.commit()
            cursor.close()
            return True
        except Exception as e:
            logger.error(f"Error deleting article: {e}")
            return False

class Contact:
    """Contact model"""
    
    def __init__(self, db_manager: DatabaseManager):
        self.db = db_manager
    
    def create(self, email: str, name: str, surname: str, message: str) -> bool:
        """Create a new contact message"""
        try:
            cursor = self.db.get_cursor()
            query = "INSERT INTO contact (email, name, surname, message) VALUES (%s, %s, %s, %s)"
            cursor.execute(query, (email, name, surname, message))
            self.db.commit()
            cursor.close()
            return True
        except Exception as e:
            logger.error(f"Error creating contact message: {e}")
            return False
    
    def get_all(self) -> List[Dict[str, Any]]:
        """Get all contact messages"""
        try:
            cursor = self.db.get_cursor()
            query = "SELECT * FROM contact ORDER BY id DESC"
            result = cursor.execute(query)
            messages = cursor.fetchall() if result > 0 else []
            cursor.close()
            return messages
        except Exception as e:
            logger.error(f"Error getting contact messages: {e}")
            return []