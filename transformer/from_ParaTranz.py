from typing import Any

import json
import os
import yaml


def represent_none(self, _):
    return self.represent_scalar('tag:yaml.org,2002:null', '')


def translate_content(translator: dict[str, str], content: dict[str, Any]):
    translate_chapter(translator, content)


def translate_chapter(translator: dict[str, str], content: dict[str, Any]):
    identifier = content["chapter"]
    if identifier in translator:
        content["text"] = translator[identifier]

    sections = content["sections"]
    for section in sections:
        translate_section(translator, section)


def translate_section(translator: dict[str, str], content: dict[str, Any]):
    identifier = content["section"]
    if identifier in translator:
        content["text"] = translator[identifier]

    if "snippet" in content:
        snippet_identifier = f"{identifier}-snippet"
        if snippet_identifier in translator:
            content["snippet"] = translator[snippet_identifier]

    rules = content["rules"]
    for rule in rules:
        translate_rule(translator, rule)


def translate_rule(translator: dict[str, str], content: dict[str, Any]):
    if "rule" in content:
        identifier = content["rule"]
        if identifier in translator:
            content["text"] = translator[identifier]

        if "examples" in content:
            examples = content["examples"]
            for order, example in enumerate(examples, start=1):
                translate_example(translator, example, identifier, order)
    elif "subsection" in content:
        identifier = content["subsection"]
        if identifier in translator:
            content["text"] = translator[identifier]

        if "examples" in content:
            examples = content["examples"]
            for order, example in enumerate(examples, start=1):
                translate_example(translator, example, identifier, order)

        rules = content["rules"]
        for rule in rules:
            translate_rule(translator, rule)
    # elif "timing_structure" in content:
    #     elements = content["elements"]
    #     for sub_index, element in enumerate(elements, start=1):
    #         parse_element(collector, element, f"{index}{sub_index}.")


# def parse_element(collector: list[dict[str, str]], content: dict[str, Any], index: str):
#     identifier = f"{index}-element"
#     if "text" in content:
#         text = content["text"]
#         write_line(collector, identifier, f"{index} {text}")
#
#     if "elements" in content:
#         elements = content["elements"]
#         for sub_index, element in enumerate(elements, start=1):
#             parse_element(collector, element, f"{index}{sub_index}.")


def translate_example(translator: dict[str, str], content: dict[str, Any], identifier: str, order: int):
    identifier = f"{identifier}-{order}-example"
    if identifier in translator:
        content["text"] = translator[identifier]


def main():
    yaml.add_representer(type(None), represent_none)
    src_folder = "../data/input/"
    dst_folder = "./from_Paratranz/"
    tranz_folder = "./paratranz/"
    filenames = sorted(os.listdir(src_folder))
    for filename in filenames:
        root, ext = os.path.splitext(filename)
        translator: dict[str, str] = dict()
        tranz_filename = os.path.join(tranz_folder, root + ".json")
        if os.path.isfile(tranz_filename):
            with open(tranz_filename, "r", encoding="utf-8") as file:
                translation: list[dict[str, str]] = json.load(file)
                for line in translation:
                    if len(line["translation"]) > 0:
                        translator[line["key"]] = line["translation"]

        src_filename = os.path.join(src_folder, filename)
        with open(src_filename, "r", encoding="utf-8") as file:
            content = yaml.safe_load(file)
            translate_content(translator, content)

        dst_filename = os.path.join(dst_folder, root + ".yaml")
        with open(dst_filename, "w", encoding="utf-8") as file:
            yaml.dump(content, file, sort_keys=False, encoding="utf-8", allow_unicode=True, width=100000)


if __name__ == "__main__":
    main()
