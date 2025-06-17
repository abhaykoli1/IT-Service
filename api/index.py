# api/index.py

from mangum import Mangum
from main import app  # Import FastAPI app from your main.py

# Wrap the FastAPI app with Mangum for AWS Lambda compatibility (used by Vercel)
handler = Mangum(app)
