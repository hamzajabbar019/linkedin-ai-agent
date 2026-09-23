from google import genai
from config import GEMINI_API_KEY

import time
import json
import re
from pathlib import Path


# =========================================================
# Gemini Client
# =========================================================

client = genai.Client(api_key=GEMINI_API_KEY)


# =========================================================
# Your LinkedIn Profile
# =========================================================

PROFILE = """
I am a Computer Science graduate interested in:

- AI Engineering
- Agentic AI
- Generative AI
- LLMs
- AI Agents
- Python
- FastAPI
- Flask
- REST APIs
- PostgreSQL
- Machine Learning
- Computer Vision
- Flutter
- Web Development
- AI-powered applications

My career direction is AI Engineering + Web Development.

My LinkedIn content goals are:

- Build professional credibility
- Share useful AI knowledge
- Follow modern AI developments
- Share practical software and AI insights
- Attract recruiters and professional opportunities
- Build a genuine technical audience

The content must match my actual technical background.

Do not claim that I personally used a technology unless
the prompt explicitly says so.
"""


# =========================================================
# Topic History
# =========================================================

HISTORY_FILE = Path("posted_topics.json")


def load_posted_topics():
    """Load previously used topic titles."""

    if not HISTORY_FILE.exists():
        return []

    try:
        with open(
            HISTORY_FILE,
            "r",
            encoding="utf-8"
        ) as file:

            data = json.load(file)

            if isinstance(data, list):
                return data

    except Exception as error:

        print(
            f"Could not read topic history: {error}"
        )

    return []


def save_posted_topic(topic):
    """Save a topic after successful generation."""

    posted_topics = load_posted_topics()

    title = topic["title"].strip()

    if title not in posted_topics:
        posted_topics.append(title)

    with open(
        HISTORY_FILE,
        "w",
        encoding="utf-8"
    ) as file:

        json.dump(
            posted_topics,
            file,
            indent=2,
            ensure_ascii=False
        )


def filter_new_topics(topics):
    """Remove topics that have already been used."""

    posted_topics = load_posted_topics()

    new_topics = []

    for topic in topics:

        title = topic["title"].strip()

        if title not in posted_topics:
            new_topics.append(topic)

    return new_topics


# =========================================================
# Find Available Gemini Models
# =========================================================

def get_available_models():

    available = []

    try:

        for model in client.models.list():

            name = getattr(
                model,
                "name",
                ""
            )

            supported_methods = getattr(
                model,
                "supported_actions",
                []
            )

            if (
                name
                and "generateContent"
                in supported_methods
            ):

                available.append(name)

    except Exception as error:

        print(
            f"Could not list Gemini models: {error}"
        )

    return available


# =========================================================
# Choose Gemini Model
# =========================================================

def choose_model():

    available_models = get_available_models()

    if not available_models:

        return "gemini-3.5-flash-lite"

    print(
        "\nAvailable compatible Gemini models:"
    )

    for model in available_models:
        print(f"  - {model}")

    preferred_models = [

        "models/gemini-3.5-flash-lite",

        "models/gemini-3.1-flash-lite",

        "models/gemini-3.5-flash",

        "models/gemini-3.6-flash",

        "models/gemini-3.7-flash",

        "models/gemini-3.8-flash",
    ]

    for preferred in preferred_models:

        if preferred in available_models:

            return preferred

    for model in available_models:

        model_lower = model.lower()

        if (
            "gemini" in model_lower
            and "flash" in model_lower
            and "image" not in model_lower
            and "tts" not in model_lower
            and "transcribe" not in model_lower
        ):

            return model

    return available_models[0]


# =========================================================
# Gemini Request With Retry
# =========================================================

def generate_with_retry(
    prompt,
    max_retries=3,
    model=None
):

    if model is None:
        model = choose_model()

    print(
        f"\nSelected Gemini model: {model}"
    )

    last_error = None

    for attempt in range(
        1,
        max_retries + 1
    ):

        try:

            print(
                f"Attempt {attempt}/{max_retries}..."
            )

            response = client.models.generate_content(

                model=model,

                contents=prompt
            )

            return response

        except Exception as error:

            last_error = error

            print(
                "\nGemini request failed:"
            )

            print(error)

            if attempt < max_retries:

                wait_time = 5 * attempt

                print(
                    f"Waiting {wait_time} seconds "
                    f"before retry..."
                )

                time.sleep(wait_time)

    print(
        "\nGemini request failed after "
        f"{max_retries} attempts."
    )

    raise last_error


# =========================================================
# Select Best Topic
# =========================================================

def select_topic(topics):

    topics_text = ""

    for i, topic in enumerate(
        topics,
        1
    ):

        topics_text += (
            f"{i}. {topic['title']}\n"
            f"Source: {topic['source']}\n"
            f"Published: "
            f"{topic.get('published', 'Unknown')}\n"
            f"Link: {topic['link']}\n\n"
        )

    prompt = f"""
You are an AI content strategist managing my LinkedIn account.

MY PROFESSIONAL PROFILE:

{PROFILE}


FRESH AI TOPICS:

{topics_text}


Choose ONE topic that is most suitable for my LinkedIn profile.

Evaluate topics based on:

1. Relevance to my technical background.
2. Relevance to AI Engineering.
3. Relevance to Agentic AI, Generative AI or LLMs.
4. Value for software developers.
5. Freshness.
6. Potential to create an informative LinkedIn post.
7. Ability to discuss the topic without inventing facts.

Avoid topics that are:

- Purely promotional
- Too generic
- Unrelated to software or AI
- Mainly entertainment
- Repetitive

Return ONLY the number of the selected topic.

Example:

7
"""

    response = generate_with_retry(prompt)

    result = response.text.strip()

    print(
        f"\nAI selected topic number: {result}"
    )

    try:

        selected_number = int(result)

        if (
            selected_number < 1
            or selected_number > len(topics)
        ):

            raise ValueError(
                "Invalid topic number"
            )

        return topics[
            selected_number - 1
        ]

    except (
        ValueError,
        TypeError
    ):

        print(
            "AI returned an invalid topic number."
        )

        print(
            "Using first topic as fallback."
        )

        return topics[0]


# =========================================================
# Generate LinkedIn Post
# =========================================================

def generate_post(topic):

    prompt = f"""
You are my personal LinkedIn content writer.

MY PROFESSIONAL PROFILE:

{PROFILE}


SELECTED TOPIC:

Title:
{topic['title']}

Source:
{topic['source']}

Published:
{topic.get('published', 'Unknown')}

Source Link:
{topic['link']}


Write a professional LinkedIn post about this topic.

Requirements:

- Sound like a real young software/AI professional.
- Use natural human language.
- Keep it around 120-180 words.
- Provide useful information or an insight.
- Explain why the topic matters to developers or AI professionals.
- Do not use fake personal experiences.
- Do not claim that I personally used a technology unless explicitly stated.
- Do not invent facts.
- Do not exaggerate.
- Avoid clickbait.
- Avoid excessive emojis.
- Do not start with "AI is changing the world".
- Do not use generic motivational language.
- Do not mention that you are an AI.
- Do not mention this prompt.
- End with a natural question when appropriate.
- Add a maximum of 3-5 relevant hashtags.

The post should feel suitable for my personal LinkedIn profile,
not like a company advertisement.

Return ONLY the final LinkedIn post.
"""

    response = generate_with_retry(prompt)

    return response.text.strip()


# =========================================================
# Basic Local Quality Checks
# =========================================================

def basic_quality_check(post):

    issues = []

    # Remove hashtags before counting normal words
    words = post.split()

    word_count = len(words)

    # Word count
    if word_count < 100:

        issues.append(
            f"Post is too short ({word_count} words)."
        )

    if word_count > 220:

        issues.append(
            f"Post is too long ({word_count} words)."
        )

    # Hashtag count
    hashtags = re.findall(
        r"#\w+",
        post
    )

    if len(hashtags) > 5:

        issues.append(
            f"Too many hashtags ({len(hashtags)})."
        )

    # Excessive emojis / symbols
    emoji_like = re.findall(
        r"[🔥🚀💡🤖✨🎯📈💻❤️]",
        post
    )

    if len(emoji_like) > 4:

        issues.append(
            "Too many emojis."
        )

    # Obvious AI-style opening
    first_line = post.strip().split("\n")[0].lower()

    if "ai is changing the world" in first_line:

        issues.append(
            "Generic AI opening detected."
        )

    # Empty post
    if not post.strip():

        issues.append(
            "Post is empty."
        )

    return issues


# =========================================================
# AI Quality Checker
# =========================================================

def ai_quality_check(
    topic,
    post
):

    prompt = f"""
You are a strict LinkedIn content quality reviewer.

MY PROFESSIONAL PROFILE:

{PROFILE}


SOURCE TOPIC:

Title:
{topic['title']}

Source:
{topic['source']}

Source Link:
{topic['link']}


GENERATED LINKEDIN POST:

{post}


Review this post before it can be published.

Check:

1. Is it relevant to the source topic?
2. Is it relevant to my professional background?
3. Does it avoid invented personal experience?
4. Does it avoid unsupported claims?
5. Does it sound natural and human?
6. Is it useful to developers or AI professionals?
7. Is it professional for LinkedIn?
8. Does it avoid excessive hype?
9. Does it avoid clickbait?
10. Are there no more than 5 hashtags?
11. Is it approximately 120-180 words?
12. Does it avoid repetitive/generic AI language?

Return ONLY valid JSON in this exact format:

{{
    "approved": true,
    "score": 9,
    "issues": []
}}

Rules:

- approved must be true or false.
- score must be an integer from 1 to 10.
- issues must be a JSON array of short strings.
- If the post is good, use an empty issues array.
- Do not add markdown.
- Do not add explanations outside the JSON.
"""

    response = generate_with_retry(
        prompt
    )

    raw = response.text.strip()

    try:

        # Remove accidental markdown fences
        raw = raw.replace(
            "```json",
            ""
        )

        raw = raw.replace(
            "```",
            ""
        )

        result = json.loads(
            raw.strip()
        )

        return result

    except Exception as error:

        print(
            "\nCould not parse AI quality result:"
        )

        print(error)

        print(
            "Raw response:"
        )

        print(raw)

        return {
            "approved": False,
            "score": 0,
            "issues": [
                "Quality checker returned invalid JSON."
            ]
        }


# =========================================================
# Complete Quality Check
# =========================================================

def check_post_quality(
    topic,
    post
):

    print(
        "\n" + "=" * 60
    )

    print(
        "QUALITY CHECK"
    )

    print(
        "=" * 60
    )

    # -----------------------------------------------------
    # Local checks
    # -----------------------------------------------------

    local_issues = basic_quality_check(
        post
    )

    if local_issues:

        print(
            "\nLocal quality issues:"
        )

        for issue in local_issues:

            print(
                f"  - {issue}"
            )

    else:

        print(
            "\nLocal checks: PASSED"
        )

    # -----------------------------------------------------
    # AI checks
    # -----------------------------------------------------

    print(
        "\nAI quality checker is reviewing the post..."
    )

    ai_result = ai_quality_check(
        topic,
        post
    )

    approved = bool(
        ai_result.get(
            "approved",
            False
        )
    )

    score = ai_result.get(
        "score",
        0
    )

    ai_issues = ai_result.get(
        "issues",
        []
    )

    print(
        f"\nAI quality score: {score}/10"
    )

    if ai_issues:

        print(
            "AI quality issues:"
        )

        for issue in ai_issues:

            print(
                f"  - {issue}"
            )

    else:

        print(
            "AI quality issues: None"
        )

    # -----------------------------------------------------
    # Final decision
    # -----------------------------------------------------

    if local_issues:

        print(
            "\nFINAL QUALITY RESULT: FAILED"
        )

        return False

    if not approved:

        print(
            "\nFINAL QUALITY RESULT: FAILED"
        )

        return False

    if isinstance(score, int):

        if score < 7:

            print(
                "\nFINAL QUALITY RESULT: FAILED"
            )

            return False

    print(
        "\nFINAL QUALITY RESULT: PASSED"
    )

    return True


# =========================================================
# Main Agent
# =========================================================

if __name__ == "__main__":

    print(
        "\n" + "=" * 60
    )

    print(
        "LINKEDIN AI CONTENT AGENT"
    )

    print(
        "=" * 60
    )

    # -----------------------------------------------------
    # 1. Research
    # -----------------------------------------------------

    print(
        "\n[1/4] Collecting fresh AI topics..."
    )

    from research import get_latest_topics

    topics = get_latest_topics()

    if not topics:

        print(
            "\nNo topics were found."
        )

        print(
            "Check your internet connection "
            "or RSS sources."
        )

        exit()

    print(
        f"\nFound {len(topics)} topics "
        f"from RSS feeds."
    )

    # -----------------------------------------------------
    # Remove Previously Used Topics
    # -----------------------------------------------------

    new_topics = filter_new_topics(
        topics
    )

    print(
        f"Found {len(new_topics)} unused topics."
    )

    if not new_topics:

        print(
            "\nAll available topics have "
            "already been used."
        )

        print(
            "No new LinkedIn post will "
            "be generated."
        )

        exit()

    topics = new_topics

    # -----------------------------------------------------
    # 2. Select Topic
    # -----------------------------------------------------

    print(
        "\n[2/4] AI is selecting "
        "the best topic..."
    )

    selected_topic = select_topic(
        topics
    )

    print(
        "\n" + "=" * 60
    )

    print(
        "SELECTED TOPIC"
    )

    print(
        "=" * 60
    )

    print(
        f"Title: "
        f"{selected_topic['title']}"
    )

    print(
        f"Source: "
        f"{selected_topic['source']}"
    )

    print(
        f"Published: "
        f"{selected_topic.get('published', 'Unknown')}"
    )

    print(
        f"Link: "
        f"{selected_topic['link']}"
    )

    # -----------------------------------------------------
    # 3. Generate Post
    # -----------------------------------------------------

    print(
        "\n[3/4] Generating LinkedIn post..."
    )

    MAX_GENERATION_ATTEMPTS = 2

    approved_post = None

    for generation_attempt in range(
        1,
        MAX_GENERATION_ATTEMPTS + 1
    ):

        print(
            f"\nPost generation attempt "
            f"{generation_attempt}/"
            f"{MAX_GENERATION_ATTEMPTS}"
        )

        post = generate_post(
            selected_topic
        )

        print(
            "\n" + "=" * 60
        )

        print(
            "GENERATED LINKEDIN POST"
        )

        print(
            "=" * 60
        )

        print(post)

        # -------------------------------------------------
        # 4. Quality Check
        # -------------------------------------------------

        print(
            "\n[4/4] Checking post quality..."
        )

        quality_passed = check_post_quality(
            selected_topic,
            post
        )

        if quality_passed:

            approved_post = post

            break

        print(
            "\nPost did not pass quality checks."
        )

        if generation_attempt < MAX_GENERATION_ATTEMPTS:

            print(
                "Regenerating the post..."
            )

    # -----------------------------------------------------
    # Final Result
    # -----------------------------------------------------

    if approved_post is None:

        print(
            "\n" + "=" * 60
        )

        print(
            "POST REJECTED"
        )

        print(
            "=" * 60
        )

        print(
            "The generated post did not pass "
            "the quality checks."
        )

        print(
            "Topic was NOT added to "
            "posted_topics.json."
        )

        exit()

    # -----------------------------------------------------
    # Save Topic
    # -----------------------------------------------------

    save_posted_topic(
        selected_topic
    )

    print(
        "\nTopic saved to posted_topics.json"
    )

    # -----------------------------------------------------
    # Final Approved Post
    # -----------------------------------------------------

    print(
        "\n" + "=" * 60
    )

    print(
        "APPROVED LINKEDIN POST"
    )

    print(
        "=" * 60
    )

    print(
        approved_post
    )

    print(
        "=" * 60
    )

    print(
        "\nAgent completed successfully."
    )
