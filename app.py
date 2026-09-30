"""
CRM Хай-Лань — Прототип воронки лидов
Запуск: python app.py
"""
import os
from datetime import datetime
from flask import Flask, render_template, request, redirect, url_for, flash
from models import db, Lead, Stage, Status, Source, Manager
from forms import LeadForm

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
    
    stage_counts = {s.id: 0 for s in stages}
    all_leads = Lead.query.all()
    for lead in all_leads:
        if lead.stage_id in stage_counts:
            stage_counts[lead.stage_id] += 1
    
    stages_list = []
    for s in stages:
        stage_dict = s.to_dict()
        stage_dict['count'] = stage_counts.get(s.id, 0)
        stages_list.append(stage_dict)
    
    return stages_list, stage_counts, all_leads


# ===== ГЛАВНАЯ СТРАНИЦА (ВОРОНКА) =====
@app.route('/')
def funnel():
    """Воронка лидов — основной экран"""
    stages_list, stage_counts, all_leads = get_stages_with_counts()

    filter_stage = request.args.get('stage', type=int)
    if filter_stage:
        leads = Lead.query.filter_by(stage_id=filter_stage).all()
    else:
        leads = all_leads

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


# ===== ПРОСМОТР ЛИДА =====
@app.route('/leads/<int:lead_id>')
def lead_detail(lead_id):
    """Детальная страница лида"""
    lead = Lead.query.get_or_404(lead_id)
    stages_list, stage_counts, all_leads = get_stages_with_counts()

    return render_template(
        'lead_detail.html',
        lead=lead.to_dict(),
        stages=stages_list,
        stage_counts=stage_counts,
        total_leads=len(all_leads),
    )


# ===== СОЗДАНИЕ ЛИДА =====
@app.route('/leads/new', methods=['GET', 'POST'])
def lead_create():
    """Создание нового лида"""
    form = LeadForm()
    
    if form.validate_on_submit():
        lead = Lead(
            created_date=datetime.utcnow().date(),
            name=form.name.data,
            phone=form.phone.data,
            city=form.city.data,
            source_id=form.source_id.data,
            client_query=form.client_query.data,
            pre_sum=form.pre_sum.data or 0,
            fact_sum=form.fact_sum.data or 0,
            commission_rate=form.commission_rate.data or 10,
            stage_id=form.stage_id.data,
            status_id=form.status_id.data,
            manager_id=form.manager_id.data,
            last_contact_date=form.last_contact_date.data,
            plan_contact_date=form.plan_contact_date.data,
            comment=form.comment.data,
            loss_reason=form.loss_reason.data,
        )
        db.session.add(lead)
        db.session.commit()
        
        flash(f'Лид "{lead.name}" успешно создан', 'success')
        return redirect(url_for('lead_detail', lead_id=lead.id))
    
    return render_template('lead_form.html', form=form, title='Новый лид')


# ===== РЕДАКТИРОВАНИЕ ЛИДА =====
@app.route('/leads/<int:lead_id>/edit', methods=['GET', 'POST'])
def lead_edit(lead_id):
    """Редактирование лида"""
    lead = Lead.query.get_or_404(lead_id)
    form = LeadForm(obj=lead)
    
    if form.validate_on_submit():
        lead.name = form.name.data
        lead.phone = form.phone.data
        lead.city = form.city.data
        lead.source_id = form.source_id.data
        lead.client_query = form.client_query.data
        lead.pre_sum = form.pre_sum.data or 0
        lead.fact_sum = form.fact_sum.data or 0
        lead.commission_rate = form.commission_rate.data or 10
        lead.stage_id = form.stage_id.data
        lead.status_id = form.status_id.data
        lead.manager_id = form.manager_id.data
        lead.last_contact_date = form.last_contact_date.data
        lead.plan_contact_date = form.plan_contact_date.data
        lead.comment = form.comment.data
        lead.loss_reason = form.loss_reason.data
        lead.updated_at = datetime.utcnow()
        
        db.session.commit()
        
        flash(f'Лид "{lead.name}" обновлён', 'success')
        return redirect(url_for('lead_detail', lead_id=lead.id))
    
    return render_template('lead_form.html', form=form, title=f'Редактирование: {lead.name}')


# ===== УДАЛЕНИЕ ЛИДА =====
@app.route('/leads/<int:lead_id>/delete', methods=['POST'])
def lead_delete(lead_id):
    """Удаление лида"""
    lead = Lead.query.get_or_404(lead_id)
    lead_name = lead.name
    
    db.session.delete(lead)
    db.session.commit()
    
    flash(f'Лид "{lead_name}" удалён', 'info')
    return redirect(url_for('funnel'))


# Создаём таблицы при первом запуске
with app.app_context():
    db.create_all()


if __name__ == '__main__':
    print("🚀 CRM Хай-Лань запущена: http://127.0.0.1:5001")
    app.run(debug=True, host="0.0.0.0", port=5001)

