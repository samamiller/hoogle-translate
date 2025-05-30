#!/usr/bin/env python3

import os
import re


def parse_md_table(content):
    """Parse a markdown table and extract data rows."""
    lines = content.strip().split("\n")
    # Filter out header lines and separator lines
    data_rows = []

    for line in lines:
        line = line.strip()
        # Skip header rows, separator rows, and empty lines
        if not line or line.startswith("| :") or line.startswith("|  Language"):
            continue

        # Handle escaped pipe characters
        temp_placeholder = "ESCAPED_PIPE_PLACEHOLDER"
        line_with_placeholders = line.replace("\\|", temp_placeholder)
        raw_columns = line_with_placeholders.split("|")[1:-1]
        columns = [col.strip().replace(temp_placeholder, "|") for col in raw_columns]

        if len(columns) >= 5:  # Ensure we have enough columns
            # Language, Algorithm, ID, Doc Link, Library
            language = columns[0]
            algo = columns[1].strip("`")  # Strip backticks
            algo_id = columns[2]
            library = columns[3].replace("`", "")
            expr = "true" if columns[4] == "Y" else "false"
            doc_link = columns[5][6:-1] if len(columns) > 5 else ""

            # Add to data rows
            data_rows.append(
                {
                    "language": language,
                    "algo": algo,
                    "id": algo_id,
                    "doc": doc_link,
                    "lib": library,
                    "sig": "TODO",
                    "expr": expr,
                }
            )

    return data_rows


def generate_clojure_map(data_rows):
    """Generate a Clojure map from the parsed data."""
    result = "(ns data)\n\n(def by-key-map\n  {\n"

    for row in data_rows:
        language = row["language"]
        algo = row["algo"]
        algo_id = row["id"]
        doc_link = row["doc"]
        library = row["lib"]
        expr = row["expr"]
        sig = row["sig"] if row["sig"] and row["sig"] != "TODO" else "-"

        # Format according to the new file pattern with Language@Algorithm@Library
        result += f'"{language}@{algo}@{library}@{algo_id}" {{:lang "{language}" :algo "{algo}" :lib "{library}" :id {algo_id} :doc "{doc_link}" :sig "{sig}" :expr {expr}}}\n'

    result += "})\n"
    return result


def main():
    # Get the root directory of the project (parent of scripts directory)
    root_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
    algorithms_path = os.path.join(root_dir, "ALGORITHMS.md")
    output_path = os.path.join(root_dir, "src", "data.cljs")

    # Read ALGORITHMS.md file from root directory
    with open(algorithms_path, encoding="utf-8") as file:
        content = file.read()

    # Parse the markdown table
    data_rows = parse_md_table(content)

    # Generate the Clojure map
    clojure_map = generate_clojure_map(data_rows)

    # Write to data.cljs in src directory
    with open(output_path, "w", encoding="utf-8") as outfile:
        outfile.write(clojure_map)

    print(f"Successfully generated {output_path} with {len(data_rows)} entries.")


if __name__ == "__main__":
    main()
