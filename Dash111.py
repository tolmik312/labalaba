from dash import Dash, html, dash_table, dcc, callback, Output, Input
import pandas as pd
import plotly.express as px

# Чтение данных из CSV файла
df = pd.read_csv('F:/py/учеба/10laba/du1.csv')  # Обновите путь к вашему CSV файлу

# Инициализация приложения
app = Dash(__name__)

# Создаем список возможных периодов анализа
available_periods = df['дата'].unique()

# Макет приложения
app.layout = html.Div([
    html.Div(children='Мое первое приложение с данными, графиком и элементами управления'),
    html.Hr(),
    dcc.RadioItems(options=[{'label': col, 'value': col} for col in ['Температура день', 'Температура вечер']], value='Температура день', id='controls-and-radio-item'),
    dcc.Dropdown(options=[{'label': str(date), 'value': date} for date in available_periods], value=available_periods[0],id='date-dropdown'),  # Добавляем выпадающий список
    dash_table.DataTable(data=df.to_dict('records'), page_size=6),
    dcc.Graph(figure={}, id='controls-and-graph'),
    html.Div(id='indicator-container', children=[
        html.Div(id='temperature-day-value'),  # Индикатор для Температуры день
        html.Div(id='temperature-evening-value')  # Индикатор для Температуры вечер
    ])
])

# Добавление элементов управления для взаимодействия
@app.callback(
    Output(component_id='controls-and-graph', component_property='figure'),
    [Input(component_id='controls-and-radio-item', component_property='value'),
     Input(component_id='date-dropdown', component_property='value')]  # Модифицируем график в зависимости от выбранного периода
)
def update_graph(col_chosen, selected_date):
    filtered_df = df[df['дата'] == selected_date]  # Фильтруем данные по выбранному периоду
    fig = px.bar(filtered_df, x='дата', y=col_chosen, title=f'Средняя {col_chosen} по дате {selected_date}')
    return fig

# Callback для обновления индикаторов
@app.callback(
    Output('temperature-day-value', 'children'),
    [Input('controls-and-radio-item', 'value'),
     Input('date-dropdown', 'value')]
)
def update_temperature_day_indicator(col_chosen, selected_date):
    filtered_df = df[df['дата'] == selected_date]  # Фильтруем данные по выбранному периоду
    avg_temperature_day = filtered_df[col_chosen].mean()
    return f'Средняя температура: {avg_temperature_day}'

# Callback для обновления индикаторов
@app.callback(
    Output('temperature-evening-value', 'children'),
    [Input('controls-and-radio-item', 'value'),
     Input('date-dropdown', 'value')]
)
def update_temperature_evening_indicator(col_chosen, selected_date):
    filtered_df = df[df['дата'] == selected_date]  # Фильтруем данные по выбранному периоду
    avg_temperature_evening = filtered_df[col_chosen].mean()
    return f'Средняя температура вечер: {avg_temperature_evening}'

# Запуск приложения
if __name__ == '__main__':
    app.run_server(debug=True)
    
