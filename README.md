# 🤖 LinkedIn AI Agent

An AI-powered automation agent that helps research topics, generate LinkedIn posts, avoid repetitive content, and publish posts automatically through LinkedIn.

The main goal of this project is to explore how **AI agents, APIs, automation, and GitHub Actions** can work together to automate a real-world content workflow.

## ✨ What This Project Does

The LinkedIn AI Agent handles the content workflow from topic research to publishing.

### 🔄 Workflow

```text
Research Topics
      ↓
Select Relevant Topic
      ↓
Check Previous Topics
      ↓
Generate LinkedIn Post
      ↓
Content Validation
      ↓
Publish to LinkedIn
      ↓
Save Topic History
      ↓
Sync History Back to GitHub
```

The agent keeps track of previously used topics so that future runs can avoid generating repetitive content.

## 🚀 Features

* 🔎 **AI Topic Research** — Finds potential topics for LinkedIn content.
* ✍️ **AI Content Generation** — Creates LinkedIn posts based on selected topics.
* ♻️ **Duplicate Topic Prevention** — Checks previously used topics before selecting new content.
* 🔗 **LinkedIn Integration** — Publishes generated posts through the LinkedIn API.
* 🔐 **LinkedIn Authentication** — Handles LinkedIn authentication and access tokens.
* 🧠 **Topic History** — Stores previously posted topics in `posted_topics.json`.
* ⚙️ **GitHub Actions Automation** — Runs the agent automatically on a scheduled workflow.
* 🔄 **Topic History Synchronization** — Updates the topic history and commits changes back to the repository.
* ▶️ **Manual Workflow Execution** — The GitHub Actions workflow can also be triggered manually.

## 🛠️ Technologies Used

* **Python**
* **AI / LLM APIs**
* **LinkedIn API**
* **GitHub Actions**
* **Git & GitHub**
* **JSON**
* **Python Virtual Environment**

## 📁 Project Structure

```text
linkedin-ai-agent/
│
├── .github/
│   └── workflows/
│       └── ...
│
├── agent.py
├── config.py
├── content.py
├── linkedin.py
├── linkedin_auth.py
├── posted_topics.json
├── research.py
├── requirements.txt
├── .gitignore
└── README.md
```

### Main Files

| File                 | Purpose                                       |
| -------------------- | --------------------------------------------- |
| `agent.py`           | Main agent workflow and orchestration         |
| `research.py`        | Topic research and selection                  |
| `content.py`         | LinkedIn post generation and content handling |
| `linkedin.py`        | LinkedIn API integration and publishing       |
| `linkedin_auth.py`   | LinkedIn authentication functionality         |
| `config.py`          | Configuration and environment settings        |
| `posted_topics.json` | Stores previously used/post topics            |
| `.github/workflows/` | Automated GitHub Actions workflows            |
| `requirements.txt`   | Python dependencies                           |

## ⚙️ Setup

### 1. Clone the Repository

```bash
git clone https://github.com/hamzajabbar019/linkedin-ai-agent.git

cd linkedin-ai-agent
```

### 2. Create a Virtual Environment

```bash
python3 -m venv venv
```

Activate it:

**Linux / macOS**

```bash
source venv/bin/activate
```

**Windows**

```bash
venv\Scripts\activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Configure Environment Variables

Create a `.env` file and add the required credentials:

```env
GEMINI_API_KEY=your_gemini_api_key
LINKEDIN_ACCESS_TOKEN=your_linkedin_access_token
```

## 🔐 GitHub Actions

The project can run automatically using GitHub Actions.

The workflow is configured to run on:

```text
Monday
Wednesday
Friday
```

at:

```text
14:00 UTC
```

which corresponds to:

```text
19:00 Pakistan Standard Time
```

The workflow uses GitHub repository secrets for authentication.

Required secrets:

```text
GEMINI_API_KEY
LINKEDIN_ACCESS_TOKEN
```

The workflow also has permission to update the repository's topic history after a successful run.

## ▶️ Running Locally

After configuring the environment variables, the agent can be run locally with:

```bash
python agent.py
```

The agent will execute the configured workflow, including topic research, content generation, topic-history checking, and LinkedIn publishing.

## 📌 Topic History

The project uses:

```text
posted_topics.json
```

to keep track of topics that have already been used.

This helps the agent avoid repeatedly generating posts around the same topic.

The topic history is also synchronized back to GitHub when the automated workflow runs.

## 🔒 Security

Sensitive credentials should always be stored as environment variables or GitHub Secrets.

Do **not** add the following to Git:

```text
.env
API keys
Access tokens
Private credentials
```

The repository's `.gitignore` is used to help prevent sensitive files from being committed.

## 🎯 Why I Built This

I built this project to learn how AI can be used for practical automation rather than only for chat-based applications.

While building it, I wanted to understand how different pieces work together:

* AI-generated content
* API integrations
* Authentication
* Automation
* GitHub Actions
* Data persistence
* Scheduled workflows

It started as a simple idea — **automate my LinkedIn posting process** — and became a practical project for learning how to build and maintain an AI-powered workflow.

## 📈 Future Improvements

Some areas I may continue improving include:

* Better topic research
* More advanced content quality checks
* Improved topic similarity detection
* More flexible posting schedules
* Better analytics and logging
* Support for additional content formats

## 👨‍💻 Author

**Hamza Jabbar**

Computer Science Graduate | Software Developer | AI & Automation Enthusiast

GitHub:
https://github.com/hamzajabbar019

LinkedIn:
https://www.linkedin.com/in/hamzajabbar019/

## ⭐ Project

If you find this project interesting, feel free to explore the repository, give it a ⭐, or use the ideas for your own automation projects.

**Repository:**
https://github.com/hamzajabbar019/linkedin-ai-agent
