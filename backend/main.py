# =============================================================================
# backend/main.py
# =============================================================================

from fastapi import FastAPI

from backend.routes.simulation import (
    router as simulation_router
)

from backend.routes.analysis import (
    router as analysis_router
)


# =============================================================================
# FASTAPI APP
# =============================================================================

app = FastAPI(

    title="Retirement CoPilot API",

    version="1.0.0",

    description="""
Backend API services for Retirement CoPilot.
"""
)


# =============================================================================
# HEALTH CHECK
# =============================================================================

@app.get("/")
def root():

    return {

        "status":
            "running",

        "service":
            "Retirement CoPilot API"
    }


# =============================================================================
# ROUTES
# =============================================================================

app.include_router(

    simulation_router,

    tags=["Simulation"]
)

app.include_router(

    analysis_router,

    tags=["Analysis"]
)