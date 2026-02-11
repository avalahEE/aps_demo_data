def create_boms(env, materials, products, subassemblies, workcenters):
    """Create BOMs for all finished products and subassemblies.

    Each BOM includes routing operations assigned to specific work centers.
    Returns list of created mrp.bom records.
    """
    BOM = env['mrp.bom']
    m = materials  # shorthand
    sa = subassemblies
    wc = workcenters

    boms = []

    # =========================================================================
    # LEVEL 3 SUBASSEMBLY BOMs (deepest)
    # =========================================================================

    # SA-BACK-PANEL — Cabinet Back Panel 6mm
    boms.append(_create_bom(env, sa['SA-BACK-PANEL'], [
        (m['SHT-HDF-3'], 0.75),    # 0.75 m² HDF 3mm
        (m['ADH-PVA-D3'], 0.05),   # 50ml PVA glue
        (m['FST-BRAD-18'], 12),     # 12 brad nails
    ], [
        _op('Cut back panel', wc['WC-SAW-01'], 5),
    ]))

    # SA-DRAWER-FRONT — Drawer Front (Pre-Edged)
    boms.append(_create_bom(env, sa['SA-DRAWER-FRONT'], [
        (m['SHT-MDF-18'], 0.15),       # MDF panel
        (m['VNR-OAK-06'], 0.15),        # Oak veneer face
        (m['EDGE-OAK-22'], 1.6),        # Edge banding ~1.6m
        (m['ADH-HOTMELT-EDGE'], 0.02),  # Edge banding adhesive
    ], [
        _op('Cut drawer front', wc['WC-SAW-01'], 6),
        _op('CNC shape drawer front', wc['WC-CNC-01'], 10),
        _op('Edge band drawer front', wc['WC-EDGE-01'], 8),
    ]))

    # SA-EDGE-PANEL — Pre-Edged Panel (generic, used for shelves/doors/tops)
    boms.append(_create_bom(env, sa['SA-EDGE-PANEL'], [
        (m['SHT-MDF-18'], 0.35),       # MDF sheet
        (m['EDGE-PVC-WHT-22'], 2.0),    # PVC edge banding
        (m['ADH-HOTMELT-EDGE'], 0.03),  # Edge adhesive
    ], [
        _op('Cut panel to size', wc['WC-SAW-01'], 6),
        _op('Edge band panel', wc['WC-EDGE-01'], 10),
    ]))

    # SA-HINGE-SET — Hinge Set (pair, with cup holes)
    boms.append(_create_bom(env, sa['SA-HINGE-SET'], [
        (m['HNG-SOFT-110'], 2),         # 2x soft-close 110° hinges
        (m['HNG-MOUNT-PLATE'], 2),       # 2x mounting plates
        (m['FST-SCREW-16'], 8),         # 8x mounting screws
    ], [
        _op('Drill hinge cups', wc['WC-CNC-01'], 8),
        _op('Mount hinge set', wc['WC-ASSM-01'], 4),
    ]))

    # SA-DRAWER-RUNNER-SET — Drawer Runner Pair
    boms.append(_create_bom(env, sa['SA-DRAWER-RUNNER-SET'], [
        (m['SLD-SOFT-400'], 1),         # 1x pair soft-close slides 400mm
        (m['FST-SCREW-16'], 8),         # 8x mounting screws
    ], [
        _op('Install drawer runners', wc['WC-ASSM-01'], 6),
    ]))

    # =========================================================================
    # LEVEL 2 SHARED SUBASSEMBLY BOMs
    # =========================================================================

    # SA-DRAWER-STD — Standard Drawer Box 400mm
    boms.append(_create_bom(env, sa['SA-DRAWER-STD'], [
        (m['SHT-PLY-BIRCH-12'], 0.5),  # Birch ply for sides/bottom
        (sa['SA-DRAWER-FRONT'], 1),      # Pre-edged front
        (sa['SA-DRAWER-RUNNER-SET'], 1), # Runner pair
        (m['FST-SCREW-35'], 8),          # Assembly screws
        (m['ADH-PVA-D3'], 0.03),         # PVA glue
        (m['FST-DOWEL-8x40'], 4),        # Dowels
    ], [
        _op('Cut drawer sides', wc['WC-SAW-01'], 10),
        _op('CNC drill dowel holes', wc['WC-CNC-01'], 12),
        _op('Assemble drawer box', wc['WC-ASSM-01'], 15),
    ]))

    # SA-DRAWER-LG — Large Drawer Box 500mm
    boms.append(_create_bom(env, sa['SA-DRAWER-LG'], [
        (m['SHT-PLY-BIRCH-12'], 0.6),
        (sa['SA-DRAWER-FRONT'], 1),
        (sa['SA-DRAWER-RUNNER-SET'], 1),
        (m['SLD-SOFT-500'], 1),          # Use 500mm slides instead
        (m['FST-SCREW-35'], 10),
        (m['ADH-PVA-D3'], 0.04),
        (m['FST-DOWEL-8x40'], 6),
    ], [
        _op('Cut large drawer sides', wc['WC-SAW-01'], 12),
        _op('CNC drill dowel holes', wc['WC-CNC-01'], 14),
        _op('Assemble large drawer', wc['WC-ASSM-01'], 18),
    ]))

    # SA-DOOR-PANEL — Standard Door Panel
    boms.append(_create_bom(env, sa['SA-DOOR-PANEL'], [
        (sa['SA-EDGE-PANEL'], 1),        # Pre-edged panel
        (sa['SA-HINGE-SET'], 1),         # Hinge set
        (m['HDL-BAR-128'], 1),           # Bar handle
        (m['FST-SCREW-16'], 2),          # Handle screws
    ], [
        _op('CNC drill handle holes', wc['WC-CNC-01'], 8),
        _op('Assemble door panel', wc['WC-ASSM-01'], 10),
    ]))

    # SA-SHELF-ADJ — Adjustable Shelf
    boms.append(_create_bom(env, sa['SA-SHELF-ADJ'], [
        (sa['SA-EDGE-PANEL'], 1),        # Pre-edged panel
        (m['CON-SHELF-5'], 4),            # 4x shelf pins
    ], [
        _op('Trim shelf to width', wc['WC-SAW-01'], 4),
    ]))

    # SA-CARCASS-BASE — Base Cabinet Carcass
    boms.append(_create_bom(env, sa['SA-CARCASS-BASE'], [
        (m['SHT-MDF-18'], 2.5),         # Sides, top, bottom
        (sa['SA-BACK-PANEL'], 1),        # Back panel
        (m['EDGE-PVC-WHT-22'], 4.0),     # Front edge banding
        (m['ADH-HOTMELT-EDGE'], 0.05),
        (m['FST-CONFIRMAT-50'], 16),     # Confirmat screws
        (m['CON-CAM-15'], 8),            # Cam locks
        (m['CON-MINIFIX-15'], 8),        # Minifix connectors
        (m['FST-DOWEL-8x40'], 12),       # Dowels
        (m['ADH-PVA-D3'], 0.1),
        (m['CAS-LEVELER-M8'], 4),        # Adjustable feet
    ], [
        _op('Cut carcass panels', wc['WC-SAW-01'], 18),
        _op('CNC drill all fittings', wc['WC-CNC-01'], 25),
        _op('Edge band front edges', wc['WC-EDGE-01'], 14),
        _op('Assemble base carcass', wc['WC-ASSM-01'], 30),
    ]))

    # SA-CARCASS-TALL — Tall Cabinet Carcass
    boms.append(_create_bom(env, sa['SA-CARCASS-TALL'], [
        (m['SHT-MDF-18'], 4.0),         # Taller panels
        (sa['SA-BACK-PANEL'], 2),        # 2x back panels (tall)
        (m['EDGE-PVC-WHT-22'], 5.0),
        (m['ADH-HOTMELT-EDGE'], 0.06),
        (m['FST-CONFIRMAT-50'], 24),
        (m['CON-CAM-15'], 12),
        (m['CON-MINIFIX-15'], 12),
        (m['FST-DOWEL-8x40'], 16),
        (m['ADH-PVA-D3'], 0.15),
        (m['CAS-LEVELER-M8'], 4),
    ], [
        _op('Cut tall carcass panels', wc['WC-SAW-01'], 22),
        _op('CNC drill all fittings', wc['WC-CNC-01'], 35),
        _op('Edge band front edges', wc['WC-EDGE-01'], 16),
        _op('Assemble tall carcass', wc['WC-ASSM-01'], 40),
    ]))

    # SA-TABLETOP-WAL — Walnut Table Top
    boms.append(_create_bom(env, sa['SA-TABLETOP-WAL'], [
        (m['WOOD-WALNUT-40x150'], 18.0),  # Solid walnut boards
        (m['ADH-PVA-D3'], 0.2),            # Glue for edge joining
        (m['FST-BISCUIT-20'], 12),         # Biscuit joints
        (m['FST-DOWEL-8x40'], 8),
    ], [
        _op('Rip boards to width', wc['WC-SAW-01'], 20),
        _op('CNC flatten and shape', wc['WC-CNC-01'], 45),
        _op('Assemble glue-up', wc['WC-ASSM-01'], 25),
    ]))

    # SA-LEG-FRAME-STEEL — Steel Leg Frame
    boms.append(_create_bom(env, sa['SA-LEG-FRAME-STEEL'], [
        (m['MTL-LEG-HAIRPIN-710'], 4),   # 4x hairpin legs
        (m['MTL-BRACKET-CORNER'], 4),     # Corner brackets
        (m['FST-BOLT-M8x50'], 8),         # Mounting bolts
        (m['FST-TNUT-M8'], 8),            # T-nuts for top
    ], [
        _op('Assemble steel frame', wc['WC-ASSM-01'], 20),
    ]))

    # SA-LEG-FRAME-OAK — Oak Leg Frame
    boms.append(_create_bom(env, sa['SA-LEG-FRAME-OAK'], [
        (m['WOOD-OAK-50x50'], 6.0),     # Leg stock
        (m['WOOD-OAK-25x100'], 4.0),    # Apron/rail stock
        (m['FST-DOWEL-8x40'], 16),       # Dowel joints
        (m['ADH-PVA-D3'], 0.1),
        (m['CON-BOLT-FURNITURE'], 4),    # Corner bolts
    ], [
        _op('Cut leg components', wc['WC-SAW-01'], 15),
        _op('CNC mortise and tenon', wc['WC-CNC-01'], 30),
        _op('Assemble leg frame', wc['WC-ASSM-01'], 25),
    ]))

    # SA-UPHOLSTERY-SEAT — Upholstered Seat Pad
    boms.append(_create_bom(env, sa['SA-UPHOLSTERY-SEAT'], [
        (m['SHT-PLY-BIRCH-12'], 0.2),   # Seat board
        (m['FOAM-HR-50'], 0.2),           # High-resilience foam
        (m['FOAM-DACRON-WRAP'], 0.25),    # Dacron wrap
        (m['FAB-LINEN-GREY'], 0.35),      # Linen fabric
        (m['FST-STAPLE-10'], 30),         # Upholstery staples
    ], [
        _op('Cut seat board', wc['WC-SAW-01'], 5),
        _op('CNC shape seat profile', wc['WC-CNC-01'], 10),
        _op('Assemble upholstery', wc['WC-ASSM-01'], 20),
    ]))

    # =========================================================================
    # PRODUCT-SPECIFIC SUBASSEMBLY BOMs
    # =========================================================================

    # SA-DESK-TOP — Executive Desk Top
    boms.append(_create_bom(env, sa['SA-DESK-TOP'], [
        (m['SHT-MDF-25'], 1.5),          # Thick MDF core
        (m['VNR-OAK-06'], 1.6),           # Oak veneer top & bottom
        (m['EDGE-OAK-45'], 3.6),          # Thick oak edge banding
        (m['ADH-CONTACT'], 0.2),           # Contact adhesive for veneer
        (m['ADH-HOTMELT-EDGE'], 0.05),
    ], [
        _op('Cut desk top panel', wc['WC-SAW-01'], 10),
        _op('CNC trim to final size', wc['WC-CNC-01'], 15),
        _op('Edge band desk top', wc['WC-EDGE-01'], 12),
    ]))

    # SA-DESK-MODESTY — Desk Modesty Panel
    boms.append(_create_bom(env, sa['SA-DESK-MODESTY'], [
        (sa['SA-EDGE-PANEL'], 1),
        (m['FST-SCREW-35'], 4),
        (m['CON-CAM-15'], 4),
    ], [
        _op('Cut modesty panel', wc['WC-SAW-01'], 5),
        _op('CNC drill fixings', wc['WC-CNC-01'], 8),
    ]))

    # SA-DESK-CABLE-MGMT — Cable Management Tray
    boms.append(_create_bom(env, sa['SA-DESK-CABLE-MGMT'], [
        (m['MTL-TUBE-25x25'], 1),          # Steel channel
        (m['FST-SCREW-16'], 6),
    ], [
        _op('Assemble cable tray', wc['WC-ASSM-01'], 8),
    ]))

    # SA-BED-HEADBOARD — King Headboard
    boms.append(_create_bom(env, sa['SA-BED-HEADBOARD'], [
        (m['SHT-MDF-18'], 1.5),
        (m['FOAM-HR-50'], 0.8),
        (m['FOAM-DACRON-WRAP'], 0.9),
        (m['FAB-VELVET-GREEN'], 1.2),
        (m['FST-STAPLE-10'], 60),
        (m['WOOD-OAK-25x100'], 3.0),    # Frame
        (m['FST-SCREW-35'], 8),
    ], [
        _op('Cut headboard frame', wc['WC-SAW-01'], 12),
        _op('CNC shape headboard', wc['WC-CNC-01'], 20),
        _op('Assemble & upholster headboard', wc['WC-ASSM-01'], 35),
    ]))

    # SA-BED-RAIL-SET — Bed Rail Set
    boms.append(_create_bom(env, sa['SA-BED-RAIL-SET'], [
        (m['WOOD-OAK-25x150'], 8.0),    # Rail boards
        (m['CON-BED-BOLT'], 4),           # Bed bolts
        (m['FST-BOLT-M8x50'], 4),
        (m['MTL-BRACKET-CORNER'], 4),
    ], [
        _op('Cut bed rails', wc['WC-SAW-01'], 10),
        _op('CNC drill bolt holes', wc['WC-CNC-01'], 12),
        _op('Assemble rail set', wc['WC-ASSM-01'], 15),
    ]))

    # SA-BED-SLAT-BASE — Slat Base System
    boms.append(_create_bom(env, sa['SA-BED-SLAT-BASE'], [
        (m['WOOD-BEECH-25x80'], 10.0),  # Slats
        (m['SHT-PLY-BIRCH-18'], 0.5),   # Center support
        (m['FST-SCREW-35'], 12),
        (m['FAB-WEBBING-JUTE'], 2.0),   # Jute webbing for slat holders
    ], [
        _op('Cut slats to length', wc['WC-SAW-01'], 15),
        _op('Assemble slat base', wc['WC-ASSM-01'], 20),
    ]))

    # SA-TV-MEDIA-SHELF — TV Console Media Shelf
    boms.append(_create_bom(env, sa['SA-TV-MEDIA-SHELF'], [
        (sa['SA-EDGE-PANEL'], 1),
        (m['ELEC-GROMMET-60'], 2),       # Cable grommets
        (m['FST-SCREW-16'], 4),
    ], [
        _op('CNC drill cable holes', wc['WC-CNC-01'], 8),
        _op('Assemble media shelf', wc['WC-ASSM-01'], 6),
    ]))

    # SA-KITCHEN-BTOP — Butcher Block Countertop
    boms.append(_create_bom(env, sa['SA-KITCHEN-BTOP'], [
        (m['WOOD-BEECH-40x50'], 15.0),  # Beech strips for butcher block
        (m['ADH-PVA-D3'], 0.25),
        (m['FST-BISCUIT-20'], 16),
    ], [
        _op('Rip strips to width', wc['WC-SAW-01'], 20),
        _op('CNC flatten butcher block', wc['WC-CNC-01'], 40),
        _op('Assemble glue-up', wc['WC-ASSM-01'], 25),
    ]))

    # SA-WARDROBE-MIRROR — Wardrobe Mirror Panel
    boms.append(_create_bom(env, sa['SA-WARDROBE-MIRROR'], [
        (m['GLS-MIRROR-4'], 1.2),        # Mirror glass
        (m['SHT-MDF-6'], 1.2),           # Backing
        (m['ADH-MIRROR'], 0.15),          # Mirror adhesive
        (m['FST-SCREW-16'], 6),
    ], [
        _op('Cut mirror backing', wc['WC-SAW-01'], 6),
        _op('Assemble mirror panel', wc['WC-ASSM-01'], 12),
    ]))

    # SA-WARDROBE-INT-DRAWER — Wardrobe Internal Drawer (smaller)
    boms.append(_create_bom(env, sa['SA-WARDROBE-INT-DRAWER'], [
        (m['SHT-PLY-BIRCH-12'], 0.35),
        (sa['SA-DRAWER-FRONT'], 1),
        (m['SLD-BALL-400'], 1),           # Ball-bearing slides
        (m['FST-SCREW-16'], 6),
        (m['ADH-PVA-D3'], 0.02),
    ], [
        _op('Cut internal drawer parts', wc['WC-SAW-01'], 8),
        _op('CNC drill slide holes', wc['WC-CNC-01'], 10),
        _op('Assemble internal drawer', wc['WC-ASSM-01'], 12),
    ]))

    # SA-COFFEE-GLASS-SHELF — Coffee Table Glass Shelf
    boms.append(_create_bom(env, sa['SA-COFFEE-GLASS-SHELF'], [
        (m['GLS-TEMPERED-6'], 0.5),      # Tempered glass
        (m['CON-SHELF-5'], 4),             # Glass shelf supports
    ], [
        _op('Assemble glass shelf', wc['WC-ASSM-01'], 6),
    ]))

    # SA-OFFICE-FILE-DRAWER — Filing Drawer (Suspension)
    boms.append(_create_bom(env, sa['SA-OFFICE-FILE-DRAWER'], [
        (m['SHT-PLY-BIRCH-12'], 0.6),
        (sa['SA-DRAWER-FRONT'], 1),
        (m['SLD-BALL-500'], 1),           # 500mm heavy-duty slides
        (m['MTL-SUSP-RAIL'], 2),          # Suspension file rails
        (m['FST-SCREW-35'], 10),
        (m['ADH-PVA-D3'], 0.03),
    ], [
        _op('Cut filing drawer parts', wc['WC-SAW-01'], 10),
        _op('CNC drill slide & rail holes', wc['WC-CNC-01'], 14),
        _op('Assemble filing drawer', wc['WC-ASSM-01'], 18),
    ]))

    # SA-CHAIR-BACKREST — Dining Chair Backrest
    boms.append(_create_bom(env, sa['SA-CHAIR-BACKREST'], [
        (m['WOOD-OAK-25x100'], 2.0),    # Backrest slats/frame
        (m['FST-DOWEL-8x40'], 6),
        (m['ADH-PVA-D3'], 0.05),
    ], [
        _op('Cut backrest components', wc['WC-SAW-01'], 8),
        _op('CNC shape backrest curves', wc['WC-CNC-01'], 18),
        _op('Assemble backrest', wc['WC-ASSM-01'], 12),
    ]))

    # SA-BOOK-CROWN — Bookcase Crown Moulding
    boms.append(_create_bom(env, sa['SA-BOOK-CROWN'], [
        (m['WOOD-OAK-25x50'], 2.5),
        (m['FST-BRAD-18'], 8),
        (m['ADH-PVA-D3'], 0.03),
    ], [
        _op('Cut crown moulding', wc['WC-SAW-01'], 8),
        _op('CNC profile moulding', wc['WC-CNC-01'], 15),
    ]))

    # SA-BOOK-BASE-PLINTH — Bookcase Base Plinth
    boms.append(_create_bom(env, sa['SA-BOOK-BASE-PLINTH'], [
        (m['SHT-MDF-18'], 0.3),
        (m['EDGE-PVC-WHT-22'], 1.5),
        (m['ADH-HOTMELT-EDGE'], 0.02),
        (m['CAS-LEVELER-M8'], 4),
    ], [
        _op('Cut plinth parts', wc['WC-SAW-01'], 6),
        _op('Edge band plinth', wc['WC-EDGE-01'], 8),
        _op('Assemble plinth', wc['WC-ASSM-01'], 10),
    ]))

    # =========================================================================
    # FINISHED PRODUCT BOMs (Level 1)
    # =========================================================================

    fp = products  # shorthand

    # FP-EXEC-DESK — Executive Office Desk (4 levels deep)
    boms.append(_create_bom(env, fp['FP-EXEC-DESK'], [
        (sa['SA-DESK-TOP'], 1),
        (sa['SA-LEG-FRAME-OAK'], 1),
        (sa['SA-DRAWER-STD'], 2),         # 2 standard drawers
        (sa['SA-DRAWER-LG'], 1),          # 1 large drawer
        (sa['SA-DESK-MODESTY'], 1),
        (sa['SA-DESK-CABLE-MGMT'], 1),
        (m['FST-SCREW-35'], 12),
        (m['CON-BOLT-FURNITURE'], 4),
        (m['PKG-CARDBOARD-LARGE'], 1),
        (m['PKG-FOAM-CORNER'], 8),
    ], [
        _op('Cut desk trim pieces', wc['WC-SAW-01'], 12),
        _op('CNC drill cable ports & assembly holes', wc['WC-CNC-01'], 18),
        _op('Edge band exposed desk edges', wc['WC-EDGE-01'], 10),
        _op('Final assembly desk', wc['WC-ASSM-01'], 60),
        _op('Finish desk', wc['WC-FINISH-01'], 35),
    ]))

    # FP-BOOK-TALL — Tall Bookcase (4 levels deep)
    boms.append(_create_bom(env, fp['FP-BOOK-TALL'], [
        (sa['SA-CARCASS-TALL'], 1),
        (sa['SA-SHELF-ADJ'], 5),          # 5 adjustable shelves
        (sa['SA-BOOK-CROWN'], 1),
        (sa['SA-BOOK-BASE-PLINTH'], 1),
        (m['FST-SCREW-35'], 8),
        (m['FST-WALL-ANCHOR'], 2),        # Anti-tip anchors
        (m['PKG-CARDBOARD-LARGE'], 1),
        (m['PKG-FOAM-CORNER'], 8),
    ], [
        _op('Cut fixed shelves & dividers', wc['WC-SAW-01'], 10),
        _op('CNC drill shelf pin holes', wc['WC-CNC-01'], 20),
        _op('Edge band visible edges', wc['WC-EDGE-01'], 12),
        _op('Final assembly bookcase', wc['WC-ASSM-01'], 45),
        _op('Finish bookcase', wc['WC-FINISH-01'], 30),
    ]))

    # FP-DINING-TBL — Dining Table 8 Seat (3 levels deep)
    boms.append(_create_bom(env, fp['FP-DINING-TBL'], [
        (sa['SA-TABLETOP-WAL'], 1),
        (sa['SA-LEG-FRAME-STEEL'], 1),
        (m['FST-BOLT-M8x50'], 8),
        (m['STN-NATURAL-OAK'], 0.3),     # Actually walnut stain on walnut
        (m['LAC-CLEAR-SATIN'], 0.5),
        (m['PKG-CARDBOARD-LARGE'], 1),
        (m['PKG-FOAM-CORNER'], 8),
        (m['PKG-BLANKET'], 1),
    ], [
        _op('Cut table trim & spacers', wc['WC-SAW-01'], 8),
        _op('CNC flatten & sand top surface', wc['WC-CNC-01'], 20),
        _op('Edge profile table edges', wc['WC-EDGE-01'], 15),
        _op('Final assembly dining table', wc['WC-ASSM-01'], 40),
        _op('Finish dining table', wc['WC-FINISH-01'], 45),
    ]))

    # FP-TV-CONSOLE — TV Console Unit (4 levels deep)
    boms.append(_create_bom(env, fp['FP-TV-CONSOLE'], [
        (sa['SA-CARCASS-BASE'], 1),
        (sa['SA-DOOR-PANEL'], 2),         # 2 doors
        (sa['SA-DRAWER-STD'], 2),         # 2 drawers
        (sa['SA-SHELF-ADJ'], 1),
        (sa['SA-TV-MEDIA-SHELF'], 1),
        (m['ELEC-LED-STRIP-3000K'], 1),   # LED strip accent
        (m['ELEC-LED-DRIVER-30W'], 1),
        (m['FST-SCREW-16'], 8),
        (m['PKG-CARDBOARD-LARGE'], 1),
        (m['PKG-FOAM-CORNER'], 8),
    ], [
        _op('Cut console top & dividers', wc['WC-SAW-01'], 12),
        _op('CNC drill cable management holes', wc['WC-CNC-01'], 15),
        _op('Edge band exposed faces', wc['WC-EDGE-01'], 10),
        _op('Final assembly TV console', wc['WC-ASSM-01'], 50),
        _op('Install LED & electrics', wc['WC-ASSM-02'], 15),
        _op('Finish TV console', wc['WC-FINISH-01'], 30),
    ]))

    # FP-WARDROBE — Wardrobe 3-Door (4 levels deep)
    boms.append(_create_bom(env, fp['FP-WARDROBE'], [
        (sa['SA-CARCASS-TALL'], 1),
        (sa['SA-DOOR-PANEL'], 2),         # 2 regular doors
        (sa['SA-WARDROBE-MIRROR'], 1),    # 1 mirror door
        (sa['SA-SHELF-ADJ'], 3),
        (sa['SA-DRAWER-STD'], 2),
        (sa['SA-WARDROBE-INT-DRAWER'], 2),
        (m['MTL-RAIL-WARDROBE'], 1),      # Clothes rail
        (m['FST-SCREW-35'], 12),
        (m['FST-WALL-ANCHOR'], 2),
        (m['PKG-CARDBOARD-LARGE'], 2),
        (m['PKG-FOAM-CORNER'], 12),
    ], [
        _op('Cut wardrobe crown & base trim', wc['WC-SAW-01'], 15),
        _op('CNC drill hanging rail & shelf pin holes', wc['WC-CNC-01'], 22),
        _op('Edge band visible panels', wc['WC-EDGE-01'], 18),
        _op('Final assembly wardrobe', wc['WC-ASSM-01'], 90),
        _op('Finish wardrobe', wc['WC-FINISH-01'], 40),
    ]))

    # FP-BED-KING — King Bed Frame (3 levels deep)
    boms.append(_create_bom(env, fp['FP-BED-KING'], [
        (sa['SA-BED-HEADBOARD'], 1),
        (sa['SA-BED-RAIL-SET'], 1),
        (sa['SA-BED-SLAT-BASE'], 1),
        (m['WOOD-OAK-50x50'], 4.0),      # Foot posts
        (m['FST-BOLT-M8x50'], 8),
        (m['CON-BED-BOLT'], 4),
        (m['PKG-CARDBOARD-LARGE'], 2),
        (m['PKG-FOAM-CORNER'], 8),
        (m['PKG-BLANKET'], 1),
    ], [
        _op('Cut foot posts & cross members', wc['WC-SAW-01'], 12),
        _op('CNC shape & drill foot posts', wc['WC-CNC-01'], 18),
        _op('Edge band headboard trim', wc['WC-EDGE-01'], 8),
        _op('Final assembly bed frame', wc['WC-ASSM-01'], 45),
        _op('Finish bed frame', wc['WC-FINISH-01'], 35),
    ]))

    # FP-DINING-CHR — Dining Chair (3 levels deep)
    boms.append(_create_bom(env, fp['FP-DINING-CHR'], [
        (sa['SA-LEG-FRAME-OAK'], 1),
        (sa['SA-UPHOLSTERY-SEAT'], 1),
        (sa['SA-CHAIR-BACKREST'], 1),
        (m['FST-SCREW-35'], 8),
        (m['CON-BOLT-FURNITURE'], 4),
        (m['CAS-FELT-PAD-25'], 4),        # Felt pads for floor
        (m['PKG-CARDBOARD-MED'], 1),
    ], [
        _op('Cut seat frame & backrest trim', wc['WC-SAW-01'], 8),
        _op('CNC contour seat & backrest', wc['WC-CNC-01'], 15),
        _op('Final assembly chair', wc['WC-ASSM-01'], 30),
        _op('Finish chair', wc['WC-FINISH-01'], 20),
    ]))

    # FP-KITCHEN-ISL — Kitchen Island (4 levels deep)
    boms.append(_create_bom(env, fp['FP-KITCHEN-ISL'], [
        (sa['SA-KITCHEN-BTOP'], 1),
        (sa['SA-CARCASS-BASE'], 1),
        (sa['SA-DOOR-PANEL'], 2),
        (sa['SA-DRAWER-STD'], 2),
        (sa['SA-SHELF-ADJ'], 2),
        (m['FST-SCREW-35'], 16),
        (m['CAS-CASTER-LOCK-75'], 4),    # Locking casters
        (m['MTL-TOWEL-RAIL'], 1),         # Towel rail
        (m['PKG-CARDBOARD-LARGE'], 1),
        (m['PKG-FOAM-CORNER'], 8),
    ], [
        _op('Cut island top trim & panels', wc['WC-SAW-01'], 12),
        _op('CNC drill utility holes & fixings', wc['WC-CNC-01'], 18),
        _op('Edge band exposed faces', wc['WC-EDGE-01'], 14),
        _op('Final assembly kitchen island', wc['WC-ASSM-01'], 60),
        _op('Finish kitchen island', wc['WC-FINISH-01'], 40),
    ]))

    # FP-OFFICE-CAB — Office Storage Cabinet (4 levels deep)
    boms.append(_create_bom(env, fp['FP-OFFICE-CAB'], [
        (sa['SA-CARCASS-BASE'], 1),
        (sa['SA-DOOR-PANEL'], 2),
        (sa['SA-SHELF-ADJ'], 2),
        (sa['SA-OFFICE-FILE-DRAWER'], 1),
        (m['CON-LOCK-CYLINDER'], 1),      # Cabinet lock
        (m['FST-SCREW-35'], 8),
        (m['PKG-CARDBOARD-LARGE'], 1),
        (m['PKG-FOAM-CORNER'], 8),
    ], [
        _op('Cut cabinet top & filler panels', wc['WC-SAW-01'], 10),
        _op('CNC drill lock & hinge holes', wc['WC-CNC-01'], 14),
        _op('Edge band front faces', wc['WC-EDGE-01'], 10),
        _op('Final assembly office cabinet', wc['WC-ASSM-01'], 45),
        _op('Finish office cabinet', wc['WC-FINISH-01'], 25),
    ]))

    # FP-COFFEE-TBL — Coffee Table (3 levels deep)
    boms.append(_create_bom(env, fp['FP-COFFEE-TBL'], [
        (sa['SA-TABLETOP-WAL'], 1),       # Smaller walnut top (reuse BOM)
        (sa['SA-LEG-FRAME-STEEL'], 1),
        (sa['SA-COFFEE-GLASS-SHELF'], 1),
        (m['FST-BOLT-M8x50'], 4),
        (m['LAC-CLEAR-SATIN'], 0.3),
        (m['PKG-CARDBOARD-MED'], 1),
        (m['PKG-FOAM-CORNER'], 4),
    ], [
        _op('Cut shelf supports & spacers', wc['WC-SAW-01'], 6),
        _op('CNC round table edges', wc['WC-CNC-01'], 12),
        _op('Final assembly coffee table', wc['WC-ASSM-01'], 25),
        _op('Finish coffee table', wc['WC-FINISH-01'], 25),
    ]))

    return boms


# =============================================================================
# Helpers
# =============================================================================

def _create_bom(env, product, components, operations):
    """Create a BOM with components and routing operations.

    Args:
        product: product.product record
        components: list of (product, qty) tuples
        operations: list of dicts with name, workcenter, time_cycle_manual
    """
    # Auto-assign sequence values (10, 20, 30, ...) so work orders
    # get proper dependency chaining via the APS connector's sequence fallback
    for i, op in enumerate(operations):
        op['sequence'] = (i + 1) * 10

    bom = env['mrp.bom'].create({
        'product_tmpl_id': product.product_tmpl_id.id,
        'product_id': product.id,
        'product_qty': 1.0,
        'type': 'normal',
        'bom_line_ids': [
            (0, 0, {
                'product_id': comp.id,
                'product_qty': qty,
            })
            for comp, qty in components
        ],
        'operation_ids': [
            (0, 0, op) for op in operations
        ],
    })
    return bom


def _op(name, workcenter, time_cycle):
    """Create an operation dict for a BOM routing line."""
    return {
        'name': name,
        'workcenter_id': workcenter.id,
        'time_cycle_manual': time_cycle,
    }
