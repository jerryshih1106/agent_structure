class Planner:
    def __init__(self, agent):
        self.agent = agent

    def process_command(self, command: str):
        """process input and excute the mission through the agent"""
        print(f"Received command: {command}")
        if "no action" in command:
            return [command.split("no action,")[1]]
        try:
            result = []
            for chunk in self.agent.stream(command):
                result.append(chunk['messages'][0].content)
            # print(self.agent)
        except Exception as e:
            result = [f"failed to summary the action: {e}"]
        return result
