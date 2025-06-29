"""TaskMind AI Slack Bot - Meeting scheduler with natural language processing."""

import os
import re
from slack_bolt import App
from slack_bolt.adapter.socket_mode import SocketModeHandler
from adapters.granite_instruct import parse_meeting_request
from adapters.teams_meetings import create_teams_meeting

# Load environment variables
SLACK_BOT_TOKEN = os.getenv("SLACK_BOT_TOKEN")
SLACK_APP_TOKEN = os.getenv("SLACK_APP_TOKEN")

# Initialize Slack App
app = App(token=SLACK_BOT_TOKEN)

# Session memory to hold state across messages
session_store = {}

@app.event("message")
def handle_user_message(event, say):
    """Handle incoming Slack messages and route them to appropriate actions."""
    user_id = event.get("user")
    text = event.get("text", "").strip().lower()
    thread_ts = event.get("ts")

    # Greeting detection
    if re.match(r"\b(hi|hello|hey )\b", text):
        say(
            channel=event["channel"],
            thread_ts=thread_ts,
            text=f"""👋 Hello <@{user_id}>! 
            Hope you're doing great!
            I'm *TaskMind AI* – your virtual assistant.
I can help you with:
• `Scheduling meetings`
• `Parsing natural language into actions`

Just type something like:
`schedule a meeting on Wednesday at 3pm with Sai to discuss Q2 sales`"""
        )
        return

    # Step 1: Natural language meeting request
    if re.search(r"(schedule|set).*(meeting|call)", text, re.IGNORECASE):
        try:
            parsed = parse_meeting_request(text)

            # Save parsed details (temporarily)
            session_store[user_id] = {
                "topic": parsed["topic"],
                "names": parsed["participants"],
                "date": parsed["date"],
                "time": parsed["time"]
            }

            say(
                channel=event["channel"],
                thread_ts=thread_ts,
                text=f""" *Meeting Request:*
• *Topic:* {parsed['topic']}
• *Participants:* {", ".join(parsed['participants'])}
• *Schedule on:* {parsed['date']}, {parsed['time']}

📨 *Please reply with participants' email addresses (comma-separated) to proceed.*
➡️ Example: `taskmindai@support.com, team@taskmindai.com` """
            )

        except Exception as e:
            say(f"Failed to parse meeting: {str(e)}, please enter details correctly.")
        return

    # Step 2: Email response
    if user_id in session_store or "," in text:
        emails = [e.strip() for e in text.split(",")]
        data = session_store.pop(user_id)
        data["participants_emails"] = emails

        try:
            meeting_link = create_teams_meeting(data)

            say(
                channel=event["channel"],
                thread_ts=event.get("thread_ts", event["ts"]),
                text=f"""✅ *Meeting Scheduled!*
• *Topic:* {data['topic']}
• *Participants:* {", ".join(data['names'])}
🔗 [Join Meeting]({meeting_link})"""
            )
        except Exception as e:
            say(f"❌ Teams meeting creation failed: {str(e)}")
        return

# Start the Slack SocketMode handler
if __name__ == "__main__":
    SocketModeHandler(app, SLACK_APP_TOKEN).start()
