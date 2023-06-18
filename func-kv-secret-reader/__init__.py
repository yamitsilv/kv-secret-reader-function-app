import os
import json
from datetime import datetime
from urllib.parse import urlparse
from azure.identity import DefaultAzureCredential
from azure.keyvault.secrets import SecretClient
import logging
import azure.functions as func


def get_secret_info(secret_name: str, key_vault_uri: str):
    credential = DefaultAzureCredential()
    secret_client = SecretClient(vault_url=key_vault_uri, credential=credential)
    secret = secret_client.get_secret(secret_name)
    date = secret.properties.created_on.strftime("%d/%m/%Y, %H:%M:%S")
    vaultname = (urlparse(key_vault_uri).netloc).split('.')[0]

    response = {
        "KeyVaultName": vaultname,
        "KeyVaultSecretName": secret.name,
        "SecretCreationDate": date,
        "SecretValue": secret.value
    }

    return response


def setup_logging():
    # Configure logging settings
    logging.basicConfig(level=logging.INFO)
    logger = logging.getLogger('azure')
    logger.setLevel(logging.WARNING)
    logger = logging.getLogger('azure.identity')
    logger.setLevel(logging.WARNING)


def main(req: func.HttpRequest) -> func.HttpResponse:
    # Set up logging
    setup_logging()

    # Get the 'name' parameter from the query string or request body
    name = req.params.get('name')
    if not name:
        try:
            req_body = req.get_json()
        except ValueError:
            pass
        else:
            name = req_body.get('name')

    if name:
        try:
            response = []
            for i in range(1, 4):
                key_vault_uri = os.environ.get(f"KeyVaultUri{i}")
                if key_vault_uri:
                    # Retrieve secret information for each Key Vault
                    secret_info = get_secret_info(name, key_vault_uri)
                    response.append(secret_info)

            if response:
                # Return the secret information as JSON
                logging.info("HTTP trigger function executed successfully and presened information in a JSON format.")
                return func.HttpResponse(json.dumps(response, indent=4), status_code=200)
            else:
                # Handle case when response is empty
                return func.HttpResponse(
                    "Something is lost, something is found. You seem lost o_0",
                    status_code=500
                )

        except Exception as e:
            # Handle exceptions during secret retrieval
            logging.error("An error occurred while retrieving secret '%s': %s", name, str(e))
            return func.HttpResponse(
                "Something went wrong o_0",
                status_code=500
            )
    else:
        # Handle case when 'name' parameter is missing
        logging.info("HTTP trigger function executed successfully without a name parameter.")
        return func.HttpResponse(
            "This HTTP triggered function executed successfully. Pass a name in the query string or in the request body for a personalized response.",
            status_code=200
        )