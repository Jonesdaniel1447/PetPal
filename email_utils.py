import os
from datetime import datetime, timedelta
from flask_mail import Message
from app import mail, app
from models import User, Pet, Reminder, Task

def send_reminder_email(user_email, pet_name, reminder_type, message_content):
    """Send reminder email for pet care tasks"""
    try:
        with app.app_context():
            msg = Message(
                subject=f"🐾 PetPal Reminder: {reminder_type} for {pet_name}",
                recipients=[user_email],
                sender=app.config['MAIL_DEFAULT_SENDER']
            )
            
            # HTML email template
            msg.html = f"""
            <!DOCTYPE html>
            <html>
            <head>
                <style>
                    body {{ font-family: Arial, sans-serif; background-color: #f8f9fa; margin: 0; padding: 20px; }}
                    .container {{ max-width: 600px; margin: 0 auto; background: white; border-radius: 15px; overflow: hidden; box-shadow: 0 10px 30px rgba(0,0,0,0.1); }}
                    .header {{ background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); color: white; padding: 30px; text-align: center; }}
                    .content {{ padding: 30px; }}
                    .pet-info {{ background: #f8f9fa; padding: 20px; border-radius: 10px; margin: 20px 0; }}
                    .footer {{ background: #f8f9fa; padding: 20px; text-align: center; color: #6c757d; }}
                    .btn {{ display: inline-block; background: linear-gradient(135deg, #667eea, #764ba2); color: white; padding: 12px 24px; text-decoration: none; border-radius: 25px; margin: 10px 0; }}
                </style>
            </head>
            <body>
                <div class="container">
                    <div class="header">
                        <h1>🐾 PetPal Reminder</h1>
                        <p>Don't forget to take care of {pet_name}!</p>
                    </div>
                    <div class="content">
                        <h2>{reminder_type}</h2>
                        <div class="pet-info">
                            <strong>Pet:</strong> {pet_name}<br>
                            <strong>Reminder:</strong> {message_content}<br>
                            <strong>Date:</strong> {datetime.now().strftime('%B %d, %Y at %I:%M %p')}
                        </div>
                        <p>This is a friendly reminder to help you maintain your pet's health and happiness.</p>
                        <p><a href="#" class="btn">View in PetPal</a></p>
                    </div>
                    <div class="footer">
                        <p>Sent with ❤️ from PetPal - Your AI-Powered Pet Care Companion</p>
                        <p><small>You're receiving this because you have reminders enabled for {pet_name}.</small></p>
                    </div>
                </div>
            </body>
            </html>
            """
            
            # Plain text fallback
            msg.body = f"""
            PetPal Reminder: {reminder_type} for {pet_name}
            
            {message_content}
            
            Date: {datetime.now().strftime('%B %d, %Y at %I:%M %p')}
            
            This is a friendly reminder to help you maintain your pet's health and happiness.
            
            --
            PetPal - Your AI-Powered Pet Care Companion
            """
            
            mail.send(msg)
            return True
            
    except Exception as e:
        app.logger.error(f"Failed to send reminder email: {e}")
        return False

def send_welcome_email(user_email, user_name):
    """Send welcome email to new users"""
    try:
        with app.app_context():
            msg = Message(
                subject="🎉 Welcome to PetPal - Your Pet Care Journey Begins!",
                recipients=[user_email],
                sender=app.config['MAIL_DEFAULT_SENDER']
            )
            
            msg.html = f"""
            <!DOCTYPE html>
            <html>
            <head>
                <style>
                    body {{ font-family: Arial, sans-serif; background-color: #f8f9fa; margin: 0; padding: 20px; }}
                    .container {{ max-width: 600px; margin: 0 auto; background: white; border-radius: 15px; overflow: hidden; box-shadow: 0 10px 30px rgba(0,0,0,0.1); }}
                    .header {{ background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); color: white; padding: 40px; text-align: center; }}
                    .content {{ padding: 30px; }}
                    .feature {{ background: #f8f9fa; padding: 15px; border-radius: 8px; margin: 15px 0; }}
                    .footer {{ background: #f8f9fa; padding: 20px; text-align: center; color: #6c757d; }}
                    .btn {{ display: inline-block; background: linear-gradient(135deg, #667eea, #764ba2); color: white; padding: 12px 24px; text-decoration: none; border-radius: 25px; margin: 10px 0; }}
                </style>
            </head>
            <body>
                <div class="container">
                    <div class="header">
                        <h1>🐾 Welcome to PetPal!</h1>
                        <p>Hi {user_name}, we're excited to help you care for your furry friends!</p>
                    </div>
                    <div class="content">
                        <h2>Get Started with PetPal</h2>
                        <p>Here's what you can do with your new account:</p>
                        
                        <div class="feature">
                            <strong>📝 Add Pet Profiles</strong><br>
                            Create detailed profiles for each of your pets with photos and information.
                        </div>
                        
                        <div class="feature">
                            <strong>🏥 Track Health Records</strong><br>
                            Keep vaccination records, vet visits, and medication schedules organized.
                        </div>
                        
                        <div class="feature">
                            <strong>🤖 AI Care Tips</strong><br>
                            Get personalized, breed-specific care recommendations powered by AI.
                        </div>
                        
                        <div class="feature">
                            <strong>📊 Monitor Weight & Health</strong><br>
                            Track your pet's weight and health trends with interactive charts.
                        </div>
                        
                        <div class="feature">
                            <strong>⏰ Smart Reminders</strong><br>
                            Never forget feeding times, walks, or important appointments.
                        </div>
                        
                        <p><a href="#" class="btn">Start Adding Your Pets</a></p>
                    </div>
                    <div class="footer">
                        <p>Need help? We're here to support you and your pets every step of the way!</p>
                        <p><small>PetPal - Because every pet deserves the best care possible.</small></p>
                    </div>
                </div>
            </body>
            </html>
            """
            
            msg.body = f"""
            Welcome to PetPal, {user_name}!
            
            We're excited to help you care for your furry friends!
            
            With PetPal, you can:
            - Add detailed pet profiles with photos
            - Track health records and vaccinations
            - Get AI-powered, breed-specific care tips
            - Monitor weight and health trends
            - Set up smart reminders for care tasks
            
            Start by adding your first pet to begin your journey!
            
            --
            PetPal Team
            """
            
            mail.send(msg)
            return True
            
    except Exception as e:
        app.logger.error(f"Failed to send welcome email: {e}")
        return False

def check_and_send_reminders():
    """Check for due reminders and send email notifications"""
    try:
        with app.app_context():
            from models import db
            
            # Get all active reminders
            current_time = datetime.now().time()
            reminders = db.session.query(Reminder).filter(
                Reminder.is_active == True,
                Reminder.schedule_time <= current_time
            ).all()
            
            sent_count = 0
            for reminder in reminders:
                pet = reminder.pet
                user = pet.owner
                
                # Check if we should send this reminder today
                if should_send_reminder_today(reminder):
                    success = send_reminder_email(
                        user_email=user.email,
                        pet_name=pet.name,
                        reminder_type=reminder.task_name,
                        message_content=reminder.description or f"Time for {reminder.task_name} for {pet.name}!"
                    )
                    
                    if success:
                        sent_count += 1
                        app.logger.info(f"Sent reminder email for {pet.name} to {user.email}")
            
            return sent_count
            
    except Exception as e:
        app.logger.error(f"Error checking reminders: {e}")
        return 0

def should_send_reminder_today(reminder):
    """Determine if a reminder should be sent today based on recurrence"""
    if not reminder.is_recurring:
        return True
    
    # For recurring reminders, implement logic based on recurrence_type
    # This is a simplified version - you might want more sophisticated scheduling
    return True

def send_health_alert_email(user_email, pet_name, alert_message):
    """Send health alert email for urgent pet care matters"""
    try:
        with app.app_context():
            msg = Message(
                subject=f"🚨 PetPal Health Alert: {pet_name}",
                recipients=[user_email],
                sender=app.config['MAIL_DEFAULT_SENDER']
            )
            
            msg.html = f"""
            <!DOCTYPE html>
            <html>
            <head>
                <style>
                    body {{ font-family: Arial, sans-serif; background-color: #f8f9fa; margin: 0; padding: 20px; }}
                    .container {{ max-width: 600px; margin: 0 auto; background: white; border-radius: 15px; overflow: hidden; box-shadow: 0 10px 30px rgba(0,0,0,0.1); }}
                    .header {{ background: linear-gradient(135deg, #dc3545, #c82333); color: white; padding: 30px; text-align: center; }}
                    .content {{ padding: 30px; }}
                    .alert {{ background: #f8d7da; border: 1px solid #f5c6cb; color: #721c24; padding: 15px; border-radius: 8px; margin: 20px 0; }}
                    .footer {{ background: #f8f9fa; padding: 20px; text-align: center; color: #6c757d; }}
                    .btn {{ display: inline-block; background: #dc3545; color: white; padding: 12px 24px; text-decoration: none; border-radius: 25px; margin: 10px 0; }}
                </style>
            </head>
            <body>
                <div class="container">
                    <div class="header">
                        <h1>🚨 Health Alert</h1>
                        <p>Important notification about {pet_name}</p>
                    </div>
                    <div class="content">
                        <div class="alert">
                            <strong>Alert:</strong> {alert_message}
                        </div>
                        <p>This alert was generated based on your pet's health records and care schedule.</p>
                        <p>If this is urgent, please contact your veterinarian immediately.</p>
                        <p><a href="#" class="btn">View Pet Details</a></p>
                    </div>
                    <div class="footer">
                        <p>PetPal Health Monitoring System</p>
                        <p><small>For emergencies, always contact your veterinarian directly.</small></p>
                    </div>
                </div>
            </body>
            </html>
            """
            
            mail.send(msg)
            return True
            
    except Exception as e:
        app.logger.error(f"Failed to send health alert email: {e}")
        return False