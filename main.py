from fastapi import FastAPI
from pydantic import BaseModel
import pickle
import json
import uvicorn
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class model_input(BaseModel):

    state:str
    dist:str
    year:int
    season:str
    Crop:str
    area:float

crop_prod_model = pickle.load(open('crop_prod.pkl', 'rb'))

@app.post('/crop_yeild_production')
def crop_prod(input_parameters : model_input):

    input_data = input_parameters.json()
    input_dictionary = json.loads(input_data)

    state = input_dictionary['state']
    dist = input_dictionary['dist']
    year = input_dictionary['year']
    season = input_dictionary['season']
    Crop = input_dictionary['Crop']
    area = input_dictionary['area']




    input_list = [state,dist,year,season,Crop,area]

    prediction = crop_prod_model.predict([input_list])

    if prediction[0]:

        return prediction[0]
    else:
        return -1

from pyngrok import ngrok
import nest_asyncio

ngrok_tunnel = ngrok.connect(8000)
print('Public URL:', ngrok_tunnel.public_url)
nest_asyncio.apply()
uvicorn.run(app, port=8000)