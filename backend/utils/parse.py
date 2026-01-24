from typing import Dict, List

def parse_validation_errors(errors: List[Dict]):
  parsed_error = {}
  for err in errors:
    value = " ".join(map(str, err["loc"][1:]))
    message = err.msg
    parsed_error[value] = message
  
  return parsed_error