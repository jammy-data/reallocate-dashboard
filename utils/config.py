import os
from pathlib import Path
from dotenv import load_dotenv

# Load environment variables from .env file if it exists
load_dotenv()

# parameters
RANDOM_STATE = int(os.getenv("RANDOM_STATE", "95829"))
PRECISION_DECIMAL_DIGITS = int(os.getenv("PRECISION_DECIMAL_DIGITS", "4"))

# Paths
PROJ_ROOT = Path(__file__).resolve().parents[1]

#Assets
ASSETS_DIR = PROJ_ROOT / "assets"

IMAGES_DIR = ASSETS_DIR / "images"
LOGOS_DIR = ASSETS_DIR / "logos"
MAPS_DIR = ASSETS_DIR / "map_snapshots"

#Components
COMPONENTS_DIR = PROJ_ROOT / "components"

HOME_DIR = COMPONENTS_DIR / "home"
PILOT_DIR = COMPONENTS_DIR / "pilot"

# Config
CONFIG_DIR = PROJ_ROOT / "config"

#Data
DATA_DIR = PROJ_ROOT / "data"

PILOTS_DIR = DATA_DIR / "pilots"

