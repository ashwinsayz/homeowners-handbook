#!/usr/bin/env python3
"""
Insert a 'materials' array into every task JSON file.
Placement: after 'pro_questions' if present, otherwise after 'steps'.
"""
import json
import os
from collections import OrderedDict

ROOT = os.path.dirname(os.path.abspath(__file__))
TASKS_DIR = os.path.join(ROOT, "data", "tasks")

# Complete materials mapping keyed by task slug
MATERIALS = {
    "replace-hvac-air-filter": [
        {"name": "MERV-11 furnace filter", "url": "https://www.amazon.com/s?k=MERV+11+furnace+filter"},
        {"name": "Filter gauge/reminder", "url": "https://www.amazon.com/s?k=filter+change+reminder"},
    ],
    "clean-ac-condenser-outdoor-unit": [
        {"name": "AC coil cleaner spray", "url": "https://www.amazon.com/s?k=AC+coil+cleaner+spray"},
        {"name": "Garden hose nozzle", "url": "https://www.homedepot.com/s/garden%20hose%20nozzle"},
        {"name": "Fin comb", "url": "https://www.amazon.com/s?k=fin+comb+air+conditioner"},
    ],
    "annual-furnace-tune-up-inspection": [
        {"name": "MERV-11 furnace filter", "url": "https://www.amazon.com/s?k=MERV+11+furnace+filter"},
    ],
    "clean-dryer-vent": [
        {"name": "Dryer vent cleaning kit", "url": "https://www.amazon.com/s?k=dryer+vent+cleaning+kit"},
        {"name": "Vacuum with hose attachment", "url": "https://www.amazon.com/s?k=vacuum+with+hose+attachment"},
    ],
    "clean-bathroom-exhaust-fan": [
        {"name": "Compressed air can", "url": "https://www.amazon.com/s?k=compressed+air+can"},
        {"name": "Soft brush set", "url": "https://www.amazon.com/s?k=soft+detail+brush+set"},
    ],
    "seal-leaky-air-ducts": [
        {"name": "Mastic duct sealant", "url": "https://www.homedepot.com/s/mastic%20duct%20sealant"},
        {"name": "Foil HVAC tape UL-181", "url": "https://www.homedepot.com/s/foil%20HVAC%20tape%20UL-181"},
        {"name": "Duct brush", "url": "https://www.amazon.com/s?k=duct+brush"},
    ],
    "install-upgrade-a-smart-thermostat": [
        {"name": "Smart thermostat", "url": "https://www.amazon.com/s?k=smart+thermostat"},
        {"name": "Wire labels", "url": "https://www.amazon.com/s?k=wire+labels"},
        {"name": "Needle-nose pliers", "url": "https://www.amazon.com/s?k=needle+nose+pliers"},
    ],
    "clear-ac-condensate-drain-line": [
        {"name": "Distilled white vinegar", "url": "https://www.amazon.com/s?k=distilled+white+vinegar"},
        {"name": "Wet/dry vacuum", "url": "https://www.homedepot.com/s/wet%20dry%20vacuum"},
        {"name": "Condensate pan tablets", "url": "https://www.amazon.com/s?k=condensate+pan+tablets"},
    ],
    "add-attic-duct-insulation": [
        {"name": "Blown-in insulation", "url": "https://www.homedepot.com/s/blown-in%20insulation"},
        {"name": "Attic ruler/depth gauge", "url": "https://www.amazon.com/s?k=attic+insulation+depth+gauge"},
        {"name": "N95 respirator", "url": "https://www.amazon.com/s?k=N95+respirator"},
        {"name": "Safety goggles", "url": "https://www.amazon.com/s?k=safety+goggles"},
        {"name": "Attic insulation blower rental", "url": "https://www.homedepot.com/s/insulation%20blower%20rental"},
    ],
    "test-whole-home-humidifier-dehumidifier": [
        {"name": "Humidistat", "url": "https://www.amazon.com/s?k=humidistat"},
        {"name": "Water panel evaporator pad", "url": "https://www.amazon.com/s?k=water+panel+evaporator+pad"},
        {"name": "Vinegar", "url": "https://www.amazon.com/s?k=white+vinegar+gallon"},
    ],
    "fix-a-running-toilet": [
        {"name": "Toilet flapper kit", "url": "https://www.homedepot.com/s/toilet%20flapper%20kit"},
        {"name": "Toilet fill valve", "url": "https://www.homedepot.com/s/toilet%20fill%20valve"},
        {"name": "Adjustable wrench", "url": "https://www.amazon.com/s?k=adjustable+wrench"},
    ],
    "unclog-a-sink-or-tub-drain": [
        {"name": "Drain snake/auger", "url": "https://www.amazon.com/s?k=drain+snake+auger"},
        {"name": "Drain hair catcher", "url": "https://www.amazon.com/s?k=drain+hair+catcher"},
        {"name": "Baking soda and vinegar", "url": "https://www.amazon.com/s?k=baking+soda+white+vinegar"},
    ],
    "replace-a-kitchen-or-bath-faucet": [
        {"name": "Kitchen or bathroom faucet", "url": "https://www.amazon.com/s?k=kitchen+bathroom+faucet"},
        {"name": "Plumber's putty", "url": "https://www.homedepot.com/s/plumber%27s%20putty"},
        {"name": "Teflon tape", "url": "https://www.homedepot.com/s/Teflon%20tape"},
        {"name": "Basin wrench", "url": "https://www.amazon.com/s?k=basin+wrench"},
        {"name": "Supply lines", "url": "https://www.homedepot.com/s/faucet%20supply%20lines"},
    ],
    "fix-a-dripping-faucet-cartridge-washer": [
        {"name": "Faucet cartridge replacement kit", "url": "https://www.amazon.com/s?k=faucet+cartridge+replacement+kit"},
        {"name": "Plumber's grease", "url": "https://www.amazon.com/s?k=plumber%27s+grease"},
        {"name": "Teflon tape", "url": "https://www.homedepot.com/s/Teflon%20tape"},
    ],
    "install-a-new-toilet": [
        {"name": "Toilet", "url": "https://www.homedepot.com/s/toilet"},
        {"name": "Wax ring with horn", "url": "https://www.homedepot.com/s/wax%20ring%20with%20horn"},
        {"name": "Toilet supply line", "url": "https://www.lowes.com/search?searchTerm=toilet+supply+line"},
        {"name": "Toilet bolts", "url": "https://www.homedepot.com/s/toilet%20bolts"},
        {"name": "Adjustable wrench", "url": "https://www.amazon.com/s?k=adjustable+wrench"},
    ],
    "fix-a-leaking-pipe-joint": [
        {"name": "Pipe repair clamp", "url": "https://www.homedepot.com/s/pipe%20repair%20clamp"},
        {"name": "Pipe epoxy putty", "url": "https://www.homedepot.com/s/pipe%20epoxy%20putty"},
        {"name": "Teflon tape", "url": "https://www.homedepot.com/s/Teflon%20tape"},
        {"name": "Pipe cutter", "url": "https://www.amazon.com/s?k=pipe+cutter"},
    ],
    "replace-a-toilet-wax-ring": [
        {"name": "Wax ring with horn", "url": "https://www.homedepot.com/s/wax%20ring%20with%20horn"},
        {"name": "Toilet supply line", "url": "https://www.lowes.com/search?searchTerm=toilet+supply+line"},
        {"name": "Rubber gloves", "url": "https://www.amazon.com/s?k=rubber+gloves"},
    ],
    "snake-a-main-sewer-line": [
        {"name": "Sewer camera rental", "url": "https://www.homedepot.com/s/sewer%20camera%20rental"},
        {"name": "Sewer cleanout plug", "url": "https://www.homedepot.com/s/sewer%20cleanout%20plug"},
    ],
    "insulate-exposed-pipes": [
        {"name": "Foam pipe insulation", "url": "https://www.homedepot.com/s/foam%20pipe%20insulation"},
        {"name": "Pipe insulation tape", "url": "https://www.amazon.com/s?k=pipe+insulation+tape"},
        {"name": "Zip ties", "url": "https://www.amazon.com/s?k=zip+ties"},
    ],
    "winterize-outdoor-spigots": [
        {"name": "Outdoor faucet cover", "url": "https://www.amazon.com/s?k=outdoor+faucet+cover"},
        {"name": "Indoor water shutoff key", "url": "https://www.amazon.com/s?k=indoor+water+shutoff+key"},
    ],
    "replace-a-garbage-disposal": [
        {"name": "Garbage disposal", "url": "https://www.amazon.com/s?k=garbage+disposal"},
        {"name": "Plumber's putty", "url": "https://www.homedepot.com/s/plumber%27s%20putty"},
        {"name": "Disposal wrench", "url": "https://www.amazon.com/s?k=garbage+disposal+wrench"},
        {"name": "Electrical cord kit", "url": "https://www.amazon.com/s?k=garbage+disposal+electrical+cord+kit"},
    ],
    "fix-a-jammed-humming-garbage-disposal": [
        {"name": "Garbage disposal wrench key", "url": "https://www.amazon.com/s?k=garbage+disposal+hex+wrench+key"},
        {"name": "Garbage disposal cleaner pods", "url": "https://www.amazon.com/s?k=garbage+disposal+cleaner+pods"},
    ],
    "replace-supply-lines-braided-hoses": [
        {"name": "Braided stainless supply lines", "url": "https://www.homedepot.com/s/braided%20stainless%20supply%20lines"},
        {"name": "Adjustable wrench", "url": "https://www.amazon.com/s?k=adjustable+wrench"},
        {"name": "Plumber's tape", "url": "https://www.homedepot.com/s/plumber%27s%20tape"},
    ],
    "test-and-maintain-a-sump-pump": [
        {"name": "Sump pump float switch", "url": "https://www.amazon.com/s?k=sump+pump+float+switch"},
        {"name": "Sump pump backup", "url": "https://www.amazon.com/s?k=sump+pump+backup"},
        {"name": "PVC cement", "url": "https://www.homedepot.com/s/PVC%20cement"},
    ],
    "flush-water-heater-sediment": [
        {"name": "Garden hose", "url": "https://www.amazon.com/s?k=garden+hose"},
        {"name": "Hose bibb", "url": "https://www.homedepot.com/s/hose%20bibb"},
        {"name": "Water heater anode rod", "url": "https://www.amazon.com/s?k=water+heater+anode+rod"},
    ],
    "replace-a-light-switch": [
        {"name": "Light switch", "url": "https://www.homedepot.com/s/light%20switch"},
        {"name": "Wire stripper", "url": "https://www.amazon.com/s?k=wire+stripper"},
        {"name": "Voltage tester", "url": "https://www.amazon.com/s?k=non-contact+voltage+tester"},
        {"name": "Electrical tape", "url": "https://www.homedepot.com/s/electrical%20tape"},
    ],
    "replace-an-electrical-outlet": [
        {"name": "Electrical outlet", "url": "https://www.homedepot.com/s/electrical%20outlet"},
        {"name": "Voltage tester", "url": "https://www.amazon.com/s?k=non-contact+voltage+tester"},
        {"name": "Wire stripper", "url": "https://www.amazon.com/s?k=wire+stripper"},
        {"name": "Electrical box", "url": "https://www.homedepot.com/s/electrical%20box"},
    ],
    "install-replace-a-gfci-outlet": [
        {"name": "GFCI outlet", "url": "https://www.homedepot.com/s/GFCI%20outlet"},
        {"name": "Voltage tester", "url": "https://www.amazon.com/s?k=non-contact+voltage+tester"},
        {"name": "Wire stripper", "url": "https://www.amazon.com/s?k=wire+stripper"},
    ],
    "reset-a-tripped-breaker": [
        {"name": "Circuit breaker finder", "url": "https://www.amazon.com/s?k=circuit+breaker+finder"},
        {"name": "Flashlight", "url": "https://www.amazon.com/s?k=flashlight"},
    ],
    "replace-a-ceiling-fan-or-light-fixture": [
        {"name": "Ceiling fan or light fixture", "url": "https://www.amazon.com/s?k=ceiling+fan+light+fixture"},
        {"name": "Ceiling fan mounting bracket", "url": "https://www.homedepot.com/s/ceiling%20fan%20mounting%20bracket"},
        {"name": "Wire nuts", "url": "https://www.homedepot.com/s/wire%20nuts"},
        {"name": "Voltage tester", "url": "https://www.amazon.com/s?k=non-contact+voltage+tester"},
    ],
    "install-a-dimmer-switch": [
        {"name": "Dimmer switch", "url": "https://www.amazon.com/s?k=dimmer+switch"},
        {"name": "Voltage tester", "url": "https://www.amazon.com/s?k=non-contact+voltage+tester"},
        {"name": "Wire stripper", "url": "https://www.amazon.com/s?k=wire+stripper"},
    ],
    "test-replace-smoke-detector-batteries": [
        {"name": "9V batteries", "url": "https://www.amazon.com/s?k=9V+batteries"},
        {"name": "AA or AAA batteries", "url": "https://www.amazon.com/s?k=AA+AAA+batteries"},
    ],
    "diagnose-a-dead-outlet-no-power": [
        {"name": "Non-contact voltage tester", "url": "https://www.amazon.com/s?k=non-contact+voltage+tester"},
        {"name": "Outlet tester plug", "url": "https://www.amazon.com/s?k=outlet+tester+plug"},
    ],
    "install-a-whole-panel-surge-protector": [
        {"name": "Whole-house surge protector SPD", "url": "https://www.amazon.com/s?k=whole+house+surge+protector+SPD"},
        {"name": "Wire connectors", "url": "https://www.homedepot.com/s/wire%20connectors"},
    ],
    "clean-gutters": [
        {"name": "Gutter scoop", "url": "https://www.amazon.com/s?k=gutter+scoop"},
        {"name": "Garden hose with spray nozzle", "url": "https://www.amazon.com/s?k=garden+hose+spray+nozzle"},
        {"name": "Safety ladder stabilizer", "url": "https://www.amazon.com/s?k=ladder+stabilizer"},
        {"name": "Work gloves", "url": "https://www.amazon.com/s?k=work+gloves"},
    ],
    "install-gutter-guards": [
        {"name": "Gutter guard", "url": "https://www.lowes.com/search?searchTerm=gutter+guard"},
        {"name": "Tin snips", "url": "https://www.amazon.com/s?k=tin+snips"},
        {"name": "Safety ladder", "url": "https://www.amazon.com/s?k=safety+ladder"},
    ],
    "patch-a-roof-leak-shingle-repair": [
        {"name": "Roofing cement", "url": "https://www.homedepot.com/s/roofing%20cement"},
        {"name": "Replacement shingles", "url": "https://www.homedepot.com/s/replacement%20shingles"},
        {"name": "Roofing nails", "url": "https://www.homedepot.com/s/roofing%20nails"},
        {"name": "Pry bar", "url": "https://www.homedepot.com/s/pry%20bar"},
    ],
    "inspect-roof-flashing": [
        {"name": "Roofing sealant/caulk", "url": "https://www.homedepot.com/s/roofing%20sealant%20caulk"},
        {"name": "Roof flashing tape", "url": "https://www.homedepot.com/s/roof%20flashing%20tape"},
        {"name": "Sheet metal flashing", "url": "https://www.homedepot.com/s/sheet%20metal%20flashing"},
    ],
    "re-caulk-exterior-trim-and-siding": [
        {"name": "Paintable exterior caulk", "url": "https://www.homedepot.com/s/paintable%20exterior%20caulk"},
        {"name": "Caulk gun", "url": "https://www.homedepot.com/s/caulk%20gun"},
        {"name": "Caulk remover tool", "url": "https://www.amazon.com/s?k=caulk+remover+tool"},
        {"name": "Painter's tape", "url": "https://www.amazon.com/s?k=painter%27s+tape"},
    ],
    "power-wash-siding-and-driveway": [
        {"name": "Pressure washer", "url": "https://www.amazon.com/s?k=pressure+washer"},
        {"name": "Pressure washer detergent", "url": "https://www.amazon.com/s?k=pressure+washer+detergent"},
        {"name": "Surface cleaner attachment", "url": "https://www.amazon.com/s?k=pressure+washer+surface+cleaner+attachment"},
    ],
    "repair-or-replace-damaged-siding": [
        {"name": "Vinyl siding", "url": "https://www.lowes.com/search?searchTerm=vinyl+siding"},
        {"name": "Siding removal tool", "url": "https://www.amazon.com/s?k=siding+removal+tool"},
        {"name": "Exterior caulk", "url": "https://www.homedepot.com/s/exterior%20caulk"},
        {"name": "Color-matched paint", "url": "https://www.homedepot.com/s/color+matched+paint"},
    ],
    "seal-foundation-cracks": [
        {"name": "Concrete crack filler", "url": "https://www.homedepot.com/s/concrete%20crack%20filler"},
        {"name": "Epoxy injection kit", "url": "https://www.amazon.com/s?k=epoxy+injection+kit+concrete"},
        {"name": "Wire brush", "url": "https://www.homedepot.com/s/wire%20brush"},
        {"name": "Hydraulic cement", "url": "https://www.homedepot.com/s/hydraulic%20cement"},
    ],
    "repair-a-driveway-crack": [
        {"name": "Asphalt crack filler", "url": "https://www.homedepot.com/s/asphalt%20crack%20filler"},
        {"name": "Asphalt patching compound", "url": "https://www.homedepot.com/s/asphalt%20patching%20compound"},
        {"name": "Tamper", "url": "https://www.homedepot.com/s/tamper"},
    ],
    "clean-and-inspect-the-chimney": [
        {"name": "Chimney cleaning log", "url": "https://www.amazon.com/s?k=chimney+cleaning+log"},
        {"name": "Chimney cap", "url": "https://www.amazon.com/s?k=chimney+cap"},
    ],
    "patch-a-small-drywall-hole": [
        {"name": "Drywall patch kit", "url": "https://www.homedepot.com/s/drywall%20patch%20kit"},
        {"name": "Spackle", "url": "https://www.homedepot.com/s/spackle"},
        {"name": "Putty knife", "url": "https://www.homedepot.com/s/putty%20knife"},
        {"name": "Sandpaper", "url": "https://www.homedepot.com/s/sandpaper"},
    ],
    "patch-a-large-drywall-hole": [
        {"name": "Drywall sheet", "url": "https://www.homedepot.com/s/drywall%20sheet"},
        {"name": "Drywall screws", "url": "https://www.homedepot.com/s/drywall%20screws"},
        {"name": "Joint compound", "url": "https://www.homedepot.com/s/joint%20compound"},
        {"name": "Drywall tape", "url": "https://www.homedepot.com/s/drywall%20tape"},
        {"name": "Corner bead", "url": "https://www.homedepot.com/s/corner%20bead"},
        {"name": "Sandpaper", "url": "https://www.homedepot.com/s/sandpaper"},
    ],
    "fix-nail-pops": [
        {"name": "Drywall screws", "url": "https://www.homedepot.com/s/drywall%20screws"},
        {"name": "Spackle", "url": "https://www.homedepot.com/s/spackle"},
        {"name": "Putty knife", "url": "https://www.homedepot.com/s/putty%20knife"},
        {"name": "Sandpaper", "url": "https://www.homedepot.com/s/sandpaper"},
    ],
    "re-caulk-bathtub-or-shower": [
        {"name": "100% silicone tub and tile caulk", "url": "https://www.homedepot.com/s/silicone%20tub%20and%20tile%20caulk"},
        {"name": "Caulk remover tool", "url": "https://www.amazon.com/s?k=caulk+remover+tool"},
        {"name": "Caulk gun", "url": "https://www.homedepot.com/s/caulk%20gun"},
        {"name": "Painter's tape", "url": "https://www.amazon.com/s?k=painter%27s+tape"},
    ],
    "paint-a-room-interior": [
        {"name": "Interior latex paint", "url": "https://www.homedepot.com/s/interior%20latex%20paint"},
        {"name": "Paint primer", "url": "https://www.homedepot.com/s/paint%20primer"},
        {"name": "Roller kit", "url": "https://www.homedepot.com/s/paint%20roller%20kit"},
        {"name": "Painter's tape", "url": "https://www.amazon.com/s?k=painter%27s+tape"},
        {"name": "Drop cloth", "url": "https://www.homedepot.com/s/drop%20cloth"},
        {"name": "Angled brush", "url": "https://www.homedepot.com/s/angled%20paint%20brush"},
    ],
    "fix-a-squeaky-floor-or-stairs": [
        {"name": "Construction adhesive", "url": "https://www.homedepot.com/s/construction%20adhesive"},
        {"name": "Wood screws", "url": "https://www.homedepot.com/s/wood%20screws"},
        {"name": "Squeak-relief screw kit", "url": "https://www.amazon.com/s?k=squeak+relief+screw+kit"},
    ],
    "repair-a-popcorn-ceiling-spot": [
        {"name": "Popcorn ceiling patch spray", "url": "https://www.amazon.com/s?k=popcorn+ceiling+patch+spray"},
        {"name": "Drywall joint compound", "url": "https://www.homedepot.com/s/drywall%20joint%20compound"},
        {"name": "Paint primer", "url": "https://www.homedepot.com/s/paint%20primer"},
    ],
    "fill-gaps-in-trim-baseboard-with-wood-filler": [
        {"name": "Paintable wood filler", "url": "https://www.homedepot.com/s/paintable%20wood%20filler"},
        {"name": "Putty knife", "url": "https://www.homedepot.com/s/putty%20knife"},
        {"name": "Sandpaper", "url": "https://www.amazon.com/s?k=sandpaper+assortment"},
    ],
    "touch-up-trim-and-baseboard-paint": [
        {"name": "Trim paint", "url": "https://www.homedepot.com/s/trim%20paint"},
        {"name": "Angled brush", "url": "https://www.homedepot.com/s/angled%20paint%20brush"},
        {"name": "Painter's tape", "url": "https://www.amazon.com/s?k=painter%27s+tape"},
    ],
    "fix-a-sticking-interior-door": [
        {"name": "Wood plane or belt sander", "url": "https://www.amazon.com/s?k=wood+hand+plane"},
        {"name": "Sandpaper", "url": "https://www.amazon.com/s?k=sandpaper+assortment"},
        {"name": "Wood sealer", "url": "https://www.homedepot.com/s/wood%20sealer"},
        {"name": "Door hinge screws", "url": "https://www.homedepot.com/s/door%20hinge%20screws"},
    ],
    "clean-refrigerator-coils": [
        {"name": "Refrigerator coil brush", "url": "https://www.amazon.com/s?k=refrigerator+coil+brush"},
        {"name": "Vacuum with brush attachment", "url": "https://www.amazon.com/s?k=vacuum+brush+attachment"},
    ],
    "replace-refrigerator-water-filter": [
        {"name": "Refrigerator water filter", "url": "https://www.amazon.com/s?k=refrigerator+water+filter"},
    ],
    "clean-dishwasher-filter-and-drain": [
        {"name": "White vinegar", "url": "https://www.amazon.com/s?k=white+vinegar+gallon"},
        {"name": "Dishwasher cleaner tablet", "url": "https://www.amazon.com/s?k=dishwasher+cleaner+tablet"},
        {"name": "Soft brush", "url": "https://www.amazon.com/s?k=soft+cleaning+brush"},
    ],
    "level-a-washing-machine": [
        {"name": "Adjustable wrench", "url": "https://www.amazon.com/s?k=adjustable+wrench"},
        {"name": "Torpedo level", "url": "https://www.amazon.com/s?k=torpedo+level"},
        {"name": "Anti-vibration pads", "url": "https://www.amazon.com/s?k=anti+vibration+pads+washing+machine"},
    ],
    "clean-washing-machine-mold-odor": [
        {"name": "Washing machine cleaner tablets", "url": "https://www.amazon.com/s?k=washing+machine+cleaner+tablets"},
        {"name": "White vinegar", "url": "https://www.amazon.com/s?k=white+vinegar+gallon"},
        {"name": "Baking soda", "url": "https://www.amazon.com/s?k=baking+soda"},
    ],
    "replace-an-oven-igniter-gas-range": [
        {"name": "Oven igniter", "url": "https://www.amazon.com/s?k=oven+igniter+gas+range"},
        {"name": "Oven-rated wire connectors", "url": "https://www.amazon.com/s?k=oven+rated+wire+connectors"},
    ],
    "deep-clean-an-oven": [
        {"name": "Oven cleaner spray", "url": "https://www.amazon.com/s?k=oven+cleaner+spray"},
        {"name": "Heavy-duty scrub pad", "url": "https://www.amazon.com/s?k=heavy+duty+scrub+pad"},
        {"name": "Baking soda", "url": "https://www.amazon.com/s?k=baking+soda"},
    ],
    "replace-range-hood-filter": [
        {"name": "Range hood grease filter", "url": "https://www.amazon.com/s?k=range+hood+grease+filter"},
        {"name": "Degreaser spray", "url": "https://www.amazon.com/s?k=kitchen+degreaser+spray"},
    ],
    "descale-a-coffee-maker-or-kettle": [
        {"name": "Descaling solution", "url": "https://www.amazon.com/s?k=descaling+solution+coffee+maker"},
        {"name": "White vinegar", "url": "https://www.amazon.com/s?k=white+vinegar+gallon"},
    ],
    "troubleshoot-a-dryer-not-heating": [
        {"name": "Dryer heating element", "url": "https://www.amazon.com/s?k=dryer+heating+element"},
        {"name": "Dryer thermal fuse", "url": "https://www.amazon.com/s?k=dryer+thermal+fuse"},
        {"name": "Dryer vent brush kit", "url": "https://www.amazon.com/s?k=dryer+vent+brush+kit"},
        {"name": "Multimeter", "url": "https://www.amazon.com/s?k=multimeter"},
    ],
    "replace-weatherstripping": [
        {"name": "Door weatherstrip kit", "url": "https://www.lowes.com/search?searchTerm=door+weatherstrip+kit"},
        {"name": "Adhesive-backed foam tape", "url": "https://www.lowes.com/search?searchTerm=adhesive+foam+tape+weatherstrip"},
        {"name": "Door sweep", "url": "https://www.lowes.com/search?searchTerm=door+sweep"},
    ],
    "re-caulk-windows": [
        {"name": "Paintable window caulk", "url": "https://www.homedepot.com/s/paintable%20window%20caulk"},
        {"name": "Caulk gun", "url": "https://www.homedepot.com/s/caulk%20gun"},
        {"name": "Caulk remover", "url": "https://www.amazon.com/s?k=caulk+remover+tool"},
    ],
    "fix-a-door-that-won-t-latch": [
        {"name": "Strike plate", "url": "https://www.homedepot.com/s/door%20strike%20plate"},
        {"name": "Door latch strike plate kit", "url": "https://www.homedepot.com/s/door%20latch%20strike%20plate%20kit"},
        {"name": "Chisel", "url": "https://www.amazon.com/s?k=wood+chisel"},
    ],
    "lubricate-door-hinges-and-hardware": [
        {"name": "WD-40 or white lithium grease", "url": "https://www.amazon.com/s?k=white+lithium+grease+spray"},
        {"name": "3-in-1 oil", "url": "https://www.amazon.com/s?k=3+in+1+oil"},
    ],
    "replace-a-broken-window-screen": [
        {"name": "Window screen replacement kit", "url": "https://www.lowes.com/search?searchTerm=window+screen+replacement+kit"},
        {"name": "Screen spline roller", "url": "https://www.amazon.com/s?k=screen+spline+roller"},
        {"name": "Screen spline", "url": "https://www.lowes.com/search?searchTerm=screen+spline"},
    ],
    "install-a-door-draft-stopper-sweep": [
        {"name": "Door sweep", "url": "https://www.lowes.com/search?searchTerm=door+sweep"},
        {"name": "Door draft stopper", "url": "https://www.amazon.com/s?k=door+draft+stopper"},
    ],
    "repair-a-garage-door-opener-sensor-issue": [
        {"name": "Garage door sensor alignment bracket", "url": "https://www.amazon.com/s?k=garage+door+sensor+alignment+bracket"},
        {"name": "Sensor wire", "url": "https://www.amazon.com/s?k=garage+door+sensor+wire"},
    ],
    "lubricate-garage-door-tracks-and-rollers": [
        {"name": "White lithium grease spray", "url": "https://www.amazon.com/s?k=white+lithium+grease+spray"},
        {"name": "Silicone spray lubricant", "url": "https://www.amazon.com/s?k=silicone+spray+lubricant"},
    ],
    "fix-a-squeaky-hardwood-floor": [
        {"name": "Squeak-relief screw kit", "url": "https://www.amazon.com/s?k=squeak+relief+screw+kit"},
        {"name": "Wood glue", "url": "https://www.homedepot.com/s/wood%20glue"},
        {"name": "Stain marker", "url": "https://www.amazon.com/s?k=wood+stain+marker"},
    ],
    "replace-a-cracked-tile": [
        {"name": "Replacement tile", "url": "https://www.lowes.com/search?searchTerm=replacement+tile"},
        {"name": "Tile adhesive mastic", "url": "https://www.homedepot.com/s/tile%20adhesive%20mastic"},
        {"name": "Tile grout", "url": "https://www.lowes.com/search?searchTerm=tile+grout"},
        {"name": "Grout float", "url": "https://www.homedepot.com/s/grout%20float"},
        {"name": "Tile spacers", "url": "https://www.lowes.com/search?searchTerm=tile+spacers"},
    ],
    "re-grout-tile": [
        {"name": "Tile grout", "url": "https://www.lowes.com/search?searchTerm=tile+grout"},
        {"name": "Grout saw/oscillating tool", "url": "https://www.amazon.com/s?k=oscillating+tool+grout+saw"},
        {"name": "Grout float", "url": "https://www.homedepot.com/s/grout%20float"},
        {"name": "Grout sealer", "url": "https://www.amazon.com/s?k=grout+sealer"},
    ],
    "patch-or-repair-vinyl-laminate-flooring": [
        {"name": "Vinyl floor repair kit", "url": "https://www.amazon.com/s?k=vinyl+floor+repair+kit"},
        {"name": "Flooring adhesive", "url": "https://www.lowes.com/search?searchTerm=flooring+adhesive"},
        {"name": "Seam sealer", "url": "https://www.amazon.com/s?k=vinyl+floor+seam+sealer"},
    ],
    "refinish-hardwood-floors": [
        {"name": "Floor finish", "url": "https://www.lowes.com/search?searchTerm=hardwood+floor+finish"},
        {"name": "Floor stain", "url": "https://www.lowes.com/search?searchTerm=hardwood+floor+stain"},
        {"name": "Floor buffer/sander rental", "url": "https://www.lowes.com/search?searchTerm=floor+sander+rental"},
        {"name": "Screen discs", "url": "https://www.lowes.com/search?searchTerm=floor+screen+discs"},
        {"name": "Tack cloth", "url": "https://www.homedepot.com/s/tack%20cloth"},
    ],
    "fix-loose-or-bubbling-carpet": [
        {"name": "Carpet seam sealer", "url": "https://www.amazon.com/s?k=carpet+seam+sealer"},
        {"name": "Carpet knee kicker", "url": "https://www.amazon.com/s?k=carpet+knee+kicker"},
        {"name": "Carpet tack strips", "url": "https://www.lowes.com/search?searchTerm=carpet+tack+strips"},
    ],
    "repair-a-squeaky-or-soft-subfloor-spot": [
        {"name": "Construction screws", "url": "https://www.homedepot.com/s/construction%20screws"},
        {"name": "Construction adhesive", "url": "https://www.homedepot.com/s/construction%20adhesive"},
        {"name": "Plywood patch", "url": "https://www.homedepot.com/s/plywood%20patch"},
    ],
    "test-and-replace-smoke-detectors": [
        {"name": "Smoke detector", "url": "https://www.amazon.com/s?k=smoke+detector"},
        {"name": "9V battery", "url": "https://www.amazon.com/s?k=9V+battery"},
    ],
    "test-and-replace-co-detectors": [
        {"name": "Carbon monoxide detector", "url": "https://www.amazon.com/s?k=carbon+monoxide+detector"},
        {"name": "AA batteries", "url": "https://www.amazon.com/s?k=AA+batteries"},
    ],
    "check-fire-extinguisher-and-service-date": [
        {"name": "ABC fire extinguisher", "url": "https://www.amazon.com/s?k=ABC+fire+extinguisher"},
        {"name": "Fire extinguisher mount bracket", "url": "https://www.amazon.com/s?k=fire+extinguisher+mount+bracket"},
    ],
    "test-gfci-and-afci-breakers": [
        {"name": "Outlet tester with GFCI test button", "url": "https://www.amazon.com/s?k=outlet+tester+GFCI+test+button"},
    ],
    "childproof-outlets-and-cabinets": [
        {"name": "Tamper-resistant outlet covers", "url": "https://www.amazon.com/s?k=tamper+resistant+outlet+covers"},
        {"name": "Cabinet safety latches", "url": "https://www.amazon.com/s?k=cabinet+safety+latches"},
        {"name": "Foam corner guards", "url": "https://www.amazon.com/s?k=foam+corner+guards"},
    ],
    "stain-and-seal-a-wood-deck": [
        {"name": "Deck stain and sealer", "url": "https://www.amazon.com/s?k=deck+stain+and+sealer"},
        {"name": "Deck cleaner", "url": "https://www.homedepot.com/s/deck%20cleaner"},
        {"name": "Pump sprayer", "url": "https://www.amazon.com/s?k=pump+sprayer"},
        {"name": "Deck brush", "url": "https://www.homedepot.com/s/deck%20brush"},
        {"name": "Painter's tape", "url": "https://www.amazon.com/s?k=painter%27s+tape"},
    ],
    "repair-loose-deck-boards-or-railings": [
        {"name": "Deck screws", "url": "https://www.homedepot.com/s/deck%20screws"},
        {"name": "Wood epoxy filler", "url": "https://www.amazon.com/s?k=wood+epoxy+filler"},
        {"name": "Post anchor", "url": "https://www.homedepot.com/s/post%20anchor"},
    ],
    "aerate-and-overseed-the-lawn": [
        {"name": "Grass seed", "url": "https://www.amazon.com/s?k=grass+seed"},
        {"name": "Lawn aerator rental", "url": "https://www.lowes.com/search?searchTerm=lawn+aerator+rental"},
        {"name": "Starter fertilizer", "url": "https://www.amazon.com/s?k=starter+fertilizer"},
        {"name": "Garden rake", "url": "https://www.amazon.com/s?k=garden+rake"},
    ],
    "winterize-a-sprinkler-irrigation-system": [
        {"name": "Blow-out adapter", "url": "https://www.amazon.com/s?k=sprinkler+blow+out+adapter"},
        {"name": "Insulation wrap for backflow preventer", "url": "https://www.amazon.com/s?k=backflow+preventer+insulation+wrap"},
    ],
    "trim-trees-and-shrubs-near-the-roofline": [
        {"name": "Bypass pruning shears", "url": "https://www.amazon.com/s?k=bypass+pruning+shears"},
        {"name": "Telescoping pruning saw", "url": "https://www.amazon.com/s?k=telescoping+pruning+saw"},
        {"name": "Safety glasses", "url": "https://www.amazon.com/s?k=safety+glasses"},
    ],
    "repair-a-fence-panel-or-post": [
        {"name": "Fence post", "url": "https://www.lowes.com/search?searchTerm=fence+post"},
        {"name": "Fence boards", "url": "https://www.lowes.com/search?searchTerm=fence+boards"},
        {"name": "Post hole concrete", "url": "https://www.homedepot.com/s/post%20hole%20concrete"},
        {"name": "Galvanized nails", "url": "https://www.homedepot.com/s/galvanized%20nails"},
    ],
    "reseal-an-asphalt-driveway": [
        {"name": "Driveway sealer", "url": "https://www.homedepot.com/s/driveway%20sealer"},
        {"name": "Crack filler", "url": "https://www.homedepot.com/s/asphalt%20crack%20filler"},
        {"name": "Squeegee applicator", "url": "https://www.homedepot.com/s/squeegee%20applicator"},
    ],
    "clean-and-store-outdoor-furniture": [
        {"name": "Outdoor furniture cleaner", "url": "https://www.amazon.com/s?k=outdoor+furniture+cleaner"},
        {"name": "Furniture covers", "url": "https://www.amazon.com/s?k=outdoor+furniture+covers"},
    ],
    "inspect-and-clean-window-wells": [
        {"name": "Window well cover", "url": "https://www.amazon.com/s?k=window+well+cover"},
        {"name": "Gravel", "url": "https://www.homedepot.com/s/landscaping%20gravel"},
        {"name": "Window well drain", "url": "https://www.homedepot.com/s/window%20well%20drain"},
    ],
    "grade-soil-away-from-the-foundation": [
        {"name": "Topsoil/fill dirt", "url": "https://www.homedepot.com/s/topsoil%20fill%20dirt"},
        {"name": "Landscaping rake", "url": "https://www.amazon.com/s?k=landscaping+rake"},
        {"name": "Sod or seed", "url": "https://www.lowes.com/search?searchTerm=sod+grass+seed"},
    ],
    "install-a-smart-thermostat": [
        {"name": "Smart thermostat", "url": "https://www.amazon.com/s?k=smart+thermostat"},
        {"name": "Wire labels", "url": "https://www.amazon.com/s?k=wire+labels"},
        {"name": "Drill and drill bits", "url": "https://www.amazon.com/s?k=drill+and+drill+bits+set"},
    ],
    "install-smart-smoke-co-detectors": [
        {"name": "Smart smoke and CO detector", "url": "https://www.amazon.com/s?k=smart+smoke+CO+detector"},
        {"name": "Drill and drill bits", "url": "https://www.amazon.com/s?k=drill+and+drill+bits+set"},
        {"name": "Wire connectors", "url": "https://www.homedepot.com/s/wire%20connectors"},
    ],
    "install-a-video-doorbell": [
        {"name": "Video doorbell", "url": "https://www.amazon.com/s?k=video+doorbell"},
        {"name": "Drill and drill bits", "url": "https://www.amazon.com/s?k=drill+and+drill+bits+set"},
        {"name": "Wire connectors", "url": "https://www.homedepot.com/s/wire%20connectors"},
    ],
    "upgrade-to-smart-locks": [
        {"name": "Smart deadbolt lock", "url": "https://www.amazon.com/s?k=smart+deadbolt+lock"},
        {"name": "Drill and hole saw kit", "url": "https://www.amazon.com/s?k=drill+hole+saw+kit"},
    ],
    "install-a-whole-home-water-leak-sensor-shutoff": [
        {"name": "Whole-home water shutoff sensor", "url": "https://www.amazon.com/s?k=whole+home+water+leak+sensor+shutoff"},
        {"name": "Pipe cutter", "url": "https://www.homedepot.com/s/pipe%20cutter"},
        {"name": "Push-fit fittings", "url": "https://www.homedepot.com/s/push+fit+fittings"},
    ],
}


def insert_after_key(d, target_key, new_key, new_value):
    """Return a new OrderedDict with new_key inserted after target_key."""
    result = OrderedDict()
    for k, v in d.items():
        result[k] = v
        if k == target_key and new_key not in d:
            result[new_key] = new_value
    return result


def process_file(path, slug, materials):
    with open(path, encoding="utf-8") as f:
        data = json.load(f, object_pairs_hook=OrderedDict)

    # Determine insertion point
    if "pro_questions" in data:
        insert_after = "pro_questions"
    else:
        insert_after = "steps"

    # Skip if already has materials
    if "materials" in data:
        print(f"  SKIP {slug} (already has materials)")
        return False

    updated = insert_after_key(data, insert_after, "materials", materials)

    with open(path, "w", encoding="utf-8") as f:
        json.dump(updated, f, indent=2, ensure_ascii=False)
        f.write("\n")

    return True


def main():
    tasks_dir = TASKS_DIR
    updated_count = 0
    missing = []

    for fname in sorted(os.listdir(tasks_dir)):
        if not fname.endswith(".json"):
            continue
        slug = fname[:-5]
        path = os.path.join(tasks_dir, fname)

        if slug not in MATERIALS:
            missing.append(slug)
            print(f"  WARNING: no materials defined for {slug}")
            continue

        changed = process_file(path, slug, MATERIALS[slug])
        if changed:
            updated_count += 1
            print(f"  OK {slug} ({len(MATERIALS[slug])} items)")

    print(f"\nDone. Updated {updated_count} files.")
    if missing:
        print(f"Missing materials definitions for {len(missing)} slugs:")
        for s in missing:
            print(f"  - {s}")


if __name__ == "__main__":
    main()
