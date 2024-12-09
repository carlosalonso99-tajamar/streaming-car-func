import logging
import requests
import azure.functions as func

app = func.FunctionApp()

# URL de tu API
API_URL = "http://127.0.0.1:5000/api/next_state"

@app.timer_trigger(schedule="*/1 * * * * *", arg_name="myTimer", run_on_startup=False,
              use_monitor=False) 
def timer_trigger(myTimer: func.TimerRequest) -> None:
    if myTimer.past_due:
        logging.info('The timer is past due!')

    try:
        # Hacer una solicitud GET a la API
        response = requests.get(API_URL)

        # Comprobar si la respuesta fue exitosa
        if response.status_code == 200:
            # Datos del estado del coche
            car_state = response.json()
            logging.info(f"Data received: {car_state}")
        elif response.status_code == 404:
            logging.warning("No more data available from the API.")
        else:
            logging.error(f"API returned an error. Status Code: {response.status_code}, Message: {response.text}")
    except requests.exceptions.RequestException as e:
        # Manejo de errores de red o conexión
        logging.error(f"Error connecting to API: {e}")

    logging.info('Python timer trigger function executed.')
