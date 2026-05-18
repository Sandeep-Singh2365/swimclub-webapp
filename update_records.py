import gazpacho
import json
from pathlib import Path


URL = "https://en.wikipedia.org/wiki/List_of_world_records_in_swimming"
RECORDS = {0,1,3,4}
COURSES = {"LC Men", "LC Women", "SC Men", "SC Women"}
# WHERE = ""
BASE_DIR = Path(__file__).resolve().parent
JSONDATA = BASE_DIR / "records.json"


html = gazpacho.get(URL)
soup = gazpacho.Soup(html)
tables = soup.find("table")
records = {}
for table, course in zip(RECORDS, COURSES):
    records[course] = {}
    for row in tables[table].find("tr")[1:]:
        columns = row.find("td")
        event = columns[0].text
        time = columns[1].text
        if "relay" not in event:
            records[course][event] = time

with open(JSONDATA, "w") as jf:
    json.dump(records, jf)