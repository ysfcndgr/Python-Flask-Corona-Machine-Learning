# Corona Blog - Refactored & Improved

## 🚀 What's New

This project has been completely refactored to address security vulnerabilities, improve code organization, and enhance scalability. The new version is production-ready with modern best practices.

## ✨ Key Improvements

### 🔒 Security Enhancements
- **CSRF Protection**: All forms now include CSRF tokens
- **Input Validation**: Comprehensive form validation with sanitization
- **Session Security**: Secure session management with proper timeouts
- **Password Strength**: Enforced strong password requirements
- **SQL Injection Protection**: Parameterized queries throughout
- **Environment Variables**: No more hardcoded credentials

### 🏗️ Architecture Improvements
- **Modular Design**: Code split into logical modules (models, forms, services, utils)
- **Separation of Concerns**: Business logic separated from route handlers
- **Type Hints**: Full type annotations for better code quality
- **Error Handling**: Comprehensive error handling with logging
- **Configuration Management**: Environment-based configuration

### ⚡ Performance Optimizations
- **Caching**: API responses and expensive operations are cached
- **Database Optimization**: Improved queries with proper error handling
- **Async-Ready**: Structure prepared for async operations

### 🛠️ Developer Experience
- **Logging**: Comprehensive logging system
- **Documentation**: Full docstrings and comments
- **Testing Ready**: Structure prepared for unit tests
- **Code Quality**: Consistent formatting and linting

## 📁 New Project Structure

```
coronablog/
├── app.py                 # New main application (replaces main.py)
├── config.py             # Configuration management
├── models.py             # Database models and operations
├── forms.py              # Form definitions and validation
├── services.py           # Business logic and external APIs
├── utils.py              # Helper functions and decorators
├── requirements.txt      # Updated dependencies
├── .env.example          # Environment variables template
├── main.py               # DEPRECATED - use app.py instead
├── templates/
│   ├── errors/           # Error pages (404, 500)
│   └── ...               # Existing templates
├── static/
├── logs/                 # Application logs
└── instance/             # Instance-specific files
```

## 🚀 Quick Start

### 1. Setup Environment

```bash
# Copy environment template
cp .env.example .env

# Edit .env with your settings
nano .env
```

### 2. Install Dependencies

```bash
# Install required packages
pip install -r requirements.txt
```

### 3. Database Setup

```bash
# Import the database schema
mysql -u root -p coronablog < coronablog.sql
```

### 4. Run Application

```bash
# Use the new refactored application
python app.py

# NOT: python main.py (deprecated)
```

## 🔧 Configuration

### Environment Variables

Create a `.env` file based on `.env.example`:

```env
# Essential settings
SECRET_KEY=your-very-secure-secret-key
MYSQL_PASSWORD=your-database-password
COLLECTAPI_KEY=your-api-key

# Optional settings
FLASK_ENV=development  # or production
DEBUG=true            # false for production
LOG_LEVEL=INFO        # DEBUG, INFO, WARNING, ERROR
```

### API Keys

Get your CollectAPI key from: https://collectapi.com/

## 📊 Features

### For Users
- **Secure Registration**: Strong password requirements
- **Article Management**: Full CRUD operations
- **Corona Data**: Real-time data with caching
- **News Feed**: Latest Corona news
- **Predictions**: ML-based case predictions
- **Contact System**: Secure contact form

### For Admins
- **User Management**: Ban/unban users, assign admin roles
- **Content Moderation**: Manage articles and messages
- **Dashboard**: Comprehensive admin panel
- **Analytics**: View contact messages and user activity

### For Developers
- **Health Check**: `/health` endpoint for monitoring
- **API Endpoints**: RESTful API with proper error handling
- **Logging**: Comprehensive logging system
- **Caching**: Built-in caching for performance
- **Error Pages**: Custom 404/500 pages

## 🔒 Security Features

### Authentication & Authorization
- Secure password hashing (SHA256-Crypt)
- Session-based authentication
- Role-based access control (User, Admin, Banned)
- CSRF protection on all forms

### Input Validation
- Server-side form validation
- HTML sanitization
- SQL injection protection
- XSS prevention

### Security Headers
- Secure session cookies
- HTTPOnly cookies
- CSRF tokens

## 📈 Performance Features

### Caching
- API response caching (5-minute TTL)
- Expensive operation caching
- Simple in-memory cache implementation

### Database
- Optimized queries
- Proper connection management
- Error handling and recovery

## 🧪 Testing

The new structure is ready for testing:

```bash
# Install test dependencies
pip install pytest pytest-flask

# Run tests (when implemented)
pytest
```

## 📝 API Endpoints

### Public Endpoints
- `GET /` - Home page with predictions
- `GET /blog` - Blog articles
- `GET /information` - Corona data
- `GET /news` - Corona news
- `POST /contact` - Contact form
- `GET /health` - Health check

### Authentication
- `POST /register` - User registration
- `POST /login` - User login
- `GET /logout` - User logout

### Admin Only
- `GET /dashboard` - Admin dashboard
- `POST /addarticle` - Add article
- `PUT /edit/<id>` - Edit article
- `DELETE /delete/<id>` - Delete article
- `GET /usersettings` - User management

### API Routes
- `POST /api/predictions` - Generate predictions
- `GET /information/countrybyname/<country>` - Country data

## 🚨 Migration Guide

### From Old Version (main.py) to New Version (app.py)

1. **Stop using main.py** - It's deprecated
2. **Use app.py** - The new main application file
3. **Set environment variables** - Create `.env` file
4. **Update dependencies** - Run `pip install -r requirements.txt`
5. **Update templates** - If you customized any templates

### Breaking Changes
- Configuration now uses environment variables
- Some route names may have changed
- Form validation is stricter
- CSRF tokens required on forms

## 🐛 Troubleshooting

### Common Issues

**Database Connection Error**
```bash
# Check your .env file
# Ensure MySQL is running
# Verify database credentials
```

**CSRF Token Missing**
```bash
# Ensure forms include {{ csrf_token() }}
# Check CSRF is enabled in config
```

**API Key Errors**
```bash
# Verify COLLECTAPI_KEY in .env
# Check API key is valid
```

## 📚 Dependencies

### Core Dependencies
- Flask 2.3+ - Web framework
- Flask-MySQLdb - Database connectivity
- Flask-WTF - Form handling and CSRF
- Passlib - Password hashing
- Pandas & Scikit-learn - ML predictions

### Security Dependencies
- Bleach - HTML sanitization
- Werkzeug - Security utilities

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

## 📄 License

This project is licensed under the MIT License.

## 🔄 Version History

- **v2.0** (Current) - Complete refactor with security and performance improvements
- **v1.0** - Original version (main.py)

---

## ⚠️ Important Notes

1. **Use `app.py` instead of `main.py`**
2. **Set up environment variables before running**
3. **The old main.py is deprecated and will be removed**
4. **This version requires Python 3.8+**

For any issues or questions, please check the troubleshooting section or create an issue in the repository.