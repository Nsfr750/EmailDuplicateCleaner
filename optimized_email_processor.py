"""
Optimized Email Processor for handling large email datasets efficiently.

This module provides optimized functions for processing large email collections
with improved memory usage and performance.
"""

import os
import hashlib
import xxhash
import email
import email.utils
import mailbox
import sqlite3
import time
import logging
from pathlib import Path
from typing import Dict, List, Tuple, Optional, Generator, Any, Set
from concurrent.futures import ThreadPoolExecutor, as_completed
from datetime import datetime

# Set up logging using the centralized logger
from struttura.logger import logger as app_logger
logger = app_logger  # Use the global logger instance

# Constants
CHUNK_SIZE = 1024 * 1024  # 1MB chunks for reading large messages
DEFAULT_DB_PATH = 'email_hashes.db'
DEFAULT_HASH_METHOD = 'xxh64'  # Using xxHash for better performance

class EmailHashCache:
    """Cache for storing and retrieving email hashes using SQLite."""
    
    def __init__(self, db_path: str = DEFAULT_DB_PATH):
        """Initialize the cache with the specified SQLite database file."""
        self.db_path = db_path
        self._init_db()
    
    def _init_db(self) -> None:
        """Initialize the database schema if it doesn't exist."""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS email_hashes (
                    message_id TEXT,
                    message_hash TEXT,
                    source_file TEXT,
                    last_modified REAL,
                    hash_method TEXT,
                    PRIMARY KEY (message_id, source_file, hash_method)
                )
            ''')
            conn.commit()
    
    def get_hash(self, message_id: str, source_file: str, hash_method: str) -> Optional[str]:
        """Get a cached hash for a message if it exists and is still valid."""
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                cursor.execute('''
                    SELECT message_hash FROM email_hashes
                    WHERE message_id = ? AND source_file = ? AND hash_method = ?
                ''', (message_id, source_file, hash_method))
                result = cursor.fetchone()
                return result[0] if result else None
        except sqlite3.Error as e:
            logger.warning(f"Error reading from hash cache: {e}")
            return None
    
    def set_hash(self, message_id: str, message_hash: str, source_file: str, hash_method: str) -> None:
        """Store a hash in the cache."""
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                cursor.execute('''
                    INSERT OR REPLACE INTO email_hashes 
                    (message_id, message_hash, source_file, last_modified, hash_method)
                    VALUES (?, ?, ?, ?, ?)
                ''', (message_id, message_hash, source_file, time.time(), hash_method))
                conn.commit()
        except sqlite3.Error as e:
            logger.warning(f"Error writing to hash cache: {e}")
    
    def clear_cache(self) -> None:
        """Clear all cached hashes."""
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                cursor.execute('DELETE FROM email_hashes')
                conn.commit()
        except sqlite3.Error as e:
            logger.error(f"Error clearing hash cache: {e}")


def compute_email_hash_fast(msg: email.message.Message, hash_method: str = DEFAULT_HASH_METHOD) -> str:
    """
    Compute a fast hash for an email message.
    
    Args:
        msg: The email message to hash
        hash_method: The hashing method to use ('xxh64', 'md5', 'sha1', etc.)
        
    Returns:
        A hexadecimal string representing the hash
    """
    # Get message ID or generate a fallback
    message_id = msg.get('Message-ID', str(time.time()) + str(hash(str(msg))))
    
    # Use xxHash for better performance if available
    if hash_method == 'xxh64' and hasattr(xxhash, 'xxh64'):
        hasher = xxhash.xxh64()
    else:
        # Fall back to standard hashlib
        hasher = hashlib.new(hash_method)
    
    # Add headers to hash
    for header in ['Message-ID', 'Date', 'From', 'Subject', 'To', 'Cc', 'Bcc']:
        if header in msg:
            hasher.update(header.encode('utf-8', errors='replace'))
            hasher.update(b': ')
            hasher.update(msg[header].encode('utf-8', errors='replace'))
            hasher.update(b'\r\n')
    
    # Add body content to hash
    if msg.is_multipart():
        for part in msg.walk():
            if part.get_content_maintype() == 'text':
                try:
                    payload = part.get_payload(decode=True)
                    if payload:
                        hasher.update(payload)
                except Exception as e:
                    logger.warning(f"Error processing message part: {e}")
    else:
        try:
            payload = msg.get_payload(decode=True)
            if payload:
                hasher.update(payload)
        except Exception as e:
            logger.warning(f"Error processing message payload: {e}")
    
    return hasher.hexdigest()


def process_mailbox_chunk(
    mbox_path: str,
    chunk_size: int = 100,
    hash_method: str = DEFAULT_HASH_METHOD,
    cache: Optional[EmailHashCache] = None
) -> Generator[Dict[str, Any], None, None]:
    """
    Process a mailbox in chunks to reduce memory usage.
    
    Args:
        mbox_path: Path to the mailbox file
        chunk_size: Number of messages to process in each chunk
        hash_method: The hashing method to use
        cache: Optional EmailHashCache instance for caching hashes
        
    Yields:
        Dictionaries containing message metadata and hash
    """
    try:
        mbox = mailbox.mbox(mbox_path)
        total_messages = len(mbox)
        
        logger.info(f"Processing {total_messages} messages in {mbox_path}")
        
        # Process messages in chunks
        for i in range(0, total_messages, chunk_size):
            chunk_end = min(i + chunk_size, total_messages)
            chunk_messages = []
            
            # Process this chunk
            for j in range(i, chunk_end):
                try:
                    msg = mbox[j]
                    message_id = msg.get('Message-ID', f'no-id-{i}-{j}')
                    
                    # Check cache first
                    cached_hash = None
                    if cache:
                        cached_hash = cache.get_hash(message_id, mbox_path, hash_method)
                    
                    if cached_hash is not None:
                        message_hash = cached_hash
                        logger.debug(f"Using cached hash for message {j+1}/{total_messages}")
                    else:
                        # Compute hash if not in cache
                        message_hash = compute_email_hash_fast(msg, hash_method)
                        # Update cache
                        if cache:
                            cache.set_hash(message_id, message_hash, mbox_path, hash_method)
                    
                    chunk_messages.append({
                        'key': j,
                        'message_id': message_id,
                        'hash': message_hash,
                        'subject': msg.get('Subject', '(No Subject)'),
                        'from': msg.get('From', '(No Sender)'),
                        'date': msg.get('Date', ''),
                        'size': len(msg.as_bytes()) if hasattr(msg, 'as_bytes') else 0,
                        'cached': cached_hash is not None
                    })
                    
                except Exception as e:
                    logger.error(f"Error processing message {j}: {e}")
            
            # Yield the processed chunk
            yield {
                'start_idx': i,
                'end_idx': chunk_end - 1,
                'total': total_messages,
                'messages': chunk_messages,
                'processed': chunk_end,
                'remaining': max(0, total_messages - chunk_end)
            }
            
    except Exception as e:
        logger.error(f"Error processing mailbox {mbox_path}: {e}")
        raise
    finally:
        if 'mbox' in locals():
            mbox.close()


def find_duplicates(
    mbox_path: str,
    hash_method: str = DEFAULT_HASH_METHOD,
    use_cache: bool = True,
    chunk_size: int = 100,
    max_workers: int = 4
) -> Dict[str, List[Dict[str, Any]] ]:
    """
    Find duplicate emails in a mailbox.
    
    Args:
        mbox_path: Path to the mailbox file
        hash_method: The hashing method to use
        use_cache: Whether to use the hash cache
        chunk_size: Number of messages to process in each chunk
        max_workers: Maximum number of worker threads
        
    Returns:
        A dictionary with 'duplicates' and 'unique' keys containing message groups
    """
    cache = EmailHashCache() if use_cache else None
    hash_groups = {}
    
    start_time = time.time()
    
    # Process the mailbox
    for chunk in process_mailbox_chunk(mbox_path, chunk_size, hash_method, cache):
        # Update progress
        progress = (chunk['processed'] / chunk['total']) * 100
        logger.info(f"Processed {chunk['processed']}/{chunk['total']} messages ({progress:.1f}%)")
        
        # Group messages by hash
        for msg in chunk['messages']:
            if msg['hash'] not in hash_groups:
                hash_groups[msg['hash']] = []
            hash_groups[msg['hash']].append(msg)
    
    # Identify duplicates and unique messages
    duplicates = {}
    unique = []
    
    for msg_hash, messages in hash_groups.items():
        if len(messages) > 1:
            # Sort messages by date if available
            try:
                messages.sort(key=lambda x: email.utils.parsedate_to_datetime(x['date']))
            except (TypeError, ValueError):
                pass
            duplicates[msg_hash] = messages
        else:
            unique.extend(messages)
    
    # Log statistics
    elapsed = time.time() - start_time
    logger.info(f"Processed {len(hash_groups)} unique messages in {elapsed:.2f} seconds")
    logger.info(f"Found {len(duplicates)} duplicate groups")
    logger.info(f"Found {len(unique)} unique messages")
    
    return {
        'duplicates': duplicates,
        'unique': unique,
        'stats': {
            'total_messages': len(hash_groups),
            'duplicate_groups': len(duplicates),
            'unique_messages': len(unique),
            'processing_time': elapsed
        }
    }


def process_multiple_mailboxes(
    mbox_paths: List[str],
    hash_method: str = DEFAULT_HASH_METHOD,
    use_cache: bool = True,
    chunk_size: int = 100,
    max_workers: int = 4
) -> Dict[str, Dict[str, List[Dict[str, Any]] ]]:
    """
    Process multiple mailboxes in parallel.
    
    Args:
        mbox_paths: List of mailbox file paths
        hash_method: The hashing method to use
        use_cache: Whether to use the hash cache
        chunk_size: Number of messages to process in each chunk
        max_workers: Maximum number of worker threads
        
    Returns:
        A dictionary mapping mailbox paths to their duplicate/unique message groups
    """
    results = {}
    
    with ThreadPoolExecutor(max_workers=min(max_workers, len(mbox_paths))) as executor:
        future_to_path = {
            executor.submit(
                find_duplicates,
                path,
                hash_method=hash_method,
                use_cache=use_cache,
                chunk_size=chunk_size,
                max_workers=max(1, max_workers // len(mbox_paths))
            ): path for path in mbox_paths
        }
        
        for future in as_completed(future_to_path):
            path = future_to_path[future]
            try:
                results[path] = future.result()
                logger.info(f"Completed processing {path}")
            except Exception as e:
                logger.error(f"Error processing {path}: {e}")
                results[path] = {'error': str(e)}
    
    return results


if __name__ == "__main__":
    import argparse
    
    parser = argparse.ArgumentParser(description='Find duplicate emails in mailboxes.')
    parser.add_argument('mailbox', nargs='+', help='Path to mailbox file(s)')
    parser.add_argument('--hash-method', default=DEFAULT_HASH_METHOD,
                       help=f'Hashing method to use (default: {DEFAULT_HASH_METHOD})')
    parser.add_argument('--no-cache', action='store_true',
                       help='Disable hash caching')
    parser.add_argument('--chunk-size', type=int, default=100,
                       help='Number of messages to process in each chunk')
    parser.add_argument('--workers', type=int, default=4,
                       help='Maximum number of worker threads')
    parser.add_argument('--verbose', '-v', action='store_true',
                       help='Enable verbose logging')
    
    args = parser.parse_args()
    
    if args.verbose:
        logger.setLevel(logging.DEBUG)
    
    results = process_multiple_mailboxes(
        args.mailbox,
        hash_method=args.hash_method,
        use_cache=not args.no_cache,
        chunk_size=args.chunk_size,
        max_workers=args.workers
    )
    
    # Print summary
    print("\n=== Processing Complete ===")
    for path, result in results.items():
        if 'error' in result:
            print(f"{path}: Error - {result['error']}")
        else:
            stats = result.get('stats', {})
            print(f"{path}:")
            print(f"  Total messages: {stats.get('total_messages', 0)}")
            print(f"  Duplicate groups: {stats.get('duplicate_groups', 0)}")
            print(f"  Unique messages: {stats.get('unique_messages', 0)}")
            print(f"  Processing time: {stats.get('processing_time', 0):.2f} seconds")
