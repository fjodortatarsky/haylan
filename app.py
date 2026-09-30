"""
CRM Хай-Лань — Прототип воронки лидов
Запуск: python app.py
"""
import os
from flask import Flask, render_template, request
from models import db, Lead, Stage, Status, Source, Manager

app = Flask(__name__)

# Конфигурация БД
basedir = os.path.abspath(os.path.dirname(__file__))
app.config['SECRET_KEY'] = 'dev-secret-key-change-me'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'haylan.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)


def get_stages_with_counts():
    """Возвращает список этапов с количеством лидов на каждом"""
    stages = Stage.query.order_by(Stage.order_num).all()
    
    # Подсчёт лидов на каждом этапе
    stage_counts = {s.id: 0 for s in stages}
    all_leads = Lead.query.all()
    for lead in all_leads:
        if lead.stage_id in stage_counts:
            stage_counts[lead.stage_id] += 1
    
    # Сериализация этапов с добавлением count
    stages_list = []
    for s in stages:
        stage_dict = s.to_dict()
        stage_dict['count'] = stage_counts.get(s.id, 0)
        stages_list.append(stage_dict)
    
    return stages_list, stage_counts, all_leads


@app.route('/')
def funnel():
    """Воронка лидов — основной экран"""
    stages_list, stage_counts, all_leads = get_stages_with_counts()

    # Фильтрация по этапу
    filter_stage = request.args.get('stage', type=int)
    if filter_stage:
        leads = Lead.query.filter_by(stage_id=filter_stage).all()
    else:
        leads = all_leads

    # Сериализация для шаблона
    leads_data = [l.to_dict() for l in leads]

    return render_template(
        'funnel.html',
        leads=leads_data,
        stages=stages_list,
        stage_counts=stage_counts,
        filter_stage=filter_stage,
        total_leads=len(all_leads),
        filtered_count=len(leads_data),
    )


@app.route('/leads/<int:lead_id>')
def lead_detail(lead_id):
    """Детали лида"""
    lead = Lead.query.get_or_404(lead_id)
    stages_list, stage_counts, all_leads = get_stages_with_counts()

    return render_template(
        'funnel.html',
        leads=[lead.to_dict()],
        stages=stages_list,
        stage_counts=stage_counts,
        filter_stage=None,
        total_leads=len(all_leads),
        filtered_count=1,
    )


# Создаём таблицы при первом запуске
with app.app_context():
    db.create_all()


if __name__ == '__main__':
    print("🚀 CRM Хай-Лань запущена: http://127.0.0.1:5001")
    app.run(debug=True, host="0.0.0.0", port=5001)


