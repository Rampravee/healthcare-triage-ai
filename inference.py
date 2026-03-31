from env import HealthEnv, ACTIONS
import os

env = HealthEnv()

def fallback_agent(obs):
    symptoms = " ".join(obs.symptoms).lower()

    if "chest pain" in symptoms or "breathing" in symptoms:
        return "emergency"
    elif "fever" in symptoms or "headache" in symptoms:
        return "home_care"
    elif "cough" in symptoms:
        return "visit_doctor"
    else:
        return "ask_more"


def get_action(obs):
    api_key = os.getenv("OPENAI_API_KEY")

    if api_key:
        try:
            from openai import OpenAI
            client = OpenAI()

            prompt = f"""
            Patient:
            Symptoms: {obs.symptoms}
            Age: {obs.age}
            History: {obs.history}

            Choose one action from {ACTIONS}.
            Only return action name.
            """

            response = client.chat.completions.create(
                model="gpt-4o-mini",
                messages=[{"role": "user", "content": prompt}]
            )

            action = response.choices[0].message.content.strip()

            if action in ACTIONS:
                return action

        except:
            pass

    return fallback_agent(obs)


total_score = 0

for level in ["easy", "medium", "hard"]:
    obs = env.reset(level)

    action = get_action(obs)

    obs, reward, done, _ = env.step(action)

    score = env.grade(action)
    total_score += score

print("FINAL SCORE:", total_score / 3)