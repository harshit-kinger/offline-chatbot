from datetime import datetime
import random

class ChatService:
    def __init__(self):
        self.session_start = datetime.now()
        self.message_count = 0

    def get_response(self, message: str) -> str:
        msg = (message or "").lower().strip()
        self.message_count += 1

        # Time & Date features
        if "time" in msg:
            return f"The current time is {datetime.now().strftime('%H:%M:%S')}"

        if "date" in msg:
            return f"Today's date is {datetime.now().strftime('%d-%m-%Y')}"

        if "day" in msg:
            return f"Today is {datetime.now().strftime('%A')}"

        if "month" in msg:
            return f"The current month is {datetime.now().strftime('%B')}"

        if "year" in msg:
            return f"The current year is {datetime.now().strftime('%Y')}"

        if "full" in msg:
            return f"{datetime.now().strftime('%A, %d %B %Y | %H:%M:%S')}"

        if "quote" in msg:
            return random.choice([
                "Consistency beats intensity.",
                "Build first. Perfect later.",
                "Small steps daily = big results.",
                "Clarity + consistency wins.",
                "Discipline creates freedom."
            ])

        if "help" in msg:
            return ("Try: time, date, day, month, year, full, quote. "
                    "You can also type: bye")

        if msg in ["bye", "exit", "quit"]:
            return "Goodbye! 👋"

        return "I’m an offline chatbot running locally. Try typing 'help' 🙂"