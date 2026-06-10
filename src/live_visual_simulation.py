import numpy as np
import pandas as pd

def generate_live_simulation(
    population_size=120,
    initial_infected=12,
    days=40,
    infection_rate=0.30,
    recovery_rate=0.08,
    death_rate=0.03,
    mask_effect=0.30,
    lockdown_effect=0.20,
    hospital_crowd_effect=0.10,
    infection_radius=6.0,
    seed=42
):
    np.random.seed(seed)

    population_size = int(population_size)
    initial_infected = min(int(initial_infected), population_size)

    x = np.random.uniform(0, 100, population_size)
    y = np.random.uniform(0, 100, population_size)

    status = np.array(["Healthy"] * population_size, dtype=object)
    infected_days = np.zeros(population_size, dtype=int)

    infected_indices = np.random.choice(population_size, initial_infected, replace=False)
    status[infected_indices] = "Infected"

    records = []
    summary = []

    movement_step = max(0.5, 4 * (1 - lockdown_effect))
    effective_infection_rate = infection_rate * (1 - mask_effect)
    effective_infection_rate = min(max(effective_infection_rate, 0), 1)

    for day in range(days + 1):

        for i in range(population_size):
            records.append({
                "day": day,
                "person_id": i,
                "x": x[i],
                "y": y[i],
                "status": status[i]
            })

        summary.append({
            "day": day,
            "healthy": int(np.sum(status == "Healthy")),
            "infected": int(np.sum(status == "Infected")),
            "recovered": int(np.sum(status == "Recovered")),
            "dead": int(np.sum(status == "Dead"))
        })

        if day == days:
            break

        alive = status != "Dead"

        x[alive] = np.clip(
            x[alive] + np.random.uniform(-movement_step, movement_step, np.sum(alive)),
            0,
            100
        )

        y[alive] = np.clip(
            y[alive] + np.random.uniform(-movement_step, movement_step, np.sum(alive)),
            0,
            100
        )

        infected_idx = np.where(status == "Infected")[0]
        healthy_idx = np.where(status == "Healthy")[0]

        new_infections = []

        for h in healthy_idx:
            if len(infected_idx) == 0:
                break

            distances = np.sqrt((x[infected_idx] - x[h]) ** 2 + (y[infected_idx] - y[h]) ** 2)
            close_contacts = np.sum(distances <= infection_radius)

            if close_contacts > 0:
                infection_probability = 1 - (1 - effective_infection_rate) ** close_contacts
                infection_probability = min(infection_probability * (1 + hospital_crowd_effect), 0.95)

                if np.random.random() < infection_probability:
                    new_infections.append(h)

        infected_idx = np.where(status == "Infected")[0]
        infected_days[infected_idx] += 1

        for i in infected_idx:
            if infected_days[i] >= 3:
                adjusted_death_rate = min(death_rate * infected_days[i], 0.25)
                adjusted_recovery_rate = min(recovery_rate * infected_days[i], 0.80)

                r = np.random.random()

                if r < adjusted_death_rate:
                    status[i] = "Dead"
                elif r < adjusted_death_rate + adjusted_recovery_rate:
                    status[i] = "Recovered"

        if new_infections:
            status[new_infections] = "Infected"
            infected_days[new_infections] = 0

    agent_df = pd.DataFrame(records)
    summary_df = pd.DataFrame(summary)

    return agent_df, summary_df
