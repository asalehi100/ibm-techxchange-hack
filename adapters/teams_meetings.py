"""
Microsoft Teams Meeting Adapter

This module provides functionality to integrate with Microsoft Teams through the Graph API
to create online meetings. It handles authentication using MSAL (Microsoft Authentication Library)
and provides methods to create Teams meetings with specified participants.

Dependencies:
    - requests: For making HTTP requests to the Graph API
    - msal: For Microsoft authentication
    - python-dotenv: For loading environment variables

Environment Variables Required:
    - AZURE_CLIENT_ID: The Azure application client ID
    - AZURE_TENANT_ID: The Azure tenant ID

Author: TaskMind AI Team
Date: June 29, 2025
"""

import requests
import msal
import os
from dotenv import load_dotenv
from datetime import datetime, timedelta

load_dotenv()

CLIENT_ID = os.getenv("AZURE_CLIENT_ID")
TENANT_ID = os.getenv("AZURE_TENANT_ID")
AUTHORITY = f"https://login.microsoftonline.com/{TENANT_ID}"
SCOPES = ["https://graph.microsoft.com/.default"]

def acquire_access_token():
    """
    Acquire an access token for Microsoft Graph API using MSAL interactive authentication.
    
    This function creates a public client application and prompts the user for interactive
    authentication to obtain an access token that can be used to make requests to the
    Microsoft Graph API.
    
    Returns:
        str: The access token string that can be used in Authorization headers
        
    Raises:
        Exception: If the access token cannot be obtained from the authentication flow
        
    Note:
        This function requires user interaction as it opens a browser window for authentication.
        The user must have appropriate permissions to access Microsoft Graph APIs.
    """
    app = msal.PublicClientApplication(client_id=CLIENT_ID, authority=AUTHORITY)
    result = app.acquire_token_interactive(scopes=SCOPES)
    if "access_token" in result:
        return result["access_token"]
    raise Exception("Could not obtain access token")

def create_teams_meeting(metadata):
    """
    Create a Microsoft Teams online meeting using the Graph API.
    
    This function creates a Teams meeting with the specified topic and participants.
    It handles authentication, constructs the appropriate API request, and returns
    the meeting join URL.
    
    Args:
        metadata (dict): A dictionary containing meeting information with the following structure:
            - topic (str): The subject/title of the meeting
            - participants_emails (list, optional): List of email addresses for meeting attendees
            
    Returns:
        str: The join URL for the created Teams meeting
        
    Raises:
        Exception: If the access token cannot be obtained
        Exception: If the Teams API request fails (non-201 status code)
        
    Example:
        >>> metadata = {
        ...     "topic": "Project Status Meeting",
        ...     "participants_emails": ["user1@example.com", "user2@example.com"]
        ... }
        >>> join_url = create_teams_meeting(metadata)
        >>> print(join_url)
        https://teams.microsoft.com/l/meetup-join/...
        
    Note:
        - Requires valid Azure credentials configured in environment variables
        - The function uses interactive authentication which may prompt the user
        - Participants will receive meeting invitations if their emails are provided
    """
    access_token = acquire_access_token()

    headers = {
        "Authorization": f"Bearer {access_token}",
        "Content-Type": "application/json"
    }

    payload = {
        "subject": metadata["topic"],
        "participants": {
            "attendees": [
                {"upn": email} for email in metadata.get("participants_emails", [])
            ]
        }
    }

    response = requests.post(
        "https://graph.microsoft.com/v1.0/me/onlineMeetings",
        headers=headers,
        json=payload
    )

    if response.status_code != 201:
        raise Exception(f"Teams API error: {response.status_code} | {response.text}")

    return response.json()["joinUrl"]
