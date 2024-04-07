import azure.functions as func
import logging
import requests
from PIL import Image
from io import BytesIO
import google.generativeai as genai

app = func.FunctionApp(http_auth_level=func.AuthLevel.ANONYMOUS)

# Replace with your Mapbox and Google Generative AI API keys
ACCESS_TOKEN = "pk.eyJ1IjoicmFrc2hpdGhyIiwiYSI6ImNsdW56NTYxczE1ZnEybW9mMjY0N2tlbHQifQ.Q6g34-WRpQwGzS_LRuUoXQ"
GENAI_API_KEY = "AIzaSyDIpA5GCERPZiTY0h6h5LLZhL1estZu8sA"

@app.route(route="function_app")
def function_app(req: func.HttpRequest) -> func.HttpResponse:
    logging.info('Python HTTP trigger function processed a request.')
    try:
        coord = req.params.get('coord')
        if not coord:
            try:
                req_body = req.get_json()
            except ValueError:
                pass
            else:
                coord = req_body.get('name')

        if coord:
            logging.info("the coord is {coord}")
        else:
            return func.HttpResponse(
                "no coord",
                status_code=200
            )
        
        latitude, longitude = coord.split()

        # Image parameters
        zoom_level = 18
        image_width = 1024
        image_height = 1024

        # Construct Mapbox API request URL
        url = f"https://api.mapbox.com/styles/v1/mapbox/satellite-v9/static/{longitude},{latitude},{zoom_level}/{image_width}x{image_height}?access_token={ACCESS_TOKEN}"

        # Get image from Mapbox
        response = requests.get(url)
        if response.status_code != 200:
            return func.HttpResponse(
                f"Error fetching image from Mapbox: {response.status_code}",
                status_code=500
            )

        image_data = BytesIO(response.content)
        image = Image.open(image_data)

        # Analyze image with Google Generative AI
        genai.configure(api_key=GENAI_API_KEY)
        model = genai.GenerativeModel('gemini-pro-vision')
        prompt = "For the given image of a street, detect if there are any obstructions, damages, or anything that could be a public inconvenience, check for potholes and humps. give the output in a jsonfied format but not as a json program, with 2 keys the first one being a bool, with true if there is something that could be raised as a complaint and false if there are no points that could be raised as a complaint. The second key's value of the output gives the response to if there are any obstructions, potholes, humps, etc. Let the first key be called complaint and the second one be called description."
        response = model.generate_content([prompt, image], stream=True)
        response.resolve()

        # Return analysis results
        return func.HttpResponse(response.text)
    except Exception as e:
        logging.error("Error processing image data: %s", e)
        return func.HttpResponse(status_code=400, body=f"Error: {e}")


