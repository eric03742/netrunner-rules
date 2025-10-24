from dataclasses import dataclass

import argparse
import os

short_month_to_full = {
  'XX': 'XX',
  '01': '1',
  '02': '2',
  '03': '3',
  '04': '4',
  '05': '5',
  '06': '6',
  '07': '7',
  '08': '8',
  '09': '9',
  '10': '10',
  '11': '11',
  '12': '12',
}

@dataclass
class Config:
  annotated: bool
  generate_nrdb_info: bool
  nrdb_info_folder: str
  effective_year: str
  effective_month: str
  effective_day: str
  php_base_path: str
  output_types: list[str]

  def version_string(self):
    return f'{self.effective_year[2:]}.{self.effective_month}'
  
  def effective_date_str(self):
    if not self.effective_month in short_month_to_full:
      raise Exception(f'Not a valid month string: {self.effective_month}')
    return f'{self.effective_year}年{self.effective_month}月{self.effective_day}日'
  
def parse_output_types(arguments: list[str]):
  lowercase_arguments = list(map(lambda x: x.lower(), arguments))
  if "all" in lowercase_arguments:
    return ["pdf", "web", "opengraph", "json"]
  return list(filter(lambda x: x == "pdf" or x == "web" or x == "opengraph" or x == "json", lowercase_arguments))

def validate_nrdb_info_folder(file: str):
    if not os.path.exists(file):
        raise argparse.ArgumentTypeError(f"{file} does not exist")
    return file

default_config = Config(False, False, "", "XXXX", "XX", "XX", "", ["all"])
