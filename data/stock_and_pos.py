"""Demo stock levels and purchase orders for material-aware scheduling.

Design intent
-------------
Creates three "tiers" of material availability so that
respectMaterialAvailability = True produces visible, interesting
scheduling behaviour when the demo dataset is synced into APS.

Tier 1 — In stock (no constraint)
  Hardware, fasteners, adhesives, edge banding, packaging.
  These are "consumables" a workshop always keeps on the shelf.

Tier 2 — Partially stocked + PO arriving in 5 days
  MDF 18 mm and Birch Plywood 12 mm — the two sheet goods used in
  virtually every carcass and drawer box.  Enough stock for ~2–3
  units of each top-level product; the rest must wait for the PO.

Tier 3 — No stock, PO only (arrive at various delays)
  • Sheet goods (other sizes)     +5 days
  • Metal components / electrical +7 days
  • Solid wood boards             +8 days
  • Veneers & surface treatments  +10 days
  • Finishes (stains, lacquers)   +12 days
  • Upholstery / foam / glass     +16 days

The result: a schedule run with the flag ON will show most MOs
delayed anywhere from 5 to 16 days depending on their BOM
composition, while assembly-only operations (fasteners/hardware)
are unconstrained.
"""

import logging
from datetime import timedelta

from odoo.fields import Datetime

_logger = logging.getLogger(__name__)


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def _stock_location(env):
    """Return WH/Stock location for the current company."""
    return env.ref('stock.stock_location_stock')


def _get_or_create_demo_vendor(env):
    """Return (or create) the demo purchasing partner."""
    Partner = env['res.partner']
    vendor = Partner.search([('name', '=', 'APS Demo Supplier')], limit=1)
    if not vendor:
        vendor = Partner.create({
            'name': 'APS Demo Supplier',
            'company_type': 'company',
            'supplier_rank': 1,
        })
    return vendor


def _add_stock(env, product, qty, location):
    """Create or update a stock.quant record for a product."""
    Quant = env['stock.quant']
    existing = Quant.search([
        ('product_id', '=', product.id),
        ('location_id', '=', location.id),
    ], limit=1)
    if existing:
        existing.quantity = qty
    else:
        Quant.with_context(inventory_mode=True).create({
            'product_id': product.id,
            'location_id': location.id,
            'quantity': qty,
        })


def _create_po(env, vendor, lines, days_until_delivery):
    """Create and confirm a purchase order with the given lines.

    lines: list of (product, qty)
    """
    now = Datetime.now()
    delivery_date = now + timedelta(days=days_until_delivery)

    po = env['purchase.order'].create({
        'partner_id': vendor.id,
        'date_planned': delivery_date,
        'order_line': [
            (0, 0, {
                'product_id': product.id,
                'product_qty': qty,
                'price_unit': 1.0,
                'date_planned': delivery_date,
                'name': product.display_name,
                'product_uom_id': product.uom_id.id,
            })
            for product, qty in lines
            if product  # skip any None entries gracefully
        ],
    })
    po.button_confirm()
    return po


# ---------------------------------------------------------------------------
# Categorised material lists (mirror materials.py groupings)
# ---------------------------------------------------------------------------

_FASTENER_CODES = [
    'FST-SCREW-30', 'FST-SCREW-35', 'FST-SCREW-40', 'FST-SCREW-50',
    'FST-SCREW-16', 'FST-CONFIRMAT-50', 'FST-CONFIRMAT-70',
    'FST-DOWEL-8x30', 'FST-DOWEL-8x40', 'FST-DOWEL-10x40',
    'FST-BISCUIT-0', 'FST-BISCUIT-10', 'FST-BISCUIT-20',
    'FST-NAIL-BRAD-25', 'FST-NAIL-BRAD-32', 'FST-NAIL-PIN-20',
    'FST-STAPLE-10', 'FST-BOLT-M6x50', 'FST-BOLT-M8x60',
    'FST-NUT-M6', 'FST-NUT-M8', 'FST-WASHER-M6', 'FST-WASHER-M8',
    'FST-TNUT-M6', 'FST-TNUT-M8', 'FST-BOLT-M8x50',
    'FST-BRAD-18', 'FST-WALL-ANCHOR',
]

_HARDWARE_CODES = [
    # Hinges
    'HNG-SOFT-110', 'HNG-SOFT-155', 'HNG-CONC-110', 'HNG-CONC-170',
    'HNG-CONC-90', 'HNG-BUTT-75', 'HNG-BUTT-100', 'HNG-PIANO-32',
    'HNG-FLAP-STAY', 'HNG-GLASS-INSET', 'HNG-DTOP-BASE', 'HNG-MOUNT-PLATE',
    # Drawer slides
    'SLD-SOFT-300', 'SLD-SOFT-400', 'SLD-SOFT-500', 'SLD-SOFT-600',
    'SLD-BALL-400', 'SLD-BALL-500', 'SLD-UNDER-400', 'SLD-UNDER-500',
    # Handles
    'HDL-BAR-96', 'HDL-BAR-128', 'HDL-BAR-160', 'HDL-BAR-256',
    'HDL-BAR-BLK-128', 'HDL-BAR-BLK-256', 'HDL-CUP-96',
    'HDL-KNOB-30', 'HDL-KNOB-35', 'HDL-KNOB-BLK-30', 'HDL-KNOB-WOOD-40',
    'HDL-RECESSED-50', 'HDL-EDGE-TAB', 'HDL-LEATHER-128', 'HDL-PUSH-OPEN',
    # Connectors
    'CON-CAM-15', 'CON-CAM-BOLT-34', 'CON-MINIFIX-15', 'CON-MINIFIX-BOLT',
    'CON-RAFIX-20', 'CON-SHELF-5', 'CON-SHELF-SPOON', 'CON-BRACKET-L',
    'CON-BRACKET-FLAT', 'CON-MODESTY-BLK', 'CON-KD-BOLT-M6',
    'CON-CROSS-DOWEL', 'CON-BED-BOLT', 'CON-BOLT-FURNITURE', 'CON-LOCK-CYLINDER',
    # Casters & levellers
    'CAS-CASTER-50', 'CAS-CASTER-75', 'CAS-CASTER-PLATE',
    'CAS-LEVELER-M8', 'CAS-LEVELER-M10', 'CAS-CASTER-LOCK-75',
    'CAS-FELT-PAD-25', 'CAS-GLIDE-25',
]

_ADHESIVE_STOCKED_CODES = [
    'ADH-PVA-D3', 'ADH-PVA-D4', 'ADH-HOTMELT-EDGE', 'ADH-HOTMELT-STICKS',
]

_EDGE_BANDING_CODES = [
    'EDGE-OAK-22', 'EDGE-OAK-42', 'EDGE-WALNUT-22', 'EDGE-WALNUT-42',
    'EDGE-BEECH-22', 'EDGE-MAPLE-22', 'EDGE-PVC-WHT-22', 'EDGE-PVC-BLK-22',
    'EDGE-PVC-WHT-42', 'EDGE-PVC-OAK-22', 'EDGE-OAK-45',
    'EDGE-ABS-WHT-22', 'EDGE-ABS-ALU-22',
]

_PACKAGING_CODES = [
    'PKG-CARDBOARD-SMALL', 'PKG-CARDBOARD-MED', 'PKG-CARDBOARD-LARGE',
    'PKG-CARDBOARD-FLAT', 'PKG-FOAM-CORNER', 'PKG-BUBBLE-WRAP',
    'PKG-STRETCH-WRAP', 'PKG-BLANKET', 'PKG-TAPE-BROWN',
]

# Sheet goods — small buffer stock to cover ~2-3 top-level units
_SHEET_GOODS_BUFFER = {
    'SHT-HDF-3': 60.0,   # back panels — relatively generous
    'SHT-MDF-18': 12.0,  # critical bottleneck — ~4 single carcasses worth
    'SHT-PLY-BIRCH-12': 4.0,  # drawer boxes — enough for ~2 products
    'SHT-MDF-6': 8.0,
}

# Sheet goods PO — all sizes, +5 days
_SHEET_GOODS_PO = {
    'SHT-MDF-6': 80.0,
    'SHT-MDF-12': 60.0,
    'SHT-MDF-18': 400.0,
    'SHT-MDF-25': 60.0,
    'SHT-MDF-MOIST-18': 40.0,
    'SHT-MDF-FIRE-18': 30.0,
    'SHT-HDF-3': 120.0,
    'SHT-PLY-BIRCH-12': 200.0,
    'SHT-PLY-BIRCH-18': 100.0,
    'SHT-PLY-BIRCH-24': 40.0,
    'SHT-PLY-POPLAR-12': 60.0,
    'SHT-PLY-POPLAR-18': 60.0,
    'SHT-PLY-MARINE-18': 30.0,
    'SHT-CHIP-16': 80.0,
    'SHT-CHIP-18': 120.0,
    'SHT-CHIP-25': 50.0,
    'SHT-MELAM-WHT-18': 100.0,
    'SHT-MELAM-BLK-18': 60.0,
    'SHT-MELAM-OAK-18': 80.0,
    'SHT-MELAM-WAL-18': 60.0,
    'SHT-OSB-18': 40.0,
}

# Metal components + electrical, +7 days
_METAL_ELEC_PO = {
    'MTL-LEG-HAIRPIN-710': 40,
    'MTL-LEG-HAIRPIN-400': 40,
    'MTL-LEG-TAPER-710': 40,
    'MTL-TUBE-25x25': 50,
    'MTL-TUBE-40x20': 50,
    'MTL-BRACKET-SHELF': 80,
    'MTL-FRAME-DESK': 30,
    'MTL-BRACKET-CORNER': 100,
    'MTL-RAIL-WARDROBE': 60,
    'MTL-SUSP-RAIL': 40,
    'MTL-TOWEL-RAIL': 30,
    'MTL-CHANNEL-WALL': 40,
    'ELEC-LED-STRIP-3000K': 30,
    'ELEC-LED-STRIP-4000K': 30,
    'ELEC-LED-DRIVER-30W': 40,
    'ELEC-SWITCH-TOUCH': 40,
    'ELEC-GROMMET-USB': 50,
    'ELEC-GROMMET-60': 60,
}

# Solid wood, +8 days
_SOLID_WOOD_PO = {
    'WOOD-OAK-25x50': 200.0,
    'WOOD-OAK-25x100': 180.0,
    'WOOD-OAK-40x60': 120.0,
    'WOOD-OAK-50x100': 100.0,
    'WOOD-OAK-50x50': 80.0,
    'WOOD-OAK-25x150': 100.0,
    'WOOD-WALNUT-25x50': 100.0,
    'WOOD-WALNUT-25x100': 120.0,
    'WOOD-WALNUT-40x150': 80.0,
    'WOOD-BEECH-25x50': 120.0,
    'WOOD-BEECH-25x100': 150.0,
    'WOOD-BEECH-30x80': 100.0,
    'WOOD-BEECH-25x80': 100.0,
    'WOOD-BEECH-40x50': 80.0,
    'WOOD-MAPLE-25x50': 80.0,
    'WOOD-MAPLE-25x100': 80.0,
    'WOOD-ASH-25x100': 80.0,
    'WOOD-ASH-40x60': 60.0,
    'WOOD-CHERRY-25x50': 60.0,
    'WOOD-CHERRY-25x100': 60.0,
    'WOOD-PINE-25x100': 100.0,
    'WOOD-PINE-40x150': 80.0,
}

# Veneer + non-stocked adhesives, +10 days
_VENEER_FINISH_PO = {
    'VNR-OAK-06': 60.0,
    'VNR-WALNUT-06': 40.0,
    'VNR-BEECH-06': 40.0,
    'VNR-MAPLE-06': 30.0,
    'VNR-CHERRY-06': 30.0,
    'VNR-ASH-06': 30.0,
    'VNR-BIRCH-06': 30.0,
    'VNR-TEAK-06': 20.0,
    'VNR-BAMBOO-06': 20.0,
    'VNR-OAK-SMOKED-06': 20.0,
    'ADH-PU-FAST': 20.0,
    'ADH-PU-EXPAND': 15.0,
    'ADH-CONTACT': 20.0,
    'ADH-CONTACT-WATER': 20.0,
    'ADH-EPOXY-5MIN': 10.0,
    'ADH-CA-THICK': 8.0,
    'ADH-MIRROR': 8.0,
}

# Stains + lacquers + paints, +12 days
_FINISHES_PO = {
    'STN-NATURAL-OAK': 20.0, 'STN-GOLDEN-OAK': 20.0, 'STN-DARK-OAK': 20.0,
    'STN-WALNUT': 20.0, 'STN-MAHOGANY': 15.0, 'STN-EBONY': 15.0,
    'STN-WHITE-WASH': 15.0, 'STN-GREY-WASH': 15.0,
    'STN-ANTIQUE-PINE': 15.0, 'STN-TEAK': 15.0,
    'LAC-CLEAR-MATT': 20.0, 'LAC-CLEAR-SATIN': 20.0, 'LAC-CLEAR-GLOSS': 20.0,
    'LAC-2K-CLEAR': 20.0, 'LAC-WATER-MATT': 20.0, 'LAC-WATER-SATIN': 20.0,
    'LAC-PRIMER-SAND': 15.0, 'LAC-HARDWAX-OIL': 15.0,
    'PNT-WHITE-MATT': 20.0, 'PNT-WHITE-SATIN': 20.0,
    'PNT-BLACK-MATT': 15.0, 'PNT-BLACK-SATIN': 15.0,
    'PNT-GREY-MATT': 15.0, 'PNT-PRIMER-WHITE': 20.0,
    'PNT-PRIMER-GREY': 15.0, 'PNT-FILLER-SPRAY': 12.0,
}

# Upholstery + foam + glass, +16 days
_SOFT_GOODS_GLASS_PO = {
    'FAB-LINEN-GREY': 50.0, 'FAB-LINEN-BEIGE': 50.0, 'FAB-LINEN-NAVY': 40.0,
    'FAB-VELVET-GREEN': 40.0, 'FAB-VELVET-BLUE': 40.0, 'FAB-VELVET-GREY': 40.0,
    'FAB-TWEED-BROWN': 30.0, 'FAB-LEATHER-BLK': 30.0, 'FAB-LEATHER-TAN': 30.0,
    'FAB-WEBBING-JUTE': 60.0, 'FAB-CANVAS-NAT': 50.0,
    'FOAM-HR-30': 40.0, 'FOAM-HR-50': 40.0, 'FOAM-HR-100': 30.0,
    'FOAM-MEMORY-50': 30.0, 'FOAM-DACRON-WRAP': 50.0, 'FOAM-FELT-PAD': 40.0,
    'GLS-TEMPERED-4': 25.0, 'GLS-TEMPERED-6': 20.0, 'GLS-TEMPERED-8': 15.0,
    'GLS-MIRROR-4': 20.0, 'GLS-FROSTED-4': 15.0, 'GLS-TINTED-GREY-6': 15.0,
}


# ---------------------------------------------------------------------------
# Main entry point
# ---------------------------------------------------------------------------

def create_stock_and_pos(env, materials):
    """Seed stock levels and purchase orders for material-aware scheduling.

    materials: dict of code -> product.product (from create_materials)
    """
    location = _stock_location(env)
    vendor = _get_or_create_demo_vendor(env)

    m = materials  # shorthand

    # -----------------------------------------------------------------------
    # Tier 1 — In stock (no scheduling constraint)
    # -----------------------------------------------------------------------
    stocked_count = 0

    for code in _FASTENER_CODES:
        if code in m:
            _add_stock(env, m[code], 5000, location)
            stocked_count += 1

    for code in _HARDWARE_CODES:
        if code in m:
            _add_stock(env, m[code], 300, location)
            stocked_count += 1

    for code in _ADHESIVE_STOCKED_CODES:
        if code in m:
            _add_stock(env, m[code], 50, location)
            stocked_count += 1

    for code in _EDGE_BANDING_CODES:
        if code in m:
            _add_stock(env, m[code], 500, location)
            stocked_count += 1

    for code in _PACKAGING_CODES:
        if code in m:
            _add_stock(env, m[code], 200, location)
            stocked_count += 1

    # Small buffer stock for critical sheet goods (covers ~2-3 top-level units)
    for code, qty in _SHEET_GOODS_BUFFER.items():
        if code in m:
            _add_stock(env, m[code], qty, location)
            stocked_count += 1

    _logger.info("Created stock records for %d material SKUs.", stocked_count)

    # -----------------------------------------------------------------------
    # Tier 2 & 3 — Purchase orders (arriving at increasing delays)
    # -----------------------------------------------------------------------
    po_specs = [
        (_SHEET_GOODS_PO, 5,   "PO-DEMO-SHEETS"),
        (_METAL_ELEC_PO,  7,   "PO-DEMO-METAL"),
        (_SOLID_WOOD_PO,  8,   "PO-DEMO-WOOD"),
        (_VENEER_FINISH_PO, 10, "PO-DEMO-VENEER"),
        (_FINISHES_PO,    12,  "PO-DEMO-FINISHES"),
        (_SOFT_GOODS_GLASS_PO, 16, "PO-DEMO-SOFT"),
    ]

    po_count = 0
    for code_qty_map, days, ref in po_specs:
        lines = [
            (m[code], qty)
            for code, qty in code_qty_map.items()
            if code in m
        ]
        if lines:
            po = _create_po(env, vendor, lines, days)
            po.name = ref  # override auto-generated name for clarity
            po_count += 1
            _logger.info(
                "Created %s: %d lines, arriving in %d days.",
                ref, len(lines), days,
            )

    _logger.info(
        "Material-aware scheduling demo: %d stock records + %d purchase orders created.",
        stocked_count, po_count,
    )
