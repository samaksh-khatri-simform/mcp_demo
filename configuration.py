from os import getenv

from pydantic_settings import BaseSettings


class Configurations(BaseSettings):
    AZURE_OPENAI_API_KEY: str = getenv("AZURE_OPENAI_API_KEY", "")
    AZURE_OPENAI_ENDPOINT: str = getenv("AZURE_OPENAI_ENDPOINT", "")
    AZURE_DEPLOYMENT_NAME: str = getenv("AZURE_DEPLOYMENT_NAME", "")
    AZURE_API_VERSION: str = getenv("AZURE_API_VERSION", "")


config = Configurations()
