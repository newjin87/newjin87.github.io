
import sys
from pathlib import Path

# Add project root to sys.path to allow imports from libs
# This file is in automation/generators/daily_briefing/
# Root is automation/
current_dir = Path(__file__).resolve().parent
project_root = current_dir.parent.parent
sys.path.append(str(project_root))

from libs import analyzer, scraper, utils
import config.settings as config
