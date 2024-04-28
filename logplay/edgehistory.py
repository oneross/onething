import os
import shutil
import sqlite3
import sys
from datetime import datetime, timedelta
import diskcache as dc
import argparse

DEFAULT_EDGE_HISTORY_DB_PATH=os.path.expanduser('~/Library/Application Support/Microsoft Edge/Default/History')

class EdgeHistory:
    def __init__(self, db_path=DEFAULT_EDGE_HISTORY_DB_PATH, ttl=300, since=None):
        self.cache = dc.Cache('./tmp/')
        self.db_path = db_path
        self.ttl = ttl
        self.since = since if since else datetime.now().replace(hour=0, minute=0, second=0, microsecond=0) - timedelta(days=1)

    def load_history(self):
        # Check if cached history exists
        history = self.cache.get('edge_history')
        if history is not None:
            return history
        
        # Copy the database to local directory to avoid working directly on the original file
        local_db_path = './tmp/History'
        shutil.copy(self.db_path, local_db_path)
        
        # Query the history from the copied database
        history = self.query_history(local_db_path)
        
        # Cache the result and set TTL
        self.cache.set('edge_history', history, expire=self.ttl)
        
        # Remove the copied database
        os.remove(local_db_path)
        
        return history

    def query_history(self, db_path):
        query = f"""
        SELECT urls.url, urls.title, datetime(visits.visit_time/1000000-11644473600, 'unixepoch', 'localtime') AS visit_time, visits.visit_duration / 1000.0 AS visit_duration_seconds
        FROM urls
        JOIN visits ON urls.id = visits.url
        WHERE datetime(visits.visit_time/1000000-11644473600, 'unixepoch', 'localtime') > datetime('{self.since.strftime('%Y-%m-%d %H:%M:%S')}')
        ORDER BY visits.visit_time DESC;
        """
        conn = sqlite3.connect(db_path)
        cur = conn.cursor()
        cur.execute(query)
        result = cur.fetchall()
        conn.close()
        return result

    def refresh_cache(self):
        self.cache.evict('edge_history')
        return self.load_history()

def parse_args():
    parser = argparse.ArgumentParser(description='Manage and view Edge browser history.')
    parser.add_argument('--history-db', type=str, help='Path to the SQLite DB file')
    parser.add_argument('--since', type=str, help='Date time filter in the format YYYY-MM-DD or YYYY-MM-DD hh:mm')
    parser.add_argument('--ttl', type=int, help='Time to live for the cache in seconds')
    parser.add_argument('--refresh', action='store_true', help='Refresh the cache by re-querying the history')
    return parser.parse_args()

if __name__ == "__main__":
    args = parse_args()
    history_db = args.history_db if args.history_db else 'foo'
    ttl = args.ttl if args.ttl else 300
    since = datetime.strptime(args.since, '%Y-%m-%d %H:%M') if args.since else None

    history = EdgeHistory(db_path=history_db, ttl=ttl, since=since)
    
    if args.refresh:
        result = history.refresh_cache()
    else:
        result = history.load_history()
    
    for item in result:
        print(item)
