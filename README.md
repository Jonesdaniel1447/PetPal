# 🐾 PetPal – AI-Powered Pet Care & Health Tracker

## Overview
PetPal is a comprehensive web application designed to help pet owners manage their pets' daily care, health records, and receive AI-generated breed-specific care recommendations. Built with Flask and PostgreSQL, it provides a complete solution for responsible pet ownership.

## ✨ Features

### 🐕 Pet Management
- Create detailed profiles for multiple pets
- Upload and manage pet photos
- Track breed-specific information and vital statistics

### 💊 Health Tracking
- Log vaccinations, medications, and vet visits
- Track weight changes with visual charts
- Maintain comprehensive health records

### 📋 Care Management
- Create and manage daily care checklists
- Set recurring reminders for feeding, grooming, and exercise
- Track task completion with timestamps

### 🤖 AI-Powered Insights
- Get personalized care tips using OpenRouter AI
- Breed-specific recommendations for diet, exercise, and grooming
- Behavioral guidance and training suggestions

### 🔐 Security & Authentication
- Secure user registration and login
- Session-based authentication
- User data isolation and privacy protection

## 🛠 Tech Stack

| Component | Technology |
|-----------|------------|
| **Frontend** | HTML5, CSS3, JavaScript (ES6+), Bootstrap 5 |
| **Backend** | Python 3.11, Flask, SQLAlchemy |
| **Database** | PostgreSQL |
| **AI/ML** | OpenRouter API |
| **Visualization** | Chart.js |
| **Icons** | Feather Icons |
| **Server** | Gunicorn |

## 📊 Database Schema

![Database ER Diagram](attached_assets/petpal_er_diagram_1749471808355.png)

### Core Entities:
- **Users**: User accounts and authentication
- **Pets**: Pet profiles and basic information
- **HealthRecords**: Medical history and health events
- **Tasks**: Care checklists and to-do items
- **Reminders**: Scheduled care notifications
- **WeightRecords**: Weight tracking over time

## 🚀 Quick Start

### Prerequisites
- Python 3.11+
- PostgreSQL 12+
- OpenRouter API key (for AI features)

### Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/yourusername/petpal.git
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
   # Edit .env with your configuration
   ```

5. **Set up database**
   ```bash
   # Create PostgreSQL database
   createdb petpal_db
   
   # Run the application to create tables
   python app.py
   ```

6. **Start the application**
   ```bash
   # Development mode
   flask run
   
   # Production mode
   gunicorn --bind 0.0.0.0:5000 main:app
   ```

## ⚙️ Configuration

### Environment Variables

Create a `.env` file with the following variables:

```env
# Database
DATABASE_URL=postgresql://username:password@localhost:5432/petpal_db

# Security
SESSION_SECRET=your-super-secret-session-key

# AI Integration
OPENROUTER_API_KEY=your-openrouter-api-key

# Application
FLASK_ENV=development
FLASK_DEBUG=True
```

### OpenRouter Setup

1. Sign up at [OpenRouter](https://openrouter.ai/)
2. Generate an API key
3. Add the key to your `.env` file
4. The application uses the free tier model by default

## 📱 Usage Guide

### Getting Started
1. **Register**: Create your account with name, email, and password
2. **Add Pets**: Create profiles for your pets with photos and details
3. **Track Health**: Log vaccinations, vet visits, and weight changes
4. **Manage Care**: Set up tasks and reminders for daily care
5. **Get AI Tips**: Receive personalized care recommendations

### Key Features

#### Pet Profiles
- Add multiple pets with detailed information
- Upload photos (supports PNG, JPG, JPEG, GIF, WebP)
- Track age, weight, breed, and species

#### Health Records
- Log different types of health events
- Visual weight tracking with charts
- Export health history for vet visits

#### Care Management
- Create custom care tasks
- Set due dates and priorities
- Mark tasks as complete
- View task history

#### AI Care Tips
- Breed-specific recommendations
- Exercise and diet guidance
- Grooming and health tips
- Training suggestions

## 🎨 UI/UX Features

- **Responsive Design**: Works on desktop, tablet, and mobile
- **Dark Theme**: Built-in dark mode support
- **Smooth Animations**: Enhanced user interactions
- **Accessible**: Screen reader friendly and keyboard navigation
- **Loading States**: Visual feedback for all operations
- **Form Validation**: Real-time validation with helpful messages

## 🔧 Development

### Project Structure
```
petpal/
├── app.py              # Flask application factory
├── main.py             # Application entry point
├── models.py           # Database models
├── routes.py           # Application routes
├── utils.py            # Utility functions
├── static/
│   ├── css/           # Stylesheets
│   ├── js/            # JavaScript files
│   └── uploads/       # Pet photos
├── templates/         # Jinja2 templates
└── requirements.txt   # Python dependencies
```

### Adding New Features
1. Create database models in `models.py`
2. Add routes in `routes.py`
3. Create templates in `templates/`
4. Add styling in `static/css/style.css`
5. Add JavaScript in `static/js/main.js`

### Testing
```bash
# Run basic tests
python -m pytest tests/

# Check code style
flake8 .

# Format code
black .
```

## 🚀 Deployment

### Using Replit (Recommended)
1. Import the repository to Replit
2. Configure environment variables in Secrets
3. Run the application using the provided configuration

### Using Heroku
1. Create a new Heroku app
2. Add PostgreSQL addon
3. Set environment variables
4. Deploy using Git

### Using Railway
1. Connect your GitHub repository
2. Configure environment variables
3. Deploy with automatic builds

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- **OpenRouter** for AI-powered care recommendations
- **Bootstrap** for responsive UI components
- **Chart.js** for beautiful data visualizations
- **Feather Icons** for clean, modern iconography
- **Flask** community for excellent documentation

## 📞 Support

For support, please open an issue on GitHub or contact the development team.

---

**Made with ❤️ for pet lovers everywhere**