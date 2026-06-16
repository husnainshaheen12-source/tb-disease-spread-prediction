import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from pathlib import Path


def run_tb_simulation(
    population_size=500,
    initial_infected=10,
    days=120,
    infection_rate=0.08,
    recovery_rate=0.04,
    death_rate=0.01,
    mask_effect=0.40,
    lockdown_effect=0.30,
    hospital_crowd_effect=0.20,
    seed=42
):
    """
    TB disease spread simulation.

    This function is used by both:
    1. Simulation page
    2. Live Visual Simulation page

    It returns the same final infected, recovered, and dead numbers
    for both pages.
    """

    rng = np.random.default_rng(seed)

    healthy = population_size - initial_infected
    infected = initial_infected
    recovered = 0
    dead = 0
    total_ever_infected = initial_infected

    results = []

    for day in range(days + 1):

        results.append({
            "day": day,
            "healthy": healthy,
            "infected": infected,
            "recovered": recovered,
            "dead": dead,
            "daily_new_infections": 0 if day == 0 else daily_new_infections,
            "daily_recoveries": 0 if day == 0 else daily_recoveries,
            "daily_deaths": 0 if day == 0 else daily_deaths,
            "total_population": population_size,
            "total_ever_infected": total_ever_infected
        })

        if day == days:
            break

        if infected <= 0 or healthy <= 0:
            daily_new_infections = 0
        else:
            intervention_factor = (1 - mask_effect) * (1 - lockdown_effect)
            crowd_factor = 1 + hospital_crowd_effect

            infection_probability = (
                infection_rate *
                (infected / population_size) *
                intervention_factor *
                crowd_factor
            )

            infection_probability = min(max(infection_probability, 0), 0.35)

            daily_new_infections = rng.binomial(healthy, infection_probability)

        if infected <= 0:
            daily_recoveries = 0
            daily_deaths = 0
        else:
            daily_deaths = rng.binomial(infected, min(max(death_rate, 0), 1))

            remaining_infected_after_death = infected - daily_deaths

            if remaining_infected_after_death <= 0:
                daily_recoveries = 0
            else:
                daily_recoveries = rng.binomial(
                    remaining_infected_after_death,
                    min(max(recovery_rate, 0), 1)
                )

        healthy = healthy - daily_new_infections
        infected = infected + daily_new_infections - daily_recoveries - daily_deaths
        recovered = recovered + daily_recoveries
        dead = dead + daily_deaths
        total_ever_infected = total_ever_infected + daily_new_infections

        healthy = max(0, healthy)
        infected = max(0, infected)
        recovered = max(0, recovered)
        dead = max(0, dead)

    return pd.DataFrame(results)


def save_simulation_outputs():
    output_dir = Path("data/processed")
    report_dir = Path("report")

    output_dir.mkdir(parents=True, exist_ok=True)
    report_dir.mkdir(parents=True, exist_ok=True)

    results_df = run_tb_simulation()

    csv_path = output_dir / "tb_simulation_results.csv"
    chart_path = report_dir / "tb_simulation_chart.png"

    results_df.to_csv(csv_path, index=False)

    plt.figure(figsize=(10, 6))
    plt.plot(results_df["day"], results_df["healthy"], label="Healthy")
    plt.plot(results_df["day"], results_df["infected"], label="Infected")
    plt.plot(results_df["day"], results_df["recovered"], label="Recovered")
    plt.plot(results_df["day"], results_df["dead"], label="Dead")
    plt.xlabel("Day")
    plt.ylabel("Number of People")
    plt.title("TB Disease Spread Simulation")
    plt.legend()
    plt.tight_layout()
    plt.savefig(chart_path)
    plt.close()

    print("Simulation completed successfully!")
    print(f"Results saved to: {csv_path}")
    print(f"Chart saved to: {chart_path}")
    print(results_df.tail())


if __name__ == "__main__":
    print("Running TB Disease Spread Simulation...")
    save_simulation_outputs()
