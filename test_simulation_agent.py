from app.agents.simulation_agent import run_retirement_simulation


result = run_retirement_simulation(
    current_age=52,
    retirement_age=60,
    current_corpus=3500000,
    monthly_investment=35000,
    annual_return=0.10
)

print("\n")
print("=" * 100)
print("RETIREMENT SIMULATION RESULT")
print("=" * 100)

for key, value in result.items():

    print(f"\n{key}: {value}")
