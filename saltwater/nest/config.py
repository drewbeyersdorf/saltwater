"""Stage I — The Nest.

The mound nest ferments vegetation and its heat sets the clutch's
temperature — which decides what every embryo becomes. Configuration is
not a file the animal reads. It is the womb the animal is made of.

SALTWATER therefore refuses to boot an agent from flags and prayers:
the environment is declared first, validated before life, and every
agent hatched from it carries its imprint.

    from saltwater import Nest

    nest = Nest(medium="estuarine", temperature=31.6, guardrails=True)
    with nest.incubate() as env:
        agent = env.clutch("harvester-07")
"""

from __future__ import annotations

from contextlib import contextmanager
from dataclasses import dataclass

from ..types import Agent, Stage

# The mound ferments between 30°C and 33°C. Outside that range,
# nothing viable hatches. The harness holds the same line.
MIN_VIABLE_TEMP = 30.0
MAX_VIABLE_TEMP = 33.0


class NestError(ValueError):
    """Raised when an environment could not produce a viable agent."""


@dataclass
class Nest:
    """Environment-as-configuration. The womb comes first."""

    medium: str = "estuarine"          # "sovereign" | "pelagic" | "estuarine"
    temperature: float = 31.6          # trait selection happens here
    guardrails: bool = True            # a nest without walls is a buffet
    traits: dict | None = None         # anything else the environment should imprint

    def __post_init__(self) -> None:
        if self.medium not in ("sovereign", "pelagic", "estuarine"):
            raise NestError(
                f"unknown medium {self.medium!r}: "
                "an agent must grow up sovereign (local), pelagic (cloud), or estuarine (both)"
            )
        if not MIN_VIABLE_TEMP <= self.temperature <= MAX_VIABLE_TEMP:
            raise NestError(
                f"temperature {self.temperature}°C is outside the viable mound "
                f"({MIN_VIABLE_TEMP}–{MAX_VIABLE_TEMP}°C): nothing raised there survives"
            )

    @property
    def environment(self) -> dict:
        """The imprint every hatchling carries."""
        return {
            "medium": self.medium,
            "temperature": self.temperature,
            "guardrails": self.guardrails,
            **(self.traits or {}),
        }

    @contextmanager
    def incubate(self):
        """Open the mound. Everything hatched inside is validated first."""
        yield self

    def clutch(self, name: str) -> Agent:
        """Hatch one agent, already shaped by its environment."""
        return Agent(name=name, environment=self.environment, stage=Stage.NEST)
