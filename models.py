"""
CRM Хай-Лань — Модели данных (SQLAlchemy)
"""
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

db = SQLAlchemy()


class Manager(db.Model):
    __tablename__ = 'managers'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    name_cn = db.Column(db.String(50))
    is_active = db.Column(db.Boolean, default=True)

    leads = db.relationship('Lead', backref='manager', lazy='dynamic')

    def to_dict(self):
        return {'id': self.id, 'name': self.name, 'name_cn': self.name_cn}


class Stage(db.Model):
    __tablename__ = 'stages'
    id = db.Column(db.Integer, primary_key=True)
    order_num = db.Column(db.Integer)
    name = db.Column(db.String(100), nullable=False)
    name_cn = db.Column(db.String(50))
    color = db.Column(db.String(20))
    badge = db.Column(db.String(50))
    deadline = db.Column(db.String(50))

    leads = db.relationship('Lead', backref='stage', lazy='dynamic')

    def to_dict(self):
        return {
            'id': self.id, 'name': self.name, 'name_cn': self.name_cn,
            'color': self.color, 'badge': self.badge, 'deadline': self.deadline
        }


class Status(db.Model):
    __tablename__ = 'statuses'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    name_cn = db.Column(db.String(50))
    css_class = db.Column(db.String(50))

    def to_dict(self):
        return {'id': self.id, 'name': self.name, 'name_cn': self.name_cn, 'cls': self.css_class}


class Source(db.Model):
    __tablename__ = 'sources'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False, unique=True)
    name_cn = db.Column(db.String(50))

    leads = db.relationship('Lead', backref='source', lazy='dynamic')

    def to_dict(self):
        return {'id': self.id, 'name': self.name, 'name_cn': self.name_cn}


class Lead(db.Model):
    __tablename__ = 'leads'
    id = db.Column(db.Integer, primary_key=True)
    created_date = db.Column(db.Date, nullable=False)
    name = db.Column(db.String(200), nullable=False)
    phone = db.Column(db.String(50))
    city = db.Column(db.String(100))
    source_id = db.Column(db.Integer, db.ForeignKey('sources.id'))
    client_query = db.Column(db.String(500))  # ← ПЕРЕИМЕНОВАНО!
    pre_sum = db.Column(db.Float, default=0)
    fact_sum = db.Column(db.Float, default=0)
    commission_rate = db.Column(db.Float, default=10)
    stage_id = db.Column(db.Integer, db.ForeignKey('stages.id'))
    status_id = db.Column(db.Integer, db.ForeignKey('statuses.id'))
    last_contact_date = db.Column(db.Date)
    plan_contact_date = db.Column(db.Date)
    manager_id = db.Column(db.Integer, db.ForeignKey('managers.id'))
    comment = db.Column(db.Text)
    loss_reason = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    status = db.relationship('Status', backref='leads')

    @property
    def commission(self):
        if self.fact_sum and self.commission_rate:
            return round(self.fact_sum * self.commission_rate / 100)
        return 0

    def to_dict(self):
        return {
            'id': self.id,
            'date': self.created_date.isoformat() if self.created_date else '',
            'name': self.name,
            'phone': self.phone,
            'city': self.city,
            'source': self.source.name if self.source else '',
            'query': self.client_query,  # ← Возвращаем как 'query' для шаблона
            'pre_sum': self.pre_sum or 0,
            'fact_sum': self.fact_sum or 0,
            'commission_rate': self.commission_rate or 0,
            'commission': self.commission,
            'stage_id': self.stage_id,
            'status_id': self.status_id,
            'last_contact': self.last_contact_date.isoformat() if self.last_contact_date else '',
            'plan_contact': self.plan_contact_date.isoformat() if self.plan_contact_date else '',
            'manager': self.manager.name if self.manager else '',
            'comment': self.comment or '',
            'loss_reason': self.loss_reason or '',
            'stage': self.stage.to_dict() if self.stage else {},
            'status': self.status.to_dict() if self.status else {},
        }


class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True)
    password_hash = db.Column(db.String(256))
    role = db.Column(db.String(20), default='viewer')
    is_active = db.Column(db.Boolean, default=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)


class AuditLog(db.Model):
    __tablename__ = 'audit_log'
    id = db.Column(db.Integer, primary_key=True)
    lead_id = db.Column(db.Integer, db.ForeignKey('leads.id'))
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    action = db.Column(db.String(20))
    old_values = db.Column(db.JSON)
    new_values = db.Column(db.JSON)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)

