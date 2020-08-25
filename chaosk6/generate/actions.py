import subprocess
import os

from logzero import logger
from pathlib import Path

__all__ = ["runScript", "stressEndpoint"]

def runScript(script: str = None, vus: int = 1, duration: str = "1s"):
    _runScript(script, vus, duration)

def stressEndpoint(endpoint: str = None, vus: int = 1, duration: str = "1s"):
    basePath = str(Path(__file__).parent)
    env = dict(**os.environ, CHAOS_K6_URL=endpoint)
    _runScript(basePath + "/single-url.js", vus, duration, env)

def _runScript(script: str = None, vus: int = 1, duration: str = "1s", envVars: dict = dict(os.environ)):
    logger.info("Running " + script)
    subprocess.check_output([
        "k6",
        "run",
        script,
        "--vus",
        str(vus),
        "--duration",
        str(duration)
      ], 
      stderr=subprocess.DEVNULL,
      env=envVars)
    
