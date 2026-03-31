from pydantic import BaseModel
import random

class Observation(BaseModel):
    symptoms: list
    age: int
    history: str

class Action(BaseModel):
    action: str

class Reward(BaseModel):
    value: float

ACTIONS = ["home_care", "visit_doctor", "emergency", "ask_more"]

class HealthEnv:

    def __init__(self):
        self.current_patient = None
        self.task_level = "easy"
        self.steps_taken = 0

    def reset(self, level="easy"):
        self.task_level = level
        self.steps_taken = 0

        if level == "easy":
            patients = [
                {"symptoms": ["fever"], "age": 25, "history": "none", "correct": "home_care"},
                {"symptoms": ["headache"], "age": 30, "history": "none", "correct": "home_care"},
            ]

        elif level == "medium":
            patients = [
                {"symptoms": ["cough"], "age": 40, "history": "none", "correct": "visit_doctor"},
                {"symptoms": ["high fever"], "age": 35, "history": "none", "correct": "visit_doctor"},
            ]

        else:
            patients = [
                {"symptoms": ["chest pain"], "age": 55, "history": "diabetes", "correct": "emergency"},
                {"symptoms": ["severe breathing issue"], "age": 60, "history": "asthma", "correct": "emergency"},
            ]

        self.current_patient = random.choice(patients)

        return Observation(
            symptoms=self.current_patient["symptoms"],
            age=self.current_patient["age"],
            history=self.current_patient["history"]
        )

    def step(self, action):
        self.steps_taken += 1
        correct_action = self.current_patient["correct"]

        # Reward logic
        if action == correct_action:
            reward_value = 1.0
            done = True

        elif action == "ask_more":
            reward_value = 0.3  
            done = False

        else:
            reward_value = -0.5
            done = False


        if self.steps_taken > 3:
            reward_value -= 0.3

        return (
            Observation(
                symptoms=self.current_patient["symptoms"],
                age=self.current_patient["age"],
                history=self.current_patient["history"]
            ),
            Reward(value=reward_value),
            done,
            {"steps": self.steps_taken}
        )

    def state(self):
        return self.current_patient

    def grade(self, action):
        if action == self.current_patient["correct"]:
            return 1.0
        elif action == "ask_more":
            return 0.5  
        else:
            return 0.0