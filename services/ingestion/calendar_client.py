"""
Google Calendar API Client
Handles OAuth and calendar event fetching/writing
"""
from typing import List, Dict, Optional
from datetime import datetime, timedelta
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import Flow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
import os


class GoogleCalendarClient:
    """Client for interacting with Google Calendar API"""
    
    SCOPES = ['https://www.googleapis.com/auth/calendar.readonly',
              'https://www.googleapis.com/auth/calendar.events']
    
    def __init__(self, credentials: Optional[Credentials] = None):
        """
        Initialize Google Calendar client
        
        Args:
            credentials: OAuth2 credentials (if already authenticated)
        """
        self.credentials = credentials
        self.service = None
        if credentials:
            self.service = build('calendar', 'v3', credentials=credentials)
    
    @classmethod
    def create_flow(cls, client_id: str, client_secret: str, redirect_uri: str):
        """
        Create OAuth flow for Google Calendar
        
        Args:
            client_id: Google OAuth client ID
            client_secret: Google OAuth client secret
            redirect_uri: Redirect URI for OAuth callback
            
        Returns:
            OAuth flow object
        """
        flow = Flow.from_client_config(
            {
                "web": {
                    "client_id": client_id,
                    "client_secret": client_secret,
                    "auth_uri": "https://accounts.google.com/o/oauth2/auth",
                    "token_uri": "https://oauth2.googleapis.com/token",
                    "redirect_uris": [redirect_uri]
                }
            },
            scopes=cls.SCOPES,
            redirect_uri=redirect_uri
        )
        return flow
    
    def get_calendars(self) -> List[Dict]:
        """Get list of user's calendars"""
        if not self.service:
            raise Exception("Service not initialized. Authenticate first.")
        
        try:
            calendar_list = self.service.calendarList().list().execute()
            return calendar_list.get('items', [])
        except HttpError as e:
            raise Exception(f"Failed to fetch calendars: {str(e)}")
    
    def get_events(self, calendar_id: str = 'primary', 
                   time_min: Optional[datetime] = None,
                   time_max: Optional[datetime] = None,
                   max_results: int = 100) -> List[Dict]:
        """
        Get events from a calendar
        
        Args:
            calendar_id: Calendar ID (default: 'primary')
            time_min: Start time for events
            time_max: End time for events
            max_results: Maximum number of results
            
        Returns:
            List of event dictionaries
        """
        if not self.service:
            raise Exception("Service not initialized. Authenticate first.")
        
        try:
            events_result = self.service.events().list(
                calendarId=calendar_id,
                timeMin=time_min.isoformat() if time_min else None,
                timeMax=time_max.isoformat() if time_max else None,
                maxResults=max_results,
                singleEvents=True,
                orderBy='startTime'
            ).execute()
            
            return events_result.get('items', [])
        except HttpError as e:
            raise Exception(f"Failed to fetch events: {str(e)}")
    
    def create_event(self, calendar_id: str, event_data: Dict) -> Dict:
        """
        Create a calendar event
        
        Args:
            calendar_id: Calendar ID
            event_data: Event data dictionary
            
        Returns:
            Created event dictionary
        """
        if not self.service:
            raise Exception("Service not initialized. Authenticate first.")
        
        try:
            event = self.service.events().insert(
                calendarId=calendar_id,
                body=event_data
            ).execute()
            return event
        except HttpError as e:
            raise Exception(f"Failed to create event: {str(e)}")
    
    def event_to_task(self, event: Dict) -> Optional[Dict]:
        """
        Convert a Google Calendar event to a task dictionary
        
        Args:
            event: Event data from Google Calendar API
            
        Returns:
            Task dictionary or None if not applicable
        """
        # Only convert events that look like tasks/assignments
        # Skip all-day events and very short events
        start = event.get('start', {})
        end = event.get('end', {})
        
        if 'dateTime' not in start:
            return None  # All-day event, skip
        
        start_time = datetime.fromisoformat(start['dateTime'].replace('Z', '+00:00'))
        end_time = datetime.fromisoformat(end['dateTime'].replace('Z', '+00:00'))
        duration = (end_time - start_time).total_seconds() / 60  # minutes
        
        if duration < 15:  # Skip very short events
            return None
        
        return {
            'title': event.get('summary', 'Untitled Event'),
            'description': event.get('description', ''),
            'due_date': end_time.isoformat(),
            'estimated_time': int(duration),
            'source': 'calendar',
            'status': 'pending'
        }


