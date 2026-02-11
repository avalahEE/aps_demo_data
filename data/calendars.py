def create_calendars(env):
    """Create 2 resource calendars: Standard Day Shift and Extended Two-Shift.

    Returns dict of key → resource.calendar record.
    """
    Calendar = env['resource.calendar']

    # --- Standard Day Shift: Mon-Fri 07:00-12:00 + 12:30-16:30 (40h/wk) ---
    standard = Calendar.create({
        'name': 'Standard Day Shift (40h)',
        'tz': 'Europe/Berlin',
        'attendance_ids': [
            # Monday-Friday morning block
            (0, 0, {'name': 'Monday Morning', 'dayofweek': '0', 'hour_from': 7.0, 'hour_to': 12.0}),
            (0, 0, {'name': 'Monday Afternoon', 'dayofweek': '0', 'hour_from': 12.5, 'hour_to': 16.5}),
            (0, 0, {'name': 'Tuesday Morning', 'dayofweek': '1', 'hour_from': 7.0, 'hour_to': 12.0}),
            (0, 0, {'name': 'Tuesday Afternoon', 'dayofweek': '1', 'hour_from': 12.5, 'hour_to': 16.5}),
            (0, 0, {'name': 'Wednesday Morning', 'dayofweek': '2', 'hour_from': 7.0, 'hour_to': 12.0}),
            (0, 0, {'name': 'Wednesday Afternoon', 'dayofweek': '2', 'hour_from': 12.5, 'hour_to': 16.5}),
            (0, 0, {'name': 'Thursday Morning', 'dayofweek': '3', 'hour_from': 7.0, 'hour_to': 12.0}),
            (0, 0, {'name': 'Thursday Afternoon', 'dayofweek': '3', 'hour_from': 12.5, 'hour_to': 16.5}),
            (0, 0, {'name': 'Friday Morning', 'dayofweek': '4', 'hour_from': 7.0, 'hour_to': 12.0}),
            (0, 0, {'name': 'Friday Afternoon', 'dayofweek': '4', 'hour_from': 12.5, 'hour_to': 16.5}),
        ],
    })

    # --- Extended Two-Shift: Mon-Fri 06:00-22:00, Sat 06:00-14:00 (78h/wk) ---
    extended = Calendar.create({
        'name': 'Extended Two-Shift (78h)',
        'tz': 'Europe/Berlin',
        'attendance_ids': [
            # Monday-Friday: two shifts
            (0, 0, {'name': 'Monday Shift 1', 'dayofweek': '0', 'hour_from': 6.0, 'hour_to': 14.0}),
            (0, 0, {'name': 'Monday Shift 2', 'dayofweek': '0', 'hour_from': 14.0, 'hour_to': 22.0}),
            (0, 0, {'name': 'Tuesday Shift 1', 'dayofweek': '1', 'hour_from': 6.0, 'hour_to': 14.0}),
            (0, 0, {'name': 'Tuesday Shift 2', 'dayofweek': '1', 'hour_from': 14.0, 'hour_to': 22.0}),
            (0, 0, {'name': 'Wednesday Shift 1', 'dayofweek': '2', 'hour_from': 6.0, 'hour_to': 14.0}),
            (0, 0, {'name': 'Wednesday Shift 2', 'dayofweek': '2', 'hour_from': 14.0, 'hour_to': 22.0}),
            (0, 0, {'name': 'Thursday Shift 1', 'dayofweek': '3', 'hour_from': 6.0, 'hour_to': 14.0}),
            (0, 0, {'name': 'Thursday Shift 2', 'dayofweek': '3', 'hour_from': 14.0, 'hour_to': 22.0}),
            (0, 0, {'name': 'Friday Shift 1', 'dayofweek': '4', 'hour_from': 6.0, 'hour_to': 14.0}),
            (0, 0, {'name': 'Friday Shift 2', 'dayofweek': '4', 'hour_from': 14.0, 'hour_to': 22.0}),
            # Saturday: morning shift only
            (0, 0, {'name': 'Saturday Shift', 'dayofweek': '5', 'hour_from': 6.0, 'hour_to': 14.0}),
        ],
    })

    return {
        'standard': standard,
        'extended': extended,
    }
