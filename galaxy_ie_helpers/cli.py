import argparse
import json

import galaxy_ie_helpers


def get():
    parser = argparse.ArgumentParser(description="Get datasets from Galaxy.")
    parser.add_argument(
        "-i",
        "--id",
        required=True,
        nargs="+",
        help="The dataset ID/name from your Galaxy history, or a regex pattern to search all files in the history",
    )
    parser.add_argument(
        "-t",
        "--identifier_type",
        choices=["hid", "name", "regex"],
        default="hid",
        help="Type of identifier; use regex when --id contains a pattern",
    )
    parser.add_argument(
        "--history-id",
        default=None,
        help="Galaxy history ID; defaults to the current Galaxy history",
    )
    args = parser.parse_args()

    results = galaxy_ie_helpers.get(args.id, args.identifier_type, args.history_id)
    if isinstance(results, str):
        print(results)
    else:
        print("\n".join(results))


def put():
    parser = argparse.ArgumentParser(description="Put datasets back into Galaxy.")
    parser.add_argument(
        "-p",
        "--filepath",
        required=True,
        nargs="+",
        help="Paths to files that should be uploaded to Galaxy",
    )
    parser.add_argument(
        "-t",
        "--filetype",
        default="auto",
        help="Galaxy file format; defaults to automatic detection",
    )
    parser.add_argument(
        "--history-id",
        default=None,
        help="Galaxy history ID; defaults to the current Galaxy history",
    )
    args = parser.parse_args()

    galaxy_ie_helpers.put(
        args.filepath, file_type=args.filetype, history_id=args.history_id
    )


def get_user_history():
    parser = argparse.ArgumentParser(description="Get the user's Galaxy history.")
    parser.add_argument(
        "--history-id",
        default=None,
        help="Galaxy history ID; defaults to the current Galaxy history",
    )
    args = parser.parse_args()
    history = galaxy_ie_helpers.get_user_history(history_id=args.history_id)
    print(json.dumps(history, indent=2))
