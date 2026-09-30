"""
CRM Хай-Лань — Прототип воронки лидов
Запуск: python app.py
"""
from flask import Flask, render_template, request
from data.demo import LEADS, STAGES, STATUSES, SOURCES

app = Flask(__name__)
app.config['SECRET_KEY'] = 'dev-secret-key-change-me'


@app.route('/')
def funnel():
    """Воронка лидов — основной экран"""
    
    # Подсчёт лидов на каждом этапе
    stage_counts = {s['id']: 0 for s in STAGES}
    for lead in LEADS:
        if lead['stage_id'] in stage_counts:
            stage_counts[lead['stage_id']] += 1
    
    # Фильтрация по этапу (через ?stage=N)
    filter_stage = request.args.get('stage', type=int)
    filtered_leads = LEADS
    if filter_stage:
        filtered_leads = [l for l in LEADS if l['stage_id'] == filter_stage]
    
    # Обогащение лидов названиями этапов/статусов
    stages_map = {s['id']: s for s in STAGES}
    statuses_map = {s['id']: s for s in STATUSES}
    
    for lead in filtered_leads:
        lead['stage'] = stages_map.get(lead['stage_id'], {})
        lead['status'] = statuses_map.get(lead['status_id'], {})
        # Расчёт комиссии
        if lead.get('fact_sum') and lead.get('commission_rate'):
            lead['commission'] = round(lead['fact_sum'] * lead['commission_rate'] / 100)
        else:
            lead['commission'] = 0
    
    return render_template(
        'funnel.html',
        leads=filtered_leads,
        stages=STAGES,
        stage_counts=stage_counts,
        filter_stage=filter_stage,
        total_leads=len(LEADS),
        filtered_count=len(filtered_leads),
    )


@app.route('/leads/<int:lead_id>')
def lead_detail(lead_id):
    """Детали лида (заглушка)"""
    lead = next((l for l in LEADS if l['id'] == lead_id), None)
    if not lead:
        return 'Лид не найден', 404
    
    stages_map = {s['id']: s for s in STAGES}
    statuses_map = {s['id']: s for s in STATUSES}
    lead['stage'] = stages_map.get(lead['stage_id'], {})
    lead['status'] = statuses_map.get(lead['status_id'], {})
    
    return render_template('funnel.html', leads=[lead], stages=STAGES,
                           stage_counts={}, filter_stage=None,
                           total_leads=1, filtered_count=1)


if __name__ == '__main__':
    print("🚀 CRM Хай-Лань запущена: http://127.0.0.1:5000")
    app.run(debug=True, port=5000)