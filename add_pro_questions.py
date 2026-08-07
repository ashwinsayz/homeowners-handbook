import json
import os
from collections import OrderedDict

TASKS_DIR = "/Users/ashwinseshadri/HomeHandbook/homeowners-handbook-repo/data/tasks"

PRO_QUESTIONS = {
    "annual-furnace-tune-up-inspection": [
        "Are you licensed and insured to work on gas/oil furnaces in this state?",
        "Does this tune-up include a combustion efficiency test and carbon monoxide safety check?",
        "How do you inspect the heat exchanger for cracks—do you use a camera?",
        "Will you provide a written report noting any parts within 1–2 years of end of life?",
        "If you find something that needs repair, will you quote it before starting work?",
        "Does the service include inspecting and cleaning the flue and venting?",
        "How often do you recommend this service for a furnace of my age and type?",
    ],
    "clean-and-inspect-the-chimney": [
        "Are you CSIA (Chimney Safety Institute of America) certified?",
        "What inspection level will you perform—Level 1, 2, or 3—and what does each cover?",
        "Do you use a video camera to inspect the flue liner for cracks or deterioration?",
        "How do you measure and remove creosote buildup, and what stage is mine at?",
        "If you find a cracked liner or structural damage, will you provide a written estimate before doing any work?",
        "Are there any fire code issues with my fireplace or insert configuration?",
        "What is the expected timeframe before I need cleaning again given my usage?",
    ],
    "install-a-whole-panel-surge-protector": [
        "Are you a licensed electrician, and do you carry liability insurance?",
        "What brand and model surge protector do you recommend, and what is its joule rating and clamping voltage?",
        "Does my panel have sufficient breaker space, or will additional panel work be needed?",
        "Will this job require a permit, and will you pull and close it?",
        "Does the unit have a status indicator light so I know when it needs replacing?",
        "Will this protect my HVAC system and large appliances, or do I need supplemental point-of-use protection?",
        "What is the warranty on the device, and does your labor come with a guarantee?",
    ],
    "patch-a-roof-leak-shingle-repair": [
        "Are you licensed, insured, and experienced specifically with shingle roofs?",
        "Will you inspect the underlayment and flashing around the repair area—not just the visible shingles?",
        "Can you match my existing shingle color, profile, and manufacturer?",
        "Will you provide before-and-after photos of the completed repair?",
        "What is the estimated remaining lifespan of my roof based on what you observe?",
        "Does the repair come with a workmanship warranty, and for how long?",
        "Should I file a homeowner's insurance claim for this damage, or would that affect my rates?",
    ],
    "snake-a-main-sewer-line": [
        "Are you a licensed plumber?",
        "Do you recommend adding a camera inspection to check for root intrusion, pipe offset, or collapse?",
        "Where is my sewer cleanout, and is it accessible without excavation?",
        "If you find a collapsed or severely damaged section, what are the repair options and rough cost range?",
        "How long should the line stay clear after this service under normal conditions?",
        "Do you offer a service guarantee, and what does it cover if the clog returns quickly?",
        "What early warning signs should I watch for to know the blockage is recurring?",
    ],
    "add-attic-duct-insulation": [
        "Are you BPI or RESNET certified, or do you have energy auditor credentials?",
        "What R-value do you recommend for my climate zone, and what is my current level?",
        "Will you air-seal attic penetrations before adding insulation, and is that included in the quote?",
        "What insulation type do you recommend—blown-in, batt, or spray foam—and why?",
        "Will you confirm soffit vents stay clear and unblocked after installation?",
        "Do you check for moisture, mold, or pest issues in the attic before insulating?",
        "Can I qualify for utility rebates or federal energy efficiency tax credits on this work?",
    ],
    "aerate-and-overseed-the-lawn": [
        "Do you use a core aerator that pulls plugs, not a spike aerator?",
        "What seed variety do you recommend for my soil type, climate, and sun/shade conditions?",
        "How many passes will you make with the aerator, and in what pattern?",
        "What starter fertilizer will you apply, and is it included in the price?",
        "What watering schedule should I follow in the weeks after overseeding?",
        "How long before the new grass is established enough to mow?",
        "What germination rate should I expect, and what is your policy if results are poor?",
    ],
    "clean-gutters": [
        "Are you insured for work at height?",
        "Will you inspect for loose hangers, sagging sections, and rust spots while you are up there?",
        "Do you flush the downspouts to confirm they drain freely?",
        "Will you check that downspout extensions are directing water at least 6 feet from the foundation?",
        "Do you take photos of any damage or problem areas you find?",
        "What is your policy if a gutter section is damaged during the cleaning?",
    ],
    "fix-a-leaking-pipe-joint": [
        "Are you a licensed plumber?",
        "Is this repair permanent, or a temporary fix that will need to be revisited?",
        "Will you inspect the surrounding pipe for corrosion, pinhole pitting, or other weak spots?",
        "Is there water damage to surrounding walls, flooring, or insulation that needs to be addressed?",
        "Is a permit required for this type of repair in my municipality?",
        "What caused this joint to fail—age, pressure surges, movement—and is it likely to recur elsewhere?",
        "Does the repair come with a warranty?",
    ],
    "fix-loose-or-bubbling-carpet": [
        "What is the root cause of the buckling—improper installation, humidity changes, or subfloor movement?",
        "Will you use a power stretcher rather than just a knee kicker to ensure a permanent fix?",
        "Will you inspect and replace any tack strips that are damaged, rusted, or pulling away?",
        "Is there any subfloor damage or moisture underneath that needs to be addressed before the re-stretch?",
        "How long should a proper power stretch last before this happens again?",
        "Do you guarantee the repair, and for how long?",
    ],
    "grade-soil-away-from-the-foundation": [
        "What slope and distance from the foundation do you recommend for proper drainage?",
        "What type of fill material do you use, and does it compact and drain appropriately?",
        "Will you check and coordinate with downspout discharge locations as part of this work?",
        "Are there underground utilities, irrigation lines, or tree roots I should know about before grading?",
        "Will this grading affect my landscaping or existing plants, and how will you protect them?",
        "How long until the new grade settles, and will I likely need a follow-up pass?",
    ],
    "inspect-roof-flashing": [
        "Will you inspect all flashing points—chimney, skylights, valleys, pipe boots, and eave drip edges?",
        "Will you check the caulk and sealant at each flashing point for cracking or separation?",
        "If flashing needs replacing, what material do you use—aluminum, galvanized steel, or copper?",
        "Do you provide a written report of findings with photos?",
        "Are there signs of existing water intrusion or staining under the flashing?",
        "What is the expected lifespan of any new flashing you install?",
    ],
    "install-a-whole-home-water-leak-sensor-shutoff": [
        "Are you a licensed plumber with experience installing smart water shutoff devices?",
        "Where on the water main will the valve be installed, and will it shut off the whole house?",
        "Will you test the automatic shutoff by simulating a leak trigger after installation?",
        "What is the power source—hardwired, battery, or both—and what is battery life?",
        "Does the system work if my Wi-Fi goes down, and how will I be notified of a shutoff?",
        "Is installation compatible with my pipe material—copper, PEX, galvanized, or CPVC?",
        "What is the warranty on the device, and does your installation labor come with a guarantee?",
    ],
    "install-gutter-guards": [
        "What type of guard do you install, and how does it perform against fine debris like pine needles and shingle grit?",
        "Are the guards compatible with my gutter size, material, and roof pitch?",
        "Will you clean the gutters thoroughly before installing the guards?",
        "What maintenance will still be required after installation, and how often?",
        "Could the guard installation void my roof manufacturer's warranty if it slides under the shingles?",
        "What is the product warranty and your installation workmanship warranty?",
    ],
    "install-smart-smoke-co-detectors": [
        "Are you a licensed electrician for hardwired installations?",
        "Will all detectors be hardwired and interconnected so every unit sounds when one triggers?",
        "Are these units compatible with my existing alarm wiring?",
        "Do they meet current building code requirements for placement and quantity in my jurisdiction?",
        "Do they include both smoke and carbon monoxide detection in one unit?",
        "What is the battery backup duration in a power outage?",
        "What is the useful lifespan and when will I need to replace the sensors?",
    ],
    "power-wash-siding-and-driveway": [
        "What PSI do you use on my siding material, and how do you adjust for vinyl versus wood versus stucco?",
        "Do you offer soft washing as an alternative for delicate surfaces like painted wood or stucco?",
        "What cleaning chemicals or detergents, if any, will you apply?",
        "How will you protect windows, plants, outdoor electrical outlets, and light fixtures?",
        "Can high-pressure water be driven behind my siding, and how do you prevent that?",
        "Are you insured for any accidental property damage during the job?",
    ],
    "refinish-hardwood-floors": [
        "Do you use a dustless sanding system, and how well does it contain fine particles?",
        "What grit progression do you use, and will you make multiple directional passes?",
        "What finish do you recommend—oil-based polyurethane, water-based, or hardwax oil—and why for my situation?",
        "Are any boards too thin from prior sandings, cupped, or damaged and unable to be refinished?",
        "How long until I can walk on the floor with socks, and how long before furniture can go back?",
        "What stain options are available, and can I see physical samples on my wood species?",
        "Are the VOC levels safe for children or pets during and after curing?",
    ],
    "repair-a-squeaky-or-soft-subfloor-spot": [
        "What is causing the issue—subfloor movement, failed fasteners, or joist damage?",
        "Will you access the area from below through the basement or crawlspace, or from above through the finished floor?",
        "If the subfloor is soft, is there rot, moisture damage, or mold present, and how extensive is it?",
        "If rot is found, should I call a mold or water remediation specialist before you proceed?",
        "Will this repair require removing and replacing any finished flooring above the affected area?",
        "What fasteners or adhesives do you use, and are they appropriate for subfloor applications?",
    ],
    "repair-or-replace-damaged-siding": [
        "Can you source siding that matches my existing profile, color, and manufacturer?",
        "Will you inspect and repair the weather barrier or house wrap behind the damaged section?",
        "Is there moisture damage, rot, or mold in the wall cavity that needs to be remediated first?",
        "Will the repair be visually seamless, or will there be a visible patch or color difference?",
        "Is a permit required for siding replacement in my area?",
        "What is the warranty on materials and your workmanship?",
    ],
    "replace-an-oven-igniter-gas-range": [
        "Are you familiar with my brand and model, and do you have access to OEM parts for it?",
        "Will you confirm the igniter is the actual fault before ordering parts—could it be the gas valve, igniter module, or wiring?",
        "Will you test for gas leaks with a detector after reassembling the range?",
        "Do you use OEM or aftermarket replacement parts, and what is the warranty on the part?",
        "What is included in the service call—diagnosis, parts, and labor?",
        "If you find additional problems, will you quote them and get my approval before proceeding?",
    ],
    "reseal-an-asphalt-driveway": [
        "How will you clean and prepare the surface—power washing, degreasing, crack filling?",
        "Will you fill all cracks before sealing, and what crack filler product do you use?",
        "How many coats will you apply, and what is the drying time between coats?",
        "What brand and formulation of sealer do you use—coal tar emulsion or asphalt emulsion—and what are the tradeoffs?",
        "How long must I stay off the driveway before driving on it?",
        "How many years should this sealing job last, and what is your workmanship warranty?",
    ],
    "seal-foundation-cracks": [
        "How do you determine whether a crack is cosmetic versus structurally significant?",
        "What repair method do you use—epoxy injection, polyurethane foam, or hydraulic cement—and why for this crack?",
        "Will you mark the crack to monitor whether it is still actively growing before sealing?",
        "Do you address the underlying drainage or hydrostatic pressure cause, or only seal the symptom?",
        "Is interior drainage or exterior waterproofing also recommended in my situation?",
        "Do you offer a warranty on the repair, and for how long?",
        "Should I have a structural engineer assess this before or after repair?",
    ],
    "seal-leaky-air-ducts": [
        "Will you use Aeroseal pressurized spray or hand-applied mastic, and which is more effective for my duct layout?",
        "Can you perform a duct blaster test before and after to quantify the leakage reduction?",
        "Will you seal both supply and return ducts?",
        "Are there sections of ductwork too deteriorated to seal that need full replacement?",
        "Will the work include insulating ducts that run through unconditioned spaces?",
        "Can I qualify for a utility rebate for duct sealing, and will you provide documentation?",
    ],
    "stain-and-seal-a-wood-deck": [
        "Will you power wash and strip all existing sealer before applying the new product?",
        "What brand and type of stain or sealer do you recommend for my wood species and climate?",
        "Are you applying a solid, semi-transparent, or clear product, and what are the tradeoffs for durability and appearance?",
        "How many coats will you apply, and how do you handle end grain and board edges?",
        "Are there any boards that are rotted, cracked, or structurally compromised that need replacing first?",
        "How long before I can use the deck after application, and when is full cure achieved?",
        "How many years should this last, and what maintenance will I need to do in between?",
    ],
    "trim-trees-and-shrubs-near-the-roofline": [
        "Are you ISA (International Society of Arboriculture) certified or a licensed arborist?",
        "What clearance from the roof surface and gutters do you recommend for each species?",
        "Are any of my trees or limbs structurally compromised and at risk of failure?",
        "How will you handle debris—is removal and disposal included in the price?",
        "Are you insured for any damage to the roof, gutters, or property during trimming?",
        "Will improper trimming harm the long-term health or structure of my trees?",
    ],
    "troubleshoot-a-dryer-not-heating": [
        "Are you experienced with my brand and model of dryer?",
        "Will you diagnose which specific component has failed—heating element, thermal fuse, thermostat, gas valve, or igniter—before quoting a repair?",
        "Do you use OEM or aftermarket replacement parts, and what is the parts warranty?",
        "Will you inspect and clean the vent line as part of this service call?",
        "If repair cost approaches the price of a new unit, will you advise me on replacement instead?",
        "What is your diagnostic fee, and does it apply toward the repair cost if I proceed?",
    ],
    "winterize-a-sprinkler-irrigation-system": [
        "Do you use compressed air blow-out, and what PSI do you use for my pipe material—PVC versus polyethylene?",
        "How many passes per zone do you make to ensure all water is expelled?",
        "Will you check for broken heads, leaks, or valve issues before winterizing?",
        "Do you document which zones were serviced and confirm each is clear?",
        "Will you properly shut off and drain the backflow preventer, and insulate it if needed?",
        "When should I schedule spring startup, and do you offer a combined annual service package?",
    ],
}


def load_json_ordered(path):
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f, object_pairs_hook=OrderedDict)


def insert_after_steps(data, questions):
    new_data = OrderedDict()
    for key, value in data.items():
        new_data[key] = value
        if key == "steps":
            new_data["pro_questions"] = questions
    return new_data


def write_json(path, data):
    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)
        f.write("\n")


updated = 0
skipped = 0
missing_files = []

for slug, questions in PRO_QUESTIONS.items():
    file_path = os.path.join(TASKS_DIR, f"{slug}.json")
    if not os.path.exists(file_path):
        missing_files.append(slug)
        continue

    data = load_json_ordered(file_path)

    if "pro_questions" in data:
        print(f"  SKIP (already has pro_questions): {slug}")
        skipped += 1
        continue

    if "steps" not in data:
        print(f"  WARNING (no 'steps' key found): {slug}")
        # Still add at end
        data["pro_questions"] = questions
    else:
        data = insert_after_steps(data, questions)

    write_json(file_path, data)
    print(f"  Updated: {slug}")
    updated += 1

print()
print(f"Summary: {updated} files updated, {skipped} already had pro_questions.")
if missing_files:
    print(f"Missing files ({len(missing_files)}): {', '.join(missing_files)}")
