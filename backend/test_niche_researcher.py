import json

from app.agents.niche_researcher import NicheResearcher


def main():

    print("\n===== CREATOROS NICHE RESEARCHER =====\n")

    researcher = NicheResearcher()

    result = researcher.research(
        "Creators, Freelancers, Students and Solopreneurs"
    )

    print(json.dumps(
        result,
        indent=4,
        ensure_ascii=False
    ))


if __name__ == "__main__":
    main()