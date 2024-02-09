import os.path
import pandas as pd

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

# If modifying these scopes, delete the file token.json.
SCOPES = ["https://www.googleapis.com/auth/spreadsheets"]

# The ID and range of a sample spreadsheet.
SAMPLE_SPREADSHEET_ID = "1bsGdEYP7TZSX1Deb99do54yzN4rjDW0VzFEHCseRwYk"
SAMPLE_RANGE_NAME = "engenharia_de_software!A3:F27"
NEW_RANGE_NAME = "engenharia_de_software!G4:H27"

def main():
    # Load credentials from token.json if available
    creds = None
    if os.path.exists("token.json"):
        creds = Credentials.from_authorized_user_file("token.json", SCOPES)
    
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                "client_secret.json", SCOPES
            )
            creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open("token.json", "w") as token:
            token.write(creds.to_json())

    try:
        # Build the Sheets API service
        service = build("sheets", "v4", credentials=creds)

        # Call the Sheets API to get data from the spreadsheet
        sheet = service.spreadsheets()
        result = sheet.values().get(spreadsheetId=SAMPLE_SPREADSHEET_ID, range=SAMPLE_RANGE_NAME).execute()
        values = result.get("values", [])

        # Convert data to DataFrame
        table = pd.DataFrame(values[1:], columns=values[0])

        # Convert grades to numeric
        table[['P1', 'P2', 'P3']] = table[['P1', 'P2', 'P3']].apply(pd.to_numeric)

        # Calculate the average
        average = (table['P1'] + table['P2'] + table['P3']) / 3

        # Convert absences to numeric
        table['Faltas'] = pd.to_numeric(table['Faltas'])

        # Check if the student has more than 15 absences
        table.loc[table['Faltas'] > 15, 'Status'] = 'Reprovado por Falta'

        # If the student does not have more than 15 absences, then assign the situation based on the average
        table.loc[table['Faltas'] <= 15, 'Status'] = pd.cut(average, 
                                                                bins=[-float('inf'), 50, 70, float('inf')], 
                                                                labels=['Reprovado por Nota', 'Exame Final', 'Aprovado'])

        # Initialize the column for the final approval grade
        table['Final Approval Grade'] = 0

        # Calculate the final approval grade for students in the "Exame Final" situation
        table.loc[table['Status'] == 'Exame Final', 'Final Approval Grade'] = ((100 - average.loc[table['Status'] == 'Exame Final'])).astype(int)

        # Convert DataFrame to values compatible with Google Sheets API
        values_to_update = table[['Status', 'Final Approval Grade']].values.tolist()

        # Update the spreadsheet with the new values
        body = {"values": values_to_update}
        result = sheet.values().update(
            spreadsheetId=SAMPLE_SPREADSHEET_ID,
            range=NEW_RANGE_NAME,
            valueInputOption="RAW",
            body=body,
        ).execute()

    except HttpError as err:
        print(err)


if __name__ == "__main__":
    main()
