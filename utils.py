import logging
import os
from functools import wraps
from flask import session, redirect, url_for, flash, request
from typing import Callable, Any, Optional
from datetime import datetime
import secrets

def setup_logging(app) -> None:
    """Setup application logging"""
    if not os.path.exists('logs'):
        os.makedirs('logs')
    
    log_level = getattr(logging, app.config.get('LOG_LEVEL', 'INFO'))
    log_file = app.config.get('LOG_FILE', 'logs/app.log')
    
    logging.basicConfig(
        level=log_level,
        format='%(asctime)s %(name)s %(levelname)s: %(message)s',
        handlers=[
            logging.FileHandler(log_file),
            logging.StreamHandler()
        ]
    )

def create_directories() -> None:
    """Create necessary directories"""
    directories = ['logs', 'static/uploads', 'instance']
    for directory in directories:
        if not os.path.exists(directory):
            os.makedirs(directory)

def login_required(f: Callable) -> Callable:
    """Decorator to require login for routes"""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if "logged_in" not in session:
            flash("You need to login to access this page", "warning")
            return redirect(url_for("auth.login"))
        return f(*args, **kwargs)
    return decorated_function

def admin_required(f: Callable) -> Callable:
    """Decorator to require admin access for routes"""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if "logged_in" not in session:
            flash("You need to login to access this page", "warning")
            return redirect(url_for("auth.login"))
        
        if session.get("status") != 1:
            flash("You don't have permission to access this page", "danger")
            return redirect(url_for("main.blog"))
        
        return f(*args, **kwargs)
    return decorated_function

def active_user_required(f: Callable) -> Callable:
    """Decorator to check if user is active (not banned)"""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if "logged_in" not in session:
            flash("You need to login to access this page", "warning")
            return redirect(url_for("auth.login"))
        
        user_status = session.get("status", 0)
        if user_status == 2:  # Banned
            flash("Your account has been suspended", "danger")
            session.clear()
            return redirect(url_for("main.blog"))
        
        return f(*args, **kwargs)
    return decorated_function

class ResponseHelper:
    """Helper class for consistent API responses"""
    
    @staticmethod
    def success(data: Any = None, message: str = "Success") -> dict:
        """Create success response"""
        return {
            "status": "success",
            "message": message,
            "data": data,
            "timestamp": datetime.utcnow().isoformat()
        }
    
    @staticmethod
    def error(message: str = "Error occurred", error_code: int = 500) -> dict:
        """Create error response"""
        return {
            "status": "error",
            "message": message,
            "error_code": error_code,
            "timestamp": datetime.utcnow().isoformat()
        }

class SecurityHelper:
    """Helper class for security-related functions"""
    
    @staticmethod
    def generate_csrf_token() -> str:
        """Generate CSRF token"""
        return secrets.token_hex(16)
    
    @staticmethod
    def generate_session_token() -> str:
        """Generate session token"""
        return secrets.token_urlsafe(32)
    
    @staticmethod
    def is_safe_url(target: str) -> bool:
        """Check if URL is safe for redirect"""
        from urllib.parse import urljoin, urlparse
        
        if not target:
            return False
        
        ref_url = urlparse(request.host_url)
        test_url = urlparse(urljoin(request.host_url, target))
        
        return test_url.scheme in ('http', 'https') and ref_url.netloc == test_url.netloc

class PaginationHelper:
    """Helper class for pagination"""
    
    def __init__(self, page: int, per_page: int, total: int):
        self.page = page
        self.per_page = per_page
        self.total = total
    
    @property
    def items(self) -> int:
        """Calculate items on current page"""
        return min(self.per_page, self.total - (self.page - 1) * self.per_page)
    
    @property
    def prev_num(self) -> Optional[int]:
        """Get previous page number"""
        return self.page - 1 if self.has_prev else None
    
    @property
    def next_num(self) -> Optional[int]:
        """Get next page number"""
        return self.page + 1 if self.has_next else None
    
    @property
    def has_prev(self) -> bool:
        """Check if has previous page"""
        return self.page > 1
    
    @property
    def has_next(self) -> bool:
        """Check if has next page"""
        return self.page < self.pages
    
    @property
    def pages(self) -> int:
        """Calculate total pages"""
        return (self.total - 1) // self.per_page + 1 if self.total > 0 else 1
    
    def iter_pages(self, left_edge: int = 2, left_current: int = 2, 
                   right_current: int = 3, right_edge: int = 2) -> list:
        """Iterate through page numbers for pagination display"""
        last = self.pages
        pages = []
        
        for num in range(1, last + 1):
            if num <= left_edge or \
               (self.page - left_current - 1 < num < self.page + right_current) or \
               num > last - right_edge:
                pages.append(num)
        
        return pages

class FileHelper:
    """Helper class for file operations"""
    
    ALLOWED_EXTENSIONS = {'txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif', 'doc', 'docx'}
    
    @staticmethod
    def allowed_file(filename: str) -> bool:
        """Check if file extension is allowed"""
        return '.' in filename and \
               filename.rsplit('.', 1)[1].lower() in FileHelper.ALLOWED_EXTENSIONS
    
    @staticmethod
    def secure_filename(filename: str) -> str:
        """Generate secure filename"""
        import unicodedata
        import re
        
        filename = unicodedata.normalize('NFKD', filename)
        filename = filename.encode('ascii', 'ignore').decode('ascii')
        filename = re.sub(r'[^\w\s-]', '', filename).strip()
        filename = re.sub(r'[-\s]+', '-', filename)
        
        # Add timestamp to avoid conflicts
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        name, ext = os.path.splitext(filename)
        return f"{name}_{timestamp}{ext}"

class ValidationHelper:
    """Helper class for validation functions"""
    
    @staticmethod
    def is_strong_password(password: str) -> tuple:
        """Check if password is strong enough"""
        errors = []
        
        if len(password) < 8:
            errors.append("Password must be at least 8 characters long")
        
        if not any(c.isupper() for c in password):
            errors.append("Password must contain at least one uppercase letter")
        
        if not any(c.islower() for c in password):
            errors.append("Password must contain at least one lowercase letter")
        
        if not any(c.isdigit() for c in password):
            errors.append("Password must contain at least one number")
        
        special_chars = "!@#$%^&*()_+-=[]{}|;:,.<>?"
        if not any(c in special_chars for c in password):
            errors.append("Password must contain at least one special character")
        
        return len(errors) == 0, errors
    
    @staticmethod
    def sanitize_input(text: str) -> str:
        """Basic input sanitization"""
        if not text:
            return ""
        
        # Remove null bytes
        text = text.replace('\x00', '')
        
        # Strip whitespace
        text = text.strip()
        
        return text

class TemplateHelper:
    """Helper functions for templates"""
    
    @staticmethod
    def truncate_text(text: str, length: int = 100, suffix: str = "...") -> str:
        """Truncate text to specified length"""
        if len(text) <= length:
            return text
        return text[:length].rsplit(' ', 1)[0] + suffix
    
    @staticmethod
    def format_datetime(dt, format_str: str = "%Y-%m-%d %H:%M") -> str:
        """Format datetime for display"""
        if isinstance(dt, str):
            try:
                # Handle ISO format strings
                if dt.endswith('Z'):
                    dt_str = dt[:-1] + '+00:00'
                else:
                    dt_str = dt
                dt = datetime.fromisoformat(dt_str)
            except ValueError:
                return dt
        
        return dt.strftime(format_str) if dt else ""
    
    @staticmethod
    def pluralize(count: int, singular: str, plural: str = None) -> str:
        """Pluralize word based on count"""
        if plural is None:
            plural = singular + 's'
        
        return singular if count == 1 else plural

# Template filters that can be added to Flask app
def register_template_filters(app):
    """Register custom template filters"""
    app.jinja_env.filters['truncate_text'] = TemplateHelper.truncate_text
    app.jinja_env.filters['format_datetime'] = TemplateHelper.format_datetime
    app.jinja_env.filters['pluralize'] = TemplateHelper.pluralize