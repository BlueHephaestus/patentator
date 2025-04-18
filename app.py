import os
from flask import Flask, render_template, request, jsonify, redirect, url_for
from celery import Celery
from processors import patentate  # Your existing code
import uuid
from dotenv import load_dotenv
import traceback

load_dotenv()

app = Flask(__name__)
app.config.update(
    CELERY_BROKER_URL=os.getenv('CELERY_BROKER_URL', 'redis://localhost:6379/0'),
    CELERY_RESULT_BACKEND=os.getenv('CELERY_RESULT_BACKEND', 'redis://localhost:6379/0'),
    SECRET_KEY=os.getenv('SECRET_KEY', 'dev-secret-key')
)

# Initialize Celery
celery = Celery(app.name, broker=app.config['CELERY_BROKER_URL'])
celery.conf.update(app.config)

# In-memory storage for task results (replace with Redis in production)
tasks = {}


@celery.task(bind=True)
def generate_patent_report_task(self, patent_id):
    """Celery task to generate patent report"""
    self.update_state(state='PROGRESS', meta={'current': 0, 'total': 100, 'status': 'Starting...'})

    try:
        # Process the patent - modify your existing function to accept progress updates
        result = patentate(patent_id, progress_callback=self.update_state)
        return {'status': 'COMPLETED', 'result': result}
    except Exception as e:
        
        return {'status': 'FAILED', 'error': traceback.format_exc()}


@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        patent_id = request.form['patent_id'].strip()
        if not patent_id:
            return render_template('index.html', error="Please enter a patent ID")

        # Start Celery task
        task = generate_patent_report_task.apply_async(args=[patent_id])
        return redirect(url_for('task_status', task_id=task.id))

    return render_template('index.html')


@app.route('/status/<task_id>')
def task_status(task_id):
    task = generate_patent_report_task.AsyncResult(task_id)

    if task.state == 'PENDING':
        response = {
            'state': task.state,
            'status': 'Pending...',
            'progress': 0
        }
    elif task.state == 'PROGRESS':
        response = {
            'state': task.state,
            'status': task.info.get('status', ''),
            'progress': task.info.get('current', 0) / task.info.get('total', 100) * 100
        }
    elif task.state == 'SUCCESS':
        response = {
            'state': task.state,
            'result': task.info.get('result', {}),
            'progress': 100
        }
    else:
        response = {
            'state': task.state,
            'status': str(task.info),
            'progress': 100
        }

    return jsonify(response)


@app.route('/results/<task_id>')
def view_results(task_id):
    task = generate_patent_report_task.AsyncResult(task_id)

    if task.state == 'SUCCESS':
        return render_template('results.html', results=task.info.get('result', {}))

    return redirect(url_for('index'))


if __name__ == '__main__':
    app.run(debug=True)