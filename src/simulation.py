import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from pathlib import Path

# Output paths
PROCESSED_DATA_DIR = Path("data/processed")
REPORT_DIR = Path("report")

PROCESSED_DATA_DIR.mkdir(parents=True, exist_ok=True)
REPORT_DIR.mkdir(parents=True, exist_ok=True)

OUTPUT_CSV = PROCESSED_DATA_DIR / "tb_simulation_results.csv"
OUTPUT_CHART = REPORT_DIR / "tb_simulation_chart.png"


def run_tb_simulation(
    population_size=500,
    initial_infected=10,
    days=60,
    infection_rate=0.08,
    recovery_rate=0.04,
    mask_effect=0.40,
    lockdown_effect=0.30,
    hospital_crowd_effect=0.20,
    seed=42
):
    """
    Simple educational TB spread simulation.

    Status:
    0 = Healthy
    1 = Infected
    2 = Recovered / Treated

    This is a simplified simulation for learning purposes.
    Real TB spread depends on many medical, social, and environmental factors.
    """

    np.random.seed(seed)

    healthy = population_size - initial_infected
    infected = initial_infected
    recovered = 0

    results = []

    for day in range(days + 1):
        results.append({
            "day": day,
            "healthy": healthy,
            "infected": infected,
            "recovered": recovered
        })

        if infected <= 0:
            continue

        # Lockdown reduces contact between people
        effective_contact_rate = infection_rate * (1 - lockdown_effect)

        # Masks reduce transmission
        effective_contact_rate = effective_contact_rate * (1 - mask_effect)

        # Hospital crowding increases transmission risk
        effective_contact_rate = effective_contact_rate * (1 + hospital_crowd_effect)

        # New infections depend on number of infected and healthy people
        possible_new_infections = int(infected * effective_contact_rate * 5)

        new_infections = min(possible_new_infections, healthy)

        # Recovery / treatment
        new_recoveries = int(infected * recovery_rate)
        new_recoveries = min(new_recoveries, infected)

        # Update counts
        healthy -= new_infections
        infected += new_infections
        infected -= new_recoveries
        recovered += new_recoveries

    return pd.DataFrame(results)


def create_simulation_chart(results_df):
    """
    Create and save line chart for simulation.
    """

    plt.figure(figsize=(10, 6))
    plt.plot(results_df["day"], results_df["healthy"], label="Healthy")
    plt.plot(results_df["day"], results_df["infected"], label="Infected")
    plt.plot(results_df["day"], results_df["recovered"], label="Recovered")

    plt.title("TB Disease Spread Simulation")
    plt.xlabel("Day")
    plt.ylabel("Number of People")
    plt.legend()
    plt.grid(True)

    plt.savefig(OUTPUT_CHART)
    plt.close()


if __name__ == "__main__":
    print("Running TB Disease Spread Simulation...")

    simulation_results = run_tb_simulation(
        population_size=500,
        initial_infected=10,
        days=60,
        infection_rate=0.08,
        recovery_rate=0.04,
        mask_effect=0.40,
        lockdown_effect=0.30,
        hospital_crowd_effect=0.20
    )

    simulation_results.to_csv(OUTPUT_CSV, index=False)
    create_simulation_chart(simulation_results)

    print("Simulation completed successfully!")
    print(f"Results saved to: {OUTPUT_CSV}")
    print(f"Chart saved to: {OUTPUT_CHART}")

    print("\nFirst 5 rows:")
    print(simulation_results.head())

    print("\nLast 5 rows:")
    print(simulation_results.tail())
