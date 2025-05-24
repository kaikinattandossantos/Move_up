from flask import Blueprint, render_template, request, flash, jsonify
from flask_login import login_required, current_user
from .models import Note, Training
from . import db
import json

views = Blueprint('views', __name__)


@views.route('/', methods=['GET', 'POST'])
@login_required
def home():
    if request.method == 'POST': 
        note = request.form.get('note')
        muscle_group = request.form.get('muscle-group')
        specific_muscle = request.form.get('specific-muscle')
        training_time = request.form.get('training-time')

        if note:
            if len(note) < 1:
                flash('Note is too short!', category='error') 
            else:
                new_note = Note(data=note, user_id=current_user.id)
                db.session.add(new_note)
                db.session.commit()
                flash('Note added!', category='success')

        if muscle_group or specific_muscle:
            plano = gerar_plano(muscle_group, training_time)
            treino = Training(
                muscle_group=muscle_group,
                specific_muscle=specific_muscle,
                training_time=training_time,
                user_id=current_user.id,
                plan_text=plano
            )
            db.session.add(treino)
            db.session.commit()
            flash('Treino gerado com sucesso!', category='success')

    trainings = Training.query.filter_by(user_id=current_user.id).order_by(Training.date.desc()).all()
    return render_template("home.html", user=current_user, trainings=trainings)


@views.route('/delete-note', methods=['POST'])
def delete_note():  
    note = json.loads(request.data) # this function expects a JSON from the INDEX.js file 
    noteId = note['noteId']
    note = Note.query.get(noteId)
    if note:
        if note.user_id == current_user.id:
            db.session.delete(note)
            db.session.commit()

    return jsonify({})

def gerar_plano(grupo, nivel):
    plano = ""

    if grupo == "Braços":
        if nivel == "básico":
            plano = (
                "Segunda-feira - Braços:\n"
                "- 3x10 Rosca direta\n"
                "- 3x12 Tríceps corda\n"
                "- 3x10 Rosca martelo"
            )
        elif nivel == "intermediario":
            plano = (
                "Segunda-feira - Braços:\n"
                "- 4x10 Rosca direta com barra\n"
                "- 4x12 Tríceps francês\n"
                "- 3x12 Rosca alternada com halteres"
            )

    elif grupo == "Peito":
        plano = (
            "Terça-feira - Peito:\n"
            "- 4x10 Supino reto\n"
            "- 4x12 Crucifixo\n"
            "- 3x10 Flexão de braços"
        )
    
    elif grupo == "Costas":
        plano = (
            "Quarta-feira - Costas:\n"
            "- 4x10 Puxada frente\n"
            "- 3x12 Remada baixa\n"
            "- 3x10 Remada curvada"
        )
    
    elif grupo == "Perna":
        plano = (
            "Quinta-feira - Pernas:\n"
            "- 4x12 Agachamento livre\n"
            "- 3x15 Cadeira extensora\n"
            "- 3x12 Stiff"
        )

    else:
        plano = "Plano padrão de corpo inteiro:\n- 3x10 Supino\n- 3x12 Agachamento\n- 3x12 Remada"

    return plano
