import json

from app.agents.niche_researcher import NicheResearcher


def main():

    print("\n===== CREATOROS NICHE RANKING =====\n")

    researcher = NicheResearcher()

    result = researcher.research(
        audience="Creators, Freelancers, Students and Solopreneurs"
    )

    print(json.dumps(
        result,
        indent=2,
        ensure_ascii=False
    ))


if __name__ == "__main__":
    main()