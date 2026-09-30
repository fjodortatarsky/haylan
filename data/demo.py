"""Демо-данные для прототипа (в памяти)"""

# ===== ЭТАПЫ ВОРОНКИ =====
STAGES = [
    {'id': 1,  'name': 'Новый лид',              'name_cn': '新客户',   'color': '#3b82f6', 'badge': 'badge-new',     'deadline': '≤ 1 дня'},
    {'id': 2,  'name': 'Предв. консультация',    'name_cn': '初步咨询', 'color': '#6366f1', 'badge': 'badge-consult',  'deadline': '≤ 3 дней'},
    {'id': 3,  'name': 'Прогрев',                'name_cn': '培育',     'color': '#f59e0b', 'badge': 'badge-warm',     'deadline': '≤ 7 дней'},
    {'id': 4,  'name': 'Контроль',               'name_cn': '跟进',     'color': '#f97316', 'badge': 'badge-control',  'deadline': '≤ 5 дней'},
    {'id': 5,  'name': 'Подтверждение поездки',  'name_cn': '确认行程', 'color': '#22c55e', 'badge': 'badge-confirm',  'deadline': '≤ 3 дней'},
    {'id': 6,  'name': 'Покупка билетов',        'name_cn': '机票购买', 'color': '#10b981', 'badge': 'badge-ticket',   'deadline': '≤ 2 дней'},
    {'id': 7,  'name': 'Прибытие',               'name_cn': '到诊所',   'color': '#059669', 'badge': 'badge-arrive',   'deadline': '≤ 1 дня'},
    {'id': 8,  'name': 'Лечение',                'name_cn': '治疗',     'color': '#16a34a', 'badge': 'badge-treat',    'deadline': 'По плану'},
    {'id': 9,  'name': 'Пост-сервис',            'name_cn': '售后服务', 'color': '#8b5cf6', 'badge': 'badge-post',     'deadline': '≤ 14 дней'},
    {'id': 10, 'name': 'Потерян',                'name_cn': '流失',     'color': '#ef4444', 'badge': 'badge-lost',     'deadline': '≤ 1 дня'},
]

# ===== СТАТУСЫ =====
STATUSES = [
    {'id': 1, 'name': 'В работе',          'name_cn': '进行中',   'cls': 'status-active'},
    {'id': 2, 'name': 'Ожидает ответа',    'name_cn': '等待回复', 'cls': 'status-wait'},
    {'id': 3, 'name': 'Выполнено',         'name_cn': '已完成',   'cls': 'status-done'},
    {'id': 4, 'name': 'Отложен',           'name_cn': '暂停',     'cls': 'status-pause'},
    {'id': 5, 'name': 'Потерян',           'name_cn': '流失',     'cls': 'status-lost'},
]

# ===== ИСТОЧНИКИ =====
SOURCES = ['Instagram', 'Telegram', 'Рекомендация', 'Сайт', 'Другое']

# ===== ЛИДЫ (демо) =====
LEADS = [
    {
        'id': 1, 'date': '2026-09-15', 'name': 'Анна К.',
        'phone': '+7 902 123-45-67', 'city': 'Томск',
        'source': 'Instagram', 'query': 'Имплантация',
        'pre_sum': 69000, 'fact_sum': 69000, 'commission_rate': 10,
        'stage_id': 8, 'status_id': 2,
        'last_contact': '2026-09-28', 'plan_contact': '2026-10-05',
        'manager': 'Лю Мин',
        'comment': 'Лечение завершено, довольна', 'loss_reason': ''
    },
    {
        'id': 2, 'date': '2026-09-20', 'name': 'Дмитрий В.',
        'phone': '+7 913 555-22-33', 'city': 'Новосибирск',
        'source': 'Рекомендация', 'query': 'Протезирование (коронки)',
        'pre_sum': 35000, 'fact_sum': 0, 'commission_rate': 10,
        'stage_id': 3, 'status_id': 1,
        'last_contact': '2026-09-25', 'plan_contact': '2026-09-30',
        'manager': 'Ван Вэй',
        'comment': 'Прислал прайс, думает', 'loss_reason': ''
    },
    {
        'id': 3, 'date': '2026-09-22', 'name': 'Ольга С.',
        'phone': '+7 911 777-88-99', 'city': 'Москва',
        'source': 'Сайт', 'query': 'Чистка + лечение кариеса',
        'pre_sum': 8000, 'fact_sum': 0, 'commission_rate': 10,
        'stage_id': 2, 'status_id': 1,
        'last_contact': '2026-09-22', 'plan_contact': '2026-09-24',
        'manager': 'Лю Мин',
        'comment': 'Ждём онлайн-консультацию', 'loss_reason': ''
    },
    {
        'id': 4, 'date': '2026-09-10', 'name': 'Сергей П.',
        'phone': '+7 923 444-55-66', 'city': 'Иркутск',
        'source': 'Telegram', 'query': 'Удаление + имплант',
        'pre_sum': 75000, 'fact_sum': 0, 'commission_rate': 10,
        'stage_id': 5, 'status_id': 2,
        'last_contact': '2026-09-27', 'plan_contact': '2026-09-29',
        'manager': 'Ван Вэй',
        'comment': 'Согласовывает даты с работой', 'loss_reason': ''
    },
    {
        'id': 5, 'date': '2026-08-28', 'name': 'Марина Л.',
        'phone': '+7 905 111-22-33', 'city': 'Красноярск',
        'source': 'Другое', 'query': 'Бюгельный протез',
        'pre_sum': 40000, 'fact_sum': 0, 'commission_rate': 10,
        'stage_id': 10, 'status_id': 5,
        'last_contact': '2026-09-05', 'plan_contact': '',
        'manager': 'Лю Мин',
        'comment': 'Передумала, нашла в РФ', 'loss_reason': 'Нашла клинику в РФ'
    },
]