from django.apps import AppConfig
from django.conf import settings
import joblib
import os

class ResultsConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'results'
    ARIMA_MODEL_FILE = os.path.join(settings.MODELS, "GridDemand.joblib")
    gridDemand_model = joblib.load(ARIMA_MODEL_FILE)
    ElecPrices_MODEL_FILE = os.path.join(settings.MODELS, "ElecPrices.joblib")
    elecPrices_model = joblib.load(ElecPrices_MODEL_FILE)