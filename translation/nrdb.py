import os
import csv
import yaml


def main():
    work_folder = os.path.dirname(os.path.abspath(__file__))
    src_filename = os.path.join(work_folder, "../generated/nrdb/nrdb.yaml")
    dst_filename = os.path.join(work_folder, "./nrdb/nrdb.yaml")
    data_filename = os.path.join(work_folder, "./nrdb/nrdb.csv")
    with open(src_filename, "r", encoding="utf-8") as src_file:
        content: dict[str, str] = yaml.safe_load(src_file)

    with open(data_filename, "r", encoding="utf-8") as data_file:
        reader = csv.reader(data_file)
        table: dict[str, str] = dict()
        for k, v in reader:
            table[k] = v
            if ":" in k:
                k1, _ = k.split(":")
                v1, _ = v.split("：")
                table[k1] = v1

    result: dict[str, str] = dict()
    for k, v in content.items():
        if (k in table) and (len(table[k]) > 0):
            result[table[k]] = v
        else:
            result[k] = v

    with open(dst_filename, "w") as dst_file:
        yaml.dump(result, dst_file, sort_keys=False, encoding="utf-8", allow_unicode=True, width=100000, default_style='"')


if __name__ == "__main__":
    main()
