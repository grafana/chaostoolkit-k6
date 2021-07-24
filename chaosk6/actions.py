import subprocess
import os

from chaoslib.deprecation import warn_about_moved_function
from logzero import logger
from pathlib import Path

__all__ = ["run_script", "stress_endpoint"]

default_log_file_path = "k6.log"


def run_script(scriptPath: str = None, vus: int = 1, duration: str = "1s", log_file: str = default_log_file_path):
    """
    Run an arbitrary k6 script with a configurable amount of VUs and duration.
    Depending on the specs of the attacking machine, possible VU amount may
    vary.
    For a non-customized 2019 Macbook Pro, it will cap around 250 +/- 50.

    Parameters
    ----------
    scriptPath : str
      Full path to the k6 test script
    vus : int
      Amount of virtual users to run the test with
    duration : str
      Duration, written as a string, ie: `1h2m3s` etc
    log_file: str
      Relative path to the file where output should be logged. Defaults to "k6.log".
    """
    logger.info("Running " + scriptPath)
    _runScript(scriptPath, vus, duration, log_file)


def stress_endpoint(endpoint: str = None, vus: int = 1, duration: str = "1s", log_file: str = default_log_file_path):
    """
    Stress a single endpoint with a configurable amount of VUs and duration.
    Depending on the specs of the attacking machine, possible VU amount may
    vary.
    For a non-customized 2019 Macbook Pro, it will cap around 250 +/- 50.

    Parameters
    ----------
    endpoint : str
      The URL to the endpoint you want to stress, including the scheme prefix.
    vus : int
      Amount of virtual users to run the test with
    duration : str
      Duration, written as a string, ie: `1h2m3s` etc
    log_file: str
      Relative path to the file where output should be logged. Defaults to "k6.log".
    """
    basePath = Path(__file__).parent
    jsPath = str(basePath.parent) + "/chaosk6/scripts"

    logger.info(
        'Stressing the endpoint "{}" with {} VUs for {}.'.format(
            endpoint, vus, duration
        )
    )

    env = dict(**os.environ, CHAOS_K6_URL=endpoint)
    r = _runScript(jsPath + "/single-endpoint.js",
                   vus, duration, log_file, env)
    logger.info("Stressing completed. Logged output to {}".format(log_file))
    return r


def _runScript(
    script: str,
    vus: int,
    duration: str,
    log_file: str,
    environ: dict = None,
):

    if not environ:
        environ = dict(os.environ)
    command = [
        "k6", "run", script, "--vus", str(vus), "--duration", str(duration)
    ]

    logs = open(log_file, "w")
    with subprocess.Popen(
        command, stderr=subprocess.STDOUT, stdout=logs, env=environ
    ) as p:
        return p.returncode is None


def runScript(scriptPath: str = None, vus: int = 1, duration: str = "1s"):
    warn_about_moved_function(
        "The action `runScript` is now called `run_script`."
        "Please consider updating your experiments accordingly.")
    return run_script(scriptPath,  vus, duration)


def stressEndpoint(endpoint: str = None, vus: int = 1, duration: str = "1s"):
    warn_about_moved_function(
        "The action `stressEndpoint` is now called `stress_endpoint`."
        "Please consider updating your experiments accordingly.")
    return run_script(endpoint,  vus, duration)
