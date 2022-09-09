import streamlit as st
import pandas as pd


header = st.container()
dataset = st.container()
modelTraining = st.container()

with header:
    st.title('привет! я тут финансовую модель на основе данных музыкальной прилаги построила. вот')
    st.text('в этом проекте я решила взять данные о подписках за последние 3 года и проанализировать динамику')

with dataset:
    st.header('Данные по подпискам в разрезе года, анализируя последние 3 года')
    st.text('у меня были данные о подписках от платформ Apphud & AppstoreConnect по ASO трафику')

    data = pd.read_csv('data.csv')
    st.write(data)

    st.text('сразу проанализируем и посчитаем средние итоговые показатели за последние 3 года ')
    st.text('по графику видно, что в среднем за последние 3 года приложение просматривалось чаще всего в ноябре')
    st.bar_chart(data['Показы'])
    st.text('монетизировалась прилага успешнее всего в начале года(в феврале) и в конце года, в декабре')
    st.bar_chart(data['Admob монетизация'])
    st.text('устанавливали прилагу чаще всего в феврале и в апреле, что удивительно, ведь это не самые активные месяцы по просмотрам')
    st.bar_chart(data['ASO установки'])

    st.text('посчитаем итоговые данные за 12 месяцев')
    sumdata = {'ASO выручка, $': data['ASO выручка'].sum().astype(int), 'Admob монетизация, $': data['Admob монетизация'].sum().astype(int), 'Показы': [4446], 'ASO установки': [1521]}
    sumdf = pd.DataFrame(data=sumdata)
    st.write(sumdf)

    st.text('средняя конверсия в клик - 1,04%')

with modelTraining:
    st.header('теперь на основе этих данных обучим нашу модель')
    st.text('здесь можно менять данные и считать итоговую прибыль')

    sel_col, disp_col = st.columns(2)
    cpi = sel_col.slider('какой будет рекламный CPI?', min_value=1, max_value=100,value=1,step=1)
    budget = sel_col.slider('какой будет рекламный бюджет?', min_value=100, max_value=10000,value=1000,step=100)
    convert = sel_col.slider('какой процент из установки в подписку?', min_value=1, max_value=100,value=50,step=1)
    averagecost = sel_col.slider('стоимость подписки', min_value=1, max_value=100,value=6,step=1)

    st.subheader('окей, данные приняты. вот что получилось в итоге:')
    st.text('количество загрузок:')
    installs = budget/cpi
    st.write(installs)
    st.text('количество подписок в первый месяц:')
    firstmonthconvert = convert/100*installs
    st.write(firstmonthconvert)

    st.text('расчет подписок с учетом удержания в течение 12 месяцев')
    subduringyear = {'1 месяц': firstmonthconvert*0.65,
                     '2 месяц': firstmonthconvert*0.5,
                     '3 месяц': firstmonthconvert*0.43,
                     '4 месяц': firstmonthconvert*0.38,
                     '5 месяц': firstmonthconvert*0.34,
                     '6 месяц': firstmonthconvert*0.3,
                     '7 месяц': firstmonthconvert*0.26,
                     '8 месяц': firstmonthconvert*0.25,
                     '9 месяц': firstmonthconvert*0.23,
                     '10 месяц': firstmonthconvert*0.21,
                     '11 месяц': firstmonthconvert*0.20,
                     '12 месяц': firstmonthconvert*0.21}

    dftotalsum = pd.DataFrame(list(subduringyear.items()),
               columns=['Месяц', 'Подписки'])

    st.bar_chart(dftotalsum['Подписки'])
    st.write(dftotalsum)

    st.text('то есть к концу года останется вот такое количество подписок:')
    st.write(firstmonthconvert*0.21)

    st.text('всего за год будет подписок:')
    totalsum = (firstmonthconvert*0.65 + firstmonthconvert*0.5 + firstmonthconvert*0.43 +
            + firstmonthconvert*0.38 + firstmonthconvert*0.34 + firstmonthconvert*0.3 +
            + firstmonthconvert*0.26 + firstmonthconvert*0.25 + firstmonthconvert*0.23 +
            + firstmonthconvert*0.21 + firstmonthconvert*0.20 + firstmonthconvert*0.21)
    st.write(totalsum)

    st.text('выручка составит')
    st.write(totalsum * averagecost)

    st.text('разрез выручки в течение 12 месяцев')
    totalsumduringyear = {'1 месяц': firstmonthconvert*0.65*averagecost,
                     '2 месяц': firstmonthconvert*0.5*averagecost,
                     '3 месяц': firstmonthconvert*0.43*averagecost,
                     '4 месяц': firstmonthconvert*0.38*averagecost,
                     '5 месяц': firstmonthconvert*0.34*averagecost,
                     '6 месяц': firstmonthconvert*0.3*averagecost,
                     '7 месяц': firstmonthconvert*0.26*averagecost,
                     '8 месяц': firstmonthconvert*0.25*averagecost,
                     '9 месяц': firstmonthconvert*0.23*averagecost,
                     '10 месяц': firstmonthconvert*0.21*averagecost,
                     '11 месяц': firstmonthconvert*0.20*averagecost,
                     '12 месяц': firstmonthconvert*0.21*averagecost}

    dftotalsum = pd.DataFrame(list(totalsumduringyear.items()),
                   columns=['Месяц', 'Выручка'])

    st.write(dftotalsum)
    st.bar_chart(dftotalsum['Выручка'])



    st.text('прибыль от Admob')
    admob_revenue = totalsum * averagecost*0.0919
    st.write(admob_revenue)


    admob_revenue_taxes = 0.00576*admob_revenue+0.02*admob_revenue
    totalsum_rev = totalsum * averagecost
    apple_revenue = totalsum_rev * 0.15
    totalsum_taxes = apple_revenue + ((totalsum_rev-apple_revenue)*0.096) + totalsum_rev *0.02


    st.text('общая сумма налогов составит')
    st.write(totalsum_taxes+admob_revenue_taxes)

    st.text('чистая прибыль')
    st.write(totalsum_rev - totalsum_taxes + admob_revenue - admob_revenue_taxes)


    st.text('ROAS')
    st.write(totalsum_rev/budget)

    st.text('ROI')
    st.write((totalsum_rev-budget)/budget*100)

    st.text('P.S важно помнить, что расчет данных производится только для расчета рекламных пользователей, без учета органики')
    st.text('данные для расчета основаны на органическом трафике в течение последних 3 лет')
