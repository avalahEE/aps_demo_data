from datetime import timedelta

from odoo.fields import Datetime


def create_maintenance(env, workcenters):
    """Create 1 preventive maintenance window blocking CNC Router.

    Scheduled for the Monday of the 3rd week from now, full day 06:00-22:00.
    """
    now = Datetime.now()

    # Find the Monday 3 weeks from now
    days_until_monday = (7 - now.weekday()) % 7  # days until next Monday
    if days_until_monday == 0:
        days_until_monday = 7  # skip to next Monday if today is Monday
    target_monday = now + timedelta(days=days_until_monday + 14)  # +2 more weeks
    maintenance_start = target_monday.replace(hour=6, minute=0, second=0, microsecond=0)
    maintenance_end = target_monday.replace(hour=22, minute=0, second=0, microsecond=0)

    cnc = workcenters['WC-CNC-01']

    # Get or create maintenance equipment for CNC
    equipment = env['maintenance.equipment'].create({
        'name': 'CNC Router - Spindle Unit',
        'workcenter_id': cnc.id,
    })

    env['maintenance.request'].create({
        'name': 'CNC Router - Annual Spindle Maintenance',
        'equipment_id': equipment.id,
        'maintenance_type': 'preventive',
        'schedule_date': maintenance_start,
        'duration': 16.0,  # 16 hours
        'block_workcenter': True,
    })
