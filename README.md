# IBM TechXchange Hackathon – June 2025

Welcome to our official team repository for **TaskMind AI** — where we transformed a complex enterprise challenge into a powerful, AI-first automation prototype.

---

## Project: TaskMind AI – LLM-Powered Workflow Orchestrator

**TaskMind AI** is a backend-driven AI Workflow Orchestrator that enables enterprise employees to automate internal operations using natural language prompts—without needing UI, portals, or forms.

For this **Hackathon MVP**, we focused on **intelligent meeting scheduling** using Slack, IBM Granite LLM, and Microsoft Teams integration.

---

## Problem Statement

In large-scale organizations, repetitive administrative tasks like scheduling meetings or onboarding employees consume valuable human bandwidth and introduce inefficiencies. These processes lack standardization, are error-prone, and are not scalable in a hybrid/remote-first world.

### Core Issues:

- Manual coordination for meetings
- Time lost in back-and-forth communication
- Fragmented tools that don’t “speak” to each other
- No intelligent system that bridges intent → action

---

## Solution: TaskMind AI

> Enable users to **orchestrate internal workflows via natural language** through a Slack bot interface.\
> The system parses instructions using **IBM Granite (8B Instruct)** and executes them by interfacing with **Microsoft Graph API** to generate Microsoft Teams meeting links.

---

## MVP Workflow: Intelligent Meeting Scheduling via Slack

### 1. **Slack Message** (User Trigger)

> *Example: “Schedule a call with Sai, Arav, Azadeh Salehi, Tharun, and Prasanna on 12 july 2025 at 11am to discuss IBM TechXchange Project Workflow.”*

### 2. **Granite AI Parsing**

- Model: `granite-3-8b-instruct`
- Output:

```json
{
  "participants": ["Sai", "Arav", "Azadeh Salehi", "Tharun", "prasanna"],
  "date": "12-07-2025",
  "time": "11:00 AM",
  "topic": "IBM TechXchange Project Workflow"
}
```

### 3. **Slack Bot Confirmation**

- A Slack bot replies:

```
Detected Meeting Details:
• Topic: IBM TechXchange Project Workflow
• Participants: Sai, Arav, Azadeh Salehi, Tharun, Prasanna
• Schedule on: 12-07-2025, 11:00 AM UTC

📨 Please reply with participants' email addresses (comma-separated) to proceed.
```

### 4. **Email Capture & Teams Link Generation**

- User provides: `sai@taskmind.ai, arav@taskmind.ai, azadehsalehi@taskmind.ai, tharun@taskmind.ai, prasanna@taskmind.ai`
- Bot uses **Microsoft Graph API** to create a **Teams meeting link**

### 5. **Slack Bot Final Output**

```
✅ Meeting Scheduled:
• Topic: IBM TechXchange Project Workflow
• Participants: Sai, Arav, Azadeh Salehi, Tharun, Prasanna
• Schedule on: 12-07-2025, 11:00 AM UTC
🔗 [Join Meeting](https://teams.microsoft.com/l/meetup-join/xyz)
```

---

## 🧠 AI Model & Prompt Configuration

| Setting            | Value                        |
| ------------------ | ---------------------------- |
| Model              | `ibm/granite-3-8b-instruct`  |
| Max Tokens         | 500                          |
| Decoding Method    | Greedy                       |
| Temperature        | 0                            |
| Stop Sequences     | None                         |
| Moderation Enabled | ✅ Granite Guardian, PII, HAP |

---

## Technologies Used

| Component               | Description                              |
| ----------------------- | ---------------------------------------- |
| **IBM Granite AI**      | Instruction-following LLM for parsing    |
| **Slack Bolt SDK**      | Slack event handling and response logic  |
| **Microsoft Graph API** | Teams meeting link generation            |
| **Azure App Reg.**      | OAuth2 + Token handling for Teams access |
| **Python + Dotenv**     | Lightweight orchestration logic          |

---

## Demo Flow

- Intro to the problem
- Natural language message in Slack
- Real-time Granite model parsing
- Slack + Teams workflow automation
- Final confirmation with meeting link
### Watch Demo video of TaskMindAI [here.](https://drive.google.com/file/d/1gVAnuJy-r390XoEMwbPh5qLlyeDuc7gX/view?usp=drive_link)
---

## 📂 Project Folder Highlights

```
├── adapters/
│   ├── granite_instruct.py   # Granite API call & parsing
│   ├── teams_meetings.py     # MS Graph integration
├── slack_bot.py              # Slack socket bot logic
├── config/
│   └── prompt_template.py    # Template prompt for LLM
├── helpers.py                # Date resolution utilities
├── .env                      # Env vars (tokens, secrets)
```

---

## 🌐 Future Scope

This MVP proves viability for a broader **AI Process Automation Platform**:

- Employee onboarding (e.g., AD account creation, LMS assignment)
- Leave approvals / policy workflows
- Calendar availability resolution
- Enterprise integrations: Zoom, Google Meet, Jira, SAP, etc.

---

## 🙌 Team Members

- **Azadeh Salehi**
- **Venkata Sai Praneeth Uppala** 
- **Arav Baboolal** 
- **Mounashree Prasanna** 
- **Tharun Kumar Reddy Yelesam**


---

## 📘 Licensing

> This repository is intended for educational and hackathon demonstration purposes only.\
> All third-party APIs used under fair usage or trial terms.

