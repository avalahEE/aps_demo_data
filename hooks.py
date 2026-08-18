import logging

from .data.calendars import create_calendars
from .data.workcenters import create_workcenters
from .data.materials import create_materials
from .data.products import create_products
from .data.boms import create_boms
from .data.manufacturing_orders import create_manufacturing_orders
from .data.maintenance import create_maintenance
from .data.shop_floor import create_shop_floor_reality
from .data.stock_and_pos import create_stock_and_pos

_logger = logging.getLogger(__name__)


def post_init_hook(env):
    """Seed complete furniture manufacturing demo data.

    Called on module install and upgrade. Idempotent — skips if
    work center WC-SAW-01 already exists.
    """
    if env['mrp.workcenter'].search_count([('code', '=', 'WC-SAW-01')]):
        # The backbone is there, but a database seeded by an older version is
        # missing everything below; each part checks for itself
        _logger.info("Manufacturing backbone already present, topping up the rest.")
        create_shop_floor_reality(env)
        return

    _logger.info("Creating APS demo data — furniture manufacturing dataset...")

    # Enable required Odoo settings
    _enable_settings(env)

    calendars = create_calendars(env)
    _logger.info("Created %d resource calendars.", len(calendars))

    workcenters = create_workcenters(env, calendars)
    _logger.info("Created %d work centers.", len(workcenters))

    materials = create_materials(env)
    _logger.info("Created %d raw materials.", len(materials))

    products, subassemblies = create_products(env)
    _logger.info("Created %d finished products and %d subassemblies.",
                 len(products), len(subassemblies))

    boms = create_boms(env, materials, products, subassemblies, workcenters)
    _logger.info("Created %d bills of materials.", len(boms))

    mo_count = create_manufacturing_orders(env, products)
    _logger.info("Created and confirmed %d manufacturing orders.", mo_count)

    create_maintenance(env, workcenters)
    _logger.info("Created maintenance window for CNC router.")

    create_stock_and_pos(env, materials)
    _logger.info("Created stock levels and purchase orders for material-aware scheduling.")

    create_shop_floor_reality(env, workcenters)

    _logger.info("APS demo data creation complete!")


def _enable_settings(env):
    """Enable required Odoo settings for demo data to work."""
    _logger.info("Enabling required settings...")

    # Enable Work Orders (needed for BOM routing operations)
    group_routings = env.ref('mrp.group_mrp_routings')
    internal_user = env.ref('base.group_user')
    internal_user.write({'implied_ids': [(4, group_routings.id)]})

    # Enable MTO route
    try:
        mto_route = env.ref('stock.route_warehouse0_mto')
        if not mto_route.active:
            mto_route.active = True
    except ValueError:
        pass

    # Enable multi-step routes (needed for Buy route)
    group_adv_location = env.ref('stock.group_adv_location', raise_if_not_found=False)
    if group_adv_location:
        group_multi_loc = env.ref('stock.group_stock_multi_locations', raise_if_not_found=False)
        if group_multi_loc:
            internal_user.write({'implied_ids': [(4, group_multi_loc.id)]})
        internal_user.write({'implied_ids': [(4, group_adv_location.id)]})

    _logger.info("Settings enabled.")
