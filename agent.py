"""
Main LinkedIn AI Agent

Flow:

1. Research fresh AI topics
2. Remove previously used topics
3. Select the most relevant topic
4. Generate LinkedIn post
5. Run quality checks
6. Publish to LinkedIn
7. Save topic only after successful publishing
"""

from content import (
    filter_new_topics,
    select_topic,
    generate_post,
    check_post_quality,
    save_posted_topic,
)

from linkedin import publish_post


def run_agent():

    print("\n" + "=" * 60)
    print("LINKEDIN AI AGENT")
    print("=" * 60)

    # --------------------------------------------------
    # STEP 1 — Research
    # --------------------------------------------------

    print("\n[1/5] Researching fresh AI topics...")

    from research import get_latest_topics

    topics = get_latest_topics()

    if not topics:

        print("\nNo AI topics were found.")
        print("Check your internet connection or RSS sources.")

        return

    print(f"Found {len(topics)} topics from RSS feeds.")

    # --------------------------------------------------
    # STEP 2 — Remove duplicates
    # --------------------------------------------------

    print("\n[2/5] Removing previously used topics...")

    new_topics = filter_new_topics(topics)

    print(f"Found {len(new_topics)} unused topics.")

    if not new_topics:

        print("\nNo unused topics are available.")
        print("The agent will not generate a duplicate post.")

        return

    # --------------------------------------------------
    # STEP 3 — Select topic
    # --------------------------------------------------

    print("\n[3/5] Selecting the best topic...")

    selected_topic = select_topic(new_topics)

    print("\n" + "=" * 60)
    print("SELECTED TOPIC")
    print("=" * 60)

    print(f"Title: {selected_topic['title']}")
    print(f"Source: {selected_topic['source']}")
    print(
        f"Published: "
        f"{selected_topic.get('published', 'Unknown')}"
    )
    print(f"Link: {selected_topic['link']}")

    # --------------------------------------------------
    # STEP 4 — Generate + quality check
    # --------------------------------------------------

    print("\n[4/5] Creating LinkedIn post...")

    max_attempts = 2
    approved_post = None

    for attempt in range(1, max_attempts + 1):

        print(
            f"\nGeneration attempt "
            f"{attempt}/{max_attempts}"
        )

        post = generate_post(selected_topic)

        print("\n" + "=" * 60)
        print("GENERATED POST")
        print("=" * 60)

        print(post)

        print("\nRunning quality checks...")

        quality_passed = check_post_quality(
            selected_topic,
            post
        )

        if quality_passed:

            approved_post = post

            break

        print("\nPost failed quality checks.")

        if attempt < max_attempts:

            print(
                "Generating a new version..."
            )

    # --------------------------------------------------
    # Check quality result
    # --------------------------------------------------

    if approved_post is None:

        print("\n" + "=" * 60)
        print("POST REJECTED")
        print("=" * 60)

        print(
            "The post failed the quality checks "
            "after multiple attempts."
        )

        print(
            "The topic was NOT saved as used."
        )

        return

    # --------------------------------------------------
    # STEP 5 — Publish
    # --------------------------------------------------

    print("\n[5/5] Publishing to LinkedIn...")

    result = publish_post(approved_post)

    # --------------------------------------------------
    # Only save topic after successful publishing
    # --------------------------------------------------

    if result.get("success"):

        save_posted_topic(selected_topic)

        print(
            "\nTopic saved to posted_topics.json"
        )

        print("\n" + "=" * 60)
        print("AGENT COMPLETED SUCCESSFULLY")
        print("=" * 60)

        print("\n✅ Post generated")
        print("✅ Quality check passed")
        print("✅ LinkedIn publication successful")
        print("✅ Topic history updated")

    else:

        print("\n" + "=" * 60)
        print("AGENT FAILED")
        print("=" * 60)

        print(
            "\nLinkedIn publishing failed."
        )

        print(
            "The topic was NOT saved as posted."
        )


if __name__ == "__main__":
    run_agent()
