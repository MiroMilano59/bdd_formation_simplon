import urllib.parse
import os
from dotenv import load_dotenv
load_dotenv()

def get_connection_uri():

    # Read URI parameters from the environment
    dbhost = os.getenv('DBHOST')
    dbname = os.getenv('DBNAME')
    dbuser = urllib.parse.quote(os.getenv('DBUSER'))
    sslmode = os.getenv('SSLMODE') # dans la doc SSLMODE=require
    password = urllib.parse.quote(os.getenv('PASSWORD')) # Pour pouvoir utiliser des mot de pass avec des caractères spéc

    # Use passwordless authentication via DefaultAzureCredential.
    # IMPORTANT! This code is for demonstration purposes only. DefaultAzureCredential() is invoked on every call.
    # In practice, it's better to persist the credential across calls and reuse it so you can take advantage of token
    # caching and minimize round trips to the identity provider. To learn more, see:
    # https://github.com/Azure/azure-sdk-for-python/blob/main/sdk/identity/azure-identity/TOKEN_CACHING.md 
    # credential = DefaultAzureCredential()

    # Call get_token() to get a token from Microsft Entra ID and add it as the password in the URI.
    # Note the requested scope parameter in the call to get_token, "https://ossrdbms-aad.database.windows.net/.default".
    # password = credential.get_token("https://ossrdbms-aad.database.windows.net/.default").token

    db_uri = f"postgresql://{dbuser}:{password}@{dbhost}/{dbname}?sslmode={sslmode}"
    return db_uri