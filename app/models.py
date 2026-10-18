from pydantic import BaseModel, Field
from enum import Enum

class Environment(str, Enum):
    dev = "dev"
    staging = "staging"
    prod = "prod"

class HealthStatus(str, Enum):
    healthy = "healthy"
    degraded = "degraded"
    down = "down"

class Service(BaseModel):
    name: str = Field(pattern=r"^[a-z0-9-]+$")
    owner: str
    environment: Environment
    version: str
    repo_url: str | None = None
    health: HealthStatus = HealthStatus.healthy

class HealthUpdate(BaseModel):
    health: HealthStatus
