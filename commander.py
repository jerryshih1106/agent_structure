from openai import OpenAI

class Commander:
    def __init__(self,input_dict):
        self.api_key = input_dict["api_key"]
        self.content = input_dict["content"]

    def start(self) -> str:
        client = OpenAI(
            api_key=self.api_key,  # This is the default and can be omitted
        )
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are a professional prompt engineer. Please break down the input content into step-by-step tasks. If there are no tasks, please reply with 'no action,[reply the input]'."},
                {"role": "user", "content": self.content},
            ],
        )
        return f"{response.choices[0].message.content.strip()}"
