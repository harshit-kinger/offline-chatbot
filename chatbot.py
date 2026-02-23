import json
import random
from datetime import datetime


class OfflineChatbot:
    def __init__(self, response_file):
        self.responses = self.load_responses(response_file)
        self.session_start = datetime.now()
        self.message_count = 0

    def load_responses(self, file_path):
        with open(file_path, "r") as file:
            return json.load(file)

    def log_chat(self, user_input, bot_response):
        with open("chat_history.txt", "a") as file:
            file.write(f"{datetime.now()} | You: {user_input}\n")
            file.write(f"{datetime.now()} | Bot: {bot_response}\n\n")

    def get_time_based_greeting(self):
        hour = datetime.now().hour
        if hour < 12:
            return "Good Morning!"
        elif hour < 17:
            return "Good Afternoon!"
        else:
            return "Good Evening!"

    def get_response(self, user_input):
        user_input = user_input.lower()
        self.message_count += 1

        # Built-in features
        if "time" in user_input:
            return f"The current time is {datetime.now().strftime('%H:%M:%S')}"

        if "date" in user_input:
            return f"Today's date is {datetime.now().strftime('%d-%m-%Y')}"

        if "day" in user_input:
            return f"Today is {datetime.now().strftime('%A')}"

        if "month" in user_input:
            return f"The current month is {datetime.now().strftime('%B')}"

        if "year" in user_input:
            return f"The current year is {datetime.now().strftime('%Y')}"

        if "full" in user_input:
            return f"Full date and time: {datetime.now().strftime('%A, %d %B %Y | %H:%M:%S')}"

        if "greet" in user_input:
            return self.get_time_based_greeting()

        if "quote" in user_input:
            quotes = [
                "Consistency beats intensity.",
                "Small improvements daily lead to big results.",
                "Build first. Perfect later.",
                "Discipline creates freedom.",
                "Stay curious. Stay building."
            ]
            return random.choice(quotes)

        if "calculate" in user_input:
            try:
                expression = user_input.replace("calculate", "")
                result = eval(expression)
                return f"The result is {result}"
            except:
                return "Invalid calculation format. Try: calculate 5 + 3"

        if "session" in user_input:
            duration = datetime.now() - self.session_start
            return f"This session has been running for {duration.seconds} seconds and {self.message_count} messages exchanged."

        # JSON-based intent matching
        for intent in self.responses.values():
            for keyword in intent["keywords"]:
                if keyword in user_input:
                    return intent["response"]

        return "I'm not sure how to respond to that yet."

    def run(self):
        print("🤖 Advanced Offline Chatbot Initialized")
        print("Type 'bye' to exit.\n")

        while True:
            user_input = input("You: ")

            response = self.get_response(user_input)
            print("Bot:", response)

            self.log_chat(user_input, response)

            if user_input.lower() in ["bye", "exit", "quit"]:
                print("Bot: Goodbye! Session ended.")
                break


if __name__ == "__main__":
    bot = OfflineChatbot("responses.json")
    bot.run()