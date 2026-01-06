import os
from dataclasses import dataclass
import streamlit as st
from dotenv import load_dotenv

load_dotenv() 

@dataclass(frozen=True)
class Settings:
    aws_read_api_url: str

def get_settings() -> Settings:
    url = ""
    try:
        url = str(st.secrets.get("AWS_READ_API_URL", "")).strip()
    except Exception:
        pass

    if not url:
        url = os.getenv("AWS_READ_API_URL", "").strip()

    if not url:
        raise RuntimeError("Missing AWS_READ_API_URL (set it in Streamlit secrets or env var).")

    return Settings(aws_read_api_url=url)
