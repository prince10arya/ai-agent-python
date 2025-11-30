import sys
from pathlib import Path

# Add current directory to path
sys.path.insert(0, str(Path(__file__).parent))

# Import FastAPI app
from main import app
from mangum import Mangum

# Vercel/Lambda handler
handler = Mangum(app)
