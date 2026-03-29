"""
Placeholder for the audit processing logic.
Implement your Excel processing script here.
"""
import os

import openpyxl
import requests
import pandas as pd

INFOR_CLIENT_ID = os.environ.get("INFOR_CLIENT_ID")
INFOR_CLIENT_SECRET = os.environ.get("INFOR_CLIENT_SECRET")
INFOR_SERVICE_ACCOUNT_ACCESS_KEY = os.environ.get("INFOR_SERVICE_ACCOUNT_ACCESS_KEY")
INFOR_SERVICE_ACCOUNT_SECRET_KEY = os.environ.get("INFOR_SERVICE_ACCOUNT_SECRET_KEY")
INFOR_ION_API_URL = os.environ.get("INFOR_ION_API_URL")
INFOR_SSO_URL = os.environ.get("INFOR_SSO_URL")


def process_excel(file_path: str) -> dict:
    # --- request token ---
    token_url = INFOR_SSO_URL + os.environ.get("INFOR_OAUTH_TOKEN")

    response = requests.post(
        token_url,
        data={
            "grant_type": "password",
            "client_id": INFOR_CLIENT_ID,
            "client_secret": INFOR_CLIENT_SECRET,
            "username": INFOR_SERVICE_ACCOUNT_ACCESS_KEY,
            "password": INFOR_SERVICE_ACCOUNT_SECRET_KEY,
        },
        headers={"Content-Type": "application/x-www-form-urlencoded"},
    )

    response.raise_for_status()  # will throw error if 400/500

    token = response.json()["access_token"]

    print("Token acquired")

    # Process the excel file
    contracts_to_check=pd.read_excel(file_path)
    print(contracts_to_check['WorkingContractID'])


    # TODO: implement audit logic here
    return {"status": "success", "message": "File received — processing placeholder ran successfully.", "data": None}
