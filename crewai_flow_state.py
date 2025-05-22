from crewai import Agent, Task
from crewai.flow import Flow, start, listen

# Define the agents
idea_agent = Agent(
    role="Idea Generator",
    goal="Come up with creative Python project ideas",
    backstory="An expert in innovative thinking for tech projects"
)

planner_agent = Agent(
    role="Project Planner",
    goal="Transform abstract ideas into concrete project plans",
    backstory="A senior project planner with years of experience in software delivery"
)

reviewer_agent = Agent(
    role="Reviewer",
    goal="Assess project plans and decide if they are ready",
    backstory="A quality control expert who approves or rejects plans based on clarity and feasibility"
)

class ProjectFlow(Flow):
    max_attempts = 3

    @start()
    def task1_generate_idea(self):
        return Task(
            description="Generate a unique and creative Python project idea.",
            expected_output="A well-described, original Python project idea.",
            agent=idea_agent
        )

    @listen(task1_generate_idea)
    def task2_expand_idea(self, idea):
        return Task(
            description=f"Take this idea and expand it into a detailed project plan: {idea}",
            expected_output="A detailed and structured Python project plan.",
            agent=planner_agent
        )

    @listen(task2_expand_idea)
    def task3_save_plan(self, plan):
        def save_to_file(plan):
            with open("project_plan.txt", "w") as f:
                f.write(plan)
            return "Plan saved to file."
        return save_to_file(plan)

    @listen(task3_save_plan)
    def task4_review_plan(self, _):
        return Task(
            description=(
                "Review the generated project plan in 'project_plan.txt'. "
                "If it is good, reply with 'ACCEPT'. If it needs improvement, reply with 'RETRY'."
            ),
            expected_output="A single word: ACCEPT or RETRY",
            agent=reviewer_agent
        )

    def kickoff(self):
        for attempt in range(self.max_attempts):
            print(f"\n🔁 Attempt {attempt + 1} of {self.max_attempts}")
            super().kickoff()
            decision = self.state.get("task4_review_plan")
            print(f"🧠 Reviewer decision: {decision}")

            if decision and decision.strip().upper() == "ACCEPT":
                print("✅ Flow completed successfully.")
                break
            elif attempt == self.max_attempts - 1:
                print("⚠️ Max attempts reached. Exiting flow.")
                break
            else:
                print("🔄 Retrying from Task 1...")

# Run the flow
if __name__ == "__main__":
    flow = ProjectFlow()
    flow.kickoff()
