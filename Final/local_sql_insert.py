import psycopg2
from psycopg2.extras import execute_values
from config import sql_user, sql_password, sql_host, sql_database, sql_port


CONN = dict(
    host=sql_host,
    port=sql_port,
    dbname=sql_database,
    user=sql_user,
    password=sql_password,
)

# -------------------------------
# 1) Master reference data
# -------------------------------

AGENCIES = [
    "Fire Marshall Office",
    "Local Law Enforcement",
    "National Park Service",
    "US Fish and Wildlife Service",
    "Emergency Medical Services",
    "State Forestry Agency",
    "County Fire Department",
    "Fire Department",
    "Red Cross",
    "Bureau of Land Management",
    "Highway Patrol",
    "Wildlife Conservation Authority",
    "Forest Service",
    "Civil Air Patrol",
    "Army Corps of Engineers",
    "National Guard",
    "Public Works",
    "Environmental Protection Agency",
]

WILDFIRE_CAUSES = [
    "Human activity",
    "Equipment use",
    "Arson",
    "Brushing wind",
    "Lightning",
    "Undefined",
]

FLOOD_CAUSES = [
    "Heavy Rainfall",
    "Snowmelt",
    "Storm Surge",
    "Levee Breach",
    "Dam Failure",
    "Undefined",
]

THREATS = (
    [("Wildfire", c) for c in WILDFIRE_CAUSES] +
    [("Flood",    c) for c in FLOOD_CAUSES] +
    [("Undefined","Undefined")]
)

# Default fallback incidents
INCIDENTS = [
    {
        "incident_name": "Default Wildfire Incident",
        "incident_type": "Wildfire",
        "ics_level": 3,
        "location": "Unknown Location",
        "weather": "Unknown",
        "resources_required": "Standard engine and hand‐crew deployment",
        "identified_cause": "Undefined",
        "incident_summary": "A generic fallback wildfire record used when no matching historic incident is found, triggering standard response protocols.",
        "response_measures": 
            "1. Initiate standard wildfire response plan;  "
            "2. Establish line construction and structure protection;  "
            "3. Mobilize aerial support."
        ,
        "anticipated_developments": "Monitor fire behavior and adjust tactics as conditions evolve.",
        "responding_agencies": "State Forestry Agency, County Fire Department, Local Law Enforcement",
    },
    {
        "incident_name": "Default Flood Incident",
        "incident_type": "Flood",
        "ics_level": 3,
        "location": "Unknown Location",
        "weather": "Unknown",
        "resources_required": "Pumps; sandbags; swift‐water rescue team",
        "identified_cause": "Undefined",
        "incident_summary":"Generic fallback flood record used when no matching historic incident is found, triggering standard flood response protocols.",
        "response_measures": 
            "1. Establish flood operations center;  "
            "2. Deploy pumps and sandbag teams;  "
            "3. Stage swift‐water rescue assets."
        ,
        "anticipated_developments": "Track river/stream gauges and weather; reassess evacuations as levels change.",
        "responding_agencies": "Public Works, Emergency Medical Services, Local Law Enforcement",
    },
    {
        "incident_name": "Trailhead Campfire Escape",
        "incident_type": "Wildfire",
        "ics_level": 2,
        "location": "Pinal Mountains, AZ, USA",
        "weather": "31 °C, 20% RH, WSW winds 22 km/h",
        "resources_required": "4 Type 3 engines; 2 hand crews; 1 helicopter bucket",
        "identified_cause": "Human activity",
        "incident_summary": "Unattended campfire escaped a ring at a popular trailhead, torching brush and juniper, threatening a nearby campground.",
        "response_measures": "1) Immediate campground evacuation; 2) Air bucket drops on head; 3) Hand lines on flanks; 4) Structure protection at campground.",
        "anticipated_developments": "Upslope winds may push head fire; expect rollout and spotting near cliff bands.",
        "responding_agencies": "County Fire Department, Local Law Enforcement, National Park Service",
    },
    {
        "incident_name": "Utility Line Right-of-Way Burn",
        "incident_type": "Wildfire",
        "ics_level": 3,
        "location": "San Pedro Valley, AZ, USA",
        "weather": "29 °C, 18% RH, variable gusts",
        "resources_required": "2 engines; 1 dozer; 1 hand crew",
        "identified_cause": "Human activity",
        "incident_summary": "A private debris burn along a utility ROW escaped containment, igniting grass and creosote.",
        "response_measures": "1) Dozer line to tie into road; 2) Wet line along ROW; 3) Patrol for slopovers.",
        "anticipated_developments": "Gusts may test control lines during afternoon peak heating.",
        "responding_agencies": "County Fire Department, Local Law Enforcement",
    },

    # ---------------------------
    # WILDFIRE — Equipment use
    # ---------------------------
    {
        "incident_name": "Ranch Tractor Spark Fire",
        "incident_type": "Wildfire",
        "ics_level": 3,
        "location": "Cochise Grasslands, AZ, USA",
        "weather": "33 °C, 15% RH, SW winds 20 km/h",
        "resources_required": "3 brush engines; 1 water tender; 1 hand crew",
        "identified_cause": "Equipment use",
        "incident_summary": "Tractor mowing dry grass generated sparks, starting multiple ignitions that merged.",
        "response_measures": "1) Anchor and flank; 2) Progressive hose lays; 3) Tender shuttle operations.",
        "anticipated_developments": "Short-range spotting in flashy fuels until humidity recovery after sunset.",
        "responding_agencies": "State Forestry Agency, Emergency Medical Services, Public Works",
    },
    {
        "incident_name": "Roadside Construction Ignition",
        "incident_type": "Wildfire",
        "ics_level": 2,
        "location": "I-10 Corridor, AZ, USA",
        "weather": "35 °C, 12% RH, gusts 30 km/h",
        "resources_required": "4 brush engines; 2 Type 2 crews; 1 dozer; 1 helicopter",
        "identified_cause": "Equipment use",
        "incident_summary": "Cutting torch during guardrail repair ignited roadside cheatgrass under red-flag winds.",
        "response_measures": "1) Aggressive initial attack; 2) Air support to slow head; 3) Highway closures and detours.",
        "anticipated_developments": "Wind shifts may threaten communications site to the east.",
        "responding_agencies": "State Forestry Agency, Bureau of Land Management, Emergency Medical Services, Public Works",
    },

    # ---------------------------
    # WILDFIRE — Arson
    # ---------------------------
    {
        "incident_name": "Whispering Wash Arson Fire",
        "incident_type": "Wildfire",
        "ics_level": 1,
        "location": "Whispering Wash, AZ, USA",
        "weather": "37 °C, 10% RH, W winds 25 km/h",
        "resources_required": "6 engines; 3 hand crews; 2 dozers; 2 helicopters; 1 airtanker",
        "identified_cause": "Arson",
        "incident_summary": "Multiple ignition points discovered along an access road with accelerant indicators.",
        "response_measures": "1) Unified command; 2) Evacuations of nearby subdivision; 3) Heavy air/ground attack; 4) Evidence preservation.",
        "anticipated_developments": "Potential for repeat ignition events; LE task force activated.",
        "responding_agencies": "Local Law Enforcement, US Fish and Wildlife Service, County Fire Department",
    },
    {
        "incident_name": "Cienega Creek Night Ignitions",
        "incident_type": "Wildfire",
        "ics_level": 2,
        "location": "Cienega Creek, AZ, USA",
        "weather": "28 °C, 18% RH, light winds",
        "resources_required": "3 engines; 1 hand crew; LE arson investigators",
        "identified_cause": "Arson",
        "incident_summary": "Two small nighttime fires set along riparian corridor; quick spread in river cane.",
        "response_measures": "1) Rapid knockdown; 2) Thermal imaging for hotspots; 3) Arson investigation.",
        "anticipated_developments": "Smoldering in cane clumps; patrol overnight.",
        "responding_agencies": "US Fish and Wildlife Service, Local Law Enforcement",
    },

    # ---------------------------
    # WILDFIRE — Brushing wind
    # ---------------------------
    {
        "incident_name": "Mesa Ridge Wind-Driven Brush Fire",
        "incident_type": "Wildfire",
        "ics_level": 2,
        "location": "Mesa Ridge, AZ, USA",
        "weather": "32 °C, 14% RH, gusts 40 km/h",
        "resources_required": "4 engines; 2 hand crews; 1 dozer",
        "identified_cause": "Brushing wind",
        "incident_summary": "High winds downed branches onto power lines, igniting brush on a steep slope.",
        "response_measures": "1) Anchor at ridge road; 2) Parallel hand line; 3) Engine hold along dozer line.",
        "anticipated_developments": "Gusts may cause spotting over lines; request additional crews if spread increases.",
        "responding_agencies": "Forest Service, Highway Patrol, Wildlife Conservation Authority",
    },
    {
        "incident_name": "Canyon Flats Grass Run",
        "incident_type": "Wildfire",
        "ics_level": 3,
        "location": "Canyon Flats, AZ, USA",
        "weather": "30 °C, 20% RH, sustained 30 km/h winds",
        "resources_required": "2 engines; 1 hand crew",
        "identified_cause": "Brushing wind",
        "incident_summary": "Wind pushed grassfire across flats towards a ranch fence line.",
        "response_measures": "1) Flank with engines; 2) Cold trail; 3) Patrol for flare-ups.",
        "anticipated_developments": "Wind easing near sunset should aid containment.",
        "responding_agencies": "Highway Patrol, Wildlife Conservation Authority",
    },

    # ---------------------------
    # WILDFIRE — Lightning
    # ---------------------------
    {
        "incident_name": "Thunder Ridge Single-Tree Strike",
        "incident_type": "Wildfire",
        "ics_level": 3,
        "location": "Thunder Ridge, MT, USA",
        "weather": "30 °C, 9% RH, isolated storms",
        "resources_required": "2 Type 3 engines; 1 helicopter bucket; 1 hand crew",
        "identified_cause": "Lightning",
        "incident_summary": "Dry lightning ignited a snag; fire creeping through grass and sage toward a comms site.",
        "response_measures": "1) Bucket drops on head; 2) Engines for structure protection; 3) Direct line on west flank.",
        "anticipated_developments": "Storm outflows may cause erratic spread; night patrol for holdovers.",
        "responding_agencies": "State Forestry Agency, Wildlife Conservation Authority, Civil Air Patrol",
    },
    {
        "incident_name": "Monsoon Rim Holdover",
        "incident_type": "Wildfire",
        "ics_level": 4,
        "location": "Mogollon Rim, AZ, USA",
        "weather": "26 °C, 30% RH, build-ups",
        "resources_required": "1 engine; 1 squad",
        "identified_cause": "Lightning",
        "incident_summary": "Smoldering log from prior storm began creeping in pine litter mid-day.",
        "response_measures": "1) Hotspot grid with IR; 2) Cold-trail perimeter; 3) Mop-up 50 feet in.",
        "anticipated_developments": "Low spread potential after evening humidity recovery.",
        "responding_agencies": "State Forestry Agency, Wildlife Conservation Authority",
    },

    # ---------------------------
    # FLOOD — Heavy Rainfall
    # ---------------------------
    {
        "incident_name": "Midwest Riverine Flood",
        "incident_type": "Flood",
        "ics_level": 3,
        "location": "Cedar Valley, IA, USA",
        "weather": "23 °C, persistent rain bands, saturated soils",
        "resources_required": "Portable pumps; sandbag teams; swift-water rescue",
        "identified_cause": "Heavy Rainfall",
        "incident_summary": "Prolonged rainfall pushed rivers above major flood stage, inundating low-lying neighborhoods.",
        "response_measures": "1) Activate EOC; 2) Sandbag levees; 3) Stage swift-water rescue; 4) Evacuate at-risk zones.",
        "anticipated_developments": "Crest expected in 24–36 hours; levee seepage likely.",
        "responding_agencies": "Public Works, Emergency Medical Services, Local Law Enforcement, Fire Department",
    },
    {
        "incident_name": "Urban Flash Flooding Event",
        "incident_type": "Flood",
        "ics_level": 2,
        "location": "Phoenix Metro, AZ, USA",
        "weather": "32 °C, monsoon cells, intense downpours",
        "resources_required": "High-capacity pumps; barricades; boat teams",
        "identified_cause": "Heavy Rainfall",
        "incident_summary": "Intense thunderstorms overwhelmed storm drains, flooding underpasses and washes.",
        "response_measures": "1) Road closures; 2) High-water rescues; 3) Pump strategic nodes; 4) Shelter support.",
        "anticipated_developments": "Additional cells could trigger secondary peaks within hours.",
        "responding_agencies": "Public Works, Local Law Enforcement, Emergency Medical Services, Fire Department",
    },

    # ---------------------------
    # FLOOD — Snowmelt
    # ---------------------------
    {
        "incident_name": "Spring Thaw Flood",
        "incident_type": "Flood",
        "ics_level": 4,
        "location": "Gallatin Range, MT, USA",
        "weather": "12 °C daytime, rapid melt, cool nights",
        "resources_required": "Culvert clearance crews; sandbags; monitoring",
        "identified_cause": "Snowmelt",
        "incident_summary": "Warm spell accelerated mountain melt, raising streams and backing water into subdivisions.",
        "response_measures": "1) Clear culverts; 2) Sandbag doorways; 3) Public advisories; 4) Monitor gauges.",
        "anticipated_developments": "Levels fluctuate with diurnal cycle; slow recession in 3–5 days.",
        "responding_agencies": "Public Works, Emergency Medical Services, Local Law Enforcement",
    },
    {
        "incident_name": "High Country Melt Surge",
        "incident_type": "Flood",
        "ics_level": 3,
        "location": "Truckee Basin, CA/NV, USA",
        "weather": "15–18 °C, sunny days, above-normal SWE",
        "resources_required": "Pumps; sandbag teams; shelter operations",
        "identified_cause": "Snowmelt",
        "incident_summary": "Above-average snowpack produced sustained high flows; bank erosion and basement flooding reported.",
        "response_measures": "1) Shore up eroded banks; 2) Pumps at critical lift stations; 3) Open shelters.",
        "anticipated_developments": "Potential for debris jams at bridges; prep chainsaw crews.",
        "responding_agencies": "Public Works, Emergency Medical Services, Local Law Enforcement",
    },

    # ---------------------------
    # FLOOD — Storm Surge
    # ---------------------------
    {
        "incident_name": "Coastal Surge Overwash",
        "incident_type": "Flood",
        "ics_level": 2,
        "location": "Outer Banks, NC, USA",
        "weather": "Tropical storm offshore, long-period swell, onshore winds",
        "resources_required": "High-water vehicles; shelter teams; utility crews",
        "identified_cause": "Storm Surge",
        "incident_summary": "Surge overwash crossed dunes, flooding roads and neighborhoods behind the barrier.",
        "response_measures": "1) Mandatory evacuation of flood zone; 2) Dune breach patrols; 3) Utility shutoffs.",
        "anticipated_developments": "Secondary surge with next high tide; expect roadway scouring.",
        "responding_agencies": "Army Corps of Engineers, National Guard, Local Law Enforcement, Emergency Medical Services",
    },
    {
        "incident_name": "Harbor Inundation Event",
        "incident_type": "Flood",
        "ics_level": 1,
        "location": "Galveston, TX, USA",
        "weather": "Hurricane landfall expected in 12h, gale conditions",
        "resources_required": "USAR task force; high-water rescue; mass care",
        "identified_cause": "Storm Surge",
        "incident_summary": "Rapidly rising surge overtopped bulkheads, flooding harbor district and hospitals.",
        "response_measures": "1) MCI planning; 2) High-water rescues; 3) Shelter and medical surge; 4) Curfew enforcement.",
        "anticipated_developments": "Peak surge coincident with landfall; widespread debris hazard.",
        "responding_agencies": "Army Corps of Engineers, National Guard, Local Law Enforcement, Emergency Medical Services",
    },

    # ---------------------------
    # FLOOD — Levee Breach
    # ---------------------------
    {
        "incident_name": "Urban Levee Breach",
        "incident_type": "Flood",
        "ics_level": 1,
        "location": "Riverbend City, LA, USA",
        "weather": "Hot, windy, no precip; upstream high release",
        "resources_required": "Heavy engineering; pumps; mass evacuation",
        "identified_cause": "Levee Breach",
        "incident_summary": "Levee segment failed under sustained high stage, flooding dense urban blocks.",
        "response_measures": "1) Declare emergency; 2) Mobilize Corps for shoring; 3) Evacuation and security.",
        "anticipated_developments": "Progressive inundation until breach sealed; life safety priority.",
        "responding_agencies": "Army Corps of Engineers, Public Works, Local Law Enforcement, Emergency Medical Services, National Guard, Fire Department",
    },
    {
        "incident_name": "Rural Backwater Overtop",
        "incident_type": "Flood",
        "ics_level": 2,
        "location": "Delta Farmlands, MS, USA",
        "weather": "Warm, breezy; upstream crest",
        "resources_required": "Dozers; rock armoring; pumps",
        "identified_cause": "Levee Breach",
        "incident_summary": "Backwater rise overtopped an agricultural levee, cutting off rural roads and homes.",
        "response_measures": "1) Temporary berm; 2) Pumpdown of isolated pockets; 3) High-water transport.",
        "anticipated_developments": "Erosion risk if flow concentrates at overtopped section.",
        "responding_agencies": "Army Corps of Engineers, Public Works, Local Law Enforcement, Emergency Medical Services, National Guard, Fire Department",
    },

    # ---------------------------
    # FLOOD — Dam Failure
    # ---------------------------
    {
        "incident_name": "Hillside Dam Emergency Drawdown",
        "incident_type": "Flood",
        "ics_level": 1,
        "location": "Hillside Reservoir, CO, USA",
        "weather": "Seasonal storms, saturated abutments, seepage observed",
        "resources_required": "Crane; siphons; heavy pumps; SAR",
        "identified_cause": "Dam Failure",
        "incident_summary": "Rapidly worsening seepage and sinkholes near spillway indicated imminent failure.",
        "response_measures": "1) Immediate downstream evacuation; 2) Emergency drawdown; 3) SAR staging.",
        "anticipated_developments": "Flash flooding likely if breach occurs; debris flow hazards downstream.",
        "responding_agencies": "Army Corps of Engineers, National Guard, Local Law Enforcement, Emergency Medical Services, Public Works, Fire Department",
    },
    {
        "incident_name": "Auxiliary Spillway Erosion",
        "incident_type": "Flood",
        "ics_level": 2,
        "location": "Clearwater Dam, MO, USA",
        "weather": "High inflows; intermittent thunderstorms",
        "resources_required": "Rock trucks; dozers; pumps",
        "identified_cause": "Dam Failure",
        "incident_summary": "Erosion noted on auxiliary spillway during high release; headcut threatening control structure.",
        "response_measures": "1) Rock armor placement; 2) Pump bypass; 3) Downstream warning and partial evac.",
        "anticipated_developments": "Further erosion possible with next cell; continuous monitoring required.",
        "responding_agencies": "Army Corps of Engineers, National Guard, Local Law Enforcement, Emergency Medical Services, Public Works, Fire Department",
    },
    # ---------------------------
    # DEFAULT (Undefined/Undefined)
    # ---------------------------
    {
    "incident_name": "Default All-Hazards Incident",
    "incident_type": "Undefined",
    "ics_level": 3,
    "location": "Unspecified Location, USA",
    "weather": "Unknown conditions; weather data unavailable or inconsistent",
    "resources_required": "Standard multi-agency dispatch; standby emergency ops center",
    "identified_cause": "Undefined",
    "incident_summary": "Generic emergency incident triggered by ambiguous signals or AI detection without conclusive threat classification.",
    "response_measures": "1) Activate local EOC; 2) Dispatch assessment team; 3) Maintain readiness posture across agencies; 4) Prepare for escalation.",
    "anticipated_developments": "Further evaluation required; threat classification pending situational updates or sensor validation.",
    "responding_agencies": "Local Law Enforcement, Emergency Medical Services, Fire Marshall Office"
    },
]

# -------------------------------
# 2) Agency participation matrix
#    (who responds to each cause, per ICS)
# -------------------------------

# same agencies for all ICS levels
def all_levels(*agencies):
    return {lvl: list(agencies) for lvl in range(1, 6)}

# WILDFIRE responding agencies per cause/ICS
WILDFIRE_AGENCIES = {
    "Human activity": {
        1: ["County Fire Department", "National Park Service", "Red Cross", "Local Law Enforcement"],
        2: ["National Park Service", "Red Cross", "Local Law Enforcement"],
        3: ["County Fire Department", "National Park Service"],
        4: ["County Fire Department", "National Park Service", "Red Cross", "Local Law Enforcement"],
        5: ["County Fire Department", "National Park Service", "Red Cross", "Local Law Enforcement"],
    },
    "Equipment use": {
        1: ["State Forestry Agency", "Emergency Medical Services", "Public Works"],
        2: ["State Forestry Agency", "Bureau of Land Management", "Emergency Medical Services", "Public Works"],
        3: ["State Forestry Agency", "Emergency Medical Services"],
        4: ["State Forestry Agency", "Bureau of Land Management", "Emergency Medical Services", "Public Works"],
        5: ["State Forestry Agency", "Bureau of Land Management", "Emergency Medical Services", "Public Works"],
    },
    "Arson": {
        1: ["US Fish and Wildlife Service"],
        2: ["Local Law Enforcement", "US Fish and Wildlife Service"],
        3: ["US Fish and Wildlife Service"],
        4: ["Local Law Enforcement", "US Fish and Wildlife Service"],
        5: ["Local Law Enforcement", "US Fish and Wildlife Service"],
    },
    "Brushing wind": {
        1: ["Highway Patrol", "Wildlife Conservation Authority"],
        2: ["Forest Service", "Highway Patrol", "Wildlife Conservation Authority"],
        3: ["Highway Patrol", "Wildlife Conservation Authority"],
        4: ["Forest Service", "Highway Patrol", "Wildlife Conservation Authority"],
        5: ["Forest Service", "Highway Patrol", "Wildlife Conservation Authority"],
    },
    "Lightning": {
        1: ["State Forestry Agency", "Wildlife Conservation Authority", "Civil Air Patrol"],
        2: ["State Forestry Agency", "Wildlife Conservation Authority", "Civil Air Patrol"],
        3: ["State Forestry Agency", "Wildlife Conservation Authority", "Civil Air Patrol"],
        4: ["Forest Service", "State Forestry Agency", "Wildlife Conservation Authority", "Civil Air Patrol"],
        5: ["Forest Service", "State Forestry Agency", "Wildlife Conservation Authority", "Civil Air Patrol"],
    },
    "Undefined": all_levels("County Fire Department", "State Forestry Agency", "Local Law Enforcement"),
}

# FLOOD responding agencies per cause/ICS
FLOOD_AGENCIES = {
    "Heavy Rainfall": all_levels("Public Works", "Emergency Medical Services", "Local Law Enforcement", "Fire Department"),
    "Snowmelt": all_levels("Public Works", "Emergency Medical Services", "Local Law Enforcement"),
    "Storm Surge": all_levels("Army Corps of Engineers", "National Guard", "Local Law Enforcement", "Emergency Medical Services"),
    "Levee Breach": all_levels("Army Corps of Engineers", "Public Works", "Local Law Enforcement", "Emergency Medical Services", "National Guard", "Fire Department"),
    "Dam Failure": all_levels("Army Corps of Engineers", "National Guard", "Local Law Enforcement", "Emergency Medical Services", "Public Works", "Fire Department"),
    "Undefined": all_levels("Public Works", "Emergency Medical Services", "Local Law Enforcement"),
}

# DEFAULT (Undefined/Undefined)
DEFAULT_AGENCIES = all_levels("Emergency Medical Services", "Local Law Enforcement", "Fire Marshall Office")

# -------------------------------
# 3) SOP
# -------------------------------

def scale(prefix, ics):
    """
    Return a resource scale suffix by ICS.
    ICS 1 = surge (largest), ICS 5 = minimal (smallest).
    """
    scale_map = {
        1: " (surge)",
        2: " (high)",
        3: " (moderate)",
        4: " (limited)",
        5: " (minimal)",
    }
    return f"{prefix}{scale_map[ics]}"

def sop_wildfire(agency, cause, ics):
    # Per-agency intent
    if agency in ("County Fire Department", "Fire Department"):
        proc = {
            1: "Assume unified command; mass evacuation support; structure protection; aerial coordination.",
            2: "Lead suppression operations; expand divisions; coordinate air/ground task forces.",
            3: "Direct line construction; point protection; staging and water supply.",
            4: "Initial attack; spot fire patrols; mop-up planning.",
            5: "Single-engine response; monitor and standby.",
        }[ics]
        res = {
            1: "6 engines; 2 tenders; 2 hand crews; 1 dozer; 1 helitack",
            2: "4 engines; 1 tender; 1 hand crew; 1 dozer",
            3: "3 engines; 1 hand crew",
            4: "2 engines",
            5: "1 engine",
        }[ics]
        return proc, res

    if agency == "State Forestry Agency":
        proc = {
            1: "State-level incident management; multi-region coordination; air asset tasking.",
            2: "Regional IMT activation; resource ordering; situation reporting.",
            3: "Deploy investigators and suppression modules; assist local IC.",
            4: "Patrol and support initial attack; advise on fire weather.",
            5: "Monitoring and technical advisories.",
        }[ics]
        res = {
            1: "1 Type 1 IMT; 2 air tankers; 1 helicopter",
            2: "1 Type 2 IMT; 1 helicopter",
            3: "1 suppression module; 2 investigators",
            4: "1 patrol unit",
            5: "1 duty officer",
        }[ics]
        return proc, res

    if agency == "National Park Service":
        proc = {
            1: "Close park units; integrate National IMT; protect cultural resources.",
            2: "Regional fire management; visitor evacuation; ops suspension.",
            3: "Type 2 crews to staging; resource protection priorities.",
            4: "Suppression module initial attack; visitor alerts.",
            5: "Lookout patrol; public guidance.",
        }[ics]
        res = {
            1: "1 National IMT; 3 closure teams; 2 PIOs",
            2: "1 regional manager; 2 rangers",
            3: "2 Type 2 crews; 1 staging officer",
            4: "1 suppression module; 1 ATV",
            5: "1 lookout team",
        }[ics]
        return proc, res

    if agency == "Local Law Enforcement":
        proc = {
            1: "Unified command with state/federal; evacuation and security.",
            2: "Regional closures; enforce perimeters; public information.",
            3: "Local evacuations; traffic control; SAR standby.",
            4: "Traffic assistance; scene security.",
            5: "Routine patrol; monitor conditions.",
        }[ics]
        res = {
            1: "10 tactical units; 1 PIO",
            2: "8 patrol units; 1 PIO",
            3: "6 patrol units",
            4: "3 patrol units",
            5: "2 patrol units",
        }[ics]
        return proc, res

    if agency == "US Fish and Wildlife Service":
        proc = {
            1: "Protect endangered habitat; federal coordination; specialized investigations.",
            2: "Deploy wildlife protection teams; coordinate with IMT for habitat buffers.",
            3: "Field monitoring for species impact; advise suppression on habitat.",
            4: "Patrol closures; assist with wildlife relocations.",
            5: "Minimal monitoring and public guidance.",
        }[ics]
        res = {
            1: "2 habitat teams; 1 federal liaison",
            2: "1 habitat team; 1 biologist",
            3: "2 biologists; 1 transport vehicle",
            4: "1 biologist; 1 pickup",
            5: "1 liaison",
        }[ics]
        return proc, res

    if agency == "Bureau of Land Management":
        proc = {
            1: "Federal land fire ops; large air/ground coordination.",
            2: "Regional BLM resources to line building and point protection.",
            3: "BLM engines/crews support local IC.",
            4: "Initial attack and patrol on BLM parcels.",
            5: "Monitor BLM lands.",
        }[ics]
        res = {
            1: "2 air tankers; 2 engines; 1 dozer",
            2: "1 air tanker; 2 engines",
            3: "2 engines",
            4: "1 engine",
            5: "1 duty unit",
        }[ics]
        return proc, res

    if agency == "Highway Patrol":
        proc = {
            1: "Statewide freeway closures and contraflow planning.",
            2: "Regional closure points; escort heavy equipment.",
            3: "Local detours; perimeter support.",
            4: "Spot closures; signage.",
            5: "Monitor and advise motorists.",
        }[ics]
        res = {
            1: "10 units; mobile message signs",
            2: "8 units; barricades",
            3: "5 units",
            4: "3 units",
            5: "2 units",
        }[ics]
        return proc, res

    if agency == "Wildlife Conservation Authority":
        proc = {
            1: "Statewide fauna protection; wildlife corridor control.",
            2: "Regional habitat advisory and relocation ops.",
            3: "Local wildlife monitoring; coordinate with IC.",
            4: "Patrol closures; small relocations.",
            5: "Advisories only.",
        }[ics]
        res = {
            1: "2 relocation teams; 1 vet support",
            2: "1 relocation team",
            3: "2 techs",
            4: "1 tech",
            5: "1 liaison",
        }[ics]
        return proc, res

    if agency == "Forest Service":
        proc = {
            1: "Federal forest IMT; large air ops; multi-division attack.",
            2: "Regional crews to anchor/flank; air recon.",
            3: "Support local IC with engines/crews.",
            4: "Initial attack on USFS lands; spotting patrols.",
            5: "Lookout reports; advisories.",
        }[ics]
        res = {
            1: "1 Type 1 IMT; 2 air tankers; 1 helo",
            2: "2 Type 2 crews; 2 engines",
            3: "2 engines; 1 crew",
            4: "1 engine",
            5: "1 lookout",
        }[ics]
        return proc, res

    if agency == "Civil Air Patrol":
        proc = {
            1: "Aerial recon for perimeter and spotting; IMT intel.",
            2: "Regional recon sorties and comms relay.",
            3: "Local recon flights as tasked.",
            4: "Limited recon flights.",
            5: "Standby aircrew.",
        }[ics]
        res = {
            1: "3 aircraft; 2 aircrews",
            2: "2 aircraft; 2 aircrews",
            3: "1 aircraft; 1 aircrew",
            4: "1 aircrew",
            5: "1 liaison",
        }[ics]
        return proc, res

    if agency == "Red Cross":
        proc = {
            1: "Mass care: shelters, reunification, bulk distribution.",
            2: "Regional shelter ops; canteen services.",
            3: "Local shelter support.",
            4: "Welfare checks and limited distribution.",
            5: "Advisory services.",
        }[ics]
        res = {
            1: "3 shelter teams; 2 ERVs",
            2: "2 shelter teams; 1 ERV",
            3: "1 shelter team",
            4: "1 mobile team",
            5: "1 liaison",
        }[ics]
        return proc, res

    if agency == "Fire Marshall Office":
        proc = {
            1: "Statewide origin & cause coordination; interagency liaison.",
            2: "Regional cause task force; evidence protocols.",
            3: "Investigators to ICP; preliminary report.",
            4: "Deputy marshal monitoring of lines for cause indicators.",
            5: "Local marshal initial origin check.",
        }[ics]
        res = {
            1: "1 state team; 1 lab; 1 federal liaison",
            2: "1 regional team; 2 evidence kits",
            3: "2 investigators; 1 portable kit",
            4: "1 deputy; 1 kit",
            5: "1 unit",
        }[ics]
        return proc, res

    # Fallback generic
    return (
        f"Support wildfire ops for cause={cause}; integrate with IC; task as assigned.",
        scale("Generic resources", ics)
    )

def sop_flood(agency, cause, ics):
    if agency == "Army Corps of Engineers":
        proc = {
            1: "Emergency levee/dam reinforcement; heavy civil works; floodway management.",
            2: "Regional engineering ops; shoring and breach repair.",
            3: "Deploy pumps and temporary barriers; technical assessment.",
            4: "Advisory and light works support.",
            5: "Remote monitoring & planning.",
        }[ics]
        res = {
            1: "2 rock-armoring units; 1 engineer battalion",
            2: "1 heavy engineer company",
            3: "2 pump units; 1 barrier kit",
            4: "1 engineer team",
            5: "1 liaison",
        }[ics]
        return proc, res

    if agency == "Public Works":
        proc = {
            1: "Citywide flood control ops; stormwater diversion; debris clearance.",
            2: "Regional culvert/ditch clearance; mobile pumps; barricades.",
            3: "Targeted pumps and sandbag crews to chokepoints.",
            4: "Localized clearing and signage.",
            5: "Routine inspection of drains.",
        }[ics]
        res = {
            1: "4 pumps; 4 sandbag teams; 2 debris crews",
            2: "3 pumps; 3 sandbag teams; barricades",
            3: "2 pumps; 2 sandbag teams; debris crew",
            4: "1 pump; 1 crew",
            5: "1 inspector",
        }[ics]
        return proc, res

    if agency == "Local Law Enforcement":
        proc = {
            1: "Mass evacuation routes; perimeter control; search & rescue coordination.",
            2: "Regional closures and detours; public info.",
            3: "Local evacuations; swift-water support traffic control.",
            4: "Flooded-road deterrence and signage.",
            5: "Patrol & monitor high water areas.",
        }[ics]
        res = {
            1: "12 patrol units; 1 PIO",
            2: "8 patrol units; barricades",
            3: "6 patrol units",
            4: "3 patrol units",
            5: "2 patrol units",
        }[ics]
        return proc, res

    if agency == "Emergency Medical Services":
        proc = {
            1: "MCI triage; water-rescue medical support; hospital surge coordination.",
            2: "Regional medical branch; evac shelter medical.",
            3: "Field hospitals on standby; transport coordination.",
            4: "On-call BLS for welfare checks.",
            5: "Public health advisories and monitoring.",
        }[ics]
        res = {
            1: "1 MCI trailer; 4 ALS; 1 supervisor",
            2: "2 ALS; 1 supervisor",
            3: "1 field hospital; 2 transport ambulances",
            4: "1 BLS unit",
            5: "1 liaison",
        }[ics]
        return proc, res

    if agency == "National Guard":
        proc = {
            1: "High-water rescue; logistics airlift; wide-area security.",
            2: "Resupply, debris ops; evac support.",
            3: "Assist with sheltering/logistics; patrol high-risk areas.",
            4: "Limited support for sandbagging and patrol.",
            5: "Standby readiness.",
        }[ics]
        res = {
            1: "2 helo teams; 4 high-water vehicles; 2 security platoons",
            2: "2 high-water vehicles; 1 logistics team",
            3: "1 logistics team; 1 patrol squad",
            4: "1 squad",
            5: "1 liaison",
        }[ics]
        return proc, res

    if agency == "Fire Department" or agency == "County Fire Department":
        proc = {
            1: "Swift-water rescue task force; evacuation and structure triage.",
            2: "Boat teams for life-safety; pump support.",
            3: "Boat rescue units on standby; sandbag support.",
            4: "Single engine company checks and standby.",
            5: "Public advisories and routine checks.",
        }[ics]
        res = {
            1: "2 rescue boats; 4 engines; 1 USAR team",
            2: "2 rescue boats; 2 engines",
            3: "1 boat; 2 engines",
            4: "1 engine",
            5: "1 duty crew",
        }[ics]
        return proc, res

    if agency == "Environmental Protection Agency":
        proc = {
            1: "Hazmat monitoring; water contamination assessments; public health guidance.",
            2: "Regional sampling and advisories; coordinate with utilities.",
            3: "Targeted sampling near critical infrastructure.",
            4: "Advisory sampling and reporting.",
            5: "Remote monitoring and guidance.",
        }[ics]
        res = {
            1: "2 hazmat teams; 1 lab trailer",
            2: "1 hazmat team",
            3: "2 sampling kits; 1 tech team",
            4: "1 sampling kit",
            5: "1 liaison",
        }[ics]
        return proc, res

    # Fallback generic
    return (
        f"Support flood ops for cause={cause}; integrate with IC; task as assigned.",
        scale("Generic resources", ics)
    )

def sop_default(agency, ics):
    if agency == "Emergency Medical Services":
        return {
            1: ("Stand up MCI triage & transport; integrate with unified command.", "1 MCI trailer; 4 ALS; 1 EMS supervisor"),
            2: ("Establish medical branch; coordinate hospital surge capacity.", "2 ALS; 1 supervisor"),
            3: ("Stage at ICP; on-scene triage/transport as required.", "1 ALS; 1 BLS"),
            4: ("Put one unit on standby; surge call coordination.", "1 BLS"),
            5: ("Monitor; provide public health advisories.", "1 public health liaison"),
        }[ics]

    if agency == "Local Law Enforcement":
        return {
            1: ("Unified command with state/federal; large-scale evacuation security.", "20 patrol units; 2 SWAT teams"),
            2: ("Regional road closures; enforce perimeters; PIO support.", "8 patrol units; 1 PIO"),
            3: ("Local evacuations & traffic control; SAR standby.", "6 patrol units"),
            4: ("Traffic assistance and scene security.", "3 patrol units"),
            5: ("Routine patrol & monitoring.", "2 patrol units"),
        }[ics]

    if agency == "Fire Marshall Office":
        return {
            1: ("Statewide investigation coordination; interagency liaison.", "1 state team; 1 lab; 1 federal liaison"),
            2: ("Regional cause task force; evidence protocols.", "1 regional team; 2 evidence kits"),
            3: ("Investigators to ICP; preliminary report.", "2 investigators; 1 portable kit"),
            4: ("Deputy marshal monitoring.", "1 deputy; 1 kit"),
            5: ("Local marshal origin check.", "1 unit"),
        }[ics]

    return (
        "Generic all-hazard support; integrate with IC; task as assigned.",
        scale("Generic resources", ics)
    )

# -------------------------------
# 4) DB helpers
# -------------------------------

def get_id(cur, sql, param):
    cur.execute(sql, (param,))
    row = cur.fetchone()
    return row[0] if row else None

def get_agency_id(cur, name):
    return get_id(cur, "SELECT agency_id FROM agencies WHERE agency_name=%s;", name)

def get_threat_id(cur, tname, tcause):
    cur.execute("SELECT threat_id FROM threats WHERE threat_name=%s AND threat_cause=%s;", (tname, tcause))
    row = cur.fetchone()
    return row[0] if row else None

def upsert_agencies(cur):
    execute_values(
        cur,
        "INSERT INTO agencies (agency_name) VALUES %s ON CONFLICT (agency_name) DO NOTHING;",
        [(a,) for a in AGENCIES]
    )

def upsert_threats(cur):
    execute_values(
        cur,
        """
        INSERT INTO threats (threat_name, threat_cause)
        VALUES %s
        ON CONFLICT (threat_name, threat_cause) DO NOTHING;
        """,
        THREATS
    )

def upsert_incidents(cur):
    for inc in INCIDENTS:
        cur.execute(
            """
            INSERT INTO incidents (
              incident_name, incident_type, ics_level, location, weather,
              resources_required, identified_cause, incident_summary,
              response_measures, anticipated_developments, responding_agencies
            )
            VALUES (
              %(incident_name)s, %(incident_type)s, %(ics_level)s, %(location)s, %(weather)s,
              %(resources_required)s, %(identified_cause)s, %(incident_summary)s,
              %(response_measures)s, %(anticipated_developments)s, %(responding_agencies)s
            )
            ON CONFLICT DO NOTHING;
            """,
            inc
        )

def insert_sop(cur, threat_id, ics, agency_id, proc, res):
    cur.execute(
        """
        INSERT INTO sops (threat_id, ics_level, agency_id, standard_operating_procedure, resources_required)
        VALUES (%s, %s, %s, %s, %s)
        ON CONFLICT (threat_id, ics_level, agency_id) DO NOTHING;
        """,
        (threat_id, ics, agency_id, proc, res)
    )

# -------------------------------
# 5) Build full SOP matrix
# -------------------------------

def build_wildfire_sops(cur):
    for cause, levels in WILDFIRE_AGENCIES.items():
        t_id = get_threat_id(cur, "Wildfire", cause)
        if not t_id:
            continue
        for ics, agencies in levels.items():
            for ag in agencies:
                a_id = get_agency_id(cur, ag)
                if not a_id:
                    continue
                proc, res = sop_wildfire(ag, cause, ics)
                insert_sop(cur, t_id, ics, a_id, proc, res)

def build_flood_sops(cur):
    for cause, levels in FLOOD_AGENCIES.items():
        t_id = get_threat_id(cur, "Flood", cause)
        if not t_id:
            continue
        for ics, agencies in levels.items():
            for ag in agencies:
                a_id = get_agency_id(cur, ag)
                if not a_id:
                    continue
                proc, res = sop_flood(ag, cause, ics)
                insert_sop(cur, t_id, ics, a_id, proc, res)

def build_default_sops(cur):
    t_id = get_threat_id(cur, "Undefined", "Undefined")
    if not t_id:
        return
    for ics, agencies in DEFAULT_AGENCIES.items():
        for ag in agencies:
            a_id = get_agency_id(cur, ag)
            if not a_id:
                continue
            proc, res = sop_default(ag, ics)
            insert_sop(cur, t_id, ics, a_id, proc, res)

# -------------------------------
# 6) entry point
# -------------------------------

def main():
    conn = psycopg2.connect(**CONN)
    try:
        with conn:
            with conn.cursor() as cur:
                upsert_agencies(cur)
                upsert_threats(cur)
                upsert_incidents(cur)

                build_wildfire_sops(cur)
                build_flood_sops(cur)
                build_default_sops(cur)

        print("agencies, threats, incidents, and SOP matrix populated.")
    finally:
        conn.close()

if __name__ == "__main__":
    main()
