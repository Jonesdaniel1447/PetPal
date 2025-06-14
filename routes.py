import os
import requests
from datetime import datetime, date
from flask import render_template, request, redirect, url_for, flash, session, jsonify
from werkzeug.utils import secure_filename
from app import app, db
from models import User, Pet, HealthRecord, Task, Reminder, WeightRecord
from utils import login_required, allowed_file, get_openrouter_tips

# --- AI Pet Name Generator ---
import requests

@app.route('/generate_pet_name', methods=['GET', 'POST'])
def generate_pet_name():
    suggested_names = []
    error = None
    if request.method == 'POST':
        species = request.form.get('species', '').strip()
        breed = request.form.get('breed', '').strip()
        gender = request.form.get('gender', '').strip()
        theme = request.form.get('theme', '').strip()
        api_key = os.environ.get('OPENROUTER_API_KEY')
        prompt = f"Suggest 5 creative pet names for a {gender} {breed} {species}. Theme: {theme}. List only the names, comma-separated."
        headers = {
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json"
        }
        data = {
            "model": "meta-llama/llama-3.1-8b-instruct:free",
            "messages": [{"role": "user", "content": prompt}]
        }
        try:
            response = requests.post(
                "https://openrouter.ai/api/v1/chat/completions",
                headers=headers,
                json=data,
                timeout=20
            )
            response.raise_for_status()
            result = response.json()
            answer = result['choices'][0]['message']['content']
            # Expecting comma-separated names
            suggested_names = [n.strip() for n in answer.split(',') if n.strip()]
        except Exception as e:
            error = f"Failed to get suggestions: {e}"
    return render_template('generate_pet_name.html', suggested_names=suggested_names, error=error)


from demo_images import create_demo_profile_picture, create_demo_variations


@app.route('/')
def index():
    return render_template('index.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        password = request.form['password']
        
        # Check if user already exists
        if User.query.filter_by(email=email).first():
            flash('Email already registered. Please use a different email.', 'error')
            return redirect(url_for('register'))
        
        # Create new user
        user = User(name=name, email=email)
        user.set_password(password)
        
        try:
            db.session.add(user)
            db.session.commit()
            flash('Registration successful! Please log in.', 'success')
            return redirect(url_for('login'))
        except Exception as e:
            db.session.rollback()
            flash('Registration failed. Please try again.', 'error')
            app.logger.error(f"Registration error: {e}")
    
    return render_template('register.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        
        user = User.query.filter_by(email=email).first()
        
        if user and user.check_password(password):
            session['user_id'] = user.id
            flash('Login successful!', 'success')
            return redirect(url_for('dashboard'))
        else:
            flash('Invalid email or password.', 'error')
    
    return render_template('login.html')

@app.route('/logout')
def logout():
    session.pop('user_id', None)
    flash('You have been logged out.', 'info')
    return redirect(url_for('index'))

@app.route('/dashboard')
@login_required
def dashboard():
    user = User.query.get(session['user_id'])
    pets = Pet.query.filter_by(user_id=user.id).all()
    
    # Get upcoming tasks for all pets
    upcoming_tasks = []
    for pet in pets:
        tasks = Task.query.filter_by(pet_id=pet.id, is_done=False).order_by(Task.due_date).limit(3).all()
        for task in tasks:
            upcoming_tasks.append({'pet': pet, 'task': task})
    
    return render_template('dashboard.html', user=user, pets=pets, upcoming_tasks=upcoming_tasks)

@app.route('/add_pet', methods=['GET', 'POST'])
@login_required
def add_pet():
    if request.method == 'POST':
        name = request.form['name']
        species = request.form['species']
        breed = request.form['breed']
        age = int(request.form['age'])
        weight = float(request.form['weight']) if request.form['weight'] else None
        
        # Handle file upload
        photo_path = None
        if 'photo' in request.files:
            file = request.files['photo']
            if file and file.filename != '' and allowed_file(file.filename):
                filename = secure_filename(file.filename)
                # Add timestamp to filename to avoid conflicts
                timestamp = datetime.now().strftime("%Y%m%d_%H%M%S_")
                filename = timestamp + filename
                file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
                
                # Create upload directory if it doesn't exist
                os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
                
                try:
                    file.save(file_path)
                    photo_path = filename
                except Exception as e:
                    flash('Failed to upload photo.', 'error')
                    app.logger.error(f"File upload error: {e}")
        
        # Create new pet
        pet = Pet(
            user_id=session['user_id'],
            name=name,
            species=species,
            breed=breed,
            age=age,
            weight=weight,
            photo_path=photo_path
        )
        
        try:
            db.session.add(pet)
            db.session.commit()
            
            # Add initial weight record if weight provided
            if weight:
                weight_record = WeightRecord(
                    pet_id=pet.id,
                    weight=weight,
                    date=date.today(),
                    notes="Initial weight record"
                )
                db.session.add(weight_record)
                db.session.commit()
            
            flash(f'{name} has been added successfully!', 'success')
            return redirect(url_for('dashboard'))
        except Exception as e:
            db.session.rollback()
            flash('Failed to add pet. Please try again.', 'error')
            app.logger.error(f"Add pet error: {e}")
    
    return render_template('add_pet.html')

@app.route('/edit_pet/<int:pet_id>', methods=['GET', 'POST'])
@login_required
def edit_pet(pet_id):
    pet = Pet.query.get_or_404(pet_id)
    
    # Check if user owns this pet
    if pet.user_id != session['user_id']:
        flash('Access denied.', 'error')
        return redirect(url_for('dashboard'))
    
    if request.method == 'POST':
        pet.name = request.form['name']
        pet.species = request.form['species']
        pet.breed = request.form['breed']
        pet.age = int(request.form['age'])
        
        old_weight = pet.weight
        new_weight = float(request.form['weight']) if request.form['weight'] else None
        pet.weight = new_weight
        
        # Handle file upload
        if 'photo' in request.files:
            file = request.files['photo']
            if file and file.filename != '' and allowed_file(file.filename):
                filename = secure_filename(file.filename)
                timestamp = datetime.now().strftime("%Y%m%d_%H%M%S_")
                filename = timestamp + filename
                file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
                
                os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
                
                try:
                    file.save(file_path)
                    # Delete old photo if exists
                    if pet.photo_path:
                        old_file_path = os.path.join(app.config['UPLOAD_FOLDER'], pet.photo_path)
                        if os.path.exists(old_file_path):
                            os.remove(old_file_path)
                    pet.photo_path = filename
                except Exception as e:
                    flash('Failed to upload photo.', 'error')
                    app.logger.error(f"File upload error: {e}")
        
        try:
            db.session.commit()
            
            # Add weight record if weight changed
            if new_weight and (old_weight != new_weight):
                weight_record = WeightRecord(
                    pet_id=pet.id,
                    weight=new_weight,
                    date=date.today(),
                    notes="Weight updated"
                )
                db.session.add(weight_record)
                db.session.commit()
            
            flash(f'{pet.name} has been updated successfully!', 'success')
            return redirect(url_for('pet_detail', pet_id=pet.id))
        except Exception as e:
            db.session.rollback()
            flash('Failed to update pet. Please try again.', 'error')
            app.logger.error(f"Edit pet error: {e}")
    
    return render_template('edit_pet.html', pet=pet)

@app.route('/pet/<int:pet_id>')
@login_required
def pet_detail(pet_id):
    pet = Pet.query.get_or_404(pet_id)
    
    # Check if user owns this pet
    if pet.user_id != session['user_id']:
        flash('Access denied.', 'error')
        return redirect(url_for('dashboard'))
    
    # Get recent health records
    recent_health_records = HealthRecord.query.filter_by(pet_id=pet_id).order_by(HealthRecord.date.desc()).limit(3).all()
    
    # Get pending tasks
    pending_tasks = Task.query.filter_by(pet_id=pet_id, is_done=False).order_by(Task.due_date).limit(5).all()
    
    # Get recent weight records for chart
    weight_records = WeightRecord.query.filter_by(pet_id=pet_id).order_by(WeightRecord.date.desc()).limit(10).all()
    
    return render_template('pet_detail.html', pet=pet, recent_health_records=recent_health_records, 
                         pending_tasks=pending_tasks, weight_records=weight_records)

@app.route('/pet/<int:pet_id>/health_records')
@login_required
def health_records(pet_id):
    pet = Pet.query.get_or_404(pet_id)
    
    # Check if user owns this pet
    if pet.user_id != session['user_id']:
        flash('Access denied.', 'error')
        return redirect(url_for('dashboard'))
    
    records = HealthRecord.query.filter_by(pet_id=pet_id).order_by(HealthRecord.date.desc()).all()
    weight_records = WeightRecord.query.filter_by(pet_id=pet_id).order_by(WeightRecord.date.desc()).all()
    
    return render_template('health_records.html', pet=pet, records=records, weight_records=weight_records)

@app.route('/pet/<int:pet_id>/add_health_record', methods=['POST'])
@login_required
def add_health_record(pet_id):
    pet = Pet.query.get_or_404(pet_id)
    
    # Check if user owns this pet
    if pet.user_id != session['user_id']:
        flash('Access denied.', 'error')
        return redirect(url_for('dashboard'))
    
    record_type = request.form['record_type']
    title = request.form['title']
    description = request.form['description']
    record_date = datetime.strptime(request.form['date'], '%Y-%m-%d').date()
    
    record = HealthRecord(
        pet_id=pet_id,
        record_type=record_type,
        title=title,
        description=description,
        date=record_date
    )
    
    try:
        db.session.add(record)
        db.session.commit()
        flash('Health record added successfully!', 'success')
    except Exception as e:
        db.session.rollback()
        flash('Failed to add health record.', 'error')
        app.logger.error(f"Add health record error: {e}")
    
    return redirect(url_for('health_records', pet_id=pet_id))

@app.route('/pet/<int:pet_id>/add_weight_record', methods=['POST'])
@login_required
def add_weight_record(pet_id):
    pet = Pet.query.get_or_404(pet_id)
    
    # Check if user owns this pet
    if pet.user_id != session['user_id']:
        flash('Access denied.', 'error')
        return redirect(url_for('dashboard'))
    
    weight = float(request.form['weight'])
    record_date = datetime.strptime(request.form['date'], '%Y-%m-%d').date()
    notes = request.form.get('notes', '')
    
    weight_record = WeightRecord(
        pet_id=pet_id,
        weight=weight,
        date=record_date,
        notes=notes
    )
    
    try:
        db.session.add(weight_record)
        # Update pet's current weight
        pet.weight = weight
        db.session.commit()
        flash('Weight record added successfully!', 'success')
    except Exception as e:
        db.session.rollback()
        flash('Failed to add weight record.', 'error')
        app.logger.error(f"Add weight record error: {e}")
    
    return redirect(url_for('health_records', pet_id=pet_id))

@app.route('/pet/<int:pet_id>/care_checklist')
@login_required
def care_checklist(pet_id):
    pet = Pet.query.get_or_404(pet_id)
    
    # Check if user owns this pet
    if pet.user_id != session['user_id']:
        flash('Access denied.', 'error')
        return redirect(url_for('dashboard'))
    
    pending_tasks = Task.query.filter_by(pet_id=pet_id, is_done=False).order_by(Task.due_date).all()
    completed_tasks = Task.query.filter_by(pet_id=pet_id, is_done=True).order_by(Task.completed_at.desc()).limit(10).all()
    
    return render_template('care_checklist.html', pet=pet, pending_tasks=pending_tasks, completed_tasks=completed_tasks)

@app.route('/pet/<int:pet_id>/add_task', methods=['GET', 'POST'])
@login_required
def add_task(pet_id):
    if request.method == 'GET':
        # Redirect GET requests to care checklist (or change to reminders if preferred)
        return redirect(url_for('care_checklist', pet_id=pet_id))
    pet = Pet.query.get_or_404(pet_id)
    
    # Check if user owns this pet
    if pet.user_id != session['user_id']:
        flash('Access denied.', 'error')
        return redirect(url_for('dashboard'))
    
    task_name = request.form['task_name']
    description = request.form.get('description', '')
    due_date = None
    if request.form.get('due_date'):
        due_date = datetime.strptime(request.form['due_date'], '%Y-%m-%d').date()
    
    task = Task(
        pet_id=pet_id,
        task_name=task_name,
        description=description,
        due_date=due_date
    )
    
    try:
        db.session.add(task)
        db.session.commit()
        flash('Task added successfully!', 'success')
    except Exception as e:
        db.session.rollback()
        flash('Failed to add task.', 'error')
        app.logger.error(f"Add task error: {e}")
    
    return redirect(url_for('care_checklist', pet_id=pet_id))

@app.route('/complete_task/<int:task_id>')
@login_required
def complete_task(task_id):
    task = Task.query.get_or_404(task_id)
    pet = Pet.query.get_or_404(task.pet_id)
    
    # Check if user owns this pet
    if pet.user_id != session['user_id']:
        flash('Access denied.', 'error')
        return redirect(url_for('dashboard'))
    
    try:
        task.is_done = True
        task.completed_at = datetime.utcnow()
        db.session.commit()
        flash('Task marked as completed!', 'success')
    except Exception as e:
        db.session.rollback()
        flash('Failed to update task.', 'error')
        app.logger.error(f"Complete task error: {e}")
    
    return redirect(url_for('care_checklist', pet_id=pet.id))

@app.route('/pet/<int:pet_id>/reminders')
@login_required
def reminders(pet_id):
    pet = Pet.query.get_or_404(pet_id)
    
    # Check if user owns this pet
    if pet.user_id != session['user_id']:
        flash('Access denied.', 'error')
        return redirect(url_for('dashboard'))
    
    active_reminders = Reminder.query.filter_by(pet_id=pet_id, is_active=True).order_by(Reminder.schedule_time).all()
    
    return render_template('reminders.html', pet=pet, reminders=active_reminders)

@app.route('/pet/<int:pet_id>/add_reminder', methods=['POST'])
@login_required
def add_reminder(pet_id):
    pet = Pet.query.get_or_404(pet_id)
    
    # Check if user owns this pet
    if pet.user_id != session['user_id']:
        flash('Access denied.', 'error')
        return redirect(url_for('dashboard'))
    
    task_name = request.form['task_name']
    description = request.form.get('description', '')
    schedule_time = datetime.strptime(request.form['schedule_time'], '%H:%M').time()
    is_recurring = 'is_recurring' in request.form
    recurrence_type = request.form.get('recurrence_type') if is_recurring else None
    
    reminder = Reminder(
        pet_id=pet_id,
        task_name=task_name,
        description=description,
        schedule_time=schedule_time,
        is_recurring=is_recurring,
        recurrence_type=recurrence_type
    )
    
    try:
        db.session.add(reminder)
        db.session.commit()
        flash('Reminder added successfully!', 'success')
    except Exception as e:
        db.session.rollback()
        flash('Failed to add reminder.', 'error')
        app.logger.error(f"Add reminder error: {e}")
    
    return redirect(url_for('reminders', pet_id=pet_id))

@app.route('/delete_pet/<int:pet_id>', methods=['POST'])
@login_required
def delete_pet(pet_id):
    pet = Pet.query.get_or_404(pet_id)
    
    # Check if user owns this pet
    if pet.user_id != session['user_id']:
        flash('Access denied.', 'error')
        return redirect(url_for('dashboard'))
    
    try:
        # Delete photo file if exists
        if pet.photo_path:
            file_path = os.path.join(app.config['UPLOAD_FOLDER'], pet.photo_path)
            if os.path.exists(file_path):
                os.remove(file_path)
        
        db.session.delete(pet)
        db.session.commit()
        flash(f'{pet.name} has been deleted.', 'info')
    except Exception as e:
        db.session.rollback()
        flash('Failed to delete pet.', 'error')
        app.logger.error(f"Delete pet error: {e}")
    
    return redirect(url_for('dashboard'))

@app.route('/weight_chart_data/<int:pet_id>')
@login_required
def weight_chart_data(pet_id):
    pet = Pet.query.get_or_404(pet_id)
    
    # Check if user owns this pet
    if pet.user_id != session['user_id']:
        return jsonify({'error': 'Access denied'}), 403
    
    weight_records = WeightRecord.query.filter_by(pet_id=pet_id).order_by(WeightRecord.date).all()
    
    data = {
        'labels': [record.date.strftime('%Y-%m-%d') for record in weight_records],
        'data': [record.weight for record in weight_records]
    }
    
    return jsonify(data)
