"""
CRM Хай-Лань — Формы для лидов
"""
from flask_wtf import FlaskForm
from wtforms import (
    StringField, SelectField, TextAreaField,
    FloatField, DateField, SubmitField
)
from wtforms.validators import DataRequired, Optional, NumberRange, Length
from models import Source, Stage, Status, Manager


class LeadForm(FlaskForm):
    """Форма создания/редактирования лида"""
    
    name = StringField('Имя клиента', validators=[
        DataRequired(message='Укажите имя клиента'),
        Length(max=200, message='Максимум 200 символов')
    ])
    
    phone = StringField('Телефон', validators=[
        Optional(),
        Length(max=50, message='Максимум 50 символов')
    ])
    
    city = StringField('Город', validators=[
        Optional(),
        Length(max=100, message='Максимум 100 символов')
    ])
    
    source_id = SelectField('Источник', coerce=int, validators=[DataRequired()])
    
    client_query = TextAreaField('Запрос клиента', validators=[
        Optional(),
        Length(max=500, message='Максимум 500 символов')
    ])
    
    pre_sum = FloatField('Предварительная сумма ₽', default=0, validators=[
        Optional(),
        NumberRange(min=0, message='Сумма не может быть отрицательной')
    ])
    
    fact_sum = FloatField('Фактическая сумма ₽', default=0, validators=[
        Optional(),
        NumberRange(min=0, message='Сумма не может быть отрицательной')
    ])
    
    commission_rate = FloatField('Комиссия %', default=10, validators=[
        Optional(),
        NumberRange(min=0, max=100, message='Комиссия от 0 до 100%')
    ])
    
    stage_id = SelectField('Этап воронки', coerce=int, validators=[DataRequired()])
    
    status_id = SelectField('Статус', coerce=int, validators=[DataRequired()])
    
    manager_id = SelectField('Менеджер', coerce=int, validators=[DataRequired()])
    
    last_contact_date = DateField('Дата последнего контакта', validators=[Optional()])
    
    plan_contact_date = DateField('Дата следующего контакта', validators=[Optional()])
    
    comment = TextAreaField('Комментарий', validators=[
        Optional(),
        Length(max=2000, message='Максимум 2000 символов')
    ])
    
    loss_reason = TextAreaField('Причина потери', validators=[
        Optional(),
        Length(max=500, message='Максимум 500 символов')
    ])
    
    submit = SubmitField('Сохранить')
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Заполняем выпадающие списки из БД
        self.source_id.choices = [(s.id, s.name) for s in Source.query.all()]
        self.stage_id.choices = [(s.id, s.name) for s in Stage.query.order_by(Stage.order_num).all()]
        self.status_id.choices = [(s.id, s.name) for s in Status.query.all()]
        self.manager_id.choices = [(m.id, m.name) for m in Manager.query.filter_by(is_active=True).all()]
