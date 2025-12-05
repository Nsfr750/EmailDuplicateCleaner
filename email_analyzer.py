"""
Email Analysis Module 2.5.2

Provides advanced analysis of email collections including:
- Sender analysis
- Timeline analysis
- Attachment analysis
- Thread/conversation analysis
- Email size distribution
- Duplicate detection with different matching strategies
"""

from typing import Dict, List, Tuple, Any, Optional, DefaultDict
from collections import defaultdict, Counter
import email
import email.utils
import re
from datetime import datetime
import logging
from pathlib import Path
import os

# Try to import optional dependencies
try:
    import pandas as pd
    PANDAS_AVAILABLE = True
except ImportError:
    PANDAS_AVAILABLE = False

try:
    import matplotlib.pyplot as plt
    MATPLOTLIB_AVAILABLE = True
except ImportError:
    MATPLOTLIB_AVAILABLE = False

class EmailAnalyzer:
    """Class for performing advanced email analysis."""
    
    def __init__(self, duplicate_finder=None):
        """Initialize the EmailAnalyzer.
        
        Args:
            duplicate_finder: Optional DuplicateEmailFinder instance
        """
        self.duplicate_finder = duplicate_finder
        self.logger = logging.getLogger(__name__)
        self.analysis_results = {}
    
    def analyze_senders(self, messages: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Analyze email senders.
        
        Args:
            messages: List of email message dictionaries
            
        Returns:
            Dictionary with sender analysis results
        """
        sender_counter = Counter()
        domain_counter = Counter()
        
        for msg in messages:
            from_header = msg.get('from', '')
            if not from_header:
                continue
                
            # Extract email address from "Name <email@example.com>"
            email_match = re.search(r'<([^>]+)>', from_header)
            if email_match:
                email_addr = email_match.group(1).lower()
            else:
                email_addr = from_header.strip().lower()
                
            sender_counter[email_addr] += 1
            
            # Extract domain
            if '@' in email_addr:
                domain = email_addr.split('@')[-1]
                domain_counter[domain] += 1
        
        return {
            'top_senders': sender_counter.most_common(20),
            'top_domains': domain_counter.most_common(20),
            'unique_senders': len(sender_counter),
            'unique_domains': len(domain_counter)
        }
    
    def analyze_timeline(self, messages: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Analyze email timeline.
        
        Args:
            messages: List of email message dictionaries
            
        Returns:
            Dictionary with timeline analysis results
        """
        dates = []
        hours = []
        weekdays = []
        
        for msg in messages:
            date_str = msg.get('date')
            if not date_str:
                continue
                
            try:
                # Try to parse the date
                date_tuple = email.utils.parsedate_tz(date_str)
                if date_tuple:
                    dt = datetime.fromtimestamp(email.utils.mktime_tz(date_tuple))
                    dates.append(dt.date())
                    hours.append(dt.hour)
                    weekdays.append(dt.weekday())  # Monday is 0, Sunday is 6
            except (TypeError, ValueError) as e:
                self.logger.debug(f"Could not parse date: {date_str}: {e}")
                continue
        
        # Calculate statistics
        if dates:
            date_range = (min(dates), max(dates))
            total_days = (max(dates) - min(dates)).days + 1
            emails_per_day = len(dates) / total_days if total_days > 0 else 0
        else:
            date_range = (None, None)
            emails_per_day = 0
        
        return {
            'date_range': date_range,
            'emails_per_day': emails_per_day,
            'hour_distribution': Counter(hours).most_common(),
            'weekday_distribution': [(d, c) for d, c in enumerate(
                [sum(1 for wd in weekdays if wd == i) for i in range(7)]
            )],
            'total_emails': len(messages)
        }
    
    def analyze_attachments(self, messages: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Analyze email attachments.
        
        Args:
            messages: List of email message dictionaries
            
        Returns:
            Dictionary with attachment analysis results
        """
        attachment_types = Counter()
        attachment_sizes = []
        emails_with_attachments = 0
        
        for msg in messages:
            has_attachments = False
            
            # Check for attachments in the email
            if 'attachments' in msg:
                for att in msg['attachments']:
                    has_attachments = True
                    # Get file extension
                    filename = att.get('filename', 'unknown')
                    ext = os.path.splitext(filename)[1].lower() or '.unknown'
                    attachment_types[ext] += 1
                    
                    # Get size if available
                    size = att.get('size', 0)
                    if size:
                        attachment_sizes.append(size)
            
            if has_attachments:
                emails_with_attachments += 1
        
        return {
            'attachment_types': attachment_types.most_common(),
            'total_attachments': sum(attachment_types.values()),
            'emails_with_attachments': emails_with_attachments,
            'attachment_size_stats': self._calculate_stats(attachment_sizes) if attachment_sizes else {}
        }
    
    def analyze_threads(self, messages: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Analyze email threads and conversations.
        
        Args:
            messages: List of email message dictionaries
            
        Returns:
            Dictionary with thread analysis results
        """
        threads = defaultdict(list)
        
        for msg in messages:
            # Use In-Reply-To or References header to group messages into threads
            thread_id = msg.get('in-reply-to') or msg.get('references', '').split()[0] if msg.get('references') else None
            
            if not thread_id:
                # If no thread ID, use subject as a fallback
                subject = msg.get('subject', '').lower()
                # Clean subject (remove Re:, Fwd:, etc.)
                clean_subject = re.sub(r'^\s*(re|fwd?):\s*', '', subject).strip()
                thread_id = f'subject:{clean_subject}'
            
            threads[thread_id].append(msg)
        
        # Calculate thread statistics
        thread_sizes = [len(msgs) for msgs in threads.values()]
        
        return {
            'total_threads': len(threads),
            'thread_size_stats': self._calculate_stats(thread_sizes) if thread_sizes else {},
            'largest_thread': max(thread_sizes) if thread_sizes else 0
        }
    
    def analyze_duplicates(self, messages: List[Dict[str, Any]], 
                          hash_method: str = 'strict') -> Dict[str, Any]:
        """Analyze duplicate emails.
        
        Args:
            messages: List of email message dictionaries
            hash_method: Method to use for detecting duplicates
                'strict': Message-ID + Date + From + Subject + Body hash
                'content': Body hash only
                'headers': Message-ID + Date + From + Subject
                'subject-sender': Subject + From
                
        Returns:
            Dictionary with duplicate analysis results
        """
        if not self.duplicate_finder:
            return {'error': 'Duplicate finder not initialized'}
            
        # Group messages by their hash
        hash_groups = defaultdict(list)
        
        for msg in messages:
            email_msg = self._dict_to_email(msg)
            if email_msg:
                msg_hash = self.duplicate_finder.compute_email_hash(email_msg, hash_method)
                hash_groups[msg_hash].append(msg)
        
        # Find duplicates (groups with more than one message)
        duplicates = {h: msgs for h, msgs in hash_groups.items() if len(msgs) > 1}
        
        return {
            'total_duplicates': sum(len(msgs) - 1 for msgs in duplicates.values()),
            'duplicate_groups': len(duplicates),
            'duplicate_sources': {h: len(msgs) for h, msgs in duplicates.items()}
        }
    
    def _dict_to_email(self, msg_dict: Dict[str, Any]) -> Optional[email.message.Message]:
        """Convert a message dictionary back to an email.message.Message."""
        try:
            msg = email.message.Message()
            for key, value in msg_dict.items():
                if key.lower() not in ['body', 'attachments']:
                    msg[key] = str(value)
            
            if 'body' in msg_dict:
                msg.set_payload(msg_dict['body'])
                
            return msg
        except Exception as e:
            self.logger.error(f"Error converting dict to email: {e}")
            return None
    
    def _calculate_stats(self, values: List[float]) -> Dict[str, float]:
        """Calculate basic statistics for a list of numeric values."""
        if not values:
            return {}
            
        if PANDAS_AVAILABLE:
            import pandas as pd
            s = pd.Series(values)
            return {
                'count': len(values),
                'mean': s.mean(),
                'median': s.median(),
                'min': s.min(),
                'max': s.max(),
                'std': s.std(),
                '25%': s.quantile(0.25),
                '50%': s.quantile(0.5),
                '75%': s.quantile(0.75)
            }
        else:
            # Fallback implementation without pandas
            n = len(values)
            if n == 0:
                return {}
                
            sorted_values = sorted(values)
            return {
                'count': n,
                'mean': sum(values) / n,
                'median': sorted_values[n//2] if n % 2 == 1 else 
                         (sorted_values[n//2 - 1] + sorted_values[n//2]) / 2,
                'min': min(values),
                'max': max(values)
            }
    
    def generate_report(self, messages: List[Dict[str, Any]], 
                       include_plots: bool = False) -> Dict[str, Any]:
        """Generate a comprehensive email analysis report.
        
        Args:
            messages: List of email message dictionaries
            include_plots: Whether to include matplotlib plots (requires matplotlib)
            
        Returns:
            Dictionary containing all analysis results
        """
        self.analysis_results = {
            'summary': {
                'total_emails': len(messages),
                'analysis_timestamp': datetime.now().isoformat()
            },
            'senders': self.analyze_senders(messages),
            'timeline': self.analyze_timeline(messages),
            'attachments': self.analyze_attachments(messages),
            'threads': self.analyze_threads(messages),
            'duplicates': self.analyze_duplicates(messages)
        }
        
        if include_plots and MATPLOTLIB_AVAILABLE:
            self._generate_plots()
        
        return self.analysis_results
    
    def _generate_plots(self):
        """Generate matplotlib plots for the analysis."""
        if not MATPLOTLIB_AVAILABLE or not self.analysis_results:
            return
            
        plots = {}
        
        # Sender distribution plot
        if 'senders' in self.analysis_results:
            senders = self.analysis_results['senders']
            if 'top_senders' in senders and senders['top_senders']:
                top_n = min(10, len(senders['top_senders']))
                top_senders = senders['top_senders'][:top_n]
                
                plt.figure(figsize=(10, 6))
                plt.barh(
                    [s[0].split('@')[0] for s in top_senders],
                    [s[1] for s in top_senders]
                )
                plt.title(f'Top {top_n} Senders')
                plt.xlabel('Number of Emails')
                plt.tight_layout()
                plots['top_senders'] = plt.gcf()
                plt.close()
        
        # Timeline plot
        if 'timeline' in self.analysis_results:
            timeline = self.analysis_results['timeline']
            if 'hour_distribution' in timeline and timeline['hour_distribution']:
                hours = [h[0] for h in timeline['hour_distribution']]
                counts = [h[1] for h in timeline['hour_distribution']]
                
                plt.figure(figsize=(10, 4))
                plt.bar(hours, counts)
                plt.title('Email Activity by Hour of Day')
                plt.xlabel('Hour of Day')
                plt.ylabel('Number of Emails')
                plt.xticks(range(0, 24))
                plt.tight_layout()
                plots['hourly_activity'] = plt.gcf()
                plt.close()
        
        # Update analysis results with plot paths
        self.analysis_results['_plots'] = plots

    def export_report(self, output_format: str = 'json', output_file: str = None) -> str:
        """Export the analysis report to a file.
        
        Args:
            output_format: Output format ('json', 'csv', 'html')
            output_file: Path to output file (if None, returns the content as string)
            
        Returns:
            The exported content if output_file is None, otherwise the path to the saved file
        """
        if not self.analysis_results:
            return "No analysis results available. Run generate_report() first."
            
        output_format = output_format.lower()
        
        if output_format == 'json':
            import json
            content = json.dumps(self.analysis_results, indent=2, default=str)
            
        elif output_format == 'csv' and PANDAS_AVAILABLE:
            import pandas as pd
            # Flatten the analysis results for CSV
            flat_data = []
            for section, data in self.analysis_results.items():
                if section.startswith('_'):
                    continue
                if isinstance(data, dict):
                    flat_data.append({'section': section, 'key': k, 'value': v} 
                                    for k, v in data.items())
            
            if flat_data:
                df = pd.concat([pd.DataFrame(section) for section in flat_data], 
                             ignore_index=True)
                content = df.to_csv(index=False)
            else:
                content = "No tabular data to export to CSV"
                
        elif output_format == 'html':
            # Simple HTML report
            content = "<html><head><title>Email Analysis Report</title></head><body>"
            content += f"<h1>Email Analysis Report</h1>"
            content += f"<p>Generated on: {self.analysis_results['summary']['analysis_timestamp']}</p>"
            
            for section, data in self.analysis_results.items():
                if section.startswith('_') or not data:
                    continue
                    
                content += f"<h2>{section.title()}</h2>"
                
                if isinstance(data, dict):
                    content += "<ul>"
                    for k, v in data.items():
                        if k != 'analysis_timestamp':
                            content += f"<li><strong>{k}:</strong> {v}</li>"
                    content += "</ul>"
                else:
                    content += f"<p>{data}</p>"
            
            content += "</body></html>"
            
        else:
            return f"Unsupported output format: {output_format}"
        
        if output_file:
            with open(output_file, 'w', encoding='utf-8') as f:
                f.write(content)
            return output_file
        else:
            return content
