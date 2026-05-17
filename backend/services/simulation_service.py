from app.agents.simulation_agent import (
    run_retirement_simulation
)

def simulate_retirement(request):

    return run_retirement_simulation(

        current_age=request.current_age,

        retirement_age=request.retirement_age,

        current_corpus=request.current_corpus,

        monthly_investment=request.monthly_investment,

        annual_return=request.annual_return
    )

