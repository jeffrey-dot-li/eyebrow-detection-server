import pynecone as pc

from dotenv import load_dotenv
import os

load_dotenv()

class EyebrowServerConfig(pc.Config):
    pass

config = EyebrowServerConfig(
    app_name="eyebrow_detection",
    db_url="sqlite:///pynecone.db",
    api_url=f"http://{os.getenv('SERVER_HOST')}:8000",
    env=pc.Env.DEV,
    bun_path="$HOME/.bun/bin/bun"
    
)
