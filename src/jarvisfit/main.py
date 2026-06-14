import sys
import time
from pathlib import Path

project_root = str(Path(__file__).resolve().parent.parent.parent)
if project_root not in sys.path:
    sys.path.insert(0, project_root)

from src.jarvisfit.crew import JarvisFitController
from src.jarvisfit.ui.gradio_app import launch_ui


def run():
    controller    = JarvisFitController()
    jarvis_thread = controller.kickoff()

    # Give voice listener thread time to initialize before UI launches
    time.sleep(1)
    print("[jarvisfit] System online. Launching UI at http://localhost:7860")

    # launch_ui blocks main thread keeping app alive
    # Voice listener runs as daemon thread alongside
    launch_ui(controller)


if __name__ == "__main__":
    run()