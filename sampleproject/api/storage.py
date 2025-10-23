"""
In-memory storage for high-performance Django app without database dependencies.
Thread-safe implementation for handling concurrent requests.
"""
import threading
from typing import Dict, Any, Optional, List
import uuid
from datetime import datetime
import json


class InMemoryStorage:
    """Thread-safe in-memory storage for API data"""

    def __init__(self):
        self._data: Dict[str, Dict[str, Any]] = {}
        self._lock = threading.RLock()
        self._initialize_default_data()

    def _initialize_default_data(self):
        """Initialize with some default data like the original app"""
        with self._lock:
            # Initialize users collection with sample data
            self._data['users'] = {
                '1': {'id': '1', 'name': 'John Doe', 'email': 'john@example.com', 'created_at': datetime.utcnow().isoformat()},
                '2': {'id': '2', 'name': 'Jane Smith', 'email': 'jane@example.com', 'created_at': datetime.utcnow().isoformat()},
                '3': {'id': '3', 'name': 'Bob Johnson', 'email': 'bob@example.com', 'created_at': datetime.utcnow().isoformat()},
            }

            # Initialize items collection for general storage
            self._data['items'] = {}

    def create(self, collection: str, data: Dict[str, Any]) -> str:
        """Create a new item in the collection"""
        with self._lock:
            if collection not in self._data:
                self._data[collection] = {}

            item_id = str(uuid.uuid4())
            item = {
                'id': item_id,
                'created_at': datetime.utcnow().isoformat(),
                'updated_at': datetime.utcnow().isoformat(),
                **data
            }
            self._data[collection][item_id] = item
            return item_id

    def get(self, collection: str, item_id: str) -> Optional[Dict[str, Any]]:
        """Get a specific item by ID"""
        with self._lock:
            return self._data.get(collection, {}).get(item_id)

    def list(self, collection: str, limit: Optional[int] = None) -> List[Dict[str, Any]]:
        """List all items in a collection"""
        with self._lock:
            items = list(self._data.get(collection, {}).values())
            if limit:
                return items[:limit]
            return items

    def update(self, collection: str, item_id: str, data: Dict[str, Any]) -> bool:
        """Update an existing item"""
        with self._lock:
            if collection in self._data and item_id in self._data[collection]:
                self._data[collection][item_id].update({
                    **data,
                    'updated_at': datetime.utcnow().isoformat()
                })
                return True
            return False

    def delete(self, collection: str, item_id: str) -> bool:
        """Delete an item"""
        with self._lock:
            if collection in self._data and item_id in self._data[collection]:
                del self._data[collection][item_id]
                return True
            return False

    def count(self, collection: str) -> int:
        """Get count of items in collection"""
        with self._lock:
            return len(self._data.get(collection, {}))

    def search(self, collection: str, **filters) -> List[Dict[str, Any]]:
        """Simple search functionality"""
        with self._lock:
            items = self._data.get(collection, {}).values()
            if not filters:
                return list(items)

            results = []
            for item in items:
                match = True
                for key, value in filters.items():
                    if key not in item or str(item[key]).lower() != str(value).lower():
                        match = False
                        break
                if match:
                    results.append(item)
            return results


# Global storage instance - singleton pattern for thread safety
storage = InMemoryStorage()
