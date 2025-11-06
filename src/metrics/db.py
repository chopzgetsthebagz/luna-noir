"""
Metrics Database Module
Tracks messages, payments, and provides KPI calculations.
"""

import sqlite3
import os
import time
import threading
from pathlib import Path

# Database path from environment or default
DB_PATH = os.getenv("METRICS_DB", "data/metrics.db")

# Ensure data directory exists
os.makedirs("data", exist_ok=True)

# Database schema
_schema = """
CREATE TABLE IF NOT EXISTS messages(
  ts INTEGER, 
  user_id TEXT, 
  is_premium INTEGER, 
  mode TEXT
);

CREATE TABLE IF NOT EXISTS payments(
  ts INTEGER, 
  user_id TEXT, 
  amount_cents INTEGER, 
  currency TEXT
);

CREATE INDEX IF NOT EXISTS idx_messages_ts ON messages(ts);
CREATE INDEX IF NOT EXISTS idx_messages_user ON messages(user_id);
CREATE INDEX IF NOT EXISTS idx_payments_ts ON payments(ts);
CREATE INDEX IF NOT EXISTS idx_payments_user ON payments(user_id);
"""

# Thread lock for concurrent access
_lock = threading.Lock()


def _conn():
    """Create database connection with WAL mode for better concurrency"""
    c = sqlite3.connect(DB_PATH)
    c.execute("PRAGMA journal_mode=WAL")
    return c


# Initialize database schema
with _conn() as c:
    c.executescript(_schema)


def log_msg(uid, is_premium, mode):
    """
    Log a message event.
    
    Args:
        uid: User ID (int or str)
        is_premium: Whether user is premium (bool or int)
        mode: Conversation mode (str)
    """
    with _lock, _conn() as c:
        c.execute(
            "INSERT INTO messages VALUES(?,?,?,?)",
            (int(time.time()), str(uid), int(is_premium), mode)
        )
        c.commit()


def log_payment(uid, amount_cents, currency):
    """
    Log a payment event.
    
    Args:
        uid: User ID (int or str)
        amount_cents: Payment amount in cents (int)
        currency: Currency code (str, e.g., "usd")
    """
    with _lock, _conn() as c:
        c.execute(
            "INSERT INTO payments VALUES(?,?,?,?)",
            (int(time.time()), str(uid), amount_cents, currency)
        )
        c.commit()


def quick_kpis(days=1):
    """
    Get quick KPIs for the last N days.
    
    Args:
        days: Number of days to look back (default: 1)
        
    Returns:
        dict with keys:
            - dau: Daily Active Users (unique users who sent messages)
            - messages: Total message count
            - premium_senders: Unique premium users who sent messages
            - total_revenue_cents: Total revenue in cents
            - conversion_rate: Premium users / Total users (%)
    """
    with _conn() as c:
        cutoff = int(time.time()) - days * 86400
        
        # Daily Active Users
        dau = c.execute(
            "SELECT COUNT(DISTINCT user_id) FROM messages WHERE ts>?",
            (cutoff,)
        ).fetchone()[0]
        
        # Total messages
        msgs = c.execute(
            "SELECT COUNT(*) FROM messages WHERE ts>?",
            (cutoff,)
        ).fetchone()[0]
        
        # Premium senders
        prem = c.execute(
            "SELECT COUNT(DISTINCT user_id) FROM messages WHERE ts>? AND is_premium=1",
            (cutoff,)
        ).fetchone()[0]
        
        # Total revenue
        revenue = c.execute(
            "SELECT COALESCE(SUM(amount_cents), 0) FROM payments WHERE ts>?",
            (cutoff,)
        ).fetchone()[0]
        
        # Conversion rate
        conversion = (prem / dau * 100) if dau > 0 else 0
        
        return {
            "dau": dau,
            "messages": msgs,
            "premium_senders": prem,
            "total_revenue_cents": revenue,
            "conversion_rate": round(conversion, 2)
        }


def get_mode_breakdown(days=1):
    """
    Get message breakdown by mode for the last N days.
    
    Args:
        days: Number of days to look back (default: 1)
        
    Returns:
        dict with mode names as keys and message counts as values
    """
    with _conn() as c:
        cutoff = int(time.time()) - days * 86400
        
        rows = c.execute(
            "SELECT mode, COUNT(*) FROM messages WHERE ts>? GROUP BY mode",
            (cutoff,)
        ).fetchall()
        
        return {mode: count for mode, count in rows}


def get_user_stats(uid):
    """
    Get stats for a specific user.
    
    Args:
        uid: User ID (int or str)
        
    Returns:
        dict with user statistics
    """
    with _conn() as c:
        uid_str = str(uid)
        
        # Total messages
        total_msgs = c.execute(
            "SELECT COUNT(*) FROM messages WHERE user_id=?",
            (uid_str,)
        ).fetchone()[0]
        
        # First message timestamp
        first_msg = c.execute(
            "SELECT MIN(ts) FROM messages WHERE user_id=?",
            (uid_str,)
        ).fetchone()[0]
        
        # Last message timestamp
        last_msg = c.execute(
            "SELECT MAX(ts) FROM messages WHERE user_id=?",
            (uid_str,)
        ).fetchone()[0]
        
        # Total payments
        total_payments = c.execute(
            "SELECT COALESCE(SUM(amount_cents), 0) FROM payments WHERE user_id=?",
            (uid_str,)
        ).fetchone()[0]
        
        return {
            "user_id": uid_str,
            "total_messages": total_msgs,
            "first_seen": first_msg,
            "last_seen": last_msg,
            "total_paid_cents": total_payments
        }

