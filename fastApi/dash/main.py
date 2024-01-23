import dash
from dash import dcc, html, Output, Input, State
from dash.dependencies import Input, Output
import dash_bootstrap_components as dbc
from dash.exceptions import PreventUpdate
import requests
from config import cell_style, header_style


app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])
app.config.prevent_initial_callbacks = "initial_duplicate"


app.layout = html.Div(
    [
        dbc.Col(
            [ 
            dbc.Row(
                [
                    dbc.Col(
                        [
                            html.Div(
                                [
                                    html.H2("Регистрация", className="text-center"),
                                    dbc.Form(
                                        [
                                            html.Div(
                                                [
                                                    dbc.Label("Email"),
                                                    dbc.Input(
                                                        type="text",
                                                        id="reg-email",
                                                    ),
                                                ],
                                                className="mb-3",
                                            ),
                                            html.Div(
                                                [
                                                    dbc.Label("Username"),
                                                    dbc.Input(
                                                        type="text",
                                                        id="reg-username",
                                                    ),
                                                ],
                                                className="mb-3",
                                            ),
                                            html.Div(
                                                [
                                                    dbc.Label("Password"),
                                                    dbc.Input(
                                                        type="password",
                                                        id="reg-password",
                                                    ),
                                                ],
                                                className="mb-3",
                                            ),
                                            html.Div(
                                                [
                                                    dbc.Label("Фамилия пользователя"),
                                                    dbc.Input(
                                                        type="text",
                                                        id="reg-surname",
                                                    ),
                                                ],
                                                className="mb-3",
                                            ),
                                            html.Div(
                                                [
                                                    dbc.Label("Имя пользователя"),
                                                    dbc.Input(
                                                        type="text",
                                                        id="reg-name",
                                                    ),
                                                ],
                                                className="mb-3",
                                            ),
                                            dbc.Button(
                                                "Зарегистрироваться",
                                                id="btn-register",
                                                color="primary",
                                                className="mt-3",
                                            ),
                                            html.Div(
                                                id="output-register",
                                                className="text-center",
                                                style={"margin-top": "15px"},
                                            ),
                                        ],
                                    ),
                                ],
                                 style={"margin": "auto", "width": "auto"},
                             ),
                         ],
                         width={"size": 4, "offset": 0},
                     ),
                 ],
                 justify="center",
                 align="center",
                 className="mt-5",
             ),
            dbc.Row(
                [
                    dbc.Col(
                        [
                            html.Div(
                                [
                                    html.H2("Авторизация", className="text-center"),
                                    dbc.Form(
                                        [
                                            html.Div(
                                                [
                                                    dbc.Label("Имя пользователя"),
                                                    dbc.Input(
                                                        type="text",
                                                        id="login-username",
                                                    ),
                                                ],
                                                className="mb-3",
                                            ),
                                            html.Div(
                                                [
                                                    dbc.Label("Пароль"),
                                                    dbc.Input(
                                                        type="password",
                                                        id="login-password",
                                                    ),
                                                ],
                                                className="mb-3",
                                            ),
                                            dbc.Button(
                                                "Войти",
                                                id="btn-login",
                                                color="primary",
                                                className="mt-3",
                                            ),
                                            html.Div(
                                                id="output-login",
                                                className="text-center",
                                                style={"margin-top": "15px"},
                                            ),
                                        ],
                                    ),
                                ],
                                style={"margin": "auto", "width": "auto"},
                            ),
                        ],
                        width={"size": 4, "offset": 0},
                    ),
                ],
                justify="center",
                align="center",
                className="mt-5",
            ),
            ],
            align="center",
            className="mt-5",
            id= "first-block-div"
        ),    
        html.Div(
            [
                html.Div(
                    [
                        html.H1("Баланс:"),
                        html.H1("Авторизация не пройдена", id="score-div"),
                        dcc.Interval(
                            id="interval-component",
                            interval=1300,  # in milliseconds
                            n_intervals=0,
                        ),
                        dcc.Store(id="token-store"),
                        html.H2("Выберите модель:"),
                    ],
                    style={"margin-left": "50px"}
                ),
                dbc.Row(
                    [
                        dbc.Col(
                            [
                                dcc.Dropdown(
                                    id="dropdown-model",
                                    options=[
                                        {
                                            "label": "LinearRegression 10 points",
                                            "value": 0,
                                        },
                                        {
                                            "label": "GBoostRegression 15 points",
                                            "value": 1,
                                        },
                                        {
                                            "label": "CatboostRegression 20 points",
                                            "value": 2,
                                        },
                                    ],
                                    value=None,
                                    style={"margin-left": "25px"},
                                ),
                            ],
                            width={"size": 3, "offset": 0},
                        ),
                    ],
                    justify="left",
                    align="left",
                ),
                dbc.Row(
                    [
                        dbc.Col(
                            [   
                                html.Div(
                                    [
                                        html.H2(
                                            "Введите данные для определения возраста:"
                                        ),
                                    ],
                                    style={"margin-left": "50px",
                                           "margin-top": "20px"}
                                ),
                                html.Div(
                                    [
                                        dbc.Row(
                                            [
                                                html.Label(
                                                    "Человек старше 65 лет?"
                                                ),
                                                dcc.Checklist(
                                                    id="checkbox-age",
                                                    options=[
                                                        {
                                                            "label": "Да",
                                                            "value": "yes",
                                                        }
                                                    ],
                                                    value=[],
                                                ),
                                            ],
                                            justify="center",
                                            align="center",
                                            style={"margin-left": "10px"},
                                        ),
                                        dbc.Row(
                                            [
                                                html.Label(
                                                    "Ваш пол"
                                                ),
                                                dcc.Dropdown(
                                                    id="dropdown-gender",
                                                    options=[
                                                        {
                                                            "label": "Мужчина",
                                                            "value": "male",
                                                        },
                                                        {
                                                            "label": "Женщина",
                                                            "value": "female",
                                                        },
                                                    ],
                                                    value=None,
                                                ),
                                            ],
                                            className="mb-3",
                                            justify="center",
                                            align="center",
                                            style={"margin": "10px"},
                                        ),
                                        dbc.Row(
                                            [
                                                html.Label(
                                                    "Сколько дней в неделю занимаетесь спортом?"
                                                ),
                                                dcc.Dropdown(
                                                    id="dropdown-sport-days",
                                                    options=[
                                                        {
                                                            "label": str(i),
                                                            "value": i,
                                                        }
                                                        for i in range(1, 8)
                                                    ],
                                                    value=None,
                                                ),
                                            ],
                                            justify="center",
                                            align="center",
                                            style={"margin": "10px"},
                                        ),
                                        dbc.Row(
                                            [
                                                html.Label("Индекс массы тела (BMI)"),
                                                dcc.Slider(
                                                    id="slider-bmi",
                                                    min=14.5,
                                                    max=70,
                                                    step=0.1,
                                                    value=None,
                                                    marks={
                                                        i: str(i)
                                                        for i in range(15, 70, 5)
                                                    },
                                                ),
                                                html.Div(
                                                    id="slider-bmi-value"
                                                ),
                                            ],
                                            justify="center",
                                            align="center",
                                            style={"margin": "10px"},
                                        ),
                                        dbc.Row(
                                            [
                                                html.Label(
                                                    "Уровень глюкозы в крови после голодания"
                                                ),
                                                dcc.Slider(
                                                    id="slider-glucose",
                                                    min=63,
                                                    max=405,
                                                    step=1,
                                                    value=None,
                                                    marks={
                                                        i: str(i)
                                                        for i in range(
                                                            70, 400, 50
                                                        )
                                                    },
                                                ),
                                                html.Div(
                                                    id="slider-glucose-value"
                                                ),
                                            ],
                                            justify="center",
                                            align="center",
                                            style={"margin": "10px"},
                                        ),
                                        dbc.Row(
                                            [
                                                html.Label("Степень диабета"),
                                                dcc.Dropdown(
                                                    id="dropdown-diabetes-degree",
                                                    options=[
                                                        {"label": "1", "value": 1},
                                                        {"label": "2", "value": 2},
                                                        {"label": "3", "value": 3},
                                                    ],
                                                    value=None,
                                                ),
                                            ],
                                            justify="center",
                                            align="center",
                                            style={"margin": "10px"},
                                        ),
                                        dbc.Row(
                                            [
                                                html.Label(
                                                    "Уровень гемоглобина"
                                                ),
                                                dcc.Slider(
                                                    id="slider-hemoglobin",
                                                    min=40,
                                                    max=600,
                                                    step=1,
                                                    value=None,
                                                    marks={
                                                        i: str(i)
                                                        for i in range(
                                                            50, 600, 50
                                                        )
                                                    },
                                                ),
                                                html.Div(
                                                    id="slider-hemoglobin-value"
                                                ),
                                            ],
                                            justify="center",
                                            align="center",
                                            style={"margin": "10px"},
                                        ),
                                        dbc.Row(
                                            [
                                                html.Label(
                                                    "Уровень инсулина в крови"
                                                ),
                                                dcc.Slider(
                                                    id="slider-insulin",
                                                    min=1,
                                                    max=100,
                                                    step=1,
                                                    value=None,
                                                    marks={
                                                        i: str(i)
                                                        for i in range(
                                                            10, 100, 10
                                                        )
                                                    },
                                                ),
                                                html.Div(
                                                    id="slider-insulin-value"
                                                ),
                                            ],
                                            justify="center",
                                            align="center",
                                            style={"margin": "10px"},
                                        ),
                                    ],
                                    style={"margin-left": "30px"},
                                ),
                                html.Div(
                                    [
                                        dbc.Button(
                                            "Получить данные",
                                            id="btn-get-data",
                                            style={"margin-right": "15px",
                                                   "margin-top": "20px"}
                                        ),
                                        dbc.Button(
                                            "Получить результат сетки",
                                            id="btn-get-result",
                                            style={"margin-left": "15px",
                                                   "margin-top": "20px"}
                                        ),
                                    ],
                                    style={"margin-left": "50px"},
                                ),
                                html.Div(id="output-data",
                                         style={"margin-left": "50px",
                                                "margin-top": "20px"},),
                                html.Div(id="output-result",
                                         style={"margin-left": "50px",
                                                "margin-top": "20px"},),
                            ],
                        ),
                        dbc.Col(
                            [
                                html.Div(
                                    [
                                        html.H3("История запросов:"),
                                        html.Table(id="history-table"),
                                    ],
                                    style={"margin-top": "25px",
                                           "width": "auto",
                                           "margin-left": "50px",
                                           "margin-right": "50px"},
                                )
                            ]
                        ),
                    ],
                    justify="left",
                    align="left",
                ),
            ],
            id="second-block-div",
            style={"display": ""},
        ),
        dcc.Interval(
            id="interval-component-main",
            interval=1000,
            n_intervals=0,
        ),
    ],
    style={
        
        "background-color": "#f2f2f2",
    },
)


def create_cols_and_data_for_table(data):
    for x in range(len(data)):
        model = data[x]["model"]
        age = "Старше 65" if data[x]["age_group"] == 1 else "Младше 65"
        gender = "Мужчина" if data[x]["gender"] == 0 else "Женщина"
        data_instance = (
            model,
            age,
            gender,
            data[x]["sport_days"],
            data[x]["bmi"],
            data[x]["glucose"],
            data[x]["diabetes_degree"],
            data[x]["hemoglobin"],
            data[x]["insulin"],
            data[x]["result"],
        )
        data[x] = data_instance
    return reversed(data)


def create_table(
    raw_data,
    keys=(
        " Модель ",
        " Воз. группа ",
        " Пол ",
        " Спорт д/н ",
        " ИМТ ",
        " Глюкоза ",
        " Диабет ",
        " Гемоглобин ",
        " Инсулин ",
        " Результат ",
    ),
):
    data = create_cols_and_data_for_table(raw_data)
    table_rows = [
        html.Tr([html.Td(h, style=cell_style) for h in row]) for row in data
    ]
    table = html.Table(
        [
            html.Thead(html.Tr([html.Th(k, style=header_style) for k in keys])),
            html.Tbody(table_rows),
        ]
    )

    return table


def get_history_list(
    history_url="http://127.0.0.1:8935/user/predict_rows", token=None
):
    headers = {"token": f"{token}"}
    try:
        response = requests.get(history_url, headers=headers)
        response.raise_for_status()
        history_strings = response.json()["predict_rows"]
        return history_strings, response.json()["predict_rows"]
    except:
        return []


@app.callback(
    Output("output-register", "children"),
    [Input("btn-register", "n_clicks")],
    [
        State("reg-email", "value"),
        State("reg-username", "value"),
        State("reg-password", "value"),
        State("reg-name", "value"),
        State("reg-surname", "value"),
    ],
)
def register_callback(
    n_clicks,
    email,
    username,
    password,
    name,
    surname,
):
    if n_clicks is None:
        raise PreventUpdate

    register_url = "http://127.0.0.1:8935/sign-up"
    data = {
        "email": email,
        "username": username,
        "password": password,
        "name": name,
        "surname": surname,
    }

    try:
        response = requests.post(register_url, json=data)
        response.raise_for_status()
        return response.json().get("message", "Registration successfull")
    except requests.HTTPError as e:
        return "Registration failed: Probably registred already"


@app.callback(
    [
        Output("token-store", "data"),
        Output(
            "history-table",
            "children",
            allow_duplicate=True,
        ),
    ],
    [Input("btn-login", "n_clicks")],
    [
        State("login-username", "value"),
        State("login-password", "value"),
    ],
)
def login_callback(n_clicks, username, password):
    if n_clicks is None:
        raise PreventUpdate

    login_url = "http://127.0.0.1:8935/token"
    data = {
        "username": username,
        "password": password,
    }

    try:
        response = requests.post(login_url, data=data)
        response.raise_for_status()
        access_token = response.json().get("access_token", "")
        hl, raw_data = get_history_list(token=access_token)
        return [access_token, create_table(raw_data)]
    except requests.HTTPError as e:
        return [None, html.Div("Не авторизован")]


@app.callback(
    [
        Output(f"slider-{field}-value", "children")
        for field in ["bmi", "glucose", "hemoglobin", "insulin"]
    ],
    [
        Input(f"slider-{field}", "value")
        for field in ["bmi", "glucose", "hemoglobin", "insulin"]
    ],
)
def update_slider_values(bmi, glucose, hemoglobin, insulin):
    return [
        f"Текущее значение: {value}"
        for value in [bmi, glucose, hemoglobin, insulin]
    ]


@app.callback(
    Output("output-data", "children"),
    Input("btn-get-data", "n_clicks"),
    State("dropdown-model", "value"),
    State("checkbox-age", "value"),
    State("dropdown-gender", "value"),
    State("dropdown-sport-days", "value"),
    State("slider-bmi", "value"),
    State("slider-glucose", "value"),
    State("dropdown-diabetes-degree", "value"),
    State("slider-hemoglobin", "value"),
    State("slider-insulin", "value"),
)
def get_and_display_data(
    n_clicks,
    model,
    age,
    gender,
    sport_days,
    bmi,
    glucose,
    diabetes_degree,
    hemoglobin,
    insulin,
):
    if n_clicks is None:
        raise dash.exceptions.PreventUpdate

    data_str = f"Model: {model},Age: {age}, Gender: {gender}, Sport Days: {sport_days}, BMI: {bmi}, Glucose: {glucose}, Diabetes Degree: {diabetes_degree}, Hemoglobin: {hemoglobin}, Insulin: {insulin}"

    return html.Div(data_str)


@app.callback(
    [
        Output(
            "history-table",
            "children",
            allow_duplicate=True,
        ),
    ],
    Input("btn-get-result", "n_clicks"),
    State("dropdown-model", "value"),
    State("checkbox-age", "value"),
    State("dropdown-gender", "value"),
    State("dropdown-sport-days", "value"),
    State("slider-bmi", "value"),
    State("slider-glucose", "value"),
    State("dropdown-diabetes-degree", "value"),
    State("slider-hemoglobin", "value"),
    State("slider-insulin", "value"),
    State("token-store", "data"),
)
def predict(
    n_clicks,
    model,
    age,
    gender,
    sport_days,
    bmi,
    glucose,
    diabetes_degree,
    hemoglobin,
    insulin,
    token,
):
    if n_clicks is not None:
        fast_api_inference_url = "http://127.0.0.1:8935/send_data"
        data = {
            "model": model,
            "age_group": age,
            "RIAGENDR": gender,
            "PAQ605": sport_days,
            "BMXBMI": bmi,
            "LBXGLU": glucose,
            "DIQ010": diabetes_degree,
            "LBXGLT": hemoglobin,
            "LBXIN": insulin,
            "token": token,
        }
        try:
            response = requests.post(fast_api_inference_url, json=data)
            response.raise_for_status()
        except requests.exceptions.RequestException as e:
            return html.Div("Не авторизован")

        try:
            hl, raw_data = get_history_list(token=token)
            return [create_table(raw_data)]
        except KeyError as e:
            return html.Div("Не авторизован")


@app.callback(
    [
        Output("score-div", "children"),
        Output("first-block-div", "style"),
        Output("second-block-div", "style"),
        Output(
            "history-table",
            "children",
            allow_duplicate=True,
        ),
    ],
    [Input("interval-component-main", "n_intervals")],
    State("token-store", "data"),
)
def update_score(n, token):
    bill_url = "http://127.0.0.1:8935/user/billing"
    headers = {"Authorization": f"{token}"}
    try:
        response = requests.get(bill_url, headers=headers)
        _, raw_data = get_history_list(token=token)
        response.raise_for_status() 
        return (
            response.json()["bill"],
            {"display": "none"},
            {"display": ""},
            create_table(raw_data),
        )
    except:
        return "Not authorized", {"display": ""}, {"display": "none"}, None


if __name__ == "__main__":
    app.run_server(debug=False, host = '0.0.0.0')
