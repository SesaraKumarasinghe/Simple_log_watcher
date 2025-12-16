from datetime import datetime
from argparse import ArgumentParser, Namespace

def log_reader(path):
    with open(path, 'r', encoding='utf-8') as f:
        for line in f:
            yield line.strip()

def log_parser(log):
    parts = log.split(" - ")

    if len(parts) != 3:
        return None

    try:
        timestamp = datetime.strptime(parts[0], '%Y-%m-%d %H:%M:%S')

    except ValueError:
        return None

    return {
        "Time": timestamp,
        "Level": parts[1],
        "Message": parts[2]
    }

def filter_by_keyword(log, keyword=""):
    return keyword.lower() in log["Message"].lower()

def filter_by_level(log, level):
    return log["Level"] == level

def filter_by_lvl_key(log, level, keyword=""):
    return log["Level"] == level and keyword.lower() in log["Message"].lower()

def cli_tool():
        parser = ArgumentParser(
            description="CLI tool for analyzing, filtering log files. more features will be added in the future.")

        parser.add_argument('--filename', '-f', type=str, required=True,
                            help="You must enter a filename/filepath to use the tool(log files only).")
        parser.add_argument('--level', '-l', choices=['ERROR', 'INFO', 'WARNING'],
                            help="Please only use capitalized values for each level.")
        parser.add_argument("--keyword", "-k", type=str, help="Enter a keyword to get accurate results.")

        args = parser.parse_args()

        for raw_line in log_reader(args.filename):
            parsed = log_parser(raw_line)

            if not parsed:
                continue

            if args.level and args.keyword:
                if not filter_by_lvl_key(parsed, args.level, args.keyword):
                    continue

            if args.level:
                if not filter_by_level(parsed, args.level):
                    continue

            if args.keyword:
                if not filter_by_keyword(parsed, args.keyword):
                    continue

            print(parsed)

if __name__ == "__main__":
    cli_tool()
