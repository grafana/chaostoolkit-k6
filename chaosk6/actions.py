import subprocess
import os

from logzero import logger
from pathlib import Path

__all__ = ["runScript", "stressEndpoint"]


def runScript(script: str = None, vus: int = 1, duration: str = "1s"):
    logger.info("Running " + script)
    _runScript(script, vus, duration)


def stressEndpoint(endpoint: str = None, vus: int = 1, duration: str = "1s"):
    basePath = Path(__file__).parent
    jsPath = str(basePath.parent) + "/scripts"

    logger.info(
        'Stressing the endpoint "{}" with {} VUs for {}.'.format(
            endpoint, vus, duration
        )
    )

    env = dict(**os.environ, CHAOS_K6_URL=endpoint)
    r = _runScript(jsPath + "/single-endpoint.js", vus, duration, env)
    logger.info("Stressing completed.")
    return r


def _runScript(
    script: str = None,
    vus: int = 1,
    duration: str = "1s",
    envVars: dict = dict(os.environ),
):
    command = ["k6", "run", script, "--vus", str(vus), "--duration", str(duration)]

    with subprocess.Popen(
        command, stderr=subprocess.STDOUT, stdout=subprocess.PIPE, env=envVars
    ) as p:
        try:
            p.wait(3)
        except subprocess.TimeoutExpired:
            logger.error("Stress test timed out")
            return False
        p.communicate()
        return p.returncode == 0
