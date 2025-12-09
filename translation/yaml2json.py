from typing import Any

import json
import os
import yaml


def write_line(collector: list[dict[str, str]], k: str, v: str):
    rule = {
        "key": k,
        "original": v,
        "translation": ""
    }
    collector.append(rule)


def parse_content(collector: list[dict[str, str]], content: dict[str, Any], index: int):
    parse_chapter(collector, content, f"{index}.")


def parse_chapter(collector: list[dict[str, str]], content: dict[str, Any], index: str):
    identifier = content["chapter"]
    text = content["text"]
    write_line(collector, identifier, f"{index} {text}")
    sections = content["sections"]
    for sub_index, section in enumerate(sections, start=1):
        parse_section(collector, section, f"{index}{sub_index}.")


def parse_section(collector: list[dict[str, str]], content: dict[str, Any], index: str):
    identifier = content["section"]
    text = content["text"]
    write_line(collector, identifier, f"{index} {text}")
    if "snippet" in content:
        snippet = content["snippet"]
        write_line(collector, f"{identifier}-snippet", snippet)

    if "toc_entry" in content:
        toc = content["toc_entry"]
        write_line(collector, f"{identifier}-toc", toc)

    rules = content["rules"]
    for sub_index, rule in enumerate(rules, start=1):
        parse_rule(collector, rule, f"{index}{sub_index}.")


def parse_rule(collector: list[dict[str, str]], content: dict[str, Any], index: str):
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
        
        if "snippet" in content:
            snippet = content["snippet"]
            write_line(collector, f"{identifier}-snippet", snippet)

        rules = content["rules"]
        for sub_index, rule in enumerate(rules, start=1):
            parse_rule(collector, rule, f"{index}{chr(ord('a') + sub_index - 1)}.")
    elif "timing_structure" in content:
        elements = content["elements"]
        for sub_index, element in enumerate(elements, start=1):
            parse_element(collector, element, f"{index}{sub_index}.")


def parse_element(collector: list[dict[str, str]], content: dict[str, Any], index: str):
    identifier = f"{index}-element"
    if "text" in content:
        text = content["text"]
        write_line(collector, identifier, f"{index} {text}")

    if "elements" in content:
        elements = content["elements"]
        for sub_index, element in enumerate(elements, start=1):
            parse_element(collector, element, f"{index}{sub_index}.")


def parse_example(collector: list[dict[str, str]], content: dict[str, Any], identifier: str, order: int):
    identifier = f"{identifier}-{order}-example"
    text = content["text"]
    write_line(collector, identifier, text)


def main():
    work_folder = os.path.dirname(os.path.abspath(__file__))
    src_folder = os.path.join(work_folder, "../data/input/")
    dst_folder = os.path.join(work_folder, "./json/")
    trans_folder = os.path.join(work_folder, "./paratranz/")
    filenames = sorted(os.listdir(src_folder))
    for index, filename in enumerate(filenames, start=1):
        root, ext = os.path.splitext(filename)
        collector: list[dict[str, str]] = list()
        src_filename = os.path.join(src_folder, filename)
        with open(src_filename, "r", encoding="utf-8") as file:
            content = yaml.safe_load(file)
            parse_content(collector, content, index)

        trans_filename = os.path.join(trans_folder, root + ".json")
        if os.path.isfile(trans_filename):
            with open(trans_filename, "r", encoding="utf-8") as file:
                entries: list[dict[str, str]] = json.load(file)
                oracle: dict[str, str] = dict()
                locale: dict[str, str] = dict()
                for line in entries:
                    oracle[line["key"]] = line["original"]
                    locale[line["key"]] = line["translation"]

                for line in collector:
                    if (line["key"] in oracle) and (line["original"] == oracle[line["key"]]):
                        line["translation"] = locale[line["key"]]

        dst_filename = os.path.join(dst_folder, root + ".json")
        with open(dst_filename, "w", encoding="utf-8") as file:
            json.dump(collector, file, ensure_ascii=False, indent=4)

        print(f"Generated: {root}.json!")


if __name__ == "__main__":
    main()
