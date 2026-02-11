import logging

_logger = logging.getLogger(__name__)

CATEGORIES = [
    {
        'name': 'Solid Wood',
        'uom_xmlid': 'uom.product_uom_kgm',
        'items': [
            ('WOOD-OAK-25x50', 'Solid Oak Board 25x50mm'),
            ('WOOD-OAK-25x100', 'Solid Oak Board 25x100mm'),
            ('WOOD-OAK-40x60', 'Solid Oak Board 40x60mm'),
            ('WOOD-OAK-50x100', 'Solid Oak Plank 50x100mm'),
            ('WOOD-WALNUT-25x50', 'Solid Walnut Board 25x50mm'),
            ('WOOD-WALNUT-25x100', 'Solid Walnut Board 25x100mm'),
            ('WOOD-WALNUT-40x150', 'Solid Walnut Plank 40x150mm'),
            ('WOOD-BEECH-25x50', 'Solid Beech Board 25x50mm'),
            ('WOOD-BEECH-25x100', 'Solid Beech Board 25x100mm'),
            ('WOOD-BEECH-30x80', 'Solid Beech Board 30x80mm'),
            ('WOOD-MAPLE-25x50', 'Solid Maple Board 25x50mm'),
            ('WOOD-MAPLE-25x100', 'Solid Maple Board 25x100mm'),
            ('WOOD-ASH-25x100', 'Solid Ash Board 25x100mm'),
            ('WOOD-ASH-40x60', 'Solid Ash Board 40x60mm'),
            ('WOOD-CHERRY-25x50', 'Solid Cherry Board 25x50mm'),
            ('WOOD-CHERRY-25x100', 'Solid Cherry Board 25x100mm'),
            ('WOOD-OAK-50x50', 'Solid Oak Square Stock 50x50mm'),
            ('WOOD-OAK-25x150', 'Solid Oak Plank 25x150mm'),
            ('WOOD-BEECH-25x80', 'Solid Beech Board 25x80mm'),
            ('WOOD-BEECH-40x50', 'Solid Beech Strip 40x50mm'),
            ('WOOD-PINE-25x100', 'Solid Pine Board 25x100mm'),
            ('WOOD-PINE-40x150', 'Solid Pine Plank 40x150mm'),
        ],
    },
    {
        'name': 'Sheet Goods',
        'uom_xmlid': None,  # m² — resolved at runtime
        'items': [
            ('SHT-MDF-12', 'MDF Board 12mm'),
            ('SHT-MDF-18', 'MDF Board 18mm'),
            ('SHT-MDF-25', 'MDF Board 25mm'),
            ('SHT-HDF-3', 'HDF Board 3mm'),
            ('SHT-PLY-BIRCH-12', 'Birch Plywood 12mm'),
            ('SHT-PLY-BIRCH-18', 'Birch Plywood 18mm'),
            ('SHT-PLY-BIRCH-24', 'Birch Plywood 24mm'),
            ('SHT-PLY-POPLAR-12', 'Poplar Plywood 12mm'),
            ('SHT-PLY-POPLAR-18', 'Poplar Plywood 18mm'),
            ('SHT-CHIP-16', 'Chipboard 16mm'),
            ('SHT-CHIP-18', 'Chipboard 18mm'),
            ('SHT-CHIP-25', 'Chipboard 25mm'),
            ('SHT-MELAM-WHT-18', 'White Melamine Chipboard 18mm'),
            ('SHT-MELAM-BLK-18', 'Black Melamine Chipboard 18mm'),
            ('SHT-MELAM-OAK-18', 'Oak Decor Melamine Chipboard 18mm'),
            ('SHT-MELAM-WAL-18', 'Walnut Decor Melamine Chipboard 18mm'),
            ('SHT-OSB-18', 'OSB/3 Board 18mm'),
            ('SHT-PLY-MARINE-18', 'Marine Plywood 18mm'),
            ('SHT-MDF-6', 'MDF Board 6mm'),
            ('SHT-MDF-MOIST-18', 'Moisture Resistant MDF 18mm'),
            ('SHT-MDF-FIRE-18', 'Fire Rated MDF 18mm'),
        ],
    },
    {
        'name': 'Veneer',
        'uom_xmlid': None,  # m²
        'items': [
            ('VNR-OAK-06', 'Oak Veneer 0.6mm'),
            ('VNR-WALNUT-06', 'Walnut Veneer 0.6mm'),
            ('VNR-BEECH-06', 'Beech Veneer 0.6mm'),
            ('VNR-MAPLE-06', 'Maple Veneer 0.6mm'),
            ('VNR-CHERRY-06', 'Cherry Veneer 0.6mm'),
            ('VNR-ASH-06', 'Ash Veneer 0.6mm'),
            ('VNR-BIRCH-06', 'Birch Veneer 0.6mm'),
            ('VNR-TEAK-06', 'Teak Veneer 0.6mm'),
            ('VNR-BAMBOO-06', 'Bamboo Veneer 0.6mm'),
            ('VNR-OAK-SMOKED-06', 'Smoked Oak Veneer 0.6mm'),
        ],
    },
    {
        'name': 'Edge Banding',
        'uom_xmlid': 'uom.product_uom_meter',
        'items': [
            ('EDGE-OAK-22', 'Oak Edge Banding 22mm'),
            ('EDGE-OAK-42', 'Oak Edge Banding 42mm'),
            ('EDGE-WALNUT-22', 'Walnut Edge Banding 22mm'),
            ('EDGE-WALNUT-42', 'Walnut Edge Banding 42mm'),
            ('EDGE-BEECH-22', 'Beech Edge Banding 22mm'),
            ('EDGE-MAPLE-22', 'Maple Edge Banding 22mm'),
            ('EDGE-PVC-WHT-22', 'White PVC Edge Banding 22mm'),
            ('EDGE-PVC-BLK-22', 'Black PVC Edge Banding 22mm'),
            ('EDGE-PVC-WHT-42', 'White PVC Edge Banding 42mm'),
            ('EDGE-PVC-OAK-22', 'Oak Decor PVC Edge Banding 22mm'),
            ('EDGE-OAK-45', 'Oak Edge Banding 45mm'),
            ('EDGE-ABS-WHT-22', 'White ABS Edge Banding 22mm'),
            ('EDGE-ABS-ALU-22', 'Aluminium Decor ABS Edge Banding 22mm'),
        ],
    },
    {
        'name': 'Fasteners',
        'uom_xmlid': 'uom.product_uom_unit',
        'items': [
            ('FST-SCREW-30', 'Wood Screw 4x30mm'),
            ('FST-SCREW-35', 'Wood Screw 4x35mm'),
            ('FST-SCREW-40', 'Wood Screw 4x40mm'),
            ('FST-SCREW-50', 'Wood Screw 4.5x50mm'),
            ('FST-SCREW-16', 'Chipboard Screw 3.5x16mm'),
            ('FST-CONFIRMAT-50', 'Confirmat Screw 7x50mm'),
            ('FST-CONFIRMAT-70', 'Confirmat Screw 7x70mm'),
            ('FST-DOWEL-8x30', 'Fluted Dowel Pin 8x30mm'),
            ('FST-DOWEL-8x40', 'Fluted Dowel Pin 8x40mm'),
            ('FST-DOWEL-10x40', 'Fluted Dowel Pin 10x40mm'),
            ('FST-BISCUIT-0', 'Biscuit Joiner #0'),
            ('FST-BISCUIT-10', 'Biscuit Joiner #10'),
            ('FST-BISCUIT-20', 'Biscuit Joiner #20'),
            ('FST-NAIL-BRAD-25', 'Brad Nail 18ga 25mm'),
            ('FST-NAIL-BRAD-32', 'Brad Nail 18ga 32mm'),
            ('FST-NAIL-PIN-20', 'Pin Nail 23ga 20mm'),
            ('FST-STAPLE-10', 'Staple 10mm'),
            ('FST-BOLT-M6x50', 'Hex Bolt M6x50mm'),
            ('FST-BOLT-M8x60', 'Hex Bolt M8x60mm'),
            ('FST-NUT-M6', 'Hex Nut M6'),
            ('FST-NUT-M8', 'Hex Nut M8'),
            ('FST-WASHER-M6', 'Flat Washer M6'),
            ('FST-WASHER-M8', 'Flat Washer M8'),
            ('FST-TNUT-M6', 'T-Nut M6'),
            ('FST-TNUT-M8', 'T-Nut M8'),
            ('FST-BOLT-M8x50', 'Hex Bolt M8x50mm'),
            ('FST-BRAD-18', 'Brad Nail 18ga 18mm'),
            ('FST-WALL-ANCHOR', 'Wall Anchor with Screw'),
        ],
    },
    {
        'name': 'Hinges',
        'uom_xmlid': 'uom.product_uom_unit',
        'items': [
            ('HNG-SOFT-110', 'Soft-Close Concealed Hinge 110\u00b0'),
            ('HNG-SOFT-155', 'Soft-Close Concealed Hinge 155\u00b0'),
            ('HNG-CONC-110', 'Concealed Hinge 110\u00b0'),
            ('HNG-CONC-170', 'Concealed Hinge 170\u00b0'),
            ('HNG-CONC-90', 'Concealed Hinge 90\u00b0 Corner'),
            ('HNG-BUTT-75', 'Butt Hinge 75mm Brushed Nickel'),
            ('HNG-BUTT-100', 'Butt Hinge 100mm Brushed Nickel'),
            ('HNG-PIANO-32', 'Piano Hinge 32mm Zinc Plated'),
            ('HNG-FLAP-STAY', 'Flap Stay Hinge with Brake'),
            ('HNG-GLASS-INSET', 'Glass Door Hinge Inset'),
            ('HNG-DTOP-BASE', 'Drop-Leaf Table Hinge Base'),
            ('HNG-MOUNT-PLATE', 'Hinge Mounting Plate Clip-On'),
        ],
    },
    {
        'name': 'Drawer Slides',
        'uom_xmlid': 'uom.product_uom_unit',
        'items': [
            ('SLD-SOFT-300', 'Soft-Close Full Extension Slide 300mm'),
            ('SLD-SOFT-400', 'Soft-Close Full Extension Slide 400mm'),
            ('SLD-SOFT-500', 'Soft-Close Full Extension Slide 500mm'),
            ('SLD-SOFT-600', 'Soft-Close Full Extension Slide 600mm'),
            ('SLD-BALL-400', 'Ball Bearing Slide 400mm'),
            ('SLD-BALL-500', 'Ball Bearing Slide 500mm'),
            ('SLD-UNDER-400', 'Undermount Soft-Close Slide 400mm'),
            ('SLD-UNDER-500', 'Undermount Soft-Close Slide 500mm'),
        ],
    },
    {
        'name': 'Handles & Knobs',
        'uom_xmlid': 'uom.product_uom_unit',
        'items': [
            ('HDL-BAR-96', 'Bar Handle Brushed Nickel 96mm'),
            ('HDL-BAR-128', 'Bar Handle Brushed Nickel 128mm'),
            ('HDL-BAR-160', 'Bar Handle Brushed Nickel 160mm'),
            ('HDL-BAR-256', 'Bar Handle Brushed Nickel 256mm'),
            ('HDL-BAR-BLK-128', 'Bar Handle Matte Black 128mm'),
            ('HDL-BAR-BLK-256', 'Bar Handle Matte Black 256mm'),
            ('HDL-CUP-96', 'Cup Pull Handle Brushed Nickel 96mm'),
            ('HDL-KNOB-30', 'Round Knob Brushed Nickel 30mm'),
            ('HDL-KNOB-35', 'Round Knob Brushed Nickel 35mm'),
            ('HDL-KNOB-BLK-30', 'Round Knob Matte Black 30mm'),
            ('HDL-KNOB-WOOD-40', 'Solid Oak Knob 40mm'),
            ('HDL-RECESSED-50', 'Recessed Flush Pull 50mm'),
            ('HDL-EDGE-TAB', 'Edge Pull Tab Handle Aluminium'),
            ('HDL-LEATHER-128', 'Leather Strap Handle 128mm'),
            ('HDL-PUSH-OPEN', 'Push-to-Open Latch'),
        ],
    },
    {
        'name': 'Connectors',
        'uom_xmlid': 'uom.product_uom_unit',
        'items': [
            ('CON-CAM-15', 'Cam Lock Fitting 15mm'),
            ('CON-CAM-BOLT-34', 'Cam Lock Bolt 34mm'),
            ('CON-MINIFIX-15', 'Minifix Connector 15mm'),
            ('CON-MINIFIX-BOLT', 'Minifix Connecting Bolt'),
            ('CON-RAFIX-20', 'Rafix Connector 20mm'),
            ('CON-SHELF-5', 'Shelf Support Pin 5mm'),
            ('CON-SHELF-SPOON', 'Shelf Support Spoon 5mm'),
            ('CON-BRACKET-L', 'L-Bracket Corner Connector'),
            ('CON-BRACKET-FLAT', 'Flat Mending Bracket'),
            ('CON-MODESTY-BLK', 'Modesty Block with Screw'),
            ('CON-KD-BOLT-M6', 'Knock-Down Bolt M6x60mm'),
            ('CON-CROSS-DOWEL', 'Cross Dowel Barrel Nut M6'),
            ('CON-BED-BOLT', 'Bed Bolt Connector Set'),
            ('CON-BOLT-FURNITURE', 'Furniture Corner Bolt'),
            ('CON-LOCK-CYLINDER', 'Cabinet Lock Cylinder'),
        ],
    },
    {
        'name': 'Casters & Levelers',
        'uom_xmlid': 'uom.product_uom_unit',
        'items': [
            ('CAS-CASTER-50', 'Twin Wheel Caster 50mm'),
            ('CAS-CASTER-75', 'Swivel Caster with Brake 75mm'),
            ('CAS-CASTER-PLATE', 'Plate Mount Caster 50mm'),
            ('CAS-LEVELER-M8', 'Adjustable Leveler M8'),
            ('CAS-LEVELER-M10', 'Adjustable Leveler M10'),
            ('CAS-CASTER-LOCK-75', 'Locking Swivel Caster 75mm'),
            ('CAS-FELT-PAD-25', 'Felt Furniture Pad 25mm'),
            ('CAS-GLIDE-25', 'Furniture Glide Nail-On 25mm'),
        ],
    },
    {
        'name': 'Adhesives',
        'uom_xmlid': 'uom.product_uom_litre',
        'items': [
            ('ADH-PVA-D3', 'PVA Wood Glue D3'),
            ('ADH-PVA-D4', 'PVA Wood Glue D4 Waterproof'),
            ('ADH-PU-FAST', 'Polyurethane Glue Fast Set'),
            ('ADH-PU-EXPAND', 'Expanding Polyurethane Glue'),
            ('ADH-CONTACT', 'Contact Adhesive Solvent-Based'),
            ('ADH-CONTACT-WATER', 'Contact Adhesive Water-Based'),
            ('ADH-HOTMELT-EDGE', 'Hot Melt Adhesive Edge Banding'),
            ('ADH-HOTMELT-STICKS', 'Hot Melt Glue Sticks 11mm'),
            ('ADH-EPOXY-5MIN', 'Epoxy Adhesive 5 Minute 2-Part'),
            ('ADH-CA-THICK', 'Cyanoacrylate Glue Thick'),
            ('ADH-MIRROR', 'Mirror Adhesive'),
        ],
    },
    {
        'name': 'Stains',
        'uom_xmlid': 'uom.product_uom_litre',
        'items': [
            ('STN-NATURAL-OAK', 'Wood Stain Natural Oak'),
            ('STN-GOLDEN-OAK', 'Wood Stain Golden Oak'),
            ('STN-DARK-OAK', 'Wood Stain Dark Oak'),
            ('STN-WALNUT', 'Wood Stain Walnut'),
            ('STN-MAHOGANY', 'Wood Stain Mahogany'),
            ('STN-EBONY', 'Wood Stain Ebony'),
            ('STN-WHITE-WASH', 'Wood Stain White Wash'),
            ('STN-GREY-WASH', 'Wood Stain Grey Wash'),
            ('STN-ANTIQUE-PINE', 'Wood Stain Antique Pine'),
            ('STN-TEAK', 'Wood Stain Teak'),
        ],
    },
    {
        'name': 'Lacquers',
        'uom_xmlid': 'uom.product_uom_litre',
        'items': [
            ('LAC-CLEAR-MATT', 'Clear Lacquer Matt'),
            ('LAC-CLEAR-SATIN', 'Clear Lacquer Satin'),
            ('LAC-CLEAR-GLOSS', 'Clear Lacquer Gloss'),
            ('LAC-2K-CLEAR', '2K Polyurethane Clear Lacquer'),
            ('LAC-WATER-MATT', 'Water-Based Lacquer Matt'),
            ('LAC-WATER-SATIN', 'Water-Based Lacquer Satin'),
            ('LAC-PRIMER-SAND', 'Sanding Primer Lacquer'),
            ('LAC-HARDWAX-OIL', 'Hardwax Oil Natural'),
        ],
    },
    {
        'name': 'Paints',
        'uom_xmlid': 'uom.product_uom_litre',
        'items': [
            ('PNT-WHITE-MATT', 'Furniture Paint White Matt'),
            ('PNT-WHITE-SATIN', 'Furniture Paint White Satin'),
            ('PNT-BLACK-MATT', 'Furniture Paint Black Matt'),
            ('PNT-BLACK-SATIN', 'Furniture Paint Black Satin'),
            ('PNT-GREY-MATT', 'Furniture Paint Grey Matt'),
            ('PNT-PRIMER-WHITE', 'MDF Primer White'),
            ('PNT-PRIMER-GREY', 'MDF Primer Grey'),
            ('PNT-FILLER-SPRAY', 'Spray Filler Primer'),
        ],
    },
    {
        'name': 'Upholstery Fabric',
        'uom_xmlid': None,  # m²
        'items': [
            ('FAB-LINEN-GREY', 'Linen Fabric Grey'),
            ('FAB-LINEN-BEIGE', 'Linen Fabric Beige'),
            ('FAB-LINEN-NAVY', 'Linen Fabric Navy'),
            ('FAB-VELVET-GREEN', 'Velvet Fabric Forest Green'),
            ('FAB-VELVET-BLUE', 'Velvet Fabric Midnight Blue'),
            ('FAB-VELVET-GREY', 'Velvet Fabric Charcoal Grey'),
            ('FAB-TWEED-BROWN', 'Tweed Fabric Brown'),
            ('FAB-LEATHER-BLK', 'Full Grain Leather Black'),
            ('FAB-LEATHER-TAN', 'Full Grain Leather Tan'),
            ('FAB-WEBBING-JUTE', 'Jute Upholstery Webbing'),
            ('FAB-CANVAS-NAT', 'Canvas Fabric Natural'),
        ],
    },
    {
        'name': 'Foam & Padding',
        'uom_xmlid': None,  # m²
        'items': [
            ('FOAM-HR-30', 'High Resilience Foam 30mm'),
            ('FOAM-HR-50', 'High Resilience Foam 50mm'),
            ('FOAM-HR-100', 'High Resilience Foam 100mm'),
            ('FOAM-MEMORY-50', 'Memory Foam 50mm'),
            ('FOAM-DACRON-WRAP', 'Dacron Wrap Padding 200g/m\u00b2'),
            ('FOAM-FELT-PAD', 'Felt Padding 10mm'),
        ],
    },
    {
        'name': 'Glass',
        'uom_xmlid': None,  # m²
        'items': [
            ('GLS-TEMPERED-4', 'Tempered Glass 4mm Clear'),
            ('GLS-TEMPERED-6', 'Tempered Glass 6mm Clear'),
            ('GLS-TEMPERED-8', 'Tempered Glass 8mm Clear'),
            ('GLS-MIRROR-4', 'Mirror Glass 4mm'),
            ('GLS-FROSTED-4', 'Frosted Glass 4mm'),
            ('GLS-TINTED-GREY-6', 'Tinted Glass Grey 6mm'),
        ],
    },
    {
        'name': 'Metal Components',
        'uom_xmlid': 'uom.product_uom_unit',
        'items': [
            ('MTL-LEG-HAIRPIN-710', 'Hairpin Table Leg 710mm Black'),
            ('MTL-LEG-HAIRPIN-400', 'Hairpin Table Leg 400mm Black'),
            ('MTL-LEG-TAPER-710', 'Tapered Steel Leg 710mm Black'),
            ('MTL-TUBE-25x25', 'Steel Square Tube 25x25mm'),
            ('MTL-TUBE-40x20', 'Steel Rectangular Tube 40x20mm'),
            ('MTL-BRACKET-SHELF', 'Steel Shelf Bracket 200mm'),
            ('MTL-FRAME-DESK', 'Steel Desk Frame Kit 1200mm'),
            ('MTL-BRACKET-CORNER', 'Steel Corner Bracket'),
            ('MTL-RAIL-WARDROBE', 'Wardrobe Clothes Rail 1000mm'),
            ('MTL-SUSP-RAIL', 'Suspension File Rail'),
            ('MTL-TOWEL-RAIL', 'Towel Rail Chrome 400mm'),
            ('MTL-CHANNEL-WALL', 'Wall Mounting Channel 1000mm'),
        ],
    },
    {
        'name': 'Electrical',
        'uom_xmlid': 'uom.product_uom_unit',
        'items': [
            ('ELEC-LED-STRIP-3000K', 'LED Strip Warm White 3000K 5m'),
            ('ELEC-LED-STRIP-4000K', 'LED Strip Neutral White 4000K 5m'),
            ('ELEC-LED-DRIVER-30W', 'LED Driver 30W 12V'),
            ('ELEC-SWITCH-TOUCH', 'Touch Dimmer Switch'),
            ('ELEC-GROMMET-USB', 'Desk Grommet with USB-A/C Ports'),
            ('ELEC-GROMMET-60', 'Cable Grommet 60mm'),
        ],
    },
    {
        'name': 'Packaging',
        'uom_xmlid': 'uom.product_uom_unit',
        'items': [
            ('PKG-CARDBOARD-SMALL', 'Cardboard Box Small 600x400x300mm'),
            ('PKG-CARDBOARD-MED', 'Cardboard Box Medium 800x500x400mm'),
            ('PKG-CARDBOARD-LARGE', 'Cardboard Box Large 1200x600x400mm'),
            ('PKG-CARDBOARD-FLAT', 'Flat Pack Cardboard Box 1600x800x100mm'),
            ('PKG-FOAM-CORNER', 'Foam Corner Protector Set'),
            ('PKG-BUBBLE-WRAP', 'Bubble Wrap Roll 1200mm'),
            ('PKG-STRETCH-WRAP', 'Stretch Wrap Roll 500mm'),
            ('PKG-BLANKET', 'Furniture Moving Blanket'),
            ('PKG-TAPE-BROWN', 'Packing Tape Brown 50mm'),
        ],
    },
]


def _resolve_sqm_uom(env):
    """Find the square meter UoM, falling back to meter if not available."""
    sqm = env['uom.uom'].search(
        [('name', 'in', ['m²', 'sq m', 'm2'])], limit=1,
    )
    if sqm:
        return sqm
    return env.ref('uom.product_uom_meter')


def create_materials(env):
    """Create ~207 raw materials across 20 categories.

    Returns dict of code -> product.product record.
    """
    buy_route = env.ref('purchase_stock.route_warehouse0_buy')
    sqm_uom = _resolve_sqm_uom(env)

    result = {}
    Product = env['product.product']

    for category in CATEGORIES:
        if category['uom_xmlid'] is not None:
            uom = env.ref(category['uom_xmlid'])
        else:
            uom = sqm_uom

        vals_list = []
        for code, name in category['items']:
            vals_list.append({
                'name': name,
                'default_code': code,
                'type': 'consu',
                'is_storable': True,
                'uom_id': uom.id,
                'route_ids': [(6, 0, [buy_route.id])],
            })

        products = Product.create(vals_list)
        for product in products:
            result[product.default_code] = product

    _logger.info(
        "Created %d materials across %d categories.",
        len(result), len(CATEGORIES),
    )
    return result
