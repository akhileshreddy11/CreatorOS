from app.services.reels.reel_generator import ReelGenerator


def main():

    print("\n===== CREATOROS REEL GENERATION TEST =====\n")

    content = {
        "hook": "Stop manually editing your long-form videos into Shorts.",
        "script": (
            "If you're a creator, you know the grind. "
            "Use AI to identify useful moments from your long-form content, "
            "create short clips, and prepare them for social media."
        ),
        "cta": "Follow CreatorOS for more AI automation workflows."
    }

    generator = ReelGenerator()

    output = generator.create_reel(
        content,
        output_name="test_creatoros_reel.mp4"
    )

    print("\n===== REEL GENERATED =====")
    print("Output:", output)


if __name__ == "__main__":
    main()