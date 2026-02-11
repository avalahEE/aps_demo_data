from datetime import timedelta

from odoo.fields import Datetime


def create_manufacturing_orders(env, products):
    """Create 30 manufacturing orders and confirm them to generate sub-MOs.

    Returns count of created parent MOs.
    """
    MO = env['mrp.production']
    now = Datetime.now()
    fp = products  # shorthand

    # Helper to compute deadline from weeks offset
    def deadline(weeks):
        return now + timedelta(weeks=weeks)

    mo_defs = [
        # (product_code, qty, weeks_offset, priority, customer, so_ref)
        ('FP-EXEC-DESK', 2, 2, '1', 'Meridian Law Group', 'SO-2026-0142'),
        ('FP-EXEC-DESK', 4, 4, '0', 'TechFlow Inc.', 'SO-2026-0155'),
        ('FP-EXEC-DESK', 1, 5, '0', '', ''),
        ('FP-BOOK-TALL', 6, 3, '1', 'City Public Library', 'SO-2026-0138'),
        ('FP-BOOK-TALL', 2, 5, '0', 'Hearthstone Interiors', 'SO-2026-0161'),
        ('FP-DINING-TBL', 3, 3, '1', 'Olive & Thyme Restaurant', 'SO-2026-0145'),
        ('FP-DINING-TBL', 1, 6, '0', 'Private customer', 'SO-2026-0170'),
        ('FP-TV-CONSOLE', 4, 2, '1', 'Nordic Living Showroom', 'SO-2026-0140'),
        ('FP-TV-CONSOLE', 3, 4, '0', '', ''),
        ('FP-TV-CONSOLE', 2, 5, '0', 'Greenfield Apartments', 'SO-2026-0158'),
        ('FP-WARDROBE', 2, 3, '1', 'Greenfield Apartments', 'SO-2026-0158'),
        ('FP-WARDROBE', 1, 4, '0', 'Private customer', 'SO-2026-0163'),
        ('FP-WARDROBE', 1, 6, '0', 'Hearthstone Interiors', 'SO-2026-0175'),
        ('FP-BED-KING', 3, 3, '1', 'Greenfield Apartments', 'SO-2026-0158'),
        ('FP-BED-KING', 1, 5, '0', 'Private customer', 'SO-2026-0168'),
        ('FP-DINING-CHR', 12, 3, '1', 'Olive & Thyme Restaurant', 'SO-2026-0145'),
        ('FP-DINING-CHR', 8, 4, '0', 'Nordic Living Showroom', 'SO-2026-0157'),
        ('FP-DINING-CHR', 6, 5, '0', '', ''),
        ('FP-KITCHEN-ISL', 2, 3, '1', 'Olive & Thyme Restaurant', 'SO-2026-0145'),
        ('FP-KITCHEN-ISL', 1, 5, '0', 'Private customer', 'SO-2026-0172'),
        ('FP-OFFICE-CAB', 6, 2, '1', 'Meridian Law Group', 'SO-2026-0142'),
        ('FP-OFFICE-CAB', 4, 4, '0', 'TechFlow Inc.', 'SO-2026-0155'),
        ('FP-OFFICE-CAB', 3, 6, '0', '', ''),
        ('FP-COFFEE-TBL', 4, 2, '1', 'Nordic Living Showroom', 'SO-2026-0140'),
        ('FP-COFFEE-TBL', 2, 4, '0', 'Hearthstone Interiors', 'SO-2026-0161'),
        ('FP-COFFEE-TBL', 3, 5, '0', '', ''),
        ('FP-EXEC-DESK', 3, 3, '1', 'Greenfield Apartments', 'SO-2026-0158'),
        ('FP-DINING-CHR', 4, 6, '0', 'Private customer', 'SO-2026-0180'),
        ('FP-TV-CONSOLE', 1, 3, '1', 'Private customer', 'SO-2026-0150'),
        ('FP-WARDROBE', 2, 4, '1', 'Nordic Living Showroom', 'SO-2026-0157'),
    ]

    mos = MO
    for product_code, qty, weeks, priority, customer, so_ref in mo_defs:
        product = fp[product_code]
        bom = env['mrp.bom']._bom_find(product)[product]

        origin_parts = []
        if so_ref:
            origin_parts.append(so_ref)
        if customer:
            origin_parts.append(customer)
        origin = ' - '.join(origin_parts) if origin_parts else False

        mo = MO.create({
            'product_id': product.id,
            'product_qty': qty,
            'bom_id': bom.id,
            'date_start': now,
            'date_deadline': deadline(weeks),
            'priority': priority,
            'origin': origin,
        })
        mos |= mo

    # Confirm all MOs — this triggers procurement and sub-MO generation
    mos.action_confirm()

    return len(mos)
