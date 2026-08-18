{
    'name': 'APS Demo Data - Furniture Manufacturing',
    'version': '17.0.3.0.0',
    'category': 'Manufacturing',
    'summary': 'Realistic furniture manufacturing demo data for APS 4 Odoo',
    'description': """
Auto-seeds a complete furniture/woodworking manufacturing dataset:
- 7 work centers (with alternatives)
- ~207 raw materials across 20 categories
- 10 finished products with 3-4 level deep BOMs
- ~25 shared subassemblies
- 30 confirmed manufacturing orders (generating ~120-180 sub-MOs)
- 1 preventive maintenance window on CNC bottleneck
- Stock levels + 6 purchase orders for material-aware scheduling demo
    """,
    'depends': ['mrp', 'mrp_maintenance', 'purchase_stock'],
    'data': [],
    'post_init_hook': 'post_init_hook',
    'installable': True,
    'application': False,
    'auto_install': False,
    'license': 'LGPL-3',
}
