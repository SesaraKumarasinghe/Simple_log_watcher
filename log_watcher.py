from datetime import datetime
from argparse import ArgumentParser
from collections import Counter

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

    # return f"{log_dict["Time"]} | {log_dict["Level"]} | {log_dict["Message"]}"

def filter_by_keyword(log, keyword=""):
    return keyword.lower() in log["Message"].lower()

def filter_by_level(log, level):
    return log["Level"] == level.upper()

def filter_by_date(log,start_date,end_date):
    s_date = datetime.strptime(start_date,"%Y-%m-%d %H:%M:%S")
    e_date = datetime.strptime(end_date,"%Y-%m-%d %H:%M:%S")

    return s_date <= log["Time"] <= e_date

def cli_tool():
        parser = ArgumentParser(
            description="CLI tool for analyzing, filtering log files. more features will be added in the future.")

        parser.add_argument('--filename', '-f', type=str, required=True,
                            help="You must enter a filename/filepath to use the tool(log files only).")
        parser.add_argument('--level', '-l',type=str,
                            help="Enter a level to get logs within a range(optional). levels - ERROR,INFO,WARNING.")
        parser.add_argument("--keyword", "-k", type=str,
                            help="Enter a keyword to get accurate results.")
        parser.add_argument('--countonly','-co',action="store_true",
                            help="Enter this command to only get a count of results available.")
        parser.add_argument("--from",type=str,dest="from_d",
                            help="Enter start date.")
        parser.add_argument("--to",type=str,default=None,dest="to_d",
                            help="Enter end date.")
        parser.add_argument("--stats",action="store_true",
                            help="This gives a full detailed statistic about the given log file.")

        args = parser.parse_args()

        if args.to_d and not args.from_d:
            parser.error("--to requires --from. Please specify --from as well.")

        if args.from_d and not args.to_d:
            args.to_d = datetime.strftime(datetime.now(), "%Y-%m-%d %H:%M:%S")

        count = 0
        level_count = Counter()
        message_count = Counter()
        keyword_count = Counter()

        for raw_line in log_reader(args.filename):
            parsed = log_parser(raw_line)

            if not parsed:
                continue

            if args.from_d and args.to_d:
                if not filter_by_date(parsed, args.from_d, args.to_d):
                    continue

            if args.level:
                if not filter_by_level(parsed, args.level):
                    continue

            if args.keyword:
                if not filter_by_keyword(parsed, args.keyword):
                    continue

            if args.stats:
                level_count[parsed["Level"]] += 1
                message_count[parsed["Message"]] += 1

                for word in parsed["Message"].split():
                    keyword_count[word.lower()] += 1

                continue

            if not args.countonly:
                print(f"{parsed['Time']} | {parsed['Level']} | {parsed['Message']}")
            count += 1

        if args.stats:
            print("=== Statistics ===")
            print(f"Total matching logs: {sum(level_count.values())}\n")

            print("Logs by level:")
            for level, count in level_count.items():
                print(f"  {level}: {count}")

            print("\nTop 5 frequent messages:")
            for msg, count in message_count.most_common(5):
                print(f"  {msg} -> {count}")

            print("\nTop 5 keywords:")
            for word, count in keyword_count.most_common(5):
                print(f"  {word} -> {count}")

        else:
            if count == 0:
                print(f"No matching results found.")

            else:
                print(f"\n{count} results.")

if __name__ == "__main__":
    cli_tool()
