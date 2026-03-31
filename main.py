from env import HealthEnv

env = HealthEnv()

def main():
    obs = env.reset("easy")
    return {
        "symptoms": obs.symptoms,
        "age": obs.age,
        "history": obs.history
    }
