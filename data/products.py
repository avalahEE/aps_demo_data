def create_products(env):
    """Create 10 finished products and ~25 shared subassemblies.

    Subassemblies get Manufacture + MTO routes so action_confirm() on
    parent MOs auto-creates sub-MOs.

    Returns (products_dict, subassemblies_dict) — both code → product.product.
    """
    Product = env['product.product']

    # Get routes
    mto_route = _get_mto_route(env)
    manufacture_route = env.ref('mrp.route_warehouse0_manufacture')

    uom_unit = env.ref('uom.product_uom_unit')

    # --- Level 3 subassemblies (deepest, shared by Level 2) ---
    level3_defs = [
        ('SA-BACK-PANEL', 'Cabinet Back Panel 6mm'),
        ('SA-DRAWER-FRONT', 'Drawer Front (Pre-Edged)'),
        ('SA-EDGE-PANEL', 'Pre-Edged Panel'),
        ('SA-HINGE-SET', 'Hinge Set (Pair, Installed)'),
        ('SA-DRAWER-RUNNER-SET', 'Drawer Runner Pair (Installed)'),
    ]

    # --- Level 2 subassemblies (shared across multiple products) ---
    level2_defs = [
        ('SA-DRAWER-STD', 'Standard Drawer Box 400mm'),
        ('SA-DRAWER-LG', 'Large Drawer Box 500mm'),
        ('SA-DOOR-PANEL', 'Standard Door Panel'),
        ('SA-SHELF-ADJ', 'Adjustable Shelf'),
        ('SA-CARCASS-BASE', 'Base Cabinet Carcass'),
        ('SA-CARCASS-TALL', 'Tall Cabinet Carcass'),
        ('SA-TABLETOP-WAL', 'Walnut Table Top'),
        ('SA-LEG-FRAME-STEEL', 'Steel Leg Frame'),
        ('SA-LEG-FRAME-OAK', 'Oak Leg Frame'),
        ('SA-UPHOLSTERY-SEAT', 'Upholstered Seat Pad'),
    ]

    # --- Product-specific subassemblies (Level 2, unique to one product) ---
    specific_defs = [
        ('SA-DESK-TOP', 'Executive Desk Top (Oak Veneer)'),
        ('SA-DESK-MODESTY', 'Desk Modesty Panel'),
        ('SA-DESK-CABLE-MGMT', 'Cable Management Tray'),
        ('SA-BED-HEADBOARD', 'King Headboard (Upholstered)'),
        ('SA-BED-RAIL-SET', 'Bed Rail Set (Pair)'),
        ('SA-BED-SLAT-BASE', 'Slat Base System'),
        ('SA-TV-MEDIA-SHELF', 'TV Console Media Shelf'),
        ('SA-KITCHEN-BTOP', 'Butcher Block Countertop'),
        ('SA-WARDROBE-MIRROR', 'Wardrobe Mirror Panel'),
        ('SA-WARDROBE-INT-DRAWER', 'Wardrobe Internal Drawer'),
        ('SA-COFFEE-GLASS-SHELF', 'Coffee Table Glass Shelf'),
        ('SA-OFFICE-FILE-DRAWER', 'Filing Drawer (Suspension)'),
        ('SA-CHAIR-BACKREST', 'Dining Chair Backrest'),
        ('SA-BOOK-CROWN', 'Bookcase Crown Moulding'),
        ('SA-BOOK-BASE-PLINTH', 'Bookcase Base Plinth'),
    ]

    subassemblies = {}

    # Create all subassemblies with Manufacture + MTO routes
    all_sa_defs = level3_defs + level2_defs + specific_defs
    for code, name in all_sa_defs:
        product = Product.create({
            'name': name,
            'default_code': code,
            'type': 'consu',
            'is_storable': True,
            'uom_id': uom_unit.id,
            'route_ids': [(6, 0, [manufacture_route.id, mto_route.id])],
        })
        subassemblies[code] = product

    # --- Finished products (10) ---
    finished_defs = [
        ('FP-EXEC-DESK', 'Executive Office Desk'),
        ('FP-BOOK-TALL', 'Tall Bookcase'),
        ('FP-DINING-TBL', 'Dining Table - 8 Seat'),
        ('FP-TV-CONSOLE', 'TV Console Unit'),
        ('FP-WARDROBE', 'Wardrobe - 3 Door'),
        ('FP-BED-KING', 'King Bed Frame'),
        ('FP-DINING-CHR', 'Dining Chair'),
        ('FP-KITCHEN-ISL', 'Kitchen Island'),
        ('FP-OFFICE-CAB', 'Office Storage Cabinet'),
        ('FP-COFFEE-TBL', 'Coffee Table'),
    ]

    products = {}
    for code, name in finished_defs:
        product = Product.create({
            'name': name,
            'default_code': code,
            'type': 'consu',
            'is_storable': True,
            'uom_id': uom_unit.id,
            'route_ids': [(6, 0, [manufacture_route.id])],
        })
        products[code] = product

    return products, subassemblies


def _get_mto_route(env):
    """Get the MTO route, trying xmlid first then fallback to name search."""
    try:
        route = env.ref('stock.route_warehouse0_mto')
        if not route.active:
            route.active = True
        return route
    except ValueError:
        route = env['stock.route'].search(
            [('name', 'ilike', 'Make To Order')], limit=1
        )
        if route and not route.active:
            route.active = True
        if not route:
            raise ValueError("MTO route not found. Ensure stock module is installed.")
        return route
