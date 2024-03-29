from pydantic_settings import BaseSettings, SettingsConfigDict
import os

class Settings(BaseSettings):
    google_api_key: str
    embedded_model_name: str
    vector_db_url: str
    vector_db_port: int
    vector_db_collection_name: str
    chat_model_name: str
    
    model_config = SettingsConfigDict(env_file=f"{os.getcwd()}/app/.env")