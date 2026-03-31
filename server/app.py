# trigger update
from fastapi import FastAPI
from env import HealthEnv

def main():
    app = FastAPI()
    env = HealthEnv()

    @app.post("/reset")
    def reset():
        obs = env.reset("easy")
        return {
            "symptoms": obs.symptoms,
            "age": obs.age,
            "history": obs.history
        }

    @app.post("/step")
    def step(action: str):
        obs, reward, done, _ = env.step(action)
        return {
            "symptoms": obs.symptoms,
            "age": obs.age,
            "history": obs.history,
            "reward": reward,
            "done": done
        }

    @app.get("/")
    def home():
        return {"message": "API is running"}

    return app
