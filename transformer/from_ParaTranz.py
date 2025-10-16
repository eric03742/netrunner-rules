from deepdiff import DeepDiff
from pprint import pprint
import os
import yaml


def represent_none(self, _):
    return self.represent_scalar('tag:yaml.org,2002:null', '')


def main():
    yaml.add_representer(type(None), represent_none)
    src_folder = "../data/input/"
    dst_folder = "./yaml/"
    filenames = sorted(os.listdir(src_folder))
    for filename in filenames:
        with open(os.path.join(src_folder, filename), "r") as file:
            content = yaml.safe_load(file)
            root, ext = os.path.splitext(filename)

        with open(os.path.join(dst_folder, root + ".yaml"), "w") as file:
            yaml.dump(content, file, sort_keys=False, encoding="utf-8", allow_unicode=True, width=100000)

        file1 = open(os.path.join(src_folder, filename), "r", encoding="utf-8")
        file2 = open(os.path.join(dst_folder, filename), "r", encoding="utf-8")
        content1 = yaml.safe_load(file1)
        content2 = yaml.safe_load(file2)
        result = DeepDiff(content1, content2)
        pprint(result, indent=2)


if __name__ == "__main__":
    main()
