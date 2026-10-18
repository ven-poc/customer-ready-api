from fastapi import FastAPI, HTTPException
from .models import Service, Environment, HealthUpdate

app = FastAPI(title="Service Inventory")
db: dict[str, Service] = {}  # swap for Postgres later via DATABASE_URL

@app.get("/health")
def liveness():
    return {"status": "ok"}

@app.get("/ready")
def readiness():
    return {"status": "ready"}  # later: check DB connectivity here

@app.post("/services", status_code=201)
def register(service: Service):
    if service.name in db:
        raise HTTPException(409, "service already registered")
    db[service.name] = service
    return service

@app.get("/services")
def list_services(environment: Environment | None = None):
    services = list(db.values())
    if environment:
        services = [s for s in services if s.environment == environment]
    return services

@app.get("/services/{name}")
def get_service(name: str):
    if name not in db:
        raise HTTPException(404, "service not found")
    return db[name]

@app.put("/services/{name}/health")
def update_health(name: str, update: HealthUpdate):
    if name not in db:
        raise HTTPException(404, "service not found")
    db[name].health = update.health
    return db[name]
