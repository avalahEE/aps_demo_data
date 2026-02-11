def create_workcenters(env, calendars):
    """Create 7 work centers with alternative pairs.

    Returns dict of code → mrp.workcenter record.
    """
    WC = env['mrp.workcenter']

    wc_defs = [
        {
            'code': 'WC-SAW-01',
            'name': 'Panel Saw - Primary',
            'calendar': 'standard',
            'capacity': 1,
            'time_efficiency': 95.0,
            'costs_hour': 45.0,
        },
        {
            'code': 'WC-SAW-02',
            'name': 'Panel Saw - Secondary',
            'calendar': 'standard',
            'capacity': 1,
            'time_efficiency': 80.0,
            'costs_hour': 35.0,
        },
        {
            'code': 'WC-CNC-01',
            'name': 'CNC Router',
            'calendar': 'extended',
            'capacity': 1,
            'time_efficiency': 92.0,
            'costs_hour': 75.0,
        },
        {
            'code': 'WC-EDGE-01',
            'name': 'Edge Banding Machine',
            'calendar': 'standard',
            'capacity': 1,
            'time_efficiency': 90.0,
            'costs_hour': 40.0,
        },
        {
            'code': 'WC-ASSM-01',
            'name': 'Assembly Station - Primary',
            'calendar': 'extended',
            'capacity': 2,
            'time_efficiency': 100.0,
            'costs_hour': 55.0,
        },
        {
            'code': 'WC-ASSM-02',
            'name': 'Assembly Station - Secondary',
            'calendar': 'standard',
            'capacity': 1,
            'time_efficiency': 85.0,
            'costs_hour': 45.0,
        },
        {
            'code': 'WC-FINISH-01',
            'name': 'Finishing & Lacquer Booth',
            'calendar': 'standard',
            'capacity': 1,
            'time_efficiency': 88.0,
            'costs_hour': 60.0,
        },
    ]

    workcenters = {}
    for wc_def in wc_defs:
        wc = WC.create({
            'name': wc_def['name'],
            'code': wc_def['code'],
            'resource_calendar_id': calendars[wc_def['calendar']].id,
            'default_capacity': wc_def['capacity'],
            'time_efficiency': wc_def['time_efficiency'],
            'costs_hour': wc_def['costs_hour'],
        })
        workcenters[wc_def['code']] = wc

    # Set alternative work center pairs (both directions)
    _set_alternatives(workcenters, 'WC-SAW-01', 'WC-SAW-02')
    _set_alternatives(workcenters, 'WC-ASSM-01', 'WC-ASSM-02')

    return workcenters


def _set_alternatives(workcenters, code_a, code_b):
    """Link two work centers as alternatives of each other."""
    wc_a = workcenters[code_a]
    wc_b = workcenters[code_b]
    wc_a.write({'alternative_workcenter_ids': [(4, wc_b.id)]})
    wc_b.write({'alternative_workcenter_ids': [(4, wc_a.id)]})
