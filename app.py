from flask import Flask, render_template, request, redirect, url_for, flash, session
from werkzeug.security import generate_password_hash, check_password_hash
import sqlite3
from functools import wraps

app = Flask(__name__)
app.secret_key = 'your_secret_key'  # Replace with a real secret key

def get_db_connection():
    conn = sqlite3.connect('event_management.db')
    conn.row_factory = sqlite3.Row
    return conn

def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user_id' not in session:
            flash('Please log in to access this page.', 'error')
            return redirect(url_for('login'))
        return f(*args, **kwargs)
    return decorated_function

@app.route('/')
def index():
    conn = get_db_connection()
    events = conn.execute('SELECT * FROM events').fetchall()
    conn.close()
    return render_template('index.html', events=events)

@app.route('/event/<int:id>')
def event_detail(id):
    conn = get_db_connection()
    event = conn.execute('SELECT * FROM events WHERE id = ?', (id,)).fetchone()
    conn.close()
    if event is None:
        flash('Event not found', 'error')
        return redirect(url_for('index'))
    return render_template('event_detail.html', event=event)

@app.route('/create_event', methods=['GET', 'POST'])
@login_required
def create_event():
    if request.method == 'POST':
        title = request.form['title']
        description = request.form['description']
        start_date = request.form['start_date']
        end_date = request.form['end_date']
        location = request.form['location']
        price = float(request.form['price'])
        quota = int(request.form['quota'])

        conn = get_db_connection()
        conn.execute('INSERT INTO events (title, description, start_date, end_date, location, price, quota) VALUES (?, ?, ?, ?, ?, ?, ?)',
                     (title, description, start_date, end_date, location, price, quota))
        conn.commit()
        conn.close()
        flash('Event created successfully', 'success')
        return redirect(url_for('index'))

    return render_template('create_event.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        email = request.form['email']
        name = request.form['name']
        surname = request.form['surname']

        conn = get_db_connection()
        user = conn.execute('SELECT * FROM users WHERE username = ?', (username,)).fetchone()
        if user:
            flash('Username already exists', 'error')
        else:
            hashed_password = generate_password_hash(password)
            conn.execute('INSERT INTO users (username, password, email, name, surname) VALUES (?, ?, ?, ?, ?)',
                         (username, hashed_password, email, name, surname))
            conn.commit()
            flash('Registration successful', 'success')
            return redirect(url_for('login'))
        conn.close()

    return render_template('register.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        conn = get_db_connection()
        user = conn.execute('SELECT * FROM users WHERE username = ?', (username,)).fetchone()
        conn.close()

        if user and check_password_hash(user['password'], password):
            session['user_id'] = user['id']
            flash('Logged in successfully', 'success')
            return redirect(url_for('index'))
        else:
            flash('Invalid username or password', 'error')

    return render_template('login.html')

@app.route('/logout')
def logout():
    session.pop('user_id', None)
    flash('Logged out successfully', 'success')
    return redirect(url_for('index'))

# @app.route('/profile')
# @login_required
# def profile():
#     conn = get_db_connection()
#     user = conn.execute('SELECT * FROM users WHERE id = ?', (session['user_id'],)).fetchone()
#     conn.close()
#     return render_template('profile.html', user=user)


@app.route('/profile')
@login_required
def profile():
    conn = get_db_connection()
    
    # Fetch user details
    user = conn.execute('SELECT * FROM users WHERE id = ?', (session['user_id'],)).fetchone()

    # Fetch registered events for the logged-in user
    registered_events = conn.execute('''
        SELECT events.* 
        FROM events 
        JOIN participations ON events.id = participations.event_id 
        WHERE participations.user_id = ?
    ''', (session['user_id'],)).fetchall()
    
    conn.close()

    return render_template('profile.html', user=user, registered_events=registered_events)

@app.route('/event/<int:id>/edit', methods=['GET', 'POST'])
@login_required
def edit_event(id):
    conn = get_db_connection()
    event = conn.execute('SELECT * FROM events WHERE id = ?', (id,)).fetchone()
    
    if event is None:
        conn.close()
        flash('Event not found', 'error')
        return redirect(url_for('index'))

    if request.method == 'POST':
        title = request.form['title']
        description = request.form['description']
        start_date = request.form['start_date']
        end_date = request.form['end_date']
        location = request.form['location']
        price = float(request.form['price'])
        quota = int(request.form['quota'])

        conn.execute('UPDATE events SET title = ?, description = ?, start_date = ?, end_date = ?, location = ?, price = ?, quota = ? WHERE id = ?',
                     (title, description, start_date, end_date, location, price, quota, id))
        conn.commit()
        conn.close()
        flash('Event updated successfully', 'success')
        return redirect(url_for('event_detail', id=id))

    conn.close()
    return render_template('edit_event.html', event=event)

@app.route('/event/<int:id>/delete', methods=['POST'])
@login_required
def delete_event(id):
    conn = get_db_connection()
    conn.execute('DELETE FROM events WHERE id = ?', (id,))
    conn.commit()
    conn.close()
    flash('Event deleted successfully', 'success')
    return redirect(url_for('index'))

@app.route('/event/<int:id>/register', methods=['POST'])
@login_required
def register_for_event(id):
    conn = get_db_connection()
    event = conn.execute('SELECT * FROM events WHERE id = ?', (id,)).fetchone()
    
    if event is None:
        conn.close()
        flash('Event not found', 'error')
        return redirect(url_for('index'))

    # Check if user is already registered
    existing_registration = conn.execute('SELECT * FROM participations WHERE user_id = ? AND event_id = ?', 
                                         (session['user_id'], id)).fetchone()
    if existing_registration:
        conn.close()
        flash('You are already registered for this event', 'error')
        return redirect(url_for('event_detail', id=id))

    # Check if there are available spots
    if event['quota'] > 0:
        conn.execute('INSERT INTO participations (user_id, event_id) VALUES (?, ?)', 
                     (session['user_id'], id))
        conn.execute('UPDATE events SET quota = quota - 1 WHERE id = ?', (id,))
        conn.commit()
        flash('Successfully registered for the event', 'success')
    else:
        flash('Sorry, this event is full', 'error')

    conn.close()
    return redirect(url_for('event_detail', id=id))

@app.route('/my_events')
@login_required
def my_events():
    conn = get_db_connection()
    events = conn.execute('''
        SELECT events.* FROM events
        JOIN participations ON events.id = participations.event_id
        WHERE participations.user_id = ?
    ''', (session['user_id'],)).fetchall()
    conn.close()
    return render_template('my_events.html', events=events)

@app.route('/edit_profile', methods=['GET', 'POST'])
def edit_profile():
    # Your edit profile logic here
    return render_template('edit_profile.html')

@app.route('/events', methods=['GET'])
@login_required
def event_list():
    search_term = request.args.get('search_term', '')

    conn = get_db_connection()
    if search_term:
        # Use SQL LIKE query to filter events by title
        events = conn.execute(
            "SELECT * FROM events WHERE title LIKE ? ORDER BY start_date",
            (f"%{search_term}%",)
        ).fetchall()
    else:
        events = conn.execute("SELECT * FROM events ORDER BY start_date").fetchall()
    conn.close()

    return render_template('event_list.html', events=events, search_term=search_term)


if __name__ == '__main__':
    app.run(debug=True)
