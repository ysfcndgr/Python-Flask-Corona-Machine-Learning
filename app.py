"""
Corona Blog Application
Refactored for better scalability, security, and maintainability
"""

import os
import logging
from flask import Flask, render_template, flash, redirect, url_for, session, request, jsonify
from flask_mysqldb import MySQL
from flask_wtf.csrf import CSRFProtect
from passlib.hash import sha256_crypt

# Import custom modules
from config import config
from models import DatabaseManager, User, Article, Contact, DatabaseError
from forms import RegisterForm, LoginForm, ArticleForm, ContactForm, PredictionForm
from services import (
    CoronaAPIService, DateService, PredictionService, 
    AuthService, ValidationService, cache
)
from utils import (
    setup_logging, create_directories, login_required, admin_required, 
    active_user_required, register_template_filters, ResponseHelper
)

# Initialize Flask app
app = Flask(__name__)

# Load configuration
config_name = os.environ.get('FLASK_ENV', 'development')
app.config.from_object(config[config_name])

# Initialize extensions
mysql = MySQL(app)
csrf = CSRFProtect(app)

# Setup logging and directories
setup_logging(app)
create_directories()
register_template_filters(app)

# Initialize services
db_manager = DatabaseManager(mysql)
user_model = User(db_manager)
article_model = Article(db_manager)
contact_model = Contact(db_manager)

corona_api = CoronaAPIService(app.config['COLLECTAPI_KEY'])
prediction_service = PredictionService()
date_service = DateService()

logger = logging.getLogger(__name__)

# Error handlers
@app.errorhandler(404)
def not_found_error(error):
    return render_template('errors/404.html'), 404

@app.errorhandler(500)
def internal_error(error):
    logger.error(f"Internal server error: {error}")
    return render_template('errors/500.html'), 500

@app.errorhandler(DatabaseError)
def database_error(error):
    logger.error(f"Database error: {error}")
    flash("A database error occurred. Please try again later.", "danger")
    return redirect(url_for('main.index'))

# Main routes
@app.route("/")
def index():
    """Home page with predictions"""
    try:
        predictions = prediction_service.generate_predictions()
        dates = date_service.get_upcoming_dates()
        form = PredictionForm()
        
        return render_template("index.html", 
                             predictions=predictions, 
                             dates=dates, 
                             form=form)
    except Exception as e:
        logger.error(f"Error in index route: {e}")
        flash("Unable to load predictions", "warning")
        return render_template("index.html", 
                             predictions=([], []), 
                             dates=[], 
                             form=PredictionForm())

@app.route("/about")
def about():
    """About page"""
    return render_template("about.html")

@app.route("/information", methods=["GET", "POST"])
def information():
    """Corona information page"""
    try:
        # Check cache first
        cached_data = cache.get('corona_info')
        if cached_data:
            total_data, country_data = cached_data
        else:
            total_data = corona_api.get_total_data()
            country_data = corona_api.get_countries_data()
            cache.set('corona_info', (total_data, country_data), 300)  # 5 minutes cache
        
        return render_template("information.html", 
                             data=total_data, 
                             countrydata=country_data)
    except Exception as e:
        logger.error(f"Error in information route: {e}")
        flash("Unable to load Corona information", "warning")
        return render_template("information.html", data={}, countrydata=[])

@app.route("/information/countrybyname/<string:country>")
def country_by_name(country):
    """Get specific country Corona data"""
    try:
        data = corona_api.get_country_by_name(country)
        return jsonify(ResponseHelper.success(data))
    except Exception as e:
        logger.error(f"Error getting country data: {e}")
        return jsonify(ResponseHelper.error("Unable to fetch country data")), 500

@app.route("/news")
def news():
    """Corona news page"""
    try:
        # Check cache first
        cached_news = cache.get('corona_news')
        if cached_news:
            news_data = cached_news
        else:
            news_data = corona_api.get_corona_news()
            cache.set('corona_news', news_data, 300)  # 5 minutes cache
        
        return render_template("news.html", 
                             coronanews=news_data, 
                             coronacount=len(news_data))
    except Exception as e:
        logger.error(f"Error in news route: {e}")
        flash("Unable to load news", "warning")
        return render_template("news.html", coronanews=[], coronacount=0)

# Authentication routes
@app.route("/register", methods=["GET", "POST"])
def register():
    """User registration"""
    form = RegisterForm()
    
    if form.validate_on_submit():
        try:
            # Check if username exists
            if user_model.username_exists(form.username.data):
                flash("Username already exists", "danger")
                return render_template("register.html", form=form)
            
            # Hash password
            password_hash = sha256_crypt.encrypt(form.password.data)
            
            # Create user
            if user_model.create(
                name=form.name.data,
                email=form.email.data,
                username=form.username.data,
                password_hash=password_hash
            ):
                flash("Registration successful! You can now login.", "success")
                return redirect(url_for("login"))
            else:
                flash("Registration failed. Please try again.", "danger")
                
        except Exception as e:
            logger.error(f"Registration error: {e}")
            flash("An error occurred during registration", "danger")
    
    return render_template("register.html", form=form)

@app.route("/login", methods=["GET", "POST"])
def login():
    """User login"""
    form = LoginForm()
    
    if form.validate_on_submit():
        try:
            user = user_model.get_by_username(form.username.data)
            
            if user and sha256_crypt.verify(form.password.data, user['pwd']):
                # Check if user is banned
                if AuthService.is_banned(user['status']):
                    flash("Your account has been suspended", "danger")
                    return render_template("blog.html", articles=[], form=form)
                
                # Set session
                session.permanent = True
                session["logged_in"] = True
                session["username"] = user['uname']
                session["status"] = user['status']
                session["user_id"] = user['id']
                
                flash(f"Welcome back, {user['name']}!", "success")
                
                # Redirect based on user role
                if AuthService.is_admin(user['status']):
                    return redirect(url_for("dashboard"))
                else:
                    return redirect(url_for("blog"))
            else:
                flash("Invalid username or password", "danger")
                
        except Exception as e:
            logger.error(f"Login error: {e}")
            flash("An error occurred during login", "danger")
    
    return render_template("blog.html", articles=article_model.get_all(), form=form)

@app.route("/logout")
@login_required
def logout():
    """User logout"""
    username = session.get("username", "User")
    session.clear()
    flash(f"Goodbye, {username}! You have been logged out.", "success")
    return redirect(url_for("blog"))

# Blog routes
@app.route("/blog", methods=["GET", "POST"])
def blog():
    """Blog page with articles"""
    if request.method == "POST":
        return login()  # Handle login form submission
    
    try:
        articles = article_model.get_all()
        return render_template("blog.html", articles=articles, form=LoginForm())
    except Exception as e:
        logger.error(f"Error in blog route: {e}")
        flash("Unable to load articles", "warning")
        return render_template("blog.html", articles=[], form=LoginForm())

@app.route("/blog/<int:article_id>")
def article_detail(article_id):
    """Article detail page"""
    try:
        article = article_model.get_by_id(article_id)
        if article:
            return render_template("detail.html", article=article)
        else:
            flash("Article not found", "warning")
            return redirect(url_for("blog"))
    except Exception as e:
        logger.error(f"Error in article detail route: {e}")
        flash("Unable to load article", "danger")
        return redirect(url_for("blog"))

# Admin routes
@app.route("/dashboard")
@admin_required
def dashboard():
    """Admin dashboard"""
    try:
        articles = article_model.get_all()
        return render_template("dashboard.html", articles=articles)
    except Exception as e:
        logger.error(f"Error in dashboard route: {e}")
        flash("Unable to load dashboard", "danger")
        return render_template("dashboard.html", articles=[])

@app.route("/addarticle", methods=["GET", "POST"])
@admin_required
def add_article():
    """Add new article"""
    form = ArticleForm()
    
    if form.validate_on_submit():
        try:
            # Sanitize content
            content = ValidationService.sanitize_html(form.content.data)
            
            if article_model.create(
                title=form.title.data,
                author=session["username"],
                content=content,
                keywords=form.keywords.data
            ):
                flash("Article successfully added", "success")
                return redirect(url_for("dashboard"))
            else:
                flash("Failed to add article", "danger")
                
        except Exception as e:
            logger.error(f"Error adding article: {e}")
            flash("An error occurred while adding the article", "danger")
    
    return render_template("addarticle.html", form=form)

@app.route("/edit/<int:article_id>", methods=["GET", "POST"])
@admin_required
def edit_article(article_id):
    """Edit article"""
    try:
        article = article_model.get_by_id(article_id)
        if not article:
            flash("Article not found", "danger")
            return redirect(url_for("dashboard"))
        
        form = ArticleForm(obj=article) if request.method == "GET" else ArticleForm()
        
        if form.validate_on_submit():
            content = ValidationService.sanitize_html(form.content.data)
            
            if article_model.update(
                article_id=article_id,
                title=form.title.data,
                content=content,
                keywords=form.keywords.data
            ):
                flash("Article successfully updated", "success")
                return redirect(url_for("dashboard"))
            else:
                flash("Failed to update article", "danger")
        
        # Pre-populate form for GET request
        if request.method == "GET":
            form.title.data = article['title']
            form.content.data = article['content']
            form.keywords.data = article['keywords']
        
        return render_template("update.html", form=form, article=article)
        
    except Exception as e:
        logger.error(f"Error editing article: {e}")
        flash("An error occurred while editing the article", "danger")
        return redirect(url_for("dashboard"))

@app.route("/delete/<int:article_id>")
@admin_required
def delete_article(article_id):
    """Delete article"""
    try:
        if article_model.delete(article_id):
            flash("Article successfully deleted", "success")
        else:
            flash("Article not found", "warning")
    except Exception as e:
        logger.error(f"Error deleting article: {e}")
        flash("An error occurred while deleting the article", "danger")
    
    return redirect(url_for("dashboard"))

# User management routes
@app.route("/usersettings")
@admin_required
def user_settings():
    """User management page"""
    try:
        users = user_model.get_all()
        return render_template("usersettings.html", users=users)
    except Exception as e:
        logger.error(f"Error in user settings route: {e}")
        flash("Unable to load user settings", "danger")
        return render_template("usersettings.html", users=[])

@app.route("/ban/<int:user_id>")
@admin_required
def ban_user(user_id):
    """Ban user"""
    try:
        if user_model.update_status(user_id, 2):  # Status 2 = banned
            flash("User successfully banned", "success")
        else:
            flash("User not found", "warning")
    except Exception as e:
        logger.error(f"Error banning user: {e}")
        flash("An error occurred while banning the user", "danger")
    
    return redirect(url_for("user_settings"))

@app.route("/removeban/<int:user_id>")
@admin_required
def remove_ban(user_id):
    """Remove user ban"""
    try:
        if user_model.update_status(user_id, 0):  # Status 0 = active
            flash("User ban successfully removed", "success")
        else:
            flash("User not found", "warning")
    except Exception as e:
        logger.error(f"Error removing ban: {e}")
        flash("An error occurred while removing the ban", "danger")
    
    return redirect(url_for("user_settings"))

@app.route("/makeadmin/<int:user_id>")
@admin_required
def make_admin(user_id):
    """Make user admin"""
    try:
        if user_model.update_status(user_id, 1):  # Status 1 = admin
            flash("User successfully made admin", "success")
        else:
            flash("User not found", "warning")
    except Exception as e:
        logger.error(f"Error making user admin: {e}")
        flash("An error occurred while updating user permissions", "danger")
    
    return redirect(url_for("user_settings"))

# Contact routes
@app.route("/contact", methods=["GET", "POST"])
def contact():
    """Contact page"""
    form = ContactForm()
    
    if form.validate_on_submit():
        try:
            if contact_model.create(
                email=form.email.data,
                name=form.name.data,
                surname=form.surname.data,
                message=form.message.data
            ):
                flash("Message sent successfully! We'll get back to you soon.", "success")
                return redirect(url_for("contact"))
            else:
                flash("Failed to send message. Please try again.", "danger")
                
        except Exception as e:
            logger.error(f"Error sending contact message: {e}")
            flash("An error occurred while sending your message", "danger")
    
    return render_template("contact.html", form=form)

@app.route("/contactmessages")
@admin_required
def contact_messages():
    """View contact messages (admin only)"""
    try:
        messages = contact_model.get_all()
        return render_template("contactmessage.html", messages=messages)
    except Exception as e:
        logger.error(f"Error loading contact messages: {e}")
        flash("Unable to load contact messages", "danger")
        return render_template("contactmessage.html", messages=[])

# API routes
@app.route("/api/predictions", methods=["POST"])
def api_predictions():
    """API endpoint for predictions"""
    try:
        form = PredictionForm()
        if form.validate_on_submit():
            days = form.days.data
            predictions = prediction_service.generate_predictions(days)
            dates = date_service.get_upcoming_dates(days)
            
            return jsonify(ResponseHelper.success({
                "predictions": predictions,
                "dates": [date_service.format_date(d) for d in dates]
            }))
        else:
            return jsonify(ResponseHelper.error("Invalid form data")), 400
            
    except Exception as e:
        logger.error(f"Error in predictions API: {e}")
        return jsonify(ResponseHelper.error("Unable to generate predictions")), 500

# Health check route
@app.route("/health")
def health_check():
    """Health check endpoint"""
    try:
        # Test database connection
        cursor = db_manager.get_cursor()
        cursor.execute("SELECT 1")
        cursor.close()
        
        return jsonify(ResponseHelper.success({
            "status": "healthy",
            "database": "connected",
            "cache": "active"
        }))
    except Exception as e:
        logger.error(f"Health check failed: {e}")
        return jsonify(ResponseHelper.error("System unhealthy")), 500

if __name__ == "__main__":
    # Run application
    app.run(
        debug=app.config.get('DEBUG', False),
        host='0.0.0.0',
        port=int(os.environ.get('PORT', 5000))
    )