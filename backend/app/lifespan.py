from contextlib import asynccontextmanager
from fastapi import FastAPI
import dill


ml_models = {}

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Load the ML model
    # English Model
    with open('english_model/model.pkl', 'rb') as file:
            ml_models['en'] = dill.load(file)
    # TODO add arabic model here
    with open('arabic_model/model.pkl', 'rb') as file:
            ml_models['ar'] = dill.load(file)
    yield
    # Clean up the ML models and release the resources
    ml_models.clear()
