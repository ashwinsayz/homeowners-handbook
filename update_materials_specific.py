#!/usr/bin/env python3
"""
Replace generic material search URLs with specific, highly-rated product URLs.
Each entry maps the existing material name (lowercase) to a new (name, url) pair.
"""
import json
import os
from collections import OrderedDict

TASKS_DIR = os.path.join(os.path.dirname(__file__), "data", "tasks")

# Maps lowercase current name → (display name, specific URL)
SPECIFIC = {
    # ── HVAC / Air Quality ────────────────────────────────────────────────
    "merv-11 furnace filter":
        ("Filtrete 1500 MPR furnace filter",
         "https://www.amazon.com/dp/B005GZ89WU"),
    "filter gauge/reminder":
        ("Filtrete Smart air filter subscription",
         "https://www.amazon.com/s?k=Filtrete+smart+air+filter+subscription+reminder"),
    "ac coil cleaner spray":
        ("Nu-Calgon Evap Foam No Rinse coil cleaner",
         "https://www.amazon.com/s?k=Nu-Calgon+Evap+Foam+No+Rinse+coil+cleaner"),
    "garden hose nozzle":
        ("Gilmour Heavy Duty Swivel Head nozzle",
         "https://www.amazon.com/s?k=Gilmour+heavy+duty+swivel+hose+nozzle"),
    "fin comb":
        ("Frost King ACF19 fin comb",
         "https://www.amazon.com/s?k=Frost+King+ACF19+air+conditioner+fin+comb"),
    "mastic duct sealant":
        ("RCD Corporation #6 duct mastic sealant",
         "https://www.homedepot.com/s/RCD%20duct%20mastic%20sealant"),
    "foil hvac tape ul-181":
        ("3M 3311 foil HVAC tape UL-181",
         "https://www.amazon.com/s?k=3M+3311+foil+HVAC+tape+UL-181"),
    "duct brush":
        ("Holikme dryer vent and duct cleaning brush kit",
         "https://www.amazon.com/s?k=Holikme+duct+cleaning+brush+kit"),
    "smart thermostat":
        ("Google Nest Thermostat",
         "https://www.amazon.com/dp/B08HRNYF2J"),
    "wire labels":
        ("Klein Tools VDL2 self-laminating wire marker book",
         "https://www.amazon.com/s?k=Klein+Tools+wire+marker+labels+self-laminating"),
    "condensate pan tablets":
        ("AC Safe air conditioner condensate pan treatment tablets",
         "https://www.amazon.com/s?k=AC+Safe+condensate+pan+tablets"),
    "blown-in insulation":
        ("Owens Corning EcoTouch blown-in insulation",
         "https://www.homedepot.com/s/Owens%20Corning%20blown-in%20insulation"),
    "attic ruler/depth gauge":
        ("Owens Corning attic insulation ruler/depth gauge",
         "https://www.amazon.com/s?k=attic+insulation+depth+gauge+ruler"),
    "n95 respirator":
        ("3M 8511 N95 respirator (10-pack)",
         "https://www.amazon.com/s?k=3M+8511+N95+respirator"),
    "safety goggles":
        ("3M SecureFit 400 safety goggles",
         "https://www.amazon.com/s?k=3M+SecureFit+400+safety+glasses+goggles"),
    "humidistat":
        ("Inkbird IHC-200 digital humidistat controller",
         "https://www.amazon.com/s?k=Inkbird+IHC-200+humidistat+controller"),
    "water panel evaporator pad":
        ("Aprilaire 10 water panel evaporator pad",
         "https://www.amazon.com/s?k=Aprilaire+10+water+panel+evaporator+pad"),

    # ── Plumbing ──────────────────────────────────────────────────────────
    "toilet flapper kit":
        ("Fluidmaster 400CRP14 fill valve and flapper kit",
         "https://www.amazon.com/dp/B007TUHQWY"),
    "toilet fill valve":
        ("Fluidmaster 400CRP14 fill valve and flapper kit",
         "https://www.amazon.com/dp/B007TUHQWY"),
    "adjustable wrench":
        ("Crescent 8-inch adjustable wrench",
         "https://www.amazon.com/dp/B00002N5L0"),
    "drain snake/auger":
        ("RIDGID 41408 hand-powered drain snake auger",
         "https://www.amazon.com/s?k=RIDGID+41408+drain+snake+auger"),
    "drain hair catcher":
        ("TubShroom hair catcher and strainer",
         "https://www.amazon.com/s?k=TubShroom+drain+hair+catcher+strainer"),
    "baking soda and vinegar":
        ("Arm & Hammer baking soda 5 lb",
         "https://www.amazon.com/s?k=Arm+%26+Hammer+baking+soda+5+lb"),
    "plumber's putty":
        ("Oatey 31166 plumber's putty 14 oz",
         "https://www.amazon.com/dp/B01GWEWOKQ"),
    "teflon tape":
        ("Harvey's white PTFE thread seal tape",
         "https://www.amazon.com/s?k=Harvey+PTFE+teflon+thread+seal+tape+plumber"),
    "plumber's tape":
        ("Harvey's white PTFE thread seal tape",
         "https://www.amazon.com/s?k=Harvey+PTFE+teflon+thread+seal+tape+plumber"),
    "basin wrench":
        ("Ridgid 2017 basin wrench",
         "https://www.amazon.com/s?k=RIDGID+2017+basin+wrench"),
    "supply lines":
        ("Eastman braided stainless faucet supply line",
         "https://www.amazon.com/s?k=Eastman+braided+stainless+faucet+supply+line"),
    "braided stainless supply lines":
        ("Eastman 10 in. braided stainless toilet supply line",
         "https://www.amazon.com/dp/B079SL47LJ"),
    "toilet supply line":
        ("Eastman 10 in. braided stainless toilet supply line",
         "https://www.amazon.com/dp/B079SL47LJ"),
    "wax ring with horn":
        ("Korky 6000BP Universal WaxFree toilet seal",
         "https://www.amazon.com/dp/B00NOD4R7M"),
    "rubber gloves":
        ("Playtex Living reusable rubber gloves",
         "https://www.amazon.com/s?k=Playtex+Living+reusable+rubber+gloves"),
    "sewer cleanout plug":
        ("Oatey 4 in. ABS snap-in clean-out plug",
         "https://www.homedepot.com/s/Oatey%204%20inch%20cleanout%20plug"),
    "pipe repair clamp":
        ("GIDDS-4030064 stainless steel pipe repair clamp",
         "https://www.amazon.com/s?k=stainless+steel+pipe+repair+clamp"),
    "pipe epoxy putty":
        ("J-B Weld WaterWeld epoxy putty stick",
         "https://www.amazon.com/s?k=JB+Weld+WaterWeld+epoxy+putty+pipe+repair"),
    "pipe cutter":
        ("RIDGID 32920 Model 15 tubing cutter",
         "https://www.amazon.com/dp/B00018AFG0"),
    "foam pipe insulation":
        ("Frost King self-sealing foam pipe insulation",
         "https://www.amazon.com/s?k=Frost+King+self-seal+foam+pipe+insulation"),
    "pipe insulation tape":
        ("Armaflex self-adhesive pipe insulation tape",
         "https://www.amazon.com/s?k=Armaflex+self-adhesive+pipe+insulation+tape"),
    "zip ties":
        ("Cable Matters 100-pack nylon cable ties (4 / 8 / 12 in. assortment)",
         "https://www.amazon.com/s?k=nylon+cable+zip+ties+assortment+pack"),
    "outdoor faucet cover":
        ("M-D Building Products 4-in. outdoor faucet cover",
         "https://www.amazon.com/s?k=M-D+Building+Products+outdoor+faucet+cover"),
    "indoor water shutoff key":
        ("B&K Ball Valve quarter-turn water shutoff key",
         "https://www.amazon.com/s?k=quarter+turn+indoor+water+shutoff+valve+key"),
    "garbage disposal":
        ("InSinkErator Badger 5 1/2 HP garbage disposal",
         "https://www.amazon.com/s?k=InSinkErator+Badger+5+garbage+disposal"),
    "disposal wrench":
        ("InSinkErator STP-00 service wrench",
         "https://www.amazon.com/s?k=InSinkErator+service+wrench"),
    "electrical cord kit":
        ("InSinkErator CRD-00 power cord kit",
         "https://www.amazon.com/s?k=InSinkErator+CRD-00+power+cord+kit"),
    "garbage disposal wrench key":
        ("InSinkErator STP-00 jam buster wrench",
         "https://www.amazon.com/s?k=InSinkErator+jam+buster+wrench"),
    "garbage disposal cleaner pods":
        ("Glisten Disposer Care foaming cleaner pods",
         "https://www.amazon.com/s?k=Glisten+Disposer+Care+foaming+pods"),
    "hose bibb":
        ("SharkBite 1/2 in. push-to-connect ball valve",
         "https://www.homedepot.com/s/SharkBite%20ball%20valve%20push%20connect"),
    "garden hose":
        ("Flexzilla 50 ft. hybrid garden hose",
         "https://www.amazon.com/s?k=Flexzilla+50+ft+garden+hose"),
    "water heater anode rod":
        ("Camco 11563 magnesium anode rod",
         "https://www.amazon.com/s?k=Camco+11563+magnesium+anode+rod+water+heater"),
    "sump pump float switch":
        ("Zoeller M53 sump pump replacement float switch",
         "https://www.amazon.com/s?k=sump+pump+replacement+float+switch"),
    "sump pump backup":
        ("Wayne ESP25 battery backup sump pump",
         "https://www.amazon.com/s?k=Wayne+ESP25+battery+backup+sump+pump"),
    "pvc cement":
        ("Oatey 31014 medium duty clear PVC cement",
         "https://www.homedepot.com/s/Oatey%20PVC%20cement%20medium%20clear"),
    "whole-home water shutoff sensor":
        ("Moen Flo smart whole-home water shutoff",
         "https://www.amazon.com/s?k=Moen+Flo+smart+water+shutoff+sensor"),
    "push-fit fittings":
        ("SharkBite push-to-connect fittings assortment",
         "https://www.amazon.com/s?k=SharkBite+push+to+connect+fittings"),
    "blow-out adapter":
        ("Orbit 67114 quick-connect blow-out adapter",
         "https://www.amazon.com/s?k=Orbit+irrigation+blow+out+adapter"),
    "insulation wrap for backflow preventer":
        ("Watts backflow preventer insulation cover",
         "https://www.amazon.com/s?k=backflow+preventer+insulation+cover+wrap"),

    # ── Electrical ────────────────────────────────────────────────────────
    "voltage tester":
        ("Klein Tools NCVT-3P non-contact voltage tester",
         "https://www.amazon.com/dp/B08DQMX7YF"),
    "non-contact voltage tester":
        ("Klein Tools NCVT-3P non-contact voltage tester",
         "https://www.amazon.com/dp/B08DQMX7YF"),
    "wire stripper":
        ("Klein Tools 11057 wire stripper/cutter",
         "https://www.amazon.com/dp/B000XEUPMQ"),
    "wire connectors":
        ("Ideal Industries 30-191 wing nut wire connectors assortment",
         "https://www.amazon.com/s?k=Ideal+Industries+wire+nut+assortment"),
    "wire nuts":
        ("Ideal Industries 30-191 wing nut wire connectors assortment",
         "https://www.amazon.com/s?k=Ideal+Industries+wire+nut+assortment"),
    "electrical tape":
        ("3M Temflex 1700 all-weather electrical tape",
         "https://www.amazon.com/s?k=3M+Temflex+1700+electrical+tape"),
    "light switch":
        ("Leviton 1451-2W 15A single-pole light switch",
         "https://www.homedepot.com/s/Leviton+15A+single+pole+light+switch"),
    "electrical outlet":
        ("Leviton 5320-W 15A duplex outlet (10-pack)",
         "https://www.homedepot.com/s/Leviton+15A+duplex+outlet+white"),
    "electrical box":
        ("Carlon B114RB single-gang PVC electrical box",
         "https://www.homedepot.com/s/Carlon+single+gang+electrical+box"),
    "gfci outlet":
        ("Leviton GFNT1-W 15A GFCI outlet self-test",
         "https://www.homedepot.com/s/Leviton+GFCI+15A+self+test+outlet+white"),
    "dimmer switch":
        ("Lutron Caseta PD-6WCL-WH smart dimmer switch",
         "https://www.amazon.com/s?k=Lutron+Caseta+PD-6WCL+smart+dimmer+switch"),
    "ceiling fan or light fixture":
        ("Hunter Fan Company 52 in. Symphony ceiling fan",
         "https://www.amazon.com/s?k=Hunter+52+inch+ceiling+fan+with+light"),
    "ceiling fan mounting bracket":
        ("Hunter 26015 ceiling fan mounting kit",
         "https://www.homedepot.com/s/ceiling+fan+mounting+bracket+kit"),
    "whole-house surge protector spd":
        ("Square D QO2CAFGN whole-house surge protector",
         "https://www.amazon.com/s?k=Square+D+QO2CAFGN+whole+house+surge+protector"),
    "outlet tester plug":
        ("Sperry Instruments GFI6302 GFCI outlet tester",
         "https://www.amazon.com/dp/B000RUL2UU"),
    "outlet tester with gfci test button":
        ("Sperry Instruments GFI6302 GFCI outlet tester",
         "https://www.amazon.com/dp/B000RUL2UU"),
    "circuit breaker finder":
        ("Klein Tools ET310 circuit breaker finder",
         "https://www.amazon.com/s?k=Klein+Tools+ET310+circuit+breaker+finder"),
    "flashlight":
        ("Streamlight 88040 ProTAC 1L-1AA flashlight",
         "https://www.amazon.com/s?k=Streamlight+ProTAC+flashlight"),
    "tamper-resistant outlet covers":
        ("Legrand TM8kkLA10 tamper-resistant outlet (10-pack)",
         "https://www.amazon.com/s?k=tamper+resistant+outlet+cover+safety"),
    "cabinet safety latches":
        ("Safety 1st adhesive magnetic cabinet locks",
         "https://www.amazon.com/s?k=Safety+1st+magnetic+cabinet+lock+adhesive"),
    "foam corner guards":
        ("Roving Cove soft corner protectors",
         "https://www.amazon.com/s?k=Roving+Cove+corner+protectors+baby+safety"),
    "9v batteries":
        ("Energizer MAX 9V batteries (8-pack)",
         "https://www.amazon.com/s?k=Energizer+MAX+9V+batteries+8+pack"),
    "9v battery":
        ("Energizer MAX 9V battery (4-pack)",
         "https://www.amazon.com/s?k=Energizer+MAX+9V+battery+4+pack"),
    "aa batteries":
        ("Energizer MAX AA batteries (24-pack)",
         "https://www.amazon.com/s?k=Energizer+MAX+AA+batteries+24+pack"),
    "aa or aaa batteries":
        ("Energizer MAX AA/AAA batteries combo pack",
         "https://www.amazon.com/s?k=Energizer+MAX+AA+AAA+combo+batteries"),
    "smoke detector":
        ("Kidde i9050 battery-operated smoke alarm",
         "https://www.amazon.com/s?k=Kidde+i9050+battery+smoke+alarm"),
    "carbon monoxide detector":
        ("Kidde KN-COB-B-LPM CO alarm with digital display",
         "https://www.amazon.com/s?k=Kidde+carbon+monoxide+detector+digital+display"),
    "smart smoke and co detector":
        ("Google Nest Protect smoke and CO alarm",
         "https://www.amazon.com/s?k=Google+Nest+Protect+smoke+CO+alarm"),
    "abc fire extinguisher":
        ("Kidde FA110 1-A:10-B:C dry chemical fire extinguisher",
         "https://www.amazon.com/s?k=Kidde+FA110+ABC+fire+extinguisher"),
    "fire extinguisher mount bracket":
        ("Amerex fire extinguisher strap mount bracket",
         "https://www.amazon.com/s?k=fire+extinguisher+mount+bracket+strap"),
    "video doorbell":
        ("Ring Video Doorbell 4 with HD video",
         "https://www.amazon.com/s?k=Ring+Video+Doorbell+4"),
    "smart deadbolt lock":
        ("Schlage Encode Plus smart WiFi deadbolt",
         "https://www.amazon.com/s?k=Schlage+Encode+Plus+smart+wifi+deadbolt"),
    "drill and hole saw kit":
        ("DEWALT 20V MAX drill driver and hole saw kit",
         "https://www.amazon.com/s?k=DEWALT+20V+drill+driver+hole+saw+kit"),
    "drill and drill bits":
        ("DEWALT DCD771C2 20V MAX drill/driver kit",
         "https://www.amazon.com/dp/B00ET5VMTU"),
    "garage door sensor alignment bracket":
        ("Chamberlain 41D2072 safety sensor alignment bracket",
         "https://www.amazon.com/s?k=garage+door+safety+sensor+alignment+bracket"),
    "sensor wire":
        ("Chamberlain 041A3357 garage door sensor wire",
         "https://www.amazon.com/s?k=garage+door+sensor+wire+2+conductor"),
    "needle-nose pliers":
        ("Klein Tools D203-6 needle-nose pliers",
         "https://www.amazon.com/s?k=Klein+Tools+D203-6+needle+nose+pliers"),

    # ── Smart home ────────────────────────────────────────────────────────
    "install-a-smart-thermostat":
        ("Google Nest Thermostat",
         "https://www.amazon.com/dp/B08HRNYF2J"),

    # ── Roof / Exterior ───────────────────────────────────────────────────
    "roofing cement":
        ("Henry HE208R56 roof cement",
         "https://www.homedepot.com/s/Henry+roof+cement+208"),
    "replacement shingles":
        ("GAF Timberline HDZ architectural shingles",
         "https://www.homedepot.com/s/GAF+Timberline+HDZ+shingles"),
    "roofing nails":
        ("Grip-Rite 1-3/4 in. galvanized roofing nails 30 oz",
         "https://www.homedepot.com/s/Grip-Rite+galvanized+roofing+nails"),
    "pry bar":
        ("Stanley FatMax 30 in. wrecking bar",
         "https://www.amazon.com/s?k=Stanley+FatMax+wrecking+bar+pry+bar"),
    "roofing sealant/caulk":
        ("Geocel 28100 Pro Flex RV roof sealant",
         "https://www.amazon.com/s?k=Geocel+ProFlex+roof+flashing+sealant+caulk"),
    "roof flashing tape":
        ("Cofair WQR625 Quick Roof flashing tape",
         "https://www.amazon.com/s?k=Cofair+Quick+Roof+repair+tape+flashing"),
    "sheet metal flashing":
        ("Amerimax 8 in. aluminum step flashing",
         "https://www.homedepot.com/s/Amerimax+step+flashing+aluminum"),
    "gutter scoop":
        ("Orbit 26084 gutter cleaning scoop",
         "https://www.amazon.com/s?k=Orbit+gutter+cleaning+scoop"),
    "garden hose with spray nozzle":
        ("Dramm 10-12380 adjustable spray gun nozzle",
         "https://www.amazon.com/s?k=Dramm+adjustable+spray+gun+nozzle"),
    "safety ladder stabilizer":
        ("Louisville Ladder LP-2200-00 ladder stabilizer",
         "https://www.amazon.com/s?k=Louisville+Ladder+LP-2200-00+stabilizer"),
    "work gloves":
        ("Mechanix Wear Original work gloves",
         "https://www.amazon.com/s?k=Mechanix+Wear+Original+work+gloves"),
    "gutter guard":
        ("Amerimax Home Products 85470 gutter guard",
         "https://www.lowes.com/search?searchTerm=Amerimax+gutter+guard"),
    "tin snips":
        ("MIDWEST Aviation Snips left/right cut combo",
         "https://www.amazon.com/s?k=MIDWEST+aviation+snips+combo+set"),
    "safety ladder":
        ("Little Giant Velocity Type IA multi-use ladder",
         "https://www.amazon.com/s?k=Little+Giant+Velocity+multi-use+ladder"),
    "chimney cleaning log":
        ("Rutland Products 97 chimney cleaning log",
         "https://www.amazon.com/s?k=Rutland+97+chimney+cleaning+creosote+log"),
    "chimney cap":
        ("Hy-C Company Single Flue galvanized chimney cap",
         "https://www.amazon.com/s?k=Hy-C+single+flue+galvanized+chimney+cap"),

    # ── Exterior / Foundation / Driveway ─────────────────────────────────
    "paintable exterior caulk":
        ("DAP Alex Flex 10 oz. paintable exterior caulk",
         "https://www.homedepot.com/s/DAP+Alex+Flex+exterior+paintable+caulk"),
    "exterior caulk":
        ("DAP Alex Flex 10 oz. paintable exterior caulk",
         "https://www.homedepot.com/s/DAP+Alex+Flex+exterior+paintable+caulk"),
    "concrete crack filler":
        ("Quikrete 864000 self-leveling polyurethane crack seal",
         "https://www.homedepot.com/s/Quikrete+polyurethane+self+leveling+crack+seal"),
    "epoxy injection kit":
        ("RadonSeal epoxy crack injection kit",
         "https://www.amazon.com/s?k=RadonSeal+epoxy+crack+injection+kit"),
    "wire brush":
        ("Forney 70491 stainless steel wire brush",
         "https://www.amazon.com/s?k=Forney+70491+wire+brush+stainless+steel"),
    "hydraulic cement":
        ("Quikrete 112011 hydraulic water-stop cement",
         "https://www.homedepot.com/s/Quikrete+hydraulic+cement"),
    "asphalt crack filler":
        ("Pli-Stix 30 ft. medium permanent asphalt crack filler",
         "https://www.homedepot.com/s/Pli-Stix+asphalt+crack+filler"),
    "asphalt patching compound":
        ("Quikrete 170109 one-component asphalt patching compound",
         "https://www.homedepot.com/s/Quikrete+asphalt+patching+compound"),
    "tamper":
        ("Bon Tool 14-356 hand tamper",
         "https://www.amazon.com/s?k=Bon+Tool+hand+tamper"),
    "driveway sealer":
        ("Armor Plex 4.75 gal. driveway filler and sealer",
         "https://www.homedepot.com/s/Armor+Plex+driveway+sealer"),
    "crack filler":
        ("Pli-Stix asphalt crack filler",
         "https://www.homedepot.com/s/Pli-Stix+asphalt+crack+filler"),
    "squeegee applicator":
        ("ProLine 24 in. driveway sealer squeegee applicator",
         "https://www.homedepot.com/s/driveway+sealer+squeegee+applicator"),
    "vinyl siding":
        ("Gentek double-4 vinyl siding",
         "https://www.lowes.com/search?searchTerm=Gentek+vinyl+siding"),
    "siding removal tool":
        ("Malco SRT1 siding removal tool",
         "https://www.amazon.com/s?k=Malco+SRT1+siding+removal+tool"),
    "color-matched paint":
        ("BEHR Premium Plus exterior paint and primer",
         "https://www.homedepot.com/s/BEHR+exterior+paint+primer"),
    "fence post":
        ("8 ft. pressure-treated pine fence post",
         "https://www.lowes.com/search?searchTerm=pressure+treated+fence+post+4x4"),
    "fence boards":
        ("Severe Weather 6 ft. dog-ear pressure-treated fence board",
         "https://www.lowes.com/search?searchTerm=pressure+treated+fence+board"),
    "post hole concrete":
        ("Quikrete Fast-Setting Concrete 50 lb.",
         "https://www.homedepot.com/s/Quikrete+Fast-Setting+Concrete+50+lb"),
    "galvanized nails":
        ("Grip-Rite 3-1/2 in. 16D galvanized common nails 5 lb",
         "https://www.homedepot.com/s/Grip-Rite+galvanized+common+nails+16D"),
    "topsoil/fill dirt":
        ("Quikrete 50 lb. top soil",
         "https://www.homedepot.com/s/Quikrete+50+lb+topsoil"),
    "landscaping rake":
        ("Bully Tools 12-tine poly landscape rake",
         "https://www.amazon.com/s?k=Bully+Tools+12+tine+poly+landscape+rake"),
    "sod or seed":
        ("Scotts Turf Builder sun and shade grass seed",
         "https://www.lowes.com/search?searchTerm=Scotts+Turf+Builder+grass+seed"),
    "window well cover":
        ("Maccourt WC32 polycarbonate window well cover",
         "https://www.amazon.com/s?k=Maccourt+polycarbonate+window+well+cover"),
    "gravel":
        ("Vigoro 0.5 cu. ft. pea gravel",
         "https://www.homedepot.com/s/Vigoro+pea+gravel+0.5+cubic+feet"),
    "window well drain":
        ("WellDuct window well drain kit",
         "https://www.amazon.com/s?k=WellDuct+window+well+drain+kit"),
    "pressure washer":
        ("Sun Joe SPX3000 2030 PSI electric pressure washer",
         "https://www.amazon.com/s?k=Sun+Joe+SPX3000+electric+pressure+washer"),
    "pressure washer detergent":
        ("Sun Joe SPX-APC1G all-purpose pressure washer detergent",
         "https://www.amazon.com/s?k=Sun+Joe+all+purpose+pressure+washer+soap"),
    "surface cleaner attachment":
        ("Sun Joe SPX-FC22 surface cleaning attachment",
         "https://www.amazon.com/s?k=pressure+washer+surface+cleaner+attachment"),

    # ── Drywall / Walls ───────────────────────────────────────────────────
    "drywall patch kit":
        ("3M 4 in. large wall repair kit",
         "https://www.homedepot.com/s/3M+large+wall+repair+kit"),
    "spackle":
        ("DAP Alex Plus 16 oz. spackling paste",
         "https://www.amazon.com/dp/B074H82BV6"),
    "putty knife":
        ("Hyde Tools 3-piece putty knife set",
         "https://www.amazon.com/dp/B000KKRHRE"),
    "sandpaper":
        ("3M Pro Grade Precision 80/120/220 grit sandpaper kit",
         "https://www.amazon.com/dp/B085RQYV4J"),
    "drywall screws":
        ("Grip-Rite #6 x 1-1/4 in. coarse thread drywall screws 5 lb",
         "https://www.amazon.com/dp/B00004YVIN"),
    "joint compound":
        ("USG Sheetrock 4.5 qt. plus 3 joint compound",
         "https://www.homedepot.com/s/USG+Sheetrock+Plus+3+joint+compound"),
    "drywall joint compound":
        ("USG Sheetrock 4.5 qt. plus 3 joint compound",
         "https://www.homedepot.com/s/USG+Sheetrock+Plus+3+joint+compound"),
    "drywall tape":
        ("USG Sheetrock fiberglass mesh drywall tape 2 in. x 150 ft.",
         "https://www.homedepot.com/s/USG+Sheetrock+fiberglass+mesh+tape"),
    "corner bead":
        ("USG Sheetrock 1-1/4 in. x 8 ft. metal corner bead",
         "https://www.homedepot.com/s/USG+Sheetrock+metal+corner+bead"),
    "drywall sheet":
        ("USG Sheetrock 1/2 in. x 4 ft. x 8 ft. drywall panel",
         "https://www.homedepot.com/s/USG+Sheetrock+1%2F2+drywall+4x8"),
    "popcorn ceiling patch spray":
        ("Homax 4090-06 acoustic ceiling texture spray",
         "https://www.amazon.com/s?k=Homax+4090+acoustic+ceiling+texture+spray"),
    "fix-nail-pops":
        ("DAP Alex Plus spackling paste",
         "https://www.amazon.com/dp/B074H82BV6"),
    "paintable wood filler":
        ("DAP Plastic Wood 16 oz. paintable wood filler",
         "https://www.homedepot.com/s/DAP+Plastic+Wood+filler+paintable"),

    # ── Paint / Caulk ─────────────────────────────────────────────────────
    "painter's tape":
        ("ScotchBlue 2090 1.88 in. x 60 yd painter's tape",
         "https://www.amazon.com/dp/B00004Z4DU"),
    "paint primer":
        ("Zinsser Bulls Eye 1-2-3 primer quart",
         "https://www.amazon.com/dp/B000H5VKBQ"),
    "interior latex paint":
        ("BEHR Premium Plus interior paint and primer",
         "https://www.homedepot.com/s/BEHR+Premium+Plus+interior+paint+primer"),
    "roller kit":
        ("Purdy 14C791014 Nylox 9 in. roller kit",
         "https://www.amazon.com/s?k=Purdy+9+inch+roller+frame+cover+kit"),
    "drop cloth":
        ("Trimaco 12 ft. x 15 ft. SuperTuff canvas drop cloth",
         "https://www.homedepot.com/s/Trimaco+canvas+drop+cloth"),
    "angled brush":
        ("Purdy XL Glide 2-1/2 in. angular sash brush",
         "https://www.amazon.com/dp/B0000DH4KH"),
    "trim paint":
        ("BEHR Premium Plus semi-gloss enamel trim paint",
         "https://www.homedepot.com/s/BEHR+semi-gloss+trim+enamel+paint"),
    "100% silicone tub and tile caulk":
        ("GE Sealants Advanced Silicone 2 tub and tile caulk",
         "https://www.homedepot.com/s/GE+Sealants+Silicone+2+tub+tile+caulk"),
    "paintable window caulk":
        ("DAP Alex Plus paintable window and door caulk",
         "https://www.homedepot.com/s/DAP+Alex+Plus+window+door+caulk+paintable"),
    "caulk gun":
        ("Newborn 930-GTD drip-free caulk gun",
         "https://www.amazon.com/dp/B000BQS5GO"),
    "caulk remover tool":
        ("ALLWAY CT31 3-in-1 caulk remover and finishing tool",
         "https://www.amazon.com/dp/B0CZ48JJ7F"),
    "caulk remover":
        ("ALLWAY CT31 3-in-1 caulk remover and finishing tool",
         "https://www.amazon.com/dp/B0CZ48JJ7F"),
    "construction adhesive":
        ("Loctite PL Premium polyurethane construction adhesive",
         "https://www.amazon.com/dp/B0H6R2NCTC"),
    "construction screws":
        ("SPAX 3 in. T-Star plus flat head construction screw (100-pack)",
         "https://www.homedepot.com/s/SPAX+3+inch+construction+screw"),

    # ── Flooring ──────────────────────────────────────────────────────────
    "squeak-relief screw kit":
        ("Squeeeeek No More complete floor repair kit",
         "https://www.amazon.com/dp/B0006IK8YE"),
    "wood screws":
        ("SPAX 1-5/8 in. T-Star plus wood screws (200-pack)",
         "https://www.homedepot.com/s/SPAX+wood+screws+1+5%2F8"),
    "wood glue":
        ("Titebond III Ultimate wood glue 8 oz.",
         "https://www.amazon.com/s?k=Titebond+III+Ultimate+wood+glue"),
    "stain marker":
        ("Old English scratch cover markers assortment",
         "https://www.amazon.com/s?k=Old+English+scratch+cover+markers+wood"),
    "tile grout":
        ("Custom Building Products Polyblend sanded grout",
         "https://www.amazon.com/dp/B000UVR5NE"),
    "grout float":
        ("QEP 10060Q molded rubber grout float",
         "https://www.amazon.com/dp/B002YCW6RC"),
    "grout saw/oscillating tool":
        ("DEWALT DWE315K oscillating multi-tool kit",
         "https://www.amazon.com/s?k=DEWALT+oscillating+multi-tool+grout+saw"),
    "grout sealer":
        ("Aqua Mix Sealer's Choice Gold grout and tile sealer",
         "https://www.amazon.com/s?k=Aqua+Mix+Sealer+Choice+Gold+grout+sealer"),
    "replacement tile":
        ("Dal-Tile ceramic floor tile",
         "https://www.lowes.com/search?searchTerm=Dal-Tile+ceramic+floor+tile"),
    "tile adhesive mastic":
        ("AcrylPro ceramic tile adhesive mastic quart",
         "https://www.homedepot.com/s/AcrylPro+ceramic+tile+adhesive+mastic"),
    "tile spacers":
        ("QEP 1/8 in. T-shaped tile spacers (300-pack)",
         "https://www.lowes.com/search?searchTerm=QEP+tile+spacers+1%2F8+inch"),
    "vinyl floor repair kit":
        ("Roberts 50-150 vinyl floor repair kit",
         "https://www.amazon.com/s?k=Roberts+vinyl+floor+repair+kit"),
    "flooring adhesive":
        ("Roberts 2057-1 vinyl flooring adhesive",
         "https://www.lowes.com/search?searchTerm=Roberts+vinyl+flooring+adhesive"),
    "seam sealer":
        ("Roberts 7725 vinyl seam sealer",
         "https://www.amazon.com/s?k=Roberts+7725+vinyl+seam+sealer"),
    "patch-or-repair-vinyl-laminate-flooring":
        ("Roberts 50-150 vinyl floor repair kit",
         "https://www.amazon.com/s?k=Roberts+vinyl+floor+repair+kit"),
    "floor finish":
        ("Bona Traffic HD commercial floor finish",
         "https://www.lowes.com/search?searchTerm=Bona+Traffic+HD+floor+finish"),
    "floor stain":
        ("Minwax Hardwood Floor Reviver high-gloss",
         "https://www.lowes.com/search?searchTerm=Minwax+hardwood+floor+reviver"),
    "screen discs":
        ("Norton 7-7/8 in. 60-grit floor sanding screen disc",
         "https://www.lowes.com/search?searchTerm=floor+sanding+screen+disc"),
    "tack cloth":
        ("Trimaco EZ Tack tack cloth (6-pack)",
         "https://www.homedepot.com/s/Trimaco+tack+cloth"),
    "carpet seam sealer":
        ("Roberts 6700 carpet seam sealer",
         "https://www.amazon.com/s?k=Roberts+6700+carpet+seam+sealer"),
    "carpet knee kicker":
        ("Roberts 10-260 Power-Lok carpet stretcher knee kicker",
         "https://www.amazon.com/s?k=Roberts+10-260+carpet+knee+kicker"),
    "carpet tack strips":
        ("Roberts tack strip for carpet (100-pack)",
         "https://www.lowes.com/search?searchTerm=Roberts+carpet+tack+strip"),
    "plywood patch":
        ("3/4 in. x 2 ft. x 4 ft. Sande plywood panel",
         "https://www.homedepot.com/s/plywood+panel+3%2F4+inch+2x4"),
    "wood epoxy filler":
        ("Elmer's E892 Carpenter's color change wood filler",
         "https://www.amazon.com/s?k=PC+Woody+Wood+Repair+Epoxy+exterior"),
    "wood sealer":
        ("BEHR 1 gal. clear wood waterproofing sealer",
         "https://www.homedepot.com/s/BEHR+wood+waterproofing+sealer+clear"),
    "wood plane or belt sander":
        ("WEN 6321 3 in. x 21 in. belt sander",
         "https://www.amazon.com/s?k=WEN+6321+belt+sander+3x21"),

    # ── Doors / Windows ───────────────────────────────────────────────────
    "door weatherstrip kit":
        ("M-D Building Products 49026 door weatherstrip kit",
         "https://www.lowes.com/search?searchTerm=M-D+Building+door+weatherstrip+kit"),
    "adhesive-backed foam tape":
        ("M-D Building Products self-adhesive foam weatherstrip",
         "https://www.lowes.com/search?searchTerm=M-D+Building+self-adhesive+foam+weatherstrip"),
    "door sweep":
        ("M-D Building Products 05389 aluminum door sweep 36 in.",
         "https://www.amazon.com/dp/B00005202G"),
    "door draft stopper":
        ("MAXTID under door draft stopper and door sweep",
         "https://www.amazon.com/s?k=MAXTID+under+door+draft+stopper"),
    "strike plate":
        ("Defiant heavy-duty security strike plate",
         "https://www.homedepot.com/s/Defiant+heavy+duty+security+strike+plate"),
    "door latch strike plate kit":
        ("Defiant heavy-duty security strike plate kit",
         "https://www.homedepot.com/s/Defiant+strike+plate+kit+door+latch"),
    "chisel":
        ("DEWALT 3-piece wood chisel set",
         "https://www.amazon.com/s?k=DEWALT+wood+chisel+set"),
    "door hinge screws":
        ("GRK Fasteners R4 3 in. premium wood screws (100-pack)",
         "https://www.homedepot.com/s/GRK+R4+3+inch+wood+screws"),
    "window screen replacement kit":
        ("Phifer Screen-Tight replacement screen kit",
         "https://www.lowes.com/search?searchTerm=Phifer+replacement+window+screen+kit"),
    "screen spline roller":
        ("Prime-Line Tools screen spline roller",
         "https://www.amazon.com/s?k=Prime-Line+screen+spline+roller"),
    "screen spline":
        ("Phifer 0.140 in. dia. vinyl screen spline",
         "https://www.lowes.com/search?searchTerm=Phifer+vinyl+screen+spline"),

    # ── Deck / Lawn / Outdoor ─────────────────────────────────────────────
    "deck stain and sealer":
        ("DEFY Extreme semi-transparent wood deck stain",
         "https://www.amazon.com/s?k=DEFY+Extreme+semi-transparent+wood+stain+sealer"),
    "deck cleaner":
        ("DEFY Wood Deck Cleaner and Brightener",
         "https://www.homedepot.com/s/DEFY+wood+deck+cleaner+brightener"),
    "pump sprayer":
        ("Chapin 20000 1-gallon poly lawn and garden pump sprayer",
         "https://www.amazon.com/s?k=Chapin+20000+garden+pump+sprayer"),
    "deck brush":
        ("Quickie 530 flagged-tip deck scrub brush",
         "https://www.homedepot.com/s/Quickie+flagged+tip+deck+brush"),
    "deck screws":
        ("DeckWise Ipe Clip 3 in. stainless composite deck screws (100-pk)",
         "https://www.homedepot.com/s/composite+deck+screws+3+inch+stainless"),
    "post anchor":
        ("Simpson Strong-Tie ABA44 post base anchor",
         "https://www.homedepot.com/s/Simpson+Strong-Tie+ABA44+post+base"),
    "grass seed":
        ("Scotts Turf Builder sun and shade grass seed",
         "https://www.amazon.com/s?k=Scotts+Turf+Builder+sun+shade+grass+seed"),
    "starter fertilizer":
        ("Scotts Turf Builder Starter Food new grass fertilizer",
         "https://www.amazon.com/s?k=Scotts+Turf+Builder+Starter+Food+fertilizer"),
    "garden rake":
        ("Bully Tools 64012 16-tine poly garden rake",
         "https://www.amazon.com/s?k=Bully+Tools+64012+16+tine+poly+rake"),
    "bypass pruning shears":
        ("Felco 2 bypass pruning shears",
         "https://www.amazon.com/s?k=Felco+2+bypass+pruning+shears"),
    "telescoping pruning saw":
        ("Corona RS 7265D RAZOR TOOTH telescoping tree pruner",
         "https://www.amazon.com/s?k=Corona+RS7265D+telescoping+pruning+saw"),
    "safety glasses":
        ("DEWALT DPG82-11C clear anti-fog safety glasses",
         "https://www.amazon.com/s?k=DEWALT+DPG82-11C+clear+safety+glasses"),
    "outdoor furniture cleaner":
        ("Star Brite 97616 marine and outdoor cleaner",
         "https://www.amazon.com/s?k=outdoor+furniture+cleaner+all+purpose"),
    "furniture covers":
        ("Classic Accessories Ravenna patio furniture set cover",
         "https://www.amazon.com/s?k=Classic+Accessories+Ravenna+patio+furniture+cover"),

    # ── Appliances ────────────────────────────────────────────────────────
    "refrigerator water filter":
        ("EveryDrop by Whirlpool filter (compatible with major brands)",
         "https://www.amazon.com/s?k=EveryDrop+refrigerator+water+filter"),
    "refrigerator coil brush":
        ("Frigidaire 5308819002 refrigerator coil brush",
         "https://www.amazon.com/s?k=refrigerator+condenser+coil+brush"),
    "vacuum with brush attachment":
        ("BISSELL Pet Hair Eraser 2281 vacuum",
         "https://www.amazon.com/s?k=vacuum+with+brush+attachment+refrigerator+coil"),
    "dishwasher cleaner tablet":
        ("Finish Dual Action Dishwasher Cleaner (3-count)",
         "https://www.amazon.com/s?k=Finish+dual+action+dishwasher+cleaner"),
    "soft brush":
        ("OXO Good Grips detail cleaning brush set",
         "https://www.amazon.com/s?k=OXO+Good+Grips+detail+brush+set"),
    "washing machine cleaner tablets":
        ("Affresh W10501250 washing machine cleaner (6-count)",
         "https://www.amazon.com/s?k=Affresh+W10501250+washing+machine+cleaner"),
    "torpedo level":
        ("Empire 36 in. cast aluminum torpedo level",
         "https://www.amazon.com/s?k=Empire+36+inch+torpedo+level"),
    "anti-vibration pads":
        ("Anti Walk anti-vibration pads for washing machine",
         "https://www.amazon.com/s?k=anti+vibration+pads+washing+machine+dryer"),
    "oven cleaner spray":
        ("Easy-Off Professional oven and grill cleaner",
         "https://www.amazon.com/s?k=Easy-Off+professional+fume+free+oven+cleaner"),
    "heavy-duty scrub pad":
        ("Scotch-Brite Heavy Duty Scrub Dots non-scratch pad (6-pack)",
         "https://www.amazon.com/s?k=Scotch-Brite+Heavy+Duty+Scrub+Dots+pad"),
    "range hood grease filter":
        ("Broan-NuTone replacement range hood grease filter",
         "https://www.amazon.com/s?k=Broan+NuTone+range+hood+grease+filter"),
    "degreaser spray":
        ("Zep Heavy-Duty Citrus Degreaser 32 oz",
         "https://www.amazon.com/s?k=Zep+Heavy+Duty+Citrus+Degreaser"),
    "descaling solution":
        ("De'Longhi EcoDecalk natural descaler 16.9 oz",
         "https://www.amazon.com/s?k=DeLonghi+EcoDecalk+descaler"),
    "white vinegar":
        ("Lucy's Family Owned natural white vinegar 1 gallon",
         "https://www.amazon.com/dp/B07985NMQD"),
    "distilled white vinegar":
        ("Lucy's Family Owned natural white vinegar 1 gallon",
         "https://www.amazon.com/dp/B07985NMQD"),
    "vinegar":
        ("Lucy's Family Owned natural white vinegar 1 gallon",
         "https://www.amazon.com/dp/B07985NMQD"),
    "baking soda":
        ("Arm & Hammer baking soda 5 lb",
         "https://www.amazon.com/s?k=Arm+%26+Hammer+baking+soda+5+lb"),
    "dryer vent cleaning kit":
        ("Holikme 25 ft. dryer vent cleaning brush kit",
         "https://www.amazon.com/s?k=Holikme+25+ft+dryer+vent+cleaning+brush+kit"),
    "vacuum with hose attachment":
        ("Vacmaster 8-gallon wet/dry vacuum",
         "https://www.amazon.com/s?k=Vacmaster+8+gallon+wet+dry+vacuum"),
    "dryer heating element":
        ("Supco DE726 universal electric dryer heating element",
         "https://www.amazon.com/s?k=universal+electric+dryer+heating+element"),
    "dryer thermal fuse":
        ("Supplying Demand dryer thermal fuse kit",
         "https://www.amazon.com/s?k=dryer+thermal+fuse+kit+universal"),
    "dryer vent brush kit":
        ("Holikme 25 ft. dryer vent cleaning brush kit",
         "https://www.amazon.com/s?k=Holikme+dryer+vent+cleaning+brush+kit"),
    "multimeter":
        ("Fluke 117 electrician's multimeter",
         "https://www.amazon.com/s?k=Fluke+117+electrician+multimeter"),
    "oven igniter":
        ("Supplying Demand universal gas range igniter",
         "https://www.amazon.com/s?k=universal+gas+oven+range+igniter+replacement"),
    "oven-rated wire connectors":
        ("Ideal Industries high-temperature rated wire connectors",
         "https://www.amazon.com/s?k=high+temperature+wire+connectors+oven+rated"),

    # ── Misc tools ────────────────────────────────────────────────────────
    "compressed air can":
        ("Dust-Off 10 oz. compressed air duster (4-pack)",
         "https://www.amazon.com/s?k=Dust-Off+compressed+air+duster+4+pack"),
    "soft brush set":
        ("OXO Good Grips detail cleaning brush set",
         "https://www.amazon.com/s?k=OXO+Good+Grips+detail+brush+cleaning+set"),
    "wet/dry vacuum":
        ("RIDGID 9-gallon 4.25-HP wet/dry shop vac",
         "https://www.homedepot.com/s/RIDGID+9+gallon+wet+dry+shop+vac"),
    "white lithium grease spray":
        ("WD-40 Specialist white lithium grease spray",
         "https://www.amazon.com/s?k=WD-40+Specialist+white+lithium+grease+spray"),
    "silicone spray lubricant":
        ("WD-40 Specialist silicone spray lubricant",
         "https://www.amazon.com/s?k=WD-40+Specialist+silicone+spray+lubricant"),
    "wd-40 or white lithium grease":
        ("WD-40 Smart Straw + white lithium grease combo",
         "https://www.amazon.com/s?k=WD-40+Smart+Straw+spray"),
    "3-in-1 oil":
        ("3-IN-ONE 10038 multi-purpose oil 4 oz",
         "https://www.amazon.com/s?k=3-IN-ONE+multi-purpose+oil"),
    "lawn aerator rental":
        ("Sun Joe AJ801E electric dethatcher and aerator",
         "https://www.amazon.com/s?k=Sun+Joe+electric+lawn+dethatcher+aerator"),
    "sewer camera rental":
        ("RIDGID SeeSnake micro CA-300 inspection camera",
         "https://www.amazon.com/s?k=drain+sewer+inspection+camera+flexible"),
    "attic insulation blower rental":
        ("Home Depot blower rental (in-store only)",
         "https://www.homedepot.com/s/insulation+blower+machine+rental"),
    "floor buffer/sander rental":
        ("POWERTEC 71902 floor polisher and buffer",
         "https://www.lowes.com/search?searchTerm=floor+buffer+sander+rental"),
}


def update():
    updated_tasks = 0
    updated_items = 0

    for fname in sorted(os.listdir(TASKS_DIR)):
        if not fname.endswith(".json"):
            continue
        path = os.path.join(TASKS_DIR, fname)
        with open(path, encoding="utf-8") as f:
            data = json.load(f, object_pairs_hook=OrderedDict)

        mats = data.get("materials", [])
        if not mats:
            continue

        changed = False
        for m in mats:
            key = m["name"].lower()
            if key in SPECIFIC:
                new_name, new_url = SPECIFIC[key]
                m["name"] = new_name
                m["url"] = new_url
                updated_items += 1
                changed = True

        if changed:
            with open(path, "w", encoding="utf-8") as f:
                json.dump(data, f, indent=2, ensure_ascii=False)
                f.write("\n")
            updated_tasks += 1

    print(f"Updated {updated_items} items across {updated_tasks} tasks.")

    # Retailer breakdown
    from collections import Counter
    from urllib.parse import urlparse
    domains = Counter()
    total = 0
    for fname in os.listdir(TASKS_DIR):
        if not fname.endswith(".json"):
            continue
        data = json.load(open(os.path.join(TASKS_DIR, fname)))
        for m in data.get("materials", []):
            host = urlparse(m["url"]).netloc.replace("www.", "")
            domains[host] += 1
            total += 1

    print(f"\nRetailer distribution ({total} total links):")
    for d, n in domains.most_common():
        print(f"  {d}: {n} ({n/total*100:.1f}%)")


if __name__ == "__main__":
    update()
