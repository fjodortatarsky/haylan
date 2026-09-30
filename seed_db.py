import sys
import os
from datetime import date

sys.path.insert(0, os.path.abspath(os.path.dirname(__file__)))

from app import app, db
from models import Stage, Status, Source, Manager, Lead


def seed():
    with app.app_context():
        if Stage.query.count() > 0:
            print("⚠️  БД уже заполнена. Очищаю перед повторным наполнением...")
            Lead.query.delete()
            Stage.query.delete()
            Status.query.delete()
            Source.query.delete()
            Manager.query.delete()
            db.session.commit()

        # ===== ЭТАПЫ =====
        stages_data = [
            (1,  'Новый лид',             '新客户',   '#3b82f6', 'badge-new',     '≤ 1 дня'),
            (2,  'Предв. консультация',   '初步咨询', '#6366f1', 'badge-consult',  '≤ 3 дней'),
            (3,  'Прогрев',               '培育',     '#f59e0b', 'badge-warm',     '≤ 7 дней'),
            (4,  'Контроль',              '跟进',     '#f97316', 'badge-control',  '≤ 5 дней'),
            (5,  'Подтверждение поездки', '确认行程', '#22c55e', 'badge-confirm',  '≤ 3 дней'),
            (6,  'Покупка билетов',       '机票购买', '#10b981', 'badge-ticket',   '≤ 2 дней'),
            (7,  'Прибытие',              '到诊所',   '#059669', 'badge-arrive',   '≤ 1 дня'),
            (8,  'Лечение',               '治疗',     '#16a34a', 'badge-treat',    'По плану'),
            (9,  'Пост-сервис',           '售后服务', '#8b5cf6', 'badge-post',     '≤ 14 дней'),
            (10, 'Потерян',               '流失',     '#ef4444', 'badge-lost',     '≤ 1 дня'),
        ]
        for order, name, name_cn, color, badge, deadline in stages_data:
            stage = Stage(order_num=order, name=name, name_cn=name_cn,
                          color=color, badge=badge, deadline=deadline)
            db.session.add(stage)

        # ===== СТАТУСЫ =====
        statuses_data = [
            ('В работе',       '进行中',   'status-active'),
            ('Ожидает ответа', '等待回复', 'status-wait'),
            ('Выполнено',      '已完成',   'status-done'),
            ('Отложен',        '暂停',     'status-pause'),
            ('Потерян',        '流失',     'status-lost'),
        ]
        for name, name_cn, css_class in statuses_data:
            status = Status(name=name, name_cn=name_cn, css_class=css_class)
            db.session.add(status)

        # ===== ИСТОЧНИКИ =====
        sources_data = [
            ('Instagram',   'Instagram'),
            ('Telegram',    'Telegram'),
            ('Рекомендация', '推荐'),
            ('Сайт',        '网站'),
            ('Другое',      '其他'),
        ]
        for name, name_cn in sources_data:
            source = Source(name=name, name_cn=name_cn)
            db.session.add(source)

        # ===== МЕНЕДЖЕРЫ =====
        managers_data = [
            ('Лю Мин',  '刘明'),
            ('Ван Вэй', '王伟'),
        ]
        for name, name_cn in managers_data:
            manager = Manager(name=name, name_cn=name_cn)
            db.session.add(manager)

        db.session.commit()

        sources = {s.name: s.id for s in Source.query.all()}
        managers = {m.name: m.id for m in Manager.query.all()}

        # ===== ДЕМО-ЛИДЫ =====
        leads_data = [
            {
                'created_date': date(2026, 9, 15), 'name': 'Анна К.',
                'phone': '+7 902 123-45-67', 'city': 'Томск',
                'source_id': sources['Instagram'], 'client_query': 'Имплантация',  # ← ИЗМЕНЕНО
                'pre_sum': 69000, 'fact_sum': 69000, 'commission_rate': 10,
                'stage_id': 8, 'status_id': 2,
                'last_contact_date': date(2026, 9, 28),
                'plan_contact_date': date(2026, 10, 5),
                'manager_id': managers['Лю Мин'],
                'comment': 'Лечение завершено, довольна', 'loss_reason': ''
            },
            {
                'created_date': date(2026, 9, 20), 'name': 'Дмитрий В.',
                'phone': '+7 913 555-22-33', 'city': 'Новосибирск',
                'source_id': sources['Рекомендация'], 'client_query': 'Протезирование (коронки)',  # ← ИЗМЕНЕНО
                'pre_sum': 35000, 'fact_sum': 0, 'commission_rate': 10,
                'stage_id': 3, 'status_id': 1,
                'last_contact_date': date(2026, 9, 25),
                'plan_contact_date': date(2026, 9, 30),
                'manager_id': managers['Ван Вэй'],
                'comment': 'Прислал прайс, думает', 'loss_reason': ''
            },
            {
                'created_date': date(2026, 9, 22), 'name': 'Ольга С.',
                'phone': '+7 911 777-88-99', 'city': 'Москва',
                'source_id': sources['Сайт'], 'client_query': 'Чистка + лечение кариеса',  # ← ИЗМЕНЕНО
                'pre_sum': 8000, 'fact_sum': 0, 'commission_rate': 10,
                'stage_id': 2, 'status_id': 1,
                'last_contact_date': date(2026, 9, 22),
                'plan_contact_date': date(2026, 9, 24),
                'manager_id': managers['Лю Мин'],
                'comment': 'Ждём онлайн-консультацию', 'loss_reason': ''
            },
            {
                'created_date': date(2026, 9, 10), 'name': 'Сергей П.',
                'phone': '+7 923 444-55-66', 'city': 'Иркутск',
                'source_id': sources['Telegram'], 'client_query': 'Удаление + имплант',  # ← ИЗМЕНЕНО
                'pre_sum': 75000, 'fact_sum': 0, 'commission_rate': 10,
                'stage_id': 5, 'status_id': 2,
                'last_contact_date': date(2026, 9, 27),
                'plan_contact_date': date(2026, 9, 29),
                'manager_id': managers['Ван Вэй'],
                'comment': 'Согласовывает даты с работой', 'loss_reason': ''
            },
            {
                'created_date': date(2026, 8, 28), 'name': 'Марина Л.',
                'phone': '+7 905 111-22-33', 'city': 'Красноярск',
                'source_id': sources['Другое'], 'client_query': 'Бюгельный протез',  # ← ИЗМЕНЕНО
                'pre_sum': 40000, 'fact_sum': 0, 'commission_rate': 10,
                'stage_id': 10, 'status_id': 5,
                'last_contact_date': date(2026, 9, 5),
                'plan_contact_date': None,
                'manager_id': managers['Лю Мин'],
                'comment': 'Передумала, нашла в РФ',
                'loss_reason': 'Нашла клинику в РФ'
            },
        ]

        for ld in leads_data:
            lead = Lead(**ld)
            db.session.add(lead)

        db.session.commit()
        print("✅ БД создана и заполнена!")
        print(f"   📋 Этапов: {Stage.query.count()}")
        print(f"   📌 Статусов: {Status.query.count()}")
        print(f"   📡 Источников: {Source.query.count()}")
        print(f"   👤 Менеджеров: {Manager.query.count()}")
        print(f"   🎯 Лидов: {Lead.query.count()}")  # ← Теперь работает!
        print(f"   💾 Файл БД: {app.config['SQLALCHEMY_DATABASE_URI']}")


if __name__ == '__main__':
    seed()

