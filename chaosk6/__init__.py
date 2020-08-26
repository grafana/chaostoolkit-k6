# -*- coding: utf-8 -*-

from typing import List
from logzero import logger
from chaoslib.discovery.discover import (
    discover_actions,
    discover_probes,
    initialize_discovery_result,
)
from chaoslib.types import Discovery, DiscoveredActivities, Secrets

"""Top-level package for chaostoolkit-k6."""

__all__ = ["discover"]
__version__ = "0.0.1"


def discover(discover_system: bool = True) -> Discovery:
    """
    Discover k6 capabilities offered by this extension.
    """
    logger.info("Discovering capabilities from chaostoolkit-k6")

    discovery = initialize_discovery_result("chaostoolkit-k6", __version__, "k6")
    discovery["activities"].extend(load_exported_activities())
    return discovery


def load_exported_activities() -> List[DiscoveredActivities]:
    activities = []
    activities.extend(discover_actions("chaosk6.generate.actions"))
    activities.extend(discover_probes("chaosk6.probes"))
    return activities
