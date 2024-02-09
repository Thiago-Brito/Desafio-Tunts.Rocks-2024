# Challlenge TuntsRocks

## Prerequisites
1. **Python**: Ensure you have Python installed on your system. You can download it from [python.org](https://www.python.org/downloads/).

2. **Python Packages**: Run the following command in your terminal to install the required Python packages:

```bash
    pip install pandas google-auth google-auth-oauthlib google-api-python-client
```

3. **Google Credentials**: You'll need Google credentials to access the Google Sheets API. Follow the instructions [here](https://developers.google.com/workspace/guides/create-credentials) to obtain the credentials (JSON file) and download the `client_secret.json` file.

4. **Spreadsheet ID and Scope**: Have the ID of the Google Sheets spreadsheet you want to modify handy. Also, ensure that the Google Sheets API scope is set up correctly in the project.

## Running the Script
1. **Download the Code**: Download the provided Python code.

2. **Credentials and Token**: Place the `client_secret.json` file (Google credentials) in the same folder as the Python code. When you run the code for the first time, it will request permission to access the Google Sheets and generate a `token.json` file with the credentials.

3. **Edit the Code**: Open the Python code in a text editor and locate the variables `SAMPLE_SPREADSHEET_ID` and `SAMPLE_RANGE_NAME`. Replace the values of these variables with the ID of your spreadsheet and the range of cells you want to update.

4. **Run the Code**: Execute the Python code in the terminal using the following command:

```bash
    python main.py
```
After successfully running the code, it will update the Google Sheets with the new calculated data. Ensure the spreadsheet has the proper permissions to be accessed by the script.