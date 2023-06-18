# Azure Function App - Key Vault Secret Reader

This Azure Function App is designed to read secrets from multiple Azure Key Vaults. It provides a simple HTTP trigger that accepts a secret name as a parameter and retrieves the secret from the specified Key Vaults. The retrieved secret information includes the Key Vault name, secret name, creation date, and secret value.

## Prerequisites

Before deploying and running the Azure Function App, ensure you have the following:

- Azure subscription
- Azure Key Vaults created with the secrets you want to access
- Azure Function App created

## Deployment

1. Clone or download this repository.

2. Configure the Azure Function App settings:
   - Set the environment variables for each Key Vault's URI:
     - `KeyVaultUri1`: URI of the first Key Vault
     - `KeyVaultUri2`: URI of the second Key Vault
     - `KeyVaultUri3`: URI of the third Key Vault
   - Ensure the Azure Function App has the necessary permissions to access the Key Vaults.

3. Deploy the Azure Function App:
   - Deploy the function code and dependencies to your Azure Function App.
   - Ensure the `__init__.py`, `readsecrets.py`, `function.json`, and `requirements.txt` files are included in the deployment.
   - Set up the appropriate triggers and bindings in the Azure Function App configuration.

## Usage

The Azure Function App exposes a simple HTTP trigger to retrieve secret information from the Key Vaults.

HTTP Trigger Endpoint:
https://<function-app-name>.azurewebsites.net/api/KeyVaultSecret?name={secret_name}

vbnet
Copy code

- Replace `<function-app-name>` with the name of your Azure Function App.
- Replace `{secret_name}` with the name of the secret you want to retrieve.

The function will loop through the configured Key Vaults (as specified by the environment variables) and retrieve the secret information if it exists. The response will include the Key Vault name, secret name, creation date, and secret value.
