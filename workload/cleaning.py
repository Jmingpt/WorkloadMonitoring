import re
import pandas as pd
from bs4 import BeautifulSoup


def categorize_notes(note):
    note_lower = note.lower()
    if "non" in note_lower:
        return "non-billable"
    elif "billable" in note_lower:
        return "billable"
    else:
        return "non-billable"


def extract_information(files, source_dir):
    columns = ["week", "name", "date", "project", "client", "task", "hours", "notes"]
    raw_data = []
    for member_file in files:
        file_path = f"{source_dir}/{member_file}"
        with open(file_path, 'r') as html_file:
            content = html_file.read()

        soup = BeautifulSoup(content, "html.parser")

        if soup.find("div", class_="team-member-name"):
            name = soup.find("div", class_="team-member-name").find("h2").get_text(strip=True)
            week = soup.find("span", class_=["pds-weight-normal", "js-date"]).get_text(strip=True)

            tables = soup.find_all("table", class_="pds-table")
            for table in tables:
                ddate = table.find("thead").find("tr").find("th").get_text(strip=True)
                rows = table.find_all("tbody")
                for row in rows:
                    if row.find("strong", class_="project"):
                        project = row.find("strong", class_="project").get_text(strip=True)
                        client = row.find("span", class_="client").get_text(strip=True)
                        client = re.sub(r'[(){}\[\]]', '', client).strip()
                        task = row.find("span", class_="task").get_text(strip=True)
                        hours = row.find("td", class_="col-hours").find("strong").get_text(strip=True)
                        try:
                            notes = row.find("span", class_="time-entry-notes").find("p").get_text(separator=' ', strip=True)
                        except AttributeError as e:
                            notes = ""
                        raw_data.append([week, name, ddate, project, client, task, hours, notes])

    data = pd.DataFrame(data=raw_data, columns=columns)
    data["hours"] = data["hours"].astype(float)
    data["billable"] = data["notes"].apply(categorize_notes)
    data = data.drop(['notes'], axis=1)

    return data
