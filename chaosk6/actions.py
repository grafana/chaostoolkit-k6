import subprocess
import os

from chaoslib.deprecation import warn_about_moved_function
from logzero import logger
from pathlib import Path

__all__ = ["run_script", "stress_endpoint"]


def run_script(script_path: str = None, vus: int = 1, duration: str = "1s", log_file: str = None,  debug: bool = False):
    """
    Run an arbitrary k6 script with a configurable amount of VUs and duration.
    Depending on the specs of the attacking machine, possible VU amount may
    vary.
    For a non-customized 2019 Macbook Pro, it will cap around 250 +/- 50.

    Parameters
    ----------
    script_path : str
      Full path to the k6 test script
    vus : int
      Amount of virtual users to run the test with
    duration : str
      Duration, written as a string, ie: `1h2m3s` etc
    log_file: str
      (Optional) Relative path to the file where output should be logged.
    """
    logger.info("Running " + script_path)
    _runScript(
        script=script_path,
        vus=vus,
        duration=duration,
        log_file=log_file,
        debug=debug
    )


def stress_endpoint(endpoint: str = None, vus: int = 1, duration: str = "1s", log_file: str = None, debug: bool = False):
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
      (Optional) Relative path to the file where output should be logged.
    """
    basePath = Path(__file__).parent
    jsPath = str(basePath.parent) + "/chaosk6/scripts"

    try:
        logger.info(
            'Stressing the endpoint "{}" with {} VUs for {}.'.format(
                endpoint, vus, duration
            )
     except OSError as e:
            return print("K6 or other dependent libraries are not installed. Validate you have installed K6 correctly. https://k6.io/docs/getting-started/installation/") 
    )

    env = dict(**os.environ, CHAOS_K6_URL=endpoint)
    r = _runScript(
        script=jsPath + "/single-endpoint.js",
        vus=vus,
        duration=duration,
        log_file=log_file,
        environ=env,
        debug=debug)

    logger.info("Stressing completed.")
    if log_file != None:
        logger.info("Logged K6 output to {}.".format(log_file))
    return r


def _runScript(
    script: str,
    vus: int,
    duration: str,
    log_file: str,
    environ: dict = None,
    debug: bool = False
):

    if not environ:
        environ = dict(os.environ)
    command = [
        "k6",
        "run",
        "-quiet",
        script,
        "--vus", str(vus),
        "--duration",
        str(duration)
    ]

    # Default output to the void
    pipeoutput = subprocess.DEVNULL
    # Use log file location if provided
    if log_file != None:
        pipeoutput = open(log_file, "w")

    with subprocess.Popen(
        command, stderr=subprocess.STDOUT, stdout=None if debug is True else pipeoutput, env=environ
    ) as p:
        return p.returncode is None


def runScript(script_path: str = None, vus: int = 1, duration: str = "1s", debug: bool = False):
    warn_about_moved_function(
        "The action `runScript` is now called `run_script`."
        "Please consider updating your experiments accordingly.")
    return run_script(script_path,  vus, duration)


def stressEndpoint(endpoint: str = None, vus: int = 1, duration: str = "1s", debug: bool = False):
    warn_about_moved_function(
        "The action `stressEndpoint` is now called `stress_endpoint`."
        "Please consider updating your experiments accordingly.")
    return run_script(endpoint,  vus, duration)
