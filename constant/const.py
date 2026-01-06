import os.path

APP_NAME="Inventory management system"

APP_VERSION=(0,0,0)


BASE_DIR=os.path.dirname(os.path.dirname(os.path.realpath(__file__)))
OUTPUT_DIR=os.path.join(BASE_DIR,'run')
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
HIDDEN_EYE = os.path.normpath(os.path.join(BASE_DIR, "..", "static", "hidden_eye.png"))
UNHIDDEN_EYE = os.path.normpath(os.path.join(BASE_DIR, "..", "static", "unhidden_eye.png"))

