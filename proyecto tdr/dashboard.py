import dash
from dash import dcc, html
from dash.dependencies import Input, Output, State
import requests

app = dash.Dash(__name__)

app.layout = html.Div([
    html.H1("Predicción de Lesiones", style={'text-align': 'center'}),
    
    html.Div([
        dcc.Input(id='age', type='number', placeholder='Edad', min=18, max=40, style={'margin': '10px', 'width': '300px'}),
        dcc.Input(id='weight', type='number', placeholder='Peso', min=50, max=150, style={'margin': '10px', 'width': '300px'}),
        dcc.Input(id='height', type='number', placeholder='Altura', min=150, max=220, style={'margin': '10px', 'width': '300px'}),
        
        html.Div(
            dcc.Dropdown(
                id='previous_injuries',
                options=[
                    {'label': 'Sí', 'value': 1},
                    {'label': 'No', 'value': 0}
                ],
                placeholder='Lesiones anteriores',
                style={'margin': '0px', 'width': '300px'}
            ),
            style={'margin': '10px', 'width': '308px'}
        ),
        
        dcc.Input(id='training_intensity', type='number', placeholder='Intensidad de entrenamiento', min=0, max=1, step=0.01, style={'margin': '10px', 'width': '300px'}),
        dcc.Input(id='recovery_time', type='number', placeholder='Tiempo de recuperación', min=1, max=10, style={'margin': '10px', 'width': '300px'}),
    ], style={'display': 'flex', 'flex-direction': 'column', 'align-items': 'center'}),
    
    html.Button('Predecir', id='predict-button', n_clicks=0, style={'margin': '10px'}),
    
    html.Div(id='prediction-output', style={'text-align': 'center', 'margin': '20px'})
])

@app.callback(
    Output('prediction-output', 'children'),
    Input('predict-button', 'n_clicks'),
    State('age', 'value'),
    State('weight', 'value'),
    State('height', 'value'),
    State('previous_injuries', 'value'),
    State('training_intensity', 'value'),
    State('recovery_time', 'value')
)
def update_output(n_clicks, age, weight, height, previous_injuries, training_intensity, recovery_time):
    if n_clicks > 0:
        if None in [age, weight, height, previous_injuries, training_intensity, recovery_time]:
            return 'Por favor, completa todos los campos.'
        
        data = [{
            'Player_Age': age,
            'Player_Weight': weight,
            'Player_Height': height,
            'Previous_Injuries': previous_injuries,
            'Training_Intensity': training_intensity,
            'Recovery_Time': recovery_time
        }]
        response = requests.post('http://127.0.0.1:5000/predict', json=data)
        prediction = response.json()[0]
        return f'Predicción de lesión: {"Sí" if prediction == 1 else "No"}'
    return ''

if __name__ == '__main__':
    app.run_server(debug=True)
