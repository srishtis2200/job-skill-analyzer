import pandas as pd
from src.skill_gap_engine_06 import ranked_skill_gap


def main():
    print("=" * 50)
    print("🔍 JOB SKILL ANALYZER")
    print("=" * 50)

    # Load dataset
    try:
        df = pd.read_csv("outputs/week4_market_insights.csv")
    except FileNotFoundError:
        print("❌ Error: dataset not found.")
        return
    except UnicodeDecodeError:
        df = pd.read_csv("outputs/week4_market_insights.csv", encoding="latin1")

    # User input
    user_input = input("\nEnter your skills (comma-separated): ")
    user_skills = [skill.strip().lower() for skill in user_input.split(",") if skill.strip()]

    target_role = input("Enter your target role: ").strip().lower()

    # Run analysis
    try:
        result = ranked_skill_gap(user_skills, target_role, df)

        print("\n📊 SKILL GAP ANALYSIS RESULT")
        print("-" * 50)

        print(result)

    except KeyError:
        print(f"\n❌ Role '{target_role}' not found.")
        print("👉 Try roles like: data analyst, data scientist, etc.")
    except Exception as e:
        print(f"\n❌ Unexpected error: {e}")

    print("\n✅ Analysis Complete!")
    print("=" * 50)


if __name__ == "__main__":
    main()