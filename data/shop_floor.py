"""Variants, lot tracking, a partial delivery and work already in progress.

Stock and purchase orders (stock_and_pos) give the plan something to wait for.
This adds the rest of what a real shop floor shows a scheduler: a product whose
bill of materials differs per variant, a component tracked by lot, an order that
was only half delivered, and work orders that are running, finished off-estimate
or overdue.
"""

import logging
from datetime import timedelta

from odoo.fields import Datetime

_logger = logging.getLogger(__name__)

VARIANT_TEMPLATE = 'Shaker Cabinet Door'
LOT_CODE = 'HNG-SOFT-LOT'


def storable_vals(env):
    """Odoo 18 introduced is_storable; before that a storable product is a type."""
    if 'is_storable' in env['product.template']._fields:
        return {'type': 'consu', 'is_storable': True}
    return {'type': 'product'}


def _stock_location(env):
    warehouse = env['stock.warehouse'].search([], limit=1)
    return warehouse.lot_stock_id


def create_shop_floor_reality(env, workcenters=None):
    """Everything below is skipped individually, so an existing demo database
    picks up whatever it is missing on upgrade."""
    _create_variant_product(env, workcenters)
    _create_lot_tracked_component(env)
    _create_partial_delivery(env)
    _stage_work_in_progress(env)


# ---------------------------------------------------------------------------
# A product whose bill of materials differs per variant
# ---------------------------------------------------------------------------

def _create_variant_product(env, workcenters=None):
    if env['product.template'].search_count([('name', '=', VARIANT_TEMPLATE)]):
        _logger.info("Variant demo product already present, skipping.")
        return

    Product = env['product.product']
    finish = env['product.attribute'].create({'name': 'Finish', 'create_variant': 'always'})
    oak, walnut = env['product.attribute.value'].create([
        {'name': 'Oak', 'attribute_id': finish.id},
        {'name': 'Walnut', 'attribute_id': finish.id},
    ])

    oak_panel = Product.create(dict(storable_vals(env),
                                    name='Oak Door Panel', default_code='PNL-OAK-DOOR'))
    walnut_panel = Product.create(dict(storable_vals(env),
                                       name='Walnut Door Panel', default_code='PNL-WAL-DOOR'))
    screws = env['product.product'].search([('default_code', '=', 'FST-SCREW-35')], limit=1)
    if not screws:
        screws = Product.create(dict(storable_vals(env),
                                     name='Door Screws', default_code='FST-SCREW-DOOR'))

    template = env['product.template'].create(dict(
        storable_vals(env),
        name=VARIANT_TEMPLATE,
        attribute_line_ids=[(0, 0, {
            'attribute_id': finish.id,
            'value_ids': [(6, 0, [oak.id, walnut.id])],
        })],
    ))
    values = {v.product_attribute_value_id.name: v.id
              for v in template.attribute_line_ids.product_template_value_ids}

    wc = workcenters or {}
    router = wc.get('WC-CNC-01') or env['mrp.workcenter'].search([], limit=1)
    booth = wc.get('WC-FINISH-01') or env['mrp.workcenter'].search(
        [('id', '!=', router.id)], limit=1) or router

    bom = env['mrp.bom'].create({
        'product_tmpl_id': template.id,        # held on the template, not a variant
        'product_qty': 1,
        'code': 'BOM-SHAKER-DOOR',
        'bom_line_ids': [
            (0, 0, {'product_id': oak_panel.id, 'product_qty': 1,
                    'bom_product_template_attribute_value_ids': [(6, 0, [values['Oak']])]}),
            (0, 0, {'product_id': walnut_panel.id, 'product_qty': 1,
                    'bom_product_template_attribute_value_ids': [(6, 0, [values['Walnut']])]}),
            (0, 0, {'product_id': screws.id, 'product_qty': 4}),
        ],
        'operation_ids': [
            (0, 0, {'name': 'Profile door', 'workcenter_id': router.id,
                    'time_cycle_manual': 25, 'sequence': 10}),
            (0, 0, {'name': 'Lacquer walnut', 'workcenter_id': booth.id,
                    'time_cycle_manual': 40, 'sequence': 20,
                    'bom_product_template_attribute_value_ids': [(6, 0, [values['Walnut']])]}),
        ],
    })

    location = _stock_location(env)
    quants = env['stock.quant'].create([
        {'product_id': panel.id, 'location_id': location.id, 'inventory_quantity': 150}
        for panel in (oak_panel, walnut_panel)
    ])
    quants.action_apply_inventory()

    now = Datetime.now()
    for variant, qty, weeks in zip(template.product_variant_ids, (24, 12), (2, 3)):
        mo = env['mrp.production'].create({
            'product_id': variant.id,
            'bom_id': bom.id,
            'product_qty': qty,
            'date_start': now + timedelta(weeks=weeks),
        })
        mo.action_confirm()
        mo.button_plan()

    _logger.info("Created %s in %d finishes, with an order for each.",
                 VARIANT_TEMPLATE, len(template.product_variant_ids))


# ---------------------------------------------------------------------------
# A component tracked by lot, with two lots of different age
# ---------------------------------------------------------------------------

def _create_lot_tracked_component(env):
    if env['product.product'].search_count([('default_code', '=', LOT_CODE)]):
        _logger.info("Lot-tracked component already present, skipping.")
        return

    hinge = env['product.product'].create(dict(
        storable_vals(env),
        name='Soft-Close Hinge (lot tracked)',
        default_code=LOT_CODE,
        tracking='lot',
    ))

    now = Datetime.now()
    location = _stock_location(env)
    for name, qty, age_days in (('LOT-2026-014', 90, 45), ('LOT-2026-031', 60, 8)):
        lot = env['stock.lot'].create({'name': name, 'product_id': hinge.id})
        quant = env['stock.quant'].create({
            'product_id': hinge.id,
            'location_id': location.id,
            'lot_id': lot.id,
            'inventory_quantity': qty,
        })
        quant.action_apply_inventory()
        quant.in_date = now - timedelta(days=age_days)

    # Put it on a real bill of materials, so orders actually compete for the lots
    bom = env['mrp.bom'].search([('code', 'like', 'BOM-FP-OFFICE-CAB%')], limit=1) \
        or env['mrp.bom'].search([('product_tmpl_id.name', 'ilike', 'cabinet')], limit=1) \
        or env['mrp.bom'].search([], limit=1)
    if bom:
        env['mrp.bom.line'].create({
            'bom_id': bom.id, 'product_id': hinge.id, 'product_qty': 8,
        })
    _logger.info("Created lot-tracked component %s with two lots.", LOT_CODE)


# ---------------------------------------------------------------------------
# A purchase order that only half arrived
# ---------------------------------------------------------------------------

def _create_partial_delivery(env):
    if env['stock.picking'].search_count([('backorder_id', '!=', False)]):
        _logger.info("A backorder already exists, skipping partial delivery.")
        return

    order = env['purchase.order'].search([('state', 'in', ('purchase', 'done'))], order='id', limit=1)
    picking = order.picking_ids.filtered(lambda p: p.state not in ('done', 'cancel'))[:1] if order else None
    if not picking:
        _logger.info("No open receipt to receive partially, skipping.")
        return

    move = picking.move_ids[:1]
    move.quantity = max(move.product_uom_qty / 2.0, 1)
    move.picked = True
    result = picking.button_validate()
    if isinstance(result, dict) and result.get('res_model') == 'stock.backorder.confirmation':
        wizard = env[result['res_model']].with_context(**(result.get('context') or {})).create({
            'pick_ids': [(4, picking.id)],
            'show_transfers': False,
        })
        wizard.process()
    _logger.info("Received half of %s, leaving a backorder open.", order.name)


# ---------------------------------------------------------------------------
# Work that is running, finished off-estimate, or overdue
# ---------------------------------------------------------------------------

def _stage_work_in_progress(env):
    MO = env['mrp.production']
    if MO.search_count([('state', '=', 'progress')]):
        _logger.info("Demo orders already carry progress, skipping.")
        return

    candidates = MO.search(
        [('state', 'in', ('confirmed', 'progress')), ('workorder_ids', '!=', False)], order='id')
    if len(candidates) < 5:
        _logger.info("Not enough orders to stage progress, skipping.")
        return

    staged = candidates[:5]
    for mo in staged:
        if not mo.workorder_ids[0].date_start:
            mo.button_plan()

    running, early, late_finish, partial, overdue = staged

    # Running and ahead of estimate
    wo = running.workorder_ids.sorted('id')[0]
    wo.button_start()
    wo.duration = wo.duration_expected * 0.9

    # Finished in a third of the time — what follows it should move up
    wo = early.workorder_ids.sorted('id')[0]
    wo.button_start()
    wo.duration = wo.duration_expected / 3
    wo.qty_producing = early.product_qty
    wo.button_finish()

    # Finished at twice the estimate — everything behind it has to give way
    wo = late_finish.workorder_ids.sorted('id')[0]
    wo.button_start()
    wo.duration = wo.duration_expected * 2
    wo.qty_producing = late_finish.product_qty
    wo.button_finish()

    # Half produced by quantity, barely any time logged
    if partial.product_qty >= 2:
        wo = partial.workorder_ids.sorted('id')[0]
        wo.button_start()
        wo.duration = wo.duration_expected * 0.2
        wo.qty_produced = partial.product_qty // 2

    # Should have started three days ago and nobody touched it
    wo = overdue.workorder_ids.sorted('id')[0]
    start = Datetime.now() - timedelta(days=3)
    env.cr.execute(
        "UPDATE mrp_workorder SET date_start = %s, date_finished = %s WHERE id = %s",
        (start, start + timedelta(minutes=int(wo.duration_expected or 60)), wo.id))
    env.cr.execute(
        "UPDATE mrp_production SET date_start = %s WHERE id = %s", (start, overdue.id))

    _logger.info(
        "Staged progress: %s running, %s finished early, %s finished late, "
        "%s half produced, %s overdue and unstarted.",
        running.name, early.name, late_finish.name, partial.name, overdue.name)
