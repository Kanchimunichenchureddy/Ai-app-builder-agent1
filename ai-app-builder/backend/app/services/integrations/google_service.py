from typing import Dict, Any, Optional, List
import requests
import json
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import Flow
from googleapiclient.discovery import build
from ....core.config import settings

class GoogleService:
    """
    Service for handling Google API integrations.
    Supports Google OAuth, Google Drive, Google Calendar, and Google Sheets.
    """
    
    def __init__(self):
        self.client_id = settings.GOOGLE_CLIENT_ID
        self.client_secret = settings.GOOGLE_CLIENT_SECRET
        self.redirect_uri = settings.GOOGLE_REDIRECT_URI
        self.scopes = [
            'https://www.googleapis.com/auth/drive.file',
            'https://www.googleapis.com/auth/calendar',
            'https://www.googleapis.com/auth/spreadsheets',
            'https://www.googleapis.com/auth/userinfo.email',
            'https://www.googleapis.com/auth/userinfo.profile'
        ]
    
    def get_oauth_flow(self) -> Flow:
        """
        Create OAuth flow for Google authentication.
        
        Returns:
            Google OAuth Flow object
        """
        flow = Flow.from_client_config(
            {
                "web": {
                    "client_id": self.client_id,
                    "client_secret": self.client_secret,
                    "auth_uri": "https://accounts.google.com/o/oauth2/auth",
                    "token_uri": "https://oauth2.googleapis.com/token",
                    "redirect_uris": [self.redirect_uri]
                }
            },
            scopes=self.scopes
        )
        flow.redirect_uri = self.redirect_uri
        return flow
    
    async def get_user_info(self, credentials: Dict[str, Any]) -> Dict[str, Any]:
        """
        Get user information from Google.
        
        Args:
            credentials: Google OAuth credentials
            
        Returns:
            Dict containing user information
        """
        try:
            creds = Credentials(
                token=credentials.get('token'),
                refresh_token=credentials.get('refresh_token'),
                token_uri=credentials.get('token_uri'),
                client_id=self.client_id,
                client_secret=self.client_secret,
                scopes=credentials.get('scopes')
            )
            
            service = build('oauth2', 'v2', credentials=creds)
            user_info = service.userinfo().get().execute()
            
            return {
                "success": True,
                "user_id": user_info.get('id'),
                "email": user_info.get('email'),
                "name": user_info.get('name'),
                "picture": user_info.get('picture')
            }
        except Exception as e:
            return {
                "success": False,
                "error": str(e),
                "error_type": "google_api_error"
            }
    
    async def create_google_drive_file(
        self,
        credentials: Dict[str, Any],
        file_name: str,
        content: str,
        mime_type: str = "text/plain"
    ) -> Dict[str, Any]:
        """
        Create a file in Google Drive.
        
        Args:
            credentials: Google OAuth credentials
            file_name: Name of the file to create
            content: Content of the file
            mime_type: MIME type of the file
            
        Returns:
            Dict containing file details
        """
        try:
            creds = Credentials(
                token=credentials.get('token'),
                refresh_token=credentials.get('refresh_token'),
                token_uri=credentials.get('token_uri'),
                client_id=self.client_id,
                client_secret=self.client_secret,
                scopes=credentials.get('scopes')
            )
            
            service = build('drive', 'v3', credentials=creds)
            
            file_metadata = {
                'name': file_name,
                'mimeType': mime_type
            }
            
            media = {
                'body': content
            }
            
            file = service.files().create(
                body=file_metadata,
                media_body=media,
                fields='id, name, mimeType, webViewLink'
            ).execute()
            
            return {
                "success": True,
                "file_id": file.get('id'),
                "file_name": file.get('name'),
                "mime_type": file.get('mimeType'),
                "web_view_link": file.get('webViewLink')
            }
        except Exception as e:
            return {
                "success": False,
                "error": str(e),
                "error_type": "google_drive_error"
            }
    
    async def create_google_sheet(
        self,
        credentials: Dict[str, Any],
        title: str,
        data: Optional[List[List[Any]]] = None
    ) -> Dict[str, Any]:
        """
        Create a Google Sheet.
        
        Args:
            credentials: Google OAuth credentials
            title: Title of the spreadsheet
            data: Optional data to populate the sheet
            
        Returns:
            Dict containing spreadsheet details
        """
        try:
            creds = Credentials(
                token=credentials.get('token'),
                refresh_token=credentials.get('refresh_token'),
                token_uri=credentials.get('token_uri'),
                client_id=self.client_id,
                client_secret=self.client_secret,
                scopes=credentials.get('scopes')
            )
            
            service = build('sheets', 'v4', credentials=creds)
            
            spreadsheet = {
                'properties': {
                    'title': title
                }
            }
            
            spreadsheet = service.spreadsheets().create(
                body=spreadsheet,
                fields='spreadsheetId'
            ).execute()
            
            spreadsheet_id = spreadsheet.get('spreadsheetId')
            
            # If data is provided, populate the sheet
            if data:
                body = {
                    'values': data
                }
                service.spreadsheets().values().update(
                    spreadsheetId=spreadsheet_id,
                    range='A1',
                    valueInputOption='RAW',
                    body=body
                ).execute()
            
            # Get spreadsheet URL
            spreadsheet_url = f"https://docs.google.com/spreadsheets/d/{spreadsheet_id}"
            
            return {
                "success": True,
                "spreadsheet_id": spreadsheet_id,
                "title": title,
                "url": spreadsheet_url
            }
        except Exception as e:
            return {
                "success": False,
                "error": str(e),
                "error_type": "google_sheets_error"
            }
    
    async def create_google_calendar_event(
        self,
        credentials: Dict[str, Any],
        event_data: Dict[str, Any]
    ) -> Dict[str, Any]:
        """
        Create a Google Calendar event.
        
        Args:
            credentials: Google OAuth credentials
            event_data: Event data including summary, start, end, etc.
            
        Returns:
            Dict containing event details
        """
        try:
            creds = Credentials(
                token=credentials.get('token'),
                refresh_token=credentials.get('refresh_token'),
                token_uri=credentials.get('token_uri'),
                client_id=self.client_id,
                client_secret=self.client_secret,
                scopes=credentials.get('scopes')
            )
            
            service = build('calendar', 'v3', credentials=creds)
            
            event = service.events().insert(
                calendarId='primary',
                body=event_data
            ).execute()
            
            return {
                "success": True,
                "event_id": event.get('id'),
                "html_link": event.get('htmlLink'),
                "summary": event.get('summary')
            }
        except Exception as e:
            return {
                "success": False,
                "error": str(e),
                "error_type": "google_calendar_error"
            }
    
    async def search_google_drive_files(
        self,
        credentials: Dict[str, Any],
        query: Optional[str] = None,
        max_results: int = 10
    ) -> Dict[str, Any]:
        """
        Search for files in Google Drive.
        
        Args:
            credentials: Google OAuth credentials
            query: Search query (optional)
            max_results: Maximum number of results to return
            
        Returns:
            Dict containing search results
        """
        try:
            creds = Credentials(
                token=credentials.get('token'),
                refresh_token=credentials.get('refresh_token'),
                token_uri=credentials.get('token_uri'),
                client_id=self.client_id,
                client_secret=self.client_secret,
                scopes=credentials.get('scopes')
            )
            
            service = build('drive', 'v3', credentials=creds)
            
            # Build query
            drive_query = query if query else ""
            
            results = service.files().list(
                q=drive_query,
                pageSize=max_results,
                fields="nextPageToken, files(id, name, mimeType, webViewLink)"
            ).execute()
            
            files = results.get('files', [])
            
            return {
                "success": True,
                "files": [
                    {
                        "id": file.get('id'),
                        "name": file.get('name'),
                        "mime_type": file.get('mimeType'),
                        "web_view_link": file.get('webViewLink')
                    }
                    for file in files
                ]
            }
        except Exception as e:
            return {
                "success": False,
                "error": str(e),
                "error_type": "google_drive_error"
            }