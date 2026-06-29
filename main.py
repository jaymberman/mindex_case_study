from src.pipeline import pipeline

# import argparse
# parser = argparse.ArgumentParser(description="Data warehouse pipeline")

# parser.add_argument(
#     "--refresh-analytics-only",
#     action="store_true",
#     help="Rebuild materialized views"
# )

# args = parser.parse_args()


def main():
    pipeline()

if __name__ == "__main__":
    main()