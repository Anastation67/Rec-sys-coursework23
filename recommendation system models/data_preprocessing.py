#!/usr/bin/env python
# coding: utf-8

import numpy as np
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import statsmodels.api as sm
from random import shuffle

import csv
import psycopg2
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT
from sqlalchemy import create_engine, MetaData, Table, Column, Identity, Integer, String, Float, Text, null
from sqlalchemy import text

from dotenv import load_dotenv

def preprocess_data():

    df = pd.read_excel("coursework2023\providers.xlsx").drop(columns=['№'])

    df = df.drop([
            '2022, Среднесписочная численность работников', 
            'Размер компании', 
            '2022, Коэффициент текущей ликвидности, %', 
            '2022, Коэффициент быстрой ликвидности, %', 
            '2022, Рентабельность капитала (ROE), %', 
            '2022, Рентабельность активов (ROA), %', 
            '2022, Коэффициент абсолютной ликвидности, %', 
            '2022, Себестоимость продаж, RUB', 
            '2022, Коэффициент оборачиваемости совокупных активов, %', 
            '2022, Период оборота активов, дни', 
            '2022, Рентабельность продаж, %', 
            '2022, Доля себестоимости как процент от выручки, %', 
            '2022, Запасы, RUB', 
            '2022, Уставный капитал , RUB', 
            '2022, Оборачиваемость основных средств, разы', 
            '2022, Период оборота основных средств, дни', 
            '2022, Рентабельность активов (п. 1.6 ст.105.8 НК РФ), %', 
            '2022, Соотношение валовой прибыли к активам компании, %', 
            '2022, Валовая рентабельность, %', 'Электронный адрес', 
            '2022, Поступления от текущих операций, RUB', 
            '2022, Платежи поставщикам и подрядчикам, RUB', 
            '2022, Поступления от продаж, RUB', 
            '2022, Поступления от инвестиционных операций, RUB', 
            '2022, Получение дивидендов, процентов, RUB', 
            '2022, Поступления арендных, лицензионных, комиссионных платежей, роялти, RUB', 
            '2022, Поступления от перепродажи финансовых вложений, RUB', 
            '2022, Поступления от выпуска акций, увеличения долей участия, RUB', 
            '2022, Поступления от выпуска облигаций, векселей и других долговых ценных бумаг и др., RUB'], axis=1)

    a = ['Сводный индикатор', 'Уставный капитал, RUB', 'Вид деятельности/отрасль', 'Руководитель - ФИО']
    for col in a:
        df = df[df[col].notna()]

    providers = df[['Наименование', 'Вид деятельности/отрасль', 'Сводный индикатор', 'Важная информация','Телефон', 
                    'Адрес (место нахождения)', 'Предмет поставки', 'Руководитель - ФИО', 'Регистрационный номер', 'Уставный капитал, RUB']].rename_axis('Registration number').reset_index()

    providers.to_csv('coursework2023\providers.csv')


def save_company_data_to_db(): 

    engine = create_engine('postgresql+psycopg2://postgres:123456@localhost/coursework2023DB')

    connection = psycopg2.connect(user="postgres", password="123456")
    connection.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
    cursor = connection.cursor()
    cursor.close()
    connection.close()

    # initialize the Metadata Object
    meta = MetaData()
    MetaData.reflect(meta, bind=engine, extend_existing=True)

    company4 = Table(
        'company4', meta,
        Column('id', Integer, Identity(), primary_key=True),
        Column('company_name', String(100), nullable=False),
        Column('industry_type', Text(), nullable=False),
        Column('summary_indicator', String(15), nullable=False),
        Column('important_info', Text()),
        Column('phone', Text()),
        Column('address', Text(), nullable=False),
        Column('sale_articles', Text(), nullable=False),
        Column('head_name', String(100)),
        Column('reg_number', String(13), nullable=False),
        Column('share_capital', Float(), nullable=False),
        extend_existing=True
    )
  
    meta.create_all(engine)

    with open('coursework2023\providers.csv', 'r', encoding="utf8") as f:
        reader = csv.reader(f)
        next(reader) # Skip the header row.
        for row in reader:
            statement = company4.insert().values(company_name = row[2], 
                                                industry_type = row[3], 
                                                summary_indicator = row[4],
                                                important_info = row[5],
                                                phone = row[6], 
                                                address = row[7], 
                                                sale_articles = row[8],  
                                                head_name = row[9], 
                                                reg_number = row[10],  
                                                share_capital = row[11]
                                              )
            with engine.connect() as conn:
                result = conn.execute(statement)
                conn.commit()


def save_comment_data_to_db():
    df = pd.read_excel("coursework2023\comments.xlsx")

    df.to_csv('coursework2023\comments.csv')

    engine = create_engine('postgresql+psycopg2://postgres:123456@localhost/coursework2023DB')

    connection = psycopg2.connect(user="postgres", password="123456")
    connection.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
    cursor = connection.cursor()
    cursor.close()
    connection.close()

    # initialize the Metadata Object
    meta = MetaData()
    MetaData.reflect(meta, bind=engine, extend_existing=True)

    comment0000 = Table(
        'comment0000', meta,
        Column('id', Integer, Identity(), primary_key=True),
        Column('company_name', String(100)),
        Column('comment', Text(), nullable=False),
        Column('user_grade', Integer),
        Column('final_grade', Float, nullable=False),
        extend_existing=True
    )

    meta.create_all(engine)

    with open('coursework2023\comments.csv', 'r', encoding="utf8") as f:
        reader = csv.reader(f)
        next(reader) # Skip the header row.
        for row in reader:
            user_grade = row[3]
            if user_grade == '\\' or user_grade == '/':
                user_grade_new = 0
            else:
                user_grade_new = user_grade
            statement = comment0000.insert().values(company_name = row[1], 
                                                comment = row[2], 
                                                user_grade = user_grade_new,
                                                final_grade = row[4],
                                              )
            with engine.connect() as conn:
                result = conn.execute(statement)
                conn.commit()


preprocess_data()
save_company_data_to_db()
save_comment_data_to_db()
