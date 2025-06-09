# 🐾 PetPal - AI-Powered Pet Care & Health Tracker

[![Version](https://img.shields.io/badge/version-2.0.0-blue.svg)](https://github.com/your-repo/petpal)
[![Python](https://img.shields.io/badge/python-3.8+-green.svg)](https://python.org)
[![Flask](https://img.shields.io/badge/flask-2.0+-red.svg)](https://flask.palletsprojects.com)
[![PostgreSQL](https://img.shields.io/badge/postgresql-13+-blue.svg)](https://postgresql.org)

A comprehensive, AI-powered web application for managing pet care, health records, and daily tasks with intelligent breed-specific recommendations and modern interactive design.

## ✨ Features

### 🏠 Core Functionality
- **Multi-Pet Management**: Create detailed profiles for unlimited pets with photo uploads
- **Health Records Tracking**: Comprehensive vaccination, medication, and vet visit history
- **Weight Monitoring**: Interactive charts and trend analysis for pet weight tracking
- **Task Management**: Smart to-do lists with due dates and completion tracking
- **Smart Reminders**: Recurring notifications for feeding, medications, and appointments
- **Emergency Contacts**: Quick access to veterinary and emergency information

### 🤖 AI-Powered Features
- **Breed-Specific Care Tips**: Personalized recommendations via OpenRouter AI integration
- **Health Insights**: AI-generated suggestions based on pet age, breed, and history
- **Dynamic Content**: Rotating daily tips and educational pet facts
- **Smart Notifications**: Contextual reminders based on pet profiles

### 🎨 Modern User Experience
- **Glassmorphism Design**: Beautiful translucent UI with gradient effects
- **Responsive Layout**: Perfect experience on desktop, tablet, and mobile
- **Interactive Animations**: Smooth transitions and engaging micro-interactions
- **Floating Action Buttons**: Quick access to common actions
- **Real-time Updates**: Live timestamp updates and dynamic content refresh
- **Accessibility**: Full keyboard navigation and screen reader support

### 📊 Analytics & Insights
- **Dashboard Statistics**: Visual overview of all pets and pending tasks
- **Weight Trend Charts**: Interactive Chart.js visualizations
- **Health Status Indicators**: Color-coded health monitoring
- **Progress Tracking**: Task completion rates and care consistency

## 🛠 Technology Stack

| Component | Technology | Purpose |
|-----------|------------|---------|
| **Backend** | Flask 2.3+ | Web framework and API |
| **Database** | PostgreSQL 13+ | Data persistence with SQLAlchemy ORM |
| **Frontend** | Bootstrap 5 | Responsive UI framework |
| **Styling** | Custom CSS3 | Glassmorphism effects and animations |
| **Charts** | Chart.js 3.9+ | Interactive weight tracking visualizations |
| **Icons** | Feather Icons | Consistent iconography |
| **AI** | OpenRouter API | Intelligent care recommendations |
| **Server** | Gunicorn | Production WSGI server |

## 🚀 Quick Start

### Prerequisites
- Python 3.8 or higher
- PostgreSQL 13 or higher
- Git

### Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/your-repo/petpal.git
   cd petpal
   ```

2. **Set up virtual environment**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Configure environment**
   ```bash
   cp .env.example .env
   # Edit .env with your settings
   ```

5. **Initialize database**
   ```bash
   flask db upgrade
   ```

6. **Run the application**
   ```bash
   python main.py
   ```

Visit `http://localhost:5000` to access PetPal!

## ⚙️ Configuration

### Environment Variables

Create a `.env` file with these essential variables:

```bash
# 🗄️ Database Configuration
DATABASE_URL=postgresql://username:password@localhost:5432/petpal_db

# 🔐 Security Settings
SESSION_SECRET=your-super-secure-session-key
FLASK_SECRET_KEY=your-flask-secret-key

# 🤖 AI Integration
OPENROUTER_API_KEY=your-openrouter-api-key-here
AI_MODEL=meta-llama/llama-3.1-8b-instruct:free

# 🌐 Application Settings
FLASK_ENV=development
FLASK_DEBUG=True

# 📸 Upload Configuration
MAX_CONTENT_LENGTH=16777216  # 16MB
UPLOAD_FOLDER=static/uploads
ALLOWED_EXTENSIONS=png,jpg,jpeg,gif,webp

# 🎨 Theme Settings
THEME_COLOR_PRIMARY=#4a90e2
THEME_COLOR_SECONDARY=#7b68ee
ENABLE_ANIMATIONS=true
CARD_STYLE=glassmorphism
```

### Feature Flags

Enable or disable features by setting these variables:

```bash
ENABLE_WEIGHT_TRACKING=true
ENABLE_AI_TIPS=true
ENABLE_PHOTO_UPLOADS=true
ENABLE_REMINDERS=true
ENABLE_HEALTH_RECORDS=true
ENABLE_TASK_MANAGEMENT=true
```

## 📱 Usage Guide

### Getting Started
1. **Create Account**: Register with email and secure password
2. **Add First Pet**: Upload photo and enter basic information (name, species, breed, age)
3. **Set Up Health Records**: Add vaccination history and vet contact information
4. **Create Care Tasks**: Set up feeding schedules and recurring reminders
5. **Track Weight**: Log regular weight measurements for health monitoring

### Advanced Features
- **AI Care Tips**: Access breed-specific recommendations on the dashboard
- **Weight Charts**: View weight trends and export data
- **Smart Reminders**: Set up complex recurring schedules
- **Multi-Pet Management**: Switch between pets using the dashboard
- **Emergency Mode**: Quick access to vet contacts and medical history

## 🎯 API Endpoints

### Pet Management
- `GET /dashboard` - Main dashboard with pet overview
- `POST /add_pet` - Create new pet profile
- `GET /pet/<id>` - View pet details
- `PUT /edit_pet/<id>` - Update pet information
- `DELETE /delete_pet/<id>` - Remove pet profile

### Health Records
- `GET /pet/<id>/health` - View health records
- `POST /pet/<id>/health/add` - Add new health record
- `GET /pet/<id>/weight/chart` - Weight chart data (JSON)

### Task Management
- `GET /pet/<id>/tasks` - View care checklist
- `POST /pet/<id>/tasks/add` - Create new task
- `PUT /tasks/<id>/complete` - Mark task as complete

## 🔧 Development

### Project Structure
```
petpal/
├── app.py              # Flask application factory
├── main.py             # Application entry point
├── models.py           # Database models
├── routes.py           # URL routes and handlers
├── utils.py            # Helper functions
├── static/
│   ├── css/
│   │   └── style.css   # Custom styles and animations
│   ├── js/
│   │   └── main.js     # Interactive functionality
│   └── uploads/        # Pet photos
├── templates/          # Jinja2 templates
├── .env               # Environment configuration
└── requirements.txt   # Python dependencies
```

### Development Commands

```bash
# Run in development mode
python main.py

# Database migrations
flask db migrate -m "Description"
flask db upgrade

# Run tests
python -m pytest

# Code formatting
black .
flake8 .
```

### Contributing

1. Fork the repository
2. Create a feature branch: `git checkout -b feature/amazing-feature`
3. Commit changes: `git commit -m 'Add amazing feature'`
4. Push to branch: `git push origin feature/amazing-feature`
5. Open a Pull Request

## 🐛 Troubleshooting

### Common Issues

**Database Connection Error**
- Verify PostgreSQL is running
- Check DATABASE_URL format
- Ensure database exists

**AI Tips Not Loading**
- Verify OPENROUTER_API_KEY is set
- Check API key validity
- Review network connectivity

**File Upload Issues**
- Check UPLOAD_FOLDER permissions
- Verify MAX_CONTENT_LENGTH setting
- Ensure allowed file extensions

### Debug Mode

Enable detailed logging:
```bash
export FLASK_DEBUG=True
export LOG_LEVEL=DEBUG
python main.py
```

## 📊 Performance

### Optimization Features
- **Database Indexing**: Optimized queries for large datasets
- **Image Compression**: Automatic photo resizing and compression
- **Caching**: Session-based caching for frequently accessed data
- **Lazy Loading**: Progressive image loading for better performance
- **Minified Assets**: Compressed CSS and JavaScript files

### Monitoring
- Performance logging enabled in production
- Error tracking with detailed stack traces
- User interaction analytics (optional)

## 🔒 Security

### Security Features
- **Password Hashing**: Secure bcrypt password storage
- **Session Management**: Secure session handling with expiration
- **CSRF Protection**: Cross-site request forgery prevention
- **Input Validation**: Comprehensive form validation and sanitization
- **File Upload Security**: Restricted file types and size limits
- **SQL Injection Prevention**: Parameterized queries with SQLAlchemy

### Best Practices
- Regular security updates
- Environment variable protection
- HTTPS enforcement in production
- Secure headers implementation

## 📈 Roadmap

### Version 2.1 (Coming Soon)
- [ ] Mobile app companion
- [ ] Veterinary portal integration
- [ ] Advanced health analytics
- [ ] Social sharing features
- [ ] Medication reminder notifications

### Version 2.2 (Future)
- [ ] Multi-language support
- [ ] Advanced AI health predictions
- [ ] Integration with pet health devices
- [ ] Telemedicine features
- [ ] Community features

## 🤝 Support

### Getting Help
- **Documentation**: Check this README and inline code comments
- **Issues**: Report bugs via GitHub Issues
- **Discussions**: Join community discussions
- **Email**: Contact support@petpal.app

### Community
- GitHub Discussions for feature requests
- Discord server for real-time chat
- Monthly community calls

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- **OpenRouter** for AI integration capabilities
- **Bootstrap Team** for the excellent CSS framework
- **Feather Icons** for beautiful iconography
- **Chart.js** for interactive visualizations
- **Flask Community** for the robust web framework
- **PostgreSQL Team** for reliable data storage

---

**Made with ❤️ for pet lovers everywhere**

*PetPal - Because every pet deserves the best care possible.*