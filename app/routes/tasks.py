from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_required, current_user
from app import db
from app.models import Task
from app.forms import TaskForm

tasks = Blueprint('tasks', __name__)

@tasks.route('/')
@login_required
def index():
    status_filter = request.args.get('status', '')
    priority_filter = request.args.get('priority', '')

    query = Task.query.filter_by(user_id=current_user.id)

    if status_filter:
        query = query.filter_by(status=status_filter)

    if priority_filter:
        query = query.filter_by(priority=priority_filter)

    user_tasks = query.order_by(Task.created_at.desc()).all()

    # Estadísticas
    total = Task.query.filter_by(user_id=current_user.id).count()
    pendientes = Task.query.filter_by(user_id=current_user.id, status='pendiente').count()
    en_progreso = Task.query.filter_by(user_id=current_user.id, status='en progreso').count()
    hechas = Task.query.filter_by(user_id=current_user.id, status='hecho').count()

    return render_template('tasks/index.html',
       tasks=user_tasks,
       total=total,
       pendientes=pendientes,
       en_progreso=en_progreso,
       hechas=hechas,
       status_filter=status_filter,
       priority_filter=priority_filter
       )

@tasks.route('/tasks/create', methods=['GET', 'POST'])
@login_required
def create():
    form = TaskForm()
    if form.validate_on_submit():
        task = Task(
            title=form.title.data,
            description=form.description.data,
            priority=form.priority.data,
            status=form.status.data,
            due_date=form.due_date.data,
            user_id=current_user.id
        )
        db.session.add(task)
        db.session.commit()
        flash('Tarea creada exitosamente.', 'success')
        return redirect(url_for('tasks.index'))
    return render_template('tasks/create.html', form=form)

@tasks.route('/tasks/<int:task_id>/edit', methods=['GET', 'POST'])
@login_required
def edit(task_id):
    task = Task.query.get_or_404(task_id)
    if task.user_id != current_user.id:
        flash('No tienes permiso para editar esta tarea.', 'danger')
        return redirect(url_for('tasks.index'))
    form = TaskForm(obj=task)
    if form.validate_on_submit():
        task.title = form.title.data
        task.description = form.description.data
        task.priority = form.priority.data
        task.status = form.status.data
        task.due_date = form.due_date.data
        db.session.commit()
        flash('Tarea actualizada exitosamente.', 'success')
        return redirect(url_for('tasks.index'))
    return render_template('tasks/edit.html', form=form, task=task)

@tasks.route('/tasks/<int:task_id>/delete', methods=['POST'])
@login_required
def delete(task_id):
    task = Task.query.get_or_404(task_id)
    if task.user_id != current_user.id:
        flash ('No tienes permiso para eliminar esta tarea.')
        return redirect(url_for('tasks.index'))
    db.session.delete(task)
    db.session.commit()
    flash('Tarea eliminada exitosamente.', 'success')
    return redirect(url_for('tasks.index'))
