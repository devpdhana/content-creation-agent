import os

from dotenv import load_dotenv

load_dotenv()


class Settings:
    NVIDIA_CHAT_MODEL_KEY: str = os.getenv("NVIDIA_CHAT_MODEL_KEY")
    NVIDIA_CHAT_MODEL: str = os.getenv("NVIDIA_CHAT_MODEL")


settings = Settings()
