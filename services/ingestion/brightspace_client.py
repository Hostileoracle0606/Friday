"""
Brightspace (D2L Valence) API Client
Handles OAuth and task fetching from UW Learn / Brightspace
"""
import requests
from typing import List, Dict, Optional
from datetime import datetime
import hmac
import hashlib
import base64
from urllib.parse import urlencode, quote


class BrightspaceClient:
    """Client for interacting with Brightspace D2L Valence API"""
    
    def __init__(self, app_id: str, app_key: str, user_id: str, user_key: str, host: str):
        """
        Initialize Brightspace client
        
        Args:
            app_id: Application ID from Brightspace
            app_key: Application Key from Brightspace
            user_id: User ID for API calls
            user_key: User Key for API calls
            host: Brightspace host (e.g., 'https://learn.uwaterloo.ca')
        """
        self.app_id = app_id
        self.app_key = app_key
        self.user_id = user_id
        self.user_key = user_key
        self.host = host.rstrip('/')
        self.api_version = "1.0"
    
    def _create_signed_request(self, method: str, route: str, params: Optional[Dict] = None) -> Dict[str, str]:
        """
        Create a signed request for Brightspace Valence API
        
        Args:
            method: HTTP method (GET, POST, etc.)
            route: API route (e.g., '/d2l/api/le/1.0/...')
            params: Query parameters
            
        Returns:
            Dictionary with signed URL and headers
        """
        timestamp = str(int(datetime.utcnow().timestamp()))
        route_with_params = route
        if params:
            route_with_params += '?' + urlencode(params)
        
        # Create signature
        sig_string = f"{method}&{quote(route_with_params, safe='')}&{timestamp}"
        sig_bytes = hmac.new(
            self.app_key.encode('utf-8'),
            sig_string.encode('utf-8'),
            hashlib.sha256
        ).digest()
        signature = base64.b64encode(sig_bytes).decode('utf-8')
        
        # Create signed URL
        signed_params = {
            'x_a': self.app_id,
            'x_b': self.user_id,
            'x_c': signature,
            'x_d': self.user_key,
            'x_t': timestamp
        }
        
        signed_url = f"{self.host}{route_with_params}&" + urlencode(signed_params)
        
        return {
            'url': signed_url,
            'headers': {
                'Content-Type': 'application/json'
            }
        }
    
    def get_courses(self) -> List[Dict]:
        """Fetch all courses for the user"""
        route = '/d2l/api/lp/1.0/enrollments/myenrollments/'
        request_data = self._create_signed_request('GET', route)
        
        try:
            response = requests.get(request_data['url'], headers=request_data['headers'])
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            raise Exception(f"Failed to fetch courses: {str(e)}")
    
    def get_course_content(self, org_unit_id: str) -> List[Dict]:
        """Fetch content modules for a course"""
        route = f'/d2l/api/le/1.0/{org_unit_id}/content/'
        request_data = self._create_signed_request('GET', route)
        
        try:
            response = requests.get(request_data['url'], headers=request_data['headers'])
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            raise Exception(f"Failed to fetch course content: {str(e)}")
    
    def get_assignments(self, org_unit_id: str) -> List[Dict]:
        """Fetch assignments for a course"""
        route = f'/d2l/api/le/1.0/{org_unit_id}/assignments/'
        request_data = self._create_signed_request('GET', route)
        
        try:
            response = requests.get(request_data['url'], headers=request_data['headers'])
            response.raise_for_status()
            data = response.json()
            return data.get('Objects', [])
        except requests.exceptions.RequestException as e:
            raise Exception(f"Failed to fetch assignments: {str(e)}")
    
    def assignment_to_task(self, assignment: Dict, course_name: str) -> Dict:
        """
        Convert a Brightspace assignment to a task dictionary
        
        Args:
            assignment: Assignment data from Brightspace API
            course_name: Name of the course
            
        Returns:
            Task dictionary compatible with TaskCreate schema
        """
        due_date = None
        if assignment.get('DueDate'):
            try:
                due_date = datetime.fromisoformat(assignment['DueDate'].replace('Z', '+00:00'))
            except (ValueError, AttributeError):
                pass
        
        # Estimate time based on assignment type (rough heuristic)
        estimated_time = 120  # Default 2 hours
        if assignment.get('Instructions', {}).get('Html'):
            # Longer instructions might mean more work
            html_len = len(assignment['Instructions']['Html'])
            estimated_time = min(300, max(60, html_len // 100))
        
        return {
            'title': f"{course_name}: {assignment.get('Name', 'Untitled Assignment')}",
            'description': assignment.get('Instructions', {}).get('Text', ''),
            'due_date': due_date.isoformat() if due_date else None,
            'estimated_time': estimated_time,
            'source': 'brightspace',
            'status': 'pending'
        }


