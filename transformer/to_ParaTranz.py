from typing import Any

import csv
import os
import yaml


def write_line(collector: list[list[str]], k: str, v: str):
    line = list()
    line.append(k)
    line.append(v)
    line.append("")
    line.append("")
    collector.append(line)


def parse_content(collector: list[list[str]], content: dict[str, Any], index: int):
    parse_chapter(collector, content, f"{index}.")


def parse_chapter(collector: list[list[str]], content: dict[str, Any], index: str):
    identifier = content["chapter"]
    text = content["text"]
    write_line(collector, identifier, f"{index} {text}")
    sections = content["sections"]
    for sub_index, section in enumerate(sections, start=1):
        parse_section(collector, section, f"{index}{sub_index}.")


def parse_section(collector: list[list[str]], content: dict[str, Any], index: str):
    identifier = content["section"]
    text = content["text"]
    write_line(collector, identifier, f"{index} {text}")
    if "snippet" in content:
        snippet = content["snippet"]
        write_line(collector, f"{identifier}-snippet", snippet)

    rules = content["rules"]
    for sub_index, rule in enumerate(rules, start=1):
        parse_rule(collector, rule, f"{index}{sub_index}.")


def parse_rule(collector: list[list[str]], content: dict[str, Any], index: str):
    if "rule" in content:
        identifier = content["rule"]
        text = content["text"]
        write_line(collector, identifier, f"{index} {text}")
        if "examples" in content:
            examples = content["examples"]
            for order, example in enumerate(examples, start=1):
                parse_example(collector, example, identifier, order)
    elif "subsection" in content:
        identifier = content["subsection"]
        text = content["text"]
        write_line(collector, identifier, f"{index} {text}")
        if "examples" in content:
            examples = content["examples"]
            for order, example in enumerate(examples, start=1):
                parse_example(collector, example, identifier, order)

        rules = content["rules"]
        for sub_index, rule in enumerate(rules, start=1):
            parse_rule(collector, rule, f"{index}{chr(ord('a') + sub_index - 1)}.")
    elif "timing_structure" in content:
        elements = content["elements"]
        for sub_index, element in enumerate(elements, start=1):
            parse_element(collector, element, f"{index}{sub_index}.")


def parse_element(collector: list[list[str]], content: dict[str, Any], index: str):
    identifier = f"{index}-element"
    if "text" in content:
        text = content["text"]
        write_line(collector, identifier, f"{index} {text}")

    if "elements" in content:
        elements = content["elements"]
        for sub_index, element in enumerate(elements, start=1):
            parse_element(collector, element, f"{index}{sub_index}.")


def parse_example(collector: list[list[str]], content: dict[str, Any], identifier: str, order: int):
    text = content["text"]
    write_line(collector, f"{identifier}-{order}-example", text)


def main():
    src_folder = "../data/input/"
    dst_folder = "./to_Paratranz/"
    filenames = sorted(os.listdir(src_folder))
    for index, filename in enumerate(filenames, start=1):
        collector = list()
        with open(os.path.join(src_folder, filename), "r") as file:
            content = yaml.safe_load(file)
            parse_content(collector, content, index)

        root, ext = os.path.splitext(filename)
        with open(os.path.join(dst_folder, root + ".csv"), "w", newline="") as file:
            writer = csv.writer(file)
            for line in collector:
                writer.writerow(line)


if __name__ == "__main__":
    main()
