import gradio as gr
from fastapi import FastAPI
from env import HealthEnv
from gradio.routes import mount_gradio_app

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


def run_simulation():
    env_local = HealthEnv()
    output = ""
    total_score = 0

    for level in ["easy", "medium", "hard"]:
        obs = env_local.reset(level)

        symptoms_text = " ".join(obs.symptoms).lower()

        if any(x in symptoms_text for x in ["chest pain", "breathing", "breath", "heart"]):
            action = "emergency"
        elif "high fever" in symptoms_text:
            action = "visit_doctor"
        elif "fever" in symptoms_text:
            action = "home_care"
        else:
            action = "ask_more"

        obs, reward, done, _ = env_local.step(action)
        score = env_local.grade(action)

        total_score += score

        output += f"## 🏥 LEVEL: {level.upper()}\n\n"
        output += f"**Symptoms:** {obs.symptoms}  \n"
        output += f"**Age:** {obs.age}  \n"
        output += f"**History:** {obs.history}  \n\n"
        output += f"**🤖 AI Decision:** `{action}`  \n"
        output += f"**🎯 Reward:** {reward}  \n"
        output += f"**📊 Score:** {score}  \n"
        output += "\n---\n\n"

    output += f"\n# 🧾 FINAL RESULT\n\n**Average Score:** `{total_score / 3:.2f}`"

    return output

demo = gr.Interface(
    fn=run_simulation,
    inputs=[],
    outputs=gr.Markdown(),
    title="Healthcare Triage AI 🏥",
    description="Simulates AI decision-making for patient triage."
)

app = mount_gradio_app(app, demo, path="/")
