#!/usr/bin/env python3
"""
Populate videoUrl for all 99 tasks.
Constraint: no single domain may exceed 15% of total (max 14 per domain).

Distribution (8 domains):
  thisoldhouse.com   13   13.1%
  familyhandyman.com 13   13.1%
  thespruce.com      13   13.1%
  bobvila.com        13   13.1%
  youtube.com        13   13.1%
  wikihow.com        13   13.1%
  lowes.com          12   12.1%
  bhg.com             9    9.1%
  total              99
"""
import json
import os
from collections import OrderedDict

TASKS_DIR = os.path.join(os.path.dirname(__file__), "data", "tasks")

URL_MAP = {
    # ── thisoldhouse.com (13) ─────────────────────────────────────────────
    "clean-gutters":
        "https://www.thisoldhouse.com/gutters/how-to-clean-gutters",
    "fix-a-running-toilet":
        "https://www.thisoldhouse.com/plumbing/how-to-fix-a-running-toilet",
    "fix-a-squeaky-floor-or-stairs":
        "https://www.thisoldhouse.com/flooring/21015195/how-to-fix-squeaky-floors",
    "flush-water-heater-sediment":
        "https://www.thisoldhouse.com/plumbing/draining-flushing-an-electric-water-heater",
    "install-a-smart-thermostat":
        "https://www.thisoldhouse.com/smart-homes/21017259/how-to-install-a-smart-thermostat",
    "install-replace-a-gfci-outlet":
        "https://www.thisoldhouse.com/electrical/how-to-upgrade-to-gfci-outlets",
    "patch-a-large-drywall-hole":
        "https://www.thisoldhouse.com/walls/how-to-patch-holes-in-drywall",
    "patch-a-small-drywall-hole":
        "https://www.thisoldhouse.com/walls/21017164/how-to-patch-drywall",
    "replace-a-garbage-disposal":
        "https://www.thisoldhouse.com/kitchens/how-to-install-a-garbage-disposal-3",
    "test-and-maintain-a-sump-pump":
        "https://www.thisoldhouse.com/basements/21015648/is-your-sump-pump-ready-for-spring",
    "install-a-new-toilet":
        "https://www.thisoldhouse.com/plumbing/how-to-install-a-toilet",
    "re-grout-tile":
        "https://www.thisoldhouse.com/bathrooms/21017108/how-to-regrout-a-tile-floor",
    "install-a-dimmer-switch":
        "https://www.thisoldhouse.com/electrical/how-to-install-a-dimmer-switch",

    # ── familyhandyman.com (13) ───────────────────────────────────────────
    "clean-dryer-vent":
        "https://www.familyhandyman.com/project/how-to-clean-dryer-vent/",
    "test-and-replace-smoke-detectors":
        "https://www.familyhandyman.com/project/install-new-hard-wired-or-battery-powered-smoke-alarms/",
    "unclog-a-sink-or-tub-drain":
        "https://www.familyhandyman.com/project/how-to-clear-clogged-drains/",
    "fix-a-jammed-humming-garbage-disposal":
        "https://www.familyhandyman.com/project/garbage-disposal-repair/",
    "replace-weatherstripping":
        "https://www.familyhandyman.com/project/how-to-replace-door-weatherstripping/",
    "lubricate-garage-door-tracks-and-rollers":
        "https://www.familyhandyman.com/project/garage-door-maintenance/",
    "paint-a-room-interior":
        "https://www.familyhandyman.com/project/how-to-paint-a-room/",
    "fix-a-door-that-won-t-latch":
        "https://www.familyhandyman.com/project/how-to-fix-a-door-that-wont-latch/",
    "replace-a-toilet-wax-ring":
        "https://www.familyhandyman.com/project/how-to-replace-a-toilet-wax-ring/",
    "install-a-video-doorbell":
        "https://www.familyhandyman.com/project/how-to-install-a-video-doorbell/",
    "replace-a-light-switch":
        "https://www.familyhandyman.com/project/how-to-replace-a-light-switch/",
    "repair-a-driveway-crack":
        "https://www.familyhandyman.com/project/how-to-repair-asphalt-driveway/",
    "fix-a-sticking-interior-door":
        "https://www.familyhandyman.com/project/how-to-fix-a-sticking-door/",

    # ── thespruce.com (13) ────────────────────────────────────────────────
    "clean-bathroom-exhaust-fan":
        "https://www.thespruce.com/how-to-clean-a-bathroom-exhaust-fan-2718906",
    "clean-refrigerator-coils":
        "https://www.thespruce.com/how-to-clean-refrigerator-coils-5116993",
    "clean-dishwasher-filter-and-drain":
        "https://www.thespruce.com/how-to-clean-a-dishwasher-4845547",
    "clean-washing-machine-mold-odor":
        "https://www.thespruce.com/clean-washing-machine-1824829",
    "fix-a-dripping-faucet-cartridge-washer":
        "https://www.thespruce.com/how-to-fix-a-dripping-faucet-2719158",
    "replace-a-kitchen-or-bath-faucet":
        "https://www.thespruce.com/how-to-replace-a-faucet-4047777",
    "re-caulk-bathtub-or-shower":
        "https://www.thespruce.com/recaulk-bathtub-or-shower-2718905",
    "re-caulk-windows":
        "https://www.thespruce.com/how-to-caulk-windows-2718797",
    "replace-a-broken-window-screen":
        "https://www.thespruce.com/how-to-repair-a-window-screen-2718773",
    "descale-a-coffee-maker-or-kettle":
        "https://www.thespruce.com/how-to-descale-a-coffee-maker-4685044",
    "deep-clean-an-oven":
        "https://www.thespruce.com/how-to-clean-oven-1900558",
    "replace-refrigerator-water-filter":
        "https://www.thespruce.com/how-to-replace-a-refrigerator-water-filter-5116974",
    "replace-range-hood-filter":
        "https://www.thespruce.com/how-to-clean-range-hood-filter-4801782",

    # ── bobvila.com (13) ──────────────────────────────────────────────────
    "seal-foundation-cracks":
        "https://www.bobvila.com/articles/how-to-fix-a-cracked-foundation/",
    "reseal-an-asphalt-driveway":
        "https://www.bobvila.com/articles/how-to-seal-a-driveway/",
    "repair-a-fence-panel-or-post":
        "https://www.bobvila.com/articles/how-to-repair-a-fence/",
    "stain-and-seal-a-wood-deck":
        "https://www.bobvila.com/articles/how-to-stain-a-deck/",
    "repair-loose-deck-boards-or-railings":
        "https://www.bobvila.com/articles/deck-repair/",
    "insulate-exposed-pipes":
        "https://www.bobvila.com/articles/how-to-insulate-pipes/",
    "patch-a-roof-leak-shingle-repair":
        "https://www.bobvila.com/articles/how-to-fix-a-roof-leak/",
    "repair-or-replace-damaged-siding":
        "https://www.bobvila.com/articles/how-to-replace-siding/",
    "power-wash-siding-and-driveway":
        "https://www.bobvila.com/articles/how-to-pressure-wash-a-house/",
    "winterize-outdoor-spigots":
        "https://www.bobvila.com/articles/how-to-winterize-outdoor-faucets/",
    "winterize-a-sprinkler-irrigation-system":
        "https://www.bobvila.com/articles/winterize-a-sprinkler-system/",
    "add-attic-duct-insulation":
        "https://www.bobvila.com/articles/attic-insulation/",
    "aerate-and-overseed-the-lawn":
        "https://www.bobvila.com/articles/how-to-aerate-a-lawn/",

    # ── youtube.com — search result pages (13) ────────────────────────────
    "clean-ac-condenser-outdoor-unit":
        "https://www.youtube.com/results?search_query=how+to+clean+AC+condenser+outdoor+unit",
    "diagnose-a-dead-outlet-no-power":
        "https://www.youtube.com/results?search_query=how+to+diagnose+dead+electrical+outlet+no+power",
    "repair-a-garage-door-opener-sensor-issue":
        "https://www.youtube.com/results?search_query=garage+door+opener+sensor+adjustment+repair",
    "replace-an-oven-igniter-gas-range":
        "https://www.youtube.com/results?search_query=how+to+replace+gas+oven+igniter",
    "troubleshoot-a-dryer-not-heating":
        "https://www.youtube.com/results?search_query=dryer+not+heating+how+to+fix",
    "level-a-washing-machine":
        "https://www.youtube.com/results?search_query=how+to+level+a+washing+machine",
    "reset-a-tripped-breaker":
        "https://www.youtube.com/results?search_query=how+to+reset+tripped+circuit+breaker",
    "replace-an-electrical-outlet":
        "https://www.youtube.com/results?search_query=how+to+replace+electrical+outlet",
    "fix-a-squeaky-hardwood-floor":
        "https://www.youtube.com/results?search_query=how+to+fix+squeaky+hardwood+floor",
    "install-a-whole-panel-surge-protector":
        "https://www.youtube.com/results?search_query=whole+house+surge+protector+installation",
    "upgrade-to-smart-locks":
        "https://www.youtube.com/results?search_query=how+to+install+a+smart+door+lock",
    "childproof-outlets-and-cabinets":
        "https://www.youtube.com/results?search_query=how+to+childproof+electrical+outlets+and+cabinets",
    "check-fire-extinguisher-and-service-date":
        "https://www.youtube.com/results?search_query=fire+extinguisher+inspection+maintenance",

    # ── wikihow.com (13) ─────────────────────────────────────────────────
    "clear-ac-condensate-drain-line":
        "https://www.wikihow.com/Clear-an-AC-Drain-Line",
    "fill-gaps-in-trim-baseboard-with-wood-filler":
        "https://www.wikihow.com/Fill-Gaps-in-Wood",
    "fix-nail-pops":
        "https://www.wikihow.com/Fix-Nail-Pops-in-Drywall",
    "install-a-door-draft-stopper-sweep":
        "https://www.wikihow.com/Install-a-Door-Sweep",
    "lubricate-door-hinges-and-hardware":
        "https://www.wikihow.com/Lubricate-Door-Hinges",
    "patch-or-repair-vinyl-laminate-flooring":
        "https://www.wikihow.com/Repair-Vinyl-Flooring",
    "re-caulk-exterior-trim-and-siding":
        "https://www.wikihow.com/Caulk-Siding",
    "repair-a-popcorn-ceiling-spot":
        "https://www.wikihow.com/Repair-a-Popcorn-Ceiling",
    "replace-supply-lines-braided-hoses":
        "https://www.wikihow.com/Replace-Toilet-Supply-Lines",
    "test-gfci-and-afci-breakers":
        "https://www.wikihow.com/Test-a-GFCI-Outlet",
    "test-whole-home-humidifier-dehumidifier":
        "https://www.wikihow.com/Test-a-Humidifier",
    "touch-up-trim-and-baseboard-paint":
        "https://www.wikihow.com/Touch-Up-Paint",
    "inspect-and-clean-window-wells":
        "https://www.wikihow.com/Clean-Window-Wells",

    # ── lowes.com (12) ────────────────────────────────────────────────────
    "fix-a-leaking-pipe-joint":
        "https://www.lowes.com/n/how-to/fix-a-leaky-pipe",
    "inspect-roof-flashing":
        "https://www.lowes.com/n/how-to/how-to-install-roof-flashing",
    "install-a-whole-home-water-leak-sensor-shutoff":
        "https://www.lowes.com/n/how-to/how-to-install-a-water-shutoff-valve",
    "install-gutter-guards":
        "https://www.lowes.com/n/how-to/how-to-install-gutter-guards",
    "install-upgrade-a-smart-thermostat":
        "https://www.lowes.com/n/how-to/how-to-install-a-programmable-thermostat",
    "refinish-hardwood-floors":
        "https://www.lowes.com/n/how-to/how-to-refinish-hardwood-floors",
    "repair-a-squeaky-or-soft-subfloor-spot":
        "https://www.lowes.com/n/how-to/how-to-fix-squeaky-floors",
    "replace-a-ceiling-fan-or-light-fixture":
        "https://www.lowes.com/n/how-to/how-to-install-a-ceiling-fan",
    "replace-a-cracked-tile":
        "https://www.lowes.com/n/how-to/how-to-replace-a-tile",
    "replace-hvac-air-filter":
        "https://www.lowes.com/n/how-to/how-to-change-an-hvac-filter",
    "seal-leaky-air-ducts":
        "https://www.lowes.com/n/how-to/how-to-seal-air-ducts",
    "snake-a-main-sewer-line":
        "https://www.lowes.com/n/how-to/how-to-unclog-a-drain",

    # ── bhg.com — Better Homes & Gardens (9) ─────────────────────────────
    "annual-furnace-tune-up-inspection":
        "https://www.bhg.com/home-improvement/advice/energy-efficient/furnace-maintenance-checklist/",
    "clean-and-inspect-the-chimney":
        "https://www.bhg.com/home-improvement/advice/how-to-clean-a-fireplace-and-chimney/",
    "fix-loose-or-bubbling-carpet":
        "https://www.bhg.com/home-improvement/flooring/carpet/how-to-re-stretch-carpet/",
    "grade-soil-away-from-the-foundation":
        "https://www.bhg.com/home-improvement/advice/grading-around-house-foundation/",
    "install-smart-smoke-co-detectors":
        "https://www.bhg.com/home-improvement/advice/home-safety/smoke-detector-placement-guide/",
    "test-and-replace-co-detectors":
        "https://www.bhg.com/home-improvement/advice/home-safety/carbon-monoxide-detector-guide/",
    "test-replace-smoke-detector-batteries":
        "https://www.bhg.com/home-improvement/advice/home-safety/smoke-detector-battery-replacement/",
    "trim-trees-and-shrubs-near-the-roofline":
        "https://www.bhg.com/gardening/trees-shrubs-vines/trees/how-to-prune-trees/",
    "clean-and-store-outdoor-furniture":
        "https://www.bhg.com/home-improvement/advice/how-to-clean-outdoor-furniture/",
}


def update_tasks():
    from urllib.parse import urlparse
    from collections import Counter

    updated = 0
    skipped = []
    domain_count = Counter()

    for fname in sorted(os.listdir(TASKS_DIR)):
        if not fname.endswith(".json"):
            continue
        path = os.path.join(TASKS_DIR, fname)
        with open(path, encoding="utf-8") as f:
            data = json.load(f, object_pairs_hook=OrderedDict)

        slug = data["slug"]
        if slug not in URL_MAP:
            skipped.append(slug)
            continue

        url = URL_MAP[slug]
        data["videoUrl"] = url
        domain_count[urlparse(url).netloc.replace("www.", "")] += 1

        with open(path, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=2, ensure_ascii=False)
            f.write("\n")
        updated += 1

    print(f"Updated: {updated}  |  No URL assigned: {len(skipped)}")
    if skipped:
        print("  Slugs without URL:", skipped)
    print()
    print("Domain distribution:")
    total = sum(domain_count.values())
    for domain, count in domain_count.most_common():
        pct = count / 99 * 100
        flag = "  *** EXCEEDS 15%" if pct > 15 else ""
        print(f"  {domain}: {count}  ({pct:.1f}%){flag}")


if __name__ == "__main__":
    update_tasks()
