import subprocess
import os

from logzero import logger
from pathlib import Path

__all__ = ["runScript", "stressEndpoint"]


def runScript(scriptPath: str = None, vus: int = 1, duration: str = "1s"):
    """
    Run an arbitrary k6 script with a configurable amount of VUs and duration.
    Depending on the specs of the attacking machine, possible VU amount may vary.
    For a non-customized 2019 Macbook Pro, it will cap around 250 +/- 50.

    Parameters
    ----------
    scriptPath : str
      Full path to the k6 test script
    vus : int
      Amount of virtual users to run the test with
    duration : str
      Duration, written as a string, ie: `1h2m3s` etc
    """
    logger.info("Running " + scriptPath)
    _runScript(scriptPath, vus, duration)


def stressEndpoint(endpoint: str = None, vus: int = 1, duration: str = "1s"):
    """
    Stress a single endpoint with a configurable amount of VUs and duration.
    Depending on the specs of the attacking machine, possible VU amount may vary.
    For a non-customized 2019 Macbook Pro, it will cap around 250 +/- 50.

    Parameters
    ----------
    endpoint : str
      The URL to the endpoint you want to stress, including the scheme prefix.
    vus : int
      Amount of virtual users to run the test with
    duration : str
      Duration, written as a string, ie: `1h2m3s` etc
    """
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
    script: str,
    vus: int,
    duration: str,
    environ: dict = dict(os.environ),
):
    command = ["k6", "run", script, "--vus", str(vus), "--duration", str(duration)]

    with subprocess.Popen(
        command, stderr=subprocess.STDOUT, stdout=subprocess.PIPE, env=environ
    ) as p:
        return p.returncode is None
