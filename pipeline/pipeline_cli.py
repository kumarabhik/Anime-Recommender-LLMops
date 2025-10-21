# XOXO/Anime/pipeline/pipeline_cli.py
import argparse, json, sys
from dotenv import load_dotenv
load_dotenv()

from pipeline.pipeline import AnimeRecommendationPipeline

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--query", required=True)
    args = parser.parse_args()

    pipe = AnimeRecommendationPipeline()
    result = pipe.recommend(args.query)
    try:
        print(json.dumps({"recommendations": result}, ensure_ascii=False))
    except Exception:
        print(json.dumps({"recommendations": str(result)}, ensure_ascii=False))

if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        print(str(e), file=sys.stderr)
        sys.exit(1)
