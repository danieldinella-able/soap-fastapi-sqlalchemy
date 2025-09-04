"""Utility per date/tempi con funzioni di comodo in formato ISO/stringa."""

from datetime import datetime, timezone, timedelta
import time

class DatetimeUtil:

    @staticmethod
    def get_now(tz=timezone.utc) -> datetime:
        return datetime.now(tz).replace(microsecond=0)

    @staticmethod
    def get_now_str(date_format="%Y-%m-%d %H:%M:%S") -> str:
        return DatetimeUtil.get_now().strftime(date_format)

    @staticmethod
    def get_now_timestamp() -> float:
        return time.time()

    @staticmethod
    def get_now_with_tz(tz=timezone.utc) -> datetime:
        return datetime.now(tz=tz).replace(microsecond=0)

    @staticmethod
    def get_now_iso_format():
        return DatetimeUtil.get_now().isoformat()

    @staticmethod
    def get_now_date_iso_format():
        return DatetimeUtil.get_now().replace(hour=0, minute=0, second=0, microsecond=0).isoformat()

    @staticmethod
    def get_not_time_12_hour_clock_format():  # 10:00 AM
        return DatetimeUtil.get_now().strftime("%I:%M %p")

    @staticmethod
    def get_with_timedelta(days: int = 0, hours: int = 0, minutes: int = 0, seconds: int = 0, tz=timezone.utc) -> datetime:
        return DatetimeUtil.get_now(tz) + timedelta(days=days, hours=hours, minutes=minutes, seconds=seconds)
