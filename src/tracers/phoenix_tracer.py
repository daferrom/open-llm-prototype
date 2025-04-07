import os
import llama_index.core
from utils import env_utils
import sys
from pathlib import Path

# Add 'src' to sys.path for allowing utils import
sys.path.append(str(Path(__file__).resolve().parent.parent))

def set_tracer_phoenix_config():
    # Load .env only on local execution
    env_utils.load_env_if_local()
    # PHOENIX Config for Tr
    PHOENIX_API_KEY = os.getenv("PHOENIX_API_KEY")
    os.environ["OTEL_EXPORTER_OTLP_HEADERS"] = f"api_key={PHOENIX_API_KEY}"

    llama_index.core.set_global_handler(
        "arize_phoenix",
        endpoint="https://llamatrace.com/v1/traces"
    )
    
if __name__ == "__main__":
    print("Setting up PHOENIX tracer configuration...")