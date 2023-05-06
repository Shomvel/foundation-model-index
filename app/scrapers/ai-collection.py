from enum import Enum, auto
import pandas as pd


class LineType(Enum):
    CATEGORY = auto()
    HEADER = auto()
    FORMAT = auto()
    ENTRY = auto()


def classify_line(line):
    if line.startswith("##"):
        return LineType.CATEGORY
    elif line.startswith("| Name"):
        return LineType.HEADER
    elif line.startswith("|---"):
        return LineType.FORMAT
    elif line.startswith("| ["):
        return LineType.ENTRY
    else:
        return None


data = []
current_category = None

with open("ai-collection.md", "r", encoding="utf-8") as file:
    for line in file:
        line_type = classify_line(line)

        if line_type == LineType.CATEGORY:
            current_category = line[3:].strip()
        elif line_type == LineType.ENTRY:
            name, title, description, _ = map(str.strip, line.split('|')[1:-1])
            name = name.split("]")[0].split("[")[1]
            if description.strip() == ".":
                description = title
                if title.strip() == ".":
                    continue
            data.append({
                "category": current_category,
                "name": name,
                "description": description
            })

df = pd.DataFrame(data)
df.to_csv("ai-collection.csv", index=False)
