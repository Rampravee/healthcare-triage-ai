from fastapi import FastAPI
from env import HealthEnv
import uvicorn

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

# 🔥 THIS IS THE MISSING PART
if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=7860)
