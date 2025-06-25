-- 1) Table definition
CREATE TABLE wildfire_emergencies (
    id              SERIAL PRIMARY KEY,
    threat_name     VARCHAR(100),
    threat_summary  TEXT,
    steps_followed  TEXT,
    resources       TEXT,
    priority        VARCHAR(15),
    cause           VARCHAR(120),
    first_responders TEXT,
    location        VARCHAR(150),
    weather         VARCHAR(120),
    date_occurred   DATE,
    time_occurred   TIME
);

-- 2) INSERT statements
INSERT INTO wildfire_emergencies
(threat_name, threat_summary, steps_followed, resources, priority, cause,
 first_responders, location, weather, date_occurred, time_occurred)
VALUES
-- 1
('Pine Creek Blaze',
'The Pine Creek Blaze ignited on a steep pine covered slope eight kilometres west of Dayton. A group of hikers noticed smoke rising from a lightning struck snag and phoned 911 at 14:07. Within thirty minutes shifting downslope winds pushed the flames into thick ground litter and ladder fuels, producing two metre flame lengths and spotting across a dry creek bed. The nearest subdivision, Willow Estates, lay 1.8 km away and contained 120 structures built before updated fire wise codes. Air quality rapidly declined and visibility on County Route 41 dropped below 300 m, complicating civilian egress. By 17:00 the fire was mapped at 37 ha with a potential to run uphill toward a communications tower.',
'Incident command established a unified command post with county fire and the state forestry agency. Incoming units triaged Willow Estates, marking defensible homes with green tape and non defensible with red. Two Type 3 engines anchored the heel, constructing a progressive hose lay uphill while a Type 2 IA crew widened an old dozer line. Air Attack orbited at 2 500 m coordinating one LAT and two SEATs that alternated retardant drops on the right flank. Law enforcement set up hard road closures and executed a reverse 911 alert for voluntary evacuation. By nightfall crews transitioned to hand tools and IR cameras, mopping hot spots within 30 m of the line.',
'2 Type 3 engines; 1 water tender; 1 Type 2 IA crew; 1 LAT; 2 SEATs; 1 dozer',
'High',
'Dry lightning',
'Dayton Rural Fire; State Forestry; Sheriff',
'Dayton, OR, USA',
'34 C, 12 % RH, gusts 25 km/h',
'2025-06-02',
'14:30'),
-- 2
('Sierra Ridge Fire',
'A camper’s unattended stove started the Sierra Ridge Fire in the Tahoe National Forest near a popular dispersed campsite. The initial flame front moved uphill through manzanita and dead fall, aligning with a 15 percent upslope and afternoon up canyon winds. The nearest highway lay only 600 m above the ignition point, and traffic backed up as smoke crossed the pavement. Cell reception was poor, delaying the first 911 call by at least twenty minutes. By the time engines arrived the fire was estimated at 22 ha with multiple rollouts. Several hikers on the Pacific Crest Trail were at risk of becoming trapped on the ridge line.',
'The local forest engine captain assumed IC and ordered immediate backpack pump deployment to protect the ridge trail until helitack arrived. Two helicopters performed bucket work on rolling material. A Hotshot crew cut direct line on the west flank while an inmate crew prepped indirect line along the highway shoulder using saw teams. Highway patrol established alternating one way traffic to keep escape routes open. Medical staged at mile marker 34 with an ALS rig. Contingency planning included a potential shelter in place at Granite Lake should downhill escape be compromised. Containment reached 30 percent by 22:00 and mop up continued overnight.',
'2 Type 6 engines; 1 Hotshot crew; 1 inmate crew; 2 Type 2 helicopters; 1 ALS ambulance',
'High',
'Unattended camp stove',
'USFS Engine 421; Tahoe Hotshots; CHP',
'Tahoe National Forest, CA, USA',
'31 C, 14 % RH, upslope 18 km/h',
'2025-07-12',
'15:10'),
-- 3
('Outback Station Burn',
'Strong northwesterly winds fanned a blaze across open rangeland near Outback Station in New South Wales. The fire began when a utility line snapped, showering dry grass with sparks amid a prolonged drought. Within an hour the head fire advanced three kilometres, threatening sheep paddocks and a heritage homestead built in 1880. Critical habitat for the endangered mallee fowl lay directly downwind. Visibility on the Cobb Highway plunged as dust and smoke mixed, prompting police to detour freight traffic. Rural residents relied on surface dams for water, forcing tankers to shuttle from a river pump site twelve kilometres away.',
'The Incident Controller implemented the New South Wales Rural Fire Service grass-fire SOP. Strike teams used a pincer attack with two heavies flanking left and right while slip-ons performed direct attack at the heel. A contract fixed-wing scooper made repeated drops from a nearby lake, cooling the head until bulldozers finished a mineral earth break. Landholders activated farm fire units for perimeter patrol and later assisted with blacking-out stumps. Wildlife officers pre-positioned cages and water troughs for displaced fauna. Power company crews de-energised the remaining lines before re-stringing conductors. By 23:00 a 25-metre black was secured and crews transitioned to night shift for patrol.',
'4 Category 1 tankers; 3 slip-ons; 1 bulldozer; 1 fixed-wing scooper; 2 farm fire units',
'Moderate',
'Sagging powerline in drought',
'NSW RFS Far West Team; Police; Power Utility',
'Outback Station, NSW, Australia',
'38 C, 8 % RH, winds 35 km/h NW',
'2025-01-19',
'13:50'),
-- 4
('Black Mesa Complex',
'A series of dry thunderstorms produced multiple lightning strikes across Black Mesa on the Navajo Nation. Three small starts quickly merged in pinyon-juniper, forming a plume dominated column visible from Flagstaff ninety kilometres south. The remote terrain lacked road access, delaying hand crews for hours and allowing the fire to grow to 1 200 hectares before initial attack. Cultural sites, including ancient cliff dwellings and ceremonial grounds, were located on the mesa rim and required special protection measures negotiated with tribal elders. The Incident Management Team anticipated a multi-day effort under Red Flag conditions.',
'The Type 2 IMT implemented the Federal Wildland Fire Policy with a full suppression strategy. Helicopter rappelers inserted to scout natural rock barriers for anchor points. Dozers were prohibited near cultural resources, so Hotshots hand cut indirect line that tied into a basalt outcrop. Portable pumps relayed water 1.5 km from a stock pond, feeding bladder bags for crew use. Structure protection groups wrapped three hogans with aluminized cloth and installed sprinkler kits powered by portable tanks. Air resources included two heavy airtankers on long term retardant and a VLAT tasked with painting the southern contingency line. Night operations relied on UAS equipped with thermal cameras to detect spots beyond control lines.',
'2 Hotshot crews; 1 rappel crew; 2 heavy airtankers; 1 VLAT; 3 portable pump kits; 1 UAS module',
'Critical',
'Lightning smolder merging',
'Navajo Nation Fire and Rescue; USFS IMT2; BIA',
'Black Mesa, AZ, USA',
'33 C, 10 % RH, winds 40 km/h SW',
'2025-05-21',
'11:25'),
-- 5
('Lakeview Canyon Fire',
'An abandoned debris pile reignited after a week of record temperatures near Lakeview Reservoir in British Columbia. The canyon channels afternoon winds that consistently exceed 40 km/h, creating a blowtorch effect on cured grass and slash piles left from recent logging. Cabins along the reservoir shore are accessed by a single gravel road susceptible to rock fall. The local volunteer department arrived with limited water and immediately requested provincial resources. Tourists boating on the reservoir were unaware of the approaching smoke column until ash began falling on the water.',
'Provincial duty officer deployed an Initial Attack Crew via helicopter to secure the downwind flank while volunteers focused on structure defence, installing sprinkler lines and clearing flammable deck furniture. An amphibious skimmer aircraft cycled every seven minutes from the reservoir surface to check the head fire. Heavy equipment constructed a safety zone on a bench above the cabins. RCMP evacuated 47 visitors by boat to the opposite shore where a reception centre was established. Night shift patrolled with FLIR to catch hidden stump fires in the steep talus slopes. Full containment was achieved after a 36 hour campaign.',
'1 volunteer engine; 1 IA crew; 1 skimmer aircraft; 2 excavators; sprinkler trailer',
'High',
'Re-ignited debris pile',
'Lakeview VFD; BC Wildfire Service; RCMP',
'Lakeview Reservoir, BC, Canada',
'30 C, 13 % RH, winds 42 km/h W',
'2025-08-03',
'16:05'),
-- 6
('Karlstad Peat Fire',
'A lightning bolt ignited a peat bog outside Karlstad, Sweden following an unusually dry spring. Although surface flames appeared minor, the fire quickly spread underground, producing dense smoke and elevated carbon monoxide levels. Nearby E18 motorway traffic experienced visibility drops to 50 metres, causing several minor collisions. The fire threatened high voltage transmission towers whose footings sat on peat mounds that could subside if combustion continued unchecked.',
'Swedish Civil Contingencies Agency activated its peat fire procedure. Firefighters trenched to mineral soil around the perimeter, then flooded sectors with high volume pumps drawing from the Klarälven River. Drone based thermal mapping guided excavator operators to hotspots that required over-digging and application of class A foam. Highway authorities installed variable message signs reducing speeds and deployed tow trucks for rapid incident clearance. Environmental officers monitored particulate matter and advised nearby schools to move activities indoors. After seven days of continuous flooding operations smouldering was reduced to safe levels and mop-up transitioned to local brigade patrols.',
'6 high volume pumps; 3 excavators; 2 drones; 1 hazmat monitor van',
'Moderate',
'Lightning in peat bog',
'Karlstad Räddningstjänsten; MSB; Trafikverket',
'Karlstad, Värmland, Sweden',
'27 C, 20 % RH, light winds 10 km/h',
'2025-06-28',
'09:40'),
-- 7
('Eagle Pass Interface Fire',
'Illegal fireworks ignited dry grass on the edge of Eagle Pass, Texas during Independence Day celebrations. Within minutes flames impinged on cedar fences separating suburban homes from a greenbelt, generating intense radiant heat that broke windows and ignited attic vents. Propane tanks connected to backyard grills vented, producing torching jets visible from two streets away. Embers carried across US Highway 277 and started spot fires in commercial landscaping.',
'The municipal fire chief activated the Wildland Urban Interface (WUI) Annex of the city emergency plan. Two ladder trucks performed direct structure defence while brush trucks knocked down fire in the greenbelt. Public works crews arrived with graders to scrape a fire break along the highway median. Police executed a rapid evacuation of three cul-de-sacs and established a reunification point at a high school gym. Mutual aid from the county supplied additional tenders to compensate for weak hydrant flow. By coordinating attic inspections with thermal imagers firefighters prevented rekindles inside void spaces. Fire watch remained in place for 48 hours.',
'2 ladder trucks; 4 brush trucks; 3 water tenders; 2 graders; 1 thermal camera team',
'High',
'Illegal fireworks',
'Eagle Pass FD; Maverick County VFD; Police',
'Eagle Pass, TX, USA',
'38 C, 15 % RH, winds 20 km/h SE',
'2025-07-04',
'20:15'),
-- 8
('Cape Flats Dune Fire',
'Strong south-easterly winds pushed a grass fire across the coastal dunes of the Cape Flats near Cape Town. Informal settlements bordering the dunes relied on plastic sheeting and recycled timber, creating highly vulnerable fuel complexes. Firebrands landed on tar-impregnated roofs, causing rapid extensions. The plume threatened to cross the N2 highway, a critical commuter corridor, during peak evening traffic. Aircraft from the provincial service were grounded by wind gusts exceeding safe limits.',
'City Fire and Rescue implemented the Community Fire Safe Plan, deploying six pumpers to protect primary structures while seasonal crews conducted indirect attack with drip torches to widen existing sand firebreaks. Volunteer Disaster Risk Management teams disseminated evacuation messages via loudhailers in Xhosa, Afrikaans and English. Traffic services orchestrated contraflow lanes on the N2 to expedite outbound traffic. A mobile water cannon truck, normally used for riot control, was repurposed to wet roofs ahead of advancing sparks. Once wind velocity dropped below 40 km/h, a spotter plane guided a contracted helicopter for precision water drops on remaining hot spots.',
'6 pumpers; 2 skid units; 1 water cannon; volunteer DRM teams; 1 helicopter',
'Critical',
'Wind driven grass ignition (unknown origin)',
'Cape Town Fire & Rescue; DRMC; Traffic Services',
'Cape Flats, Cape Town, South Africa',
'29 C, 18 % RH, winds 50 km/h SE',
'2025-02-17',
'17:55'),
-- 9
('Maui Gulch Fire',
'A malfunctioning power tool during brush clearing sparked the Maui Gulch Fire near Lahaina. The ignition site sat at the base of a steep gulch choked with non-native Guinea grass that had cured after an extended drought. Diurnal winds rapidly funneled fire upslope toward residential areas and historic cultural sites. Air tour helicopters reported a towering convection column visible from offshore.',
'County Fire Department established a Staging Area at a golf course and deployed Type 1 helicopters with snorkel buckets sourced from private operators. Crews executed a coordinated “pump and roll” along a narrow access road while Hotshots cut direct line on the ridge crest. Emergency Management pushed Wireless Emergency Alerts to cell phones and activated tsunami sirens in wildland voice mode to capture public attention. Public Works bulldozed a contingency fire break paralleling the utility corridor. Cultural liaisons consulted on site to protect archeological features. Containment lines held despite 35 km/h wind shifts thanks to aggressive night bucket work.',
'2 Type 1 helicopters; 1 Hotshot crew; 3 engines; 2 bulldozers; EM alert system',
'High',
'Sparks from power tool',
'Maui County FD; Private Helis; Public Works',
'Lahaina, Maui, HI, USA',
'32 C, 11 % RH, winds 35 km/h NE',
'2025-03-14',
'13:20'),
-- 10
('Red River Backburn',
'An escaped prescribed burn on ranch land near the Red River in Oklahoma jumped control lines following a sudden frontal passage. The fire spotted across the river into Texas jurisdiction, complicating command and control. Fine flashy fuels combined with 8 % relative humidity produced extreme fire behaviour, including 100 m plus spotting. Powerlines crossing the river arc-flashed multiple times, starting secondary ignitions.',
'An interstate liaison established Unified Command between Oklahoma Forestry Services and Texas A&M Forest Service. A helicopter equipped with an ignition sphere dispenser conducted strategic backburns ahead of the main head fire to steer it into ploughed cotton fields. Type 6 engine strike teams patrolled river levees while National Guard Blackhawks performed bucket drops. A mobile air-quality lab tracked PM2.5 levels affecting a downwind elementary school, prompting early dismissal. Ranchers used tractors with disks to expand fire breaks, coordinated via radio patches with incident command. By 01:00 forward spread was stopped on both sides of the river.',
'2 Blackhawks; 1 PSD helicopter; 4 Type 6 engines; 3 tractors with disks; air-quality trailer',
'High',
'Escaped prescribed burn',
'Oklahoma FS; Texas A&M FS; National Guard',
'Red River, OK/TX, USA',
'28 C, 8 % RH, winds 30 km/h N',
'2025-04-09',
'11:10');

/* ---------- ROW 11 ---------- */
INSERT INTO wildfire_emergencies
(threat_name, threat_summary, steps_followed, resources, priority, cause,
 first_responders, location, weather, date_occurred, time_occurred)
VALUES
(
'Blue Mountain Remote Fire',
'Lightning struck an isolated juniper snag in Idaho’s Owyhee back-country during a dry-storm that produced zero rainfall. Because the ignition sat twelve kilometres from the nearest two-track, smoke was not reported until a ranch pilot radioed dispatch while moving cattle. By the time the call reached South Fork Dispatch, the fire had already run up a brush-covered draw and crested a rimrock bench, producing a convection column visible from the highway. Critical sage-grouse habitat and a historic stagecoach station lay directly down-wind. Afternoon instability, single-digit humidity and aligned slope-wind factors generated three-metre flame lengths and one-kilometre spotting, making direct attack initially unsafe for ground crews.',
'BLM activated the Remote Area Initial-Attack SOP. Two Type 3 helicopters inserted a four-person helirappel module to recon safe anchor points while Air Attack mapped heat with an IR sensor. The rappellers cold-trailed the heel and built an anchor, then directed two SEAT retardant drops to slow the right flank. A Type 4 engine escorted by UTVs followed a ranch road and installed a progressive hose lay supported by a portable pump drafting from a stock pond. Wildlife officers flagged sage-grouse leks and adjusted line placement to avoid disturbance. At last light the fire was 30 % contained; night operations used UAS with FLIR to catch long-range spots.',
'2 Type 3 helicopters; 2 SEATs; 1 Type 4 engine; 1 helirappel module; 2 UTVs; 1 portable pump',
'Moderate',
'Dry lightning',
'BLM Engine 112; Owyhee Rangeland Fire Protection Association; Idaho State Police',
'Owyhee Mountains, ID, USA',
'33 °C, 9 % RH, W winds 28 km/h',
'2025-06-15',
'14:55'
);

/* ---------- ROW 12 ---------- */
INSERT INTO wildfire_emergencies
(threat_name, threat_summary, steps_followed, resources, priority, cause,
 first_responders, location, weather, date_occurred, time_occurred)
VALUES
(
'Silver Valley Industrial Interface Fire',
'Sparks from an angle-grinder at a metal-scrap facility landed in adjacent cheatgrass during a heat wave in Nevada’s Silver Valley. The grass fire quickly impinged on stacked shipping containers full of solvents, releasing a dense black smoke plume that triggered multiple 911 calls and automatic gas-monitor alarms. The flame front then jumped a rail spur and began burning willow thickets along a seasonal drainage that funnels toward a neighborhood of manufactured homes. Power and fiber optics for the mine district run overhead along the same corridor, multiplying critical-infrastructure exposure.',
'The municipal fire chief declared a Unified Haz-Wildfire Response. A HazMat engine cooled hazardous-material containers with class B foam while brush units flanked the grass fire. Rail-company crash-rescue equipped with a foam cannon positioned at a switchyard to protect tank cars. Public-works graders pushed a sixty-metre dozed line tying into a gravel pit. A reverse-911 order prompted residents to evacuate to a community center where Red Cross set up air-purifying shelters. Drones with electro-optical and gas-sensing payloads mapped flammable vapor clouds and hottest terrain. By midnight all hotspots within thirty metres of containers were extinguished and responsibility transitioned to on-site industrial fire-watch.',
'1 HazMat engine; 3 Type 6 brush engines; 1 foam tender; 2 drones; 2 public-works graders',
'High',
'Hot-work sparks',
'Silver Valley FD; Industrial Brigade; Union Pacific Police',
'Silver Valley, NV, USA',
'40 °C, 7 % RH, gusts 22 km/h S',
'2025-08-09',
'13:18'
);

/* ---------- ROW 13 ---------- */
INSERT INTO wildfire_emergencies
(threat_name, threat_summary, steps_followed, resources, priority, cause,
 first_responders, location, weather, date_occurred, time_occurred)
VALUES
(
'Glacier Pass Crown Fire',
'An illegal campfire left smoldering above treeline in Montana’s Glacier Pass reignited beneath a chinook wind event. The fire crowned rapidly through beetle-killed lodgepole pine, throwing firebrands two kilometres ahead into wind-polished talus slopes. The sole access is a historic pack trail, and a commercial pack-string with nine clients was overnighting inside the projected spread. Dense smoke obstructed the only helicopter LZ, delaying extraction. The wind-driven column threatened to cross the Continental Divide crest and fall into a separate drainage feeding public water supply for a mountain town.',
'The Northern Rockies Coordination Center mobilized a Type 1 IMT and launched the Alpine Evacuation SOP. A rappel-capable helicopter inserted two smokejumpers at first light to cut a landing pad on a moraine. Once cleared, a Type 1 long-line helicopter short-hauled the pack-string clients to a safety meadow. Hotshots spiked out at the Divide and executed indirect handline tying into snowfields and rock outcrops while aerial ignitions with PSD spheres burned out fuels between the line and main column. A portable retardant plant at the ski-area parking lot reloaded VLATs, maximizing cycle efficiency. Water-supply managers opened sediment bypass gates downstream in anticipation of ash flow.',
'1 Type 1 IMT; 1 Type 1 helicopter; 1 rappel ship; 1 VLAT; 2 Hotshot crews; 2 smokejumpers; PSD kit',
'Critical',
'Unextinguished campfire',
'USFS IMT1; Flathead County SAR; MT DNRC',
'Glacier Pass, MT, USA',
'28 °C, 11 % RH, W winds 45 km/h',
'2025-07-29',
'06:30'
);

/* ---------- ROW 14 ---------- */
INSERT INTO wildfire_emergencies
(threat_name, threat_summary, steps_followed, resources, priority, cause,
 first_responders, location, weather, date_occurred, time_occurred)
VALUES
(
'Pan-Amazon Riverbank Fire',
'A subsistence farmer’s slash-and-burn clearing on a drought-stressed river terrace in Pará state, Brazil, escaped into secondary rainforest. The head fire paralleled the Xingu River, producing thick pyrocumulus clouds that forced suspension of regional air traffic. Indigenous villages downstream rely on river transport and smoke obscuration halted boat navigation. Biodiversity survey plots containing endangered mahogany seedlings were within three hours of projected spread. Regional carbon-flux monitoring stations recorded spikes, triggering international media attention.',
'IBAMA deployed the Amazon Task Force in accordance with the Integrated Fire Management Plan. Motorized canoes ferried brigadistas along the river to establish wet-line with backpack pumps and floatable bladder bags. An amphibious “Fire Boss” scooper cycled every five minutes off the river, laying foam-enhanced water on advancing fingers. Drone-based loudspeaker systems delivered evacuation messages in native Kayapó language. Environmental NGOs set up camera traps ahead of the flank to monitor wildlife escape routes. A mobile weather-station network fed real-time data to the SIM-Queimadas modelling platform, guiding priorities for back-burn operations upriver. After three days and fifty millimetres of pump-and-roll, perimeter was secured.',
'1 Fire Boss aircraft; 4 riverine pump crews; 12 backpack pumps; drone loudspeaker system; mobile weather net',
'High',
'Escaped agricultural burn',
'IBAMA PrevFogo; Pará Military Fire Brigade; Kayapó Village Guards',
'Xingu River, Pará, Brazil',
'35 °C, 18 % RH, E winds 16 km/h',
'2025-09-04',
'10:05'
);

/* ---------- ROW 15 ---------- */
INSERT INTO wildfire_emergencies
(threat_name, threat_summary, steps_followed, resources, priority, cause,
 first_responders, location, weather, date_occurred, time_occurred)
VALUES
(
'Rhinewald Tunnel Fire',
'Grinding sparks from track maintenance ignited dry grass along the Swiss-Italian border near the 1 km long Rhinewald rail tunnel. The flames climbed the steep south portal embankment and began torching larch trees situated above the tunnel ventilation shaft. Heated air and embers were drawn into the shaft, tripping smoke detectors inside the tunnel and forcing an emergency stop of a northbound freight train carrying ethanol. Alpine Föhn winds risked lofting embers over the crest toward the village of Splügen.',
'The Canton Graubünden Alarmplan for “Tunnel-Waldbrand” was activated. Railway fire-suppression wagons pre-positioned inside the tunnel discharged CAFS through hydrants to prevent internal spread. Outside, the volunteer Bergfeuerwehr established hose lays anchored to hydrants at each portal while a contract helicopter performed Bambi-bucket drops sourced from the Hinterrhein. The civil-protection service issued cell-broadcast alerts instructing residents to close windows against smoke. Alpine Rescue teams roped in sawyers to fell snags threatening the ventilation stack. Swiss Federal Railways engineers staged thermal cameras along the tunnel roof to detect heat transfer. Containment was achieved within twelve hours, allowing rail traffic to resume with speed restrictions.',
'1 rail fire wagon; 4 CAFS engines; 1 helicopter with 900 L bucket; Alpine Rescue saw team; thermal-cam crew',
'Moderate',
'Sparks from rail grinder',
'Bergfeuerwehr Splügen; SBB Fire Service; Civil Protection GR',
'Splügen, Graubünden, Switzerland',
'23 °C, 14 % RH, Föhn winds 35 km/h',
'2025-05-11',
'02:47'
);

/* ---------- ROW 16 ---------- */
INSERT INTO wildfire_emergencies
(threat_name, threat_summary, steps_followed, resources, priority, cause,
 first_responders, location, weather, date_occurred, time_occurred)
VALUES
(
'Kansai Hillside Fire',
'A municipal green-waste burn near Kyoto’s western hills flared when a gust front arrived ahead of Typhoon Akari, scattering embers into bamboo thickets. The fire ascended a pilgrimage trail used by hundreds of tourists each day and threatened wooden Shinto shrines dating back to the Heian period. Steep stone steps, narrow alleys, and overhead electrical wires complicated engine access. Simultaneous typhoon evacuation traffic clogged arterial roads, delaying additional resources.',
'Kyoto City Fire Department invoked the Historic-Structure Protection SOP. Portable high-pressure pumps drafted from koi ponds to supply sprinkler rings installed around shrine roofs treated with traditional cypress bark. Volunteer bucket brigades from local temple associations assisted with hose advancement up the steps. A Prefectural Police drone relayed infrared video to a mobile command post parked outside the torii gate. The Forestry Agency inserted a chain-saw team via cable-car to create a three-metre wide mineral soil break along a ridgeline. As typhoon rain bands arrived six hours later, crews leveraged wetting conditions to secure the perimeter and transitioned to salvage and overhaul.',
'5 pumpers; 1 portable pump set; community bucket brigade; drone recon; Forestry saw team',
'High',
'Escaped green-waste burn',
'Kyoto CFD; Prefectural Police; Forestry Agency',
'Arashiyama Hills, Kyoto, Japan',
'31 °C, 17 % RH, gusts 40 km/h S',
'2025-09-22',
'14:12'
);

/* ---------- ROW 17 ---------- */
INSERT INTO wildfire_emergencies
(threat_name, threat_summary, steps_followed, resources, priority, cause,
 first_responders, location, weather, date_occurred, time_occurred)
VALUES
(
'Patagonia Steppe Fire',
'A hunter’s idling four-wheel-drive overheated and expelled flaming carbon particles through the exhaust, igniting feather grass on Argentina’s Santa Cruz steppe. The flat terrain but strong westerlies created a fast-moving linear head fire that threatened high-voltage transmission towers supplying the Cerro Viento wind-farm. Guanaco herds fled toward Highway 40, causing multiple vehicle collisions in heavy smoke. Limited water sources forced firefighters to rely on tanker shuttle from a distant estancia windmill.',
'The Servicio Nacional de Manejo del Fuego dispatched an air-tractor scooper and a modular “brigada forestal” with slip-on units. Two road-graders from Vialidad Nacional executed parallel bladed breaks 100 m apart, enabling ignition crews to back-burn off the leeward line. The wind-farm operator engaged its private brigade to foam the bases of turbine towers and remotely feathered blades to reduce mechanical ignition risk. Highway patrol implemented rolling closures and guided motorists to a pre-identified smoke-safe refuge. By the second operational period, flanking lines held and mop-up teams applied gel retardant to residual peat patches near riparian corridors.',
'1 Air-tractor; 3 slip-on trucks; 2 graders; wind-farm brigade; gel retardant unit',
'Moderate',
'Vehicle exhaust sparks',
'SNMF Brigada South; Wind-farm ER Team; Gendarmería Nacional',
'Santa Cruz Province, Argentina',
'26 °C, 12 % RH, W winds 55 km/h',
'2025-11-03',
'11:58'
);

/* ---------- ROW 18 ---------- */
INSERT INTO wildfire_emergencies
(threat_name, threat_summary, steps_followed, resources, priority, cause,
 first_responders, location, weather, date_occurred, time_occurred)
VALUES
(
'Siberian Taiga Peat-Crown Complex',
'A derecho storm toppled electricity pylons in Irkutsk Oblast, sending live wires onto desiccated peat. The resulting ground fire smoldered for ten days before flaring into adjacent larch forest under record heat. Once surface flames reached the canopy, crowning rates exceeded two kilometres per hour. Smoke advected into the city of Bratsk, raising PM2.5 concentrations above 500 µg/m³ and grounding commercial flights. Critical gas pipelines ran three kilometres north of the ignition zone.',
'EMERCOM executed the Federal Wildfire-Peat Unified Plan. An Il-76 tanker aircraft dropped 42 tons of water on the most active crown run while ground crews trenched peat layers to mineral soil using amphibious tracked excavators. Portable pumps relayed water from the Angara River through four kilometres of hose, supplemented by a high-pressure rail-pump wagon on a siding. Satellite hotspot data from “Suomi-NPP” fed into the LES-2 decision-support platform, updating evacuation triggers for nearby dachas. Pipeline operators depressurised sections and sprayed suppressant foam over valves. After a week, rainfall and continuous flooding reduced deep-seated heat and agencies transitioned to patrol status.',
'1 Il-76 tanker; 4 amphibious excavators; 6 portable pumps; rail-pump wagon; satellite data link',
'Critical',
'Downed powerline on peat',
'EMERCOM; Avialesookhrana; Transneft Pipeline Fire Team',
'Irkutsk Oblast, Russia',
'30 °C, 8 % RH, SW winds 25 km/h',
'2025-07-07',
'08:20'
);

/* ---------- ROW 19 ---------- */
INSERT INTO wildfire_emergencies
(threat_name, threat_summary, steps_followed, resources, priority, cause,
 first_responders, location, weather, date_occurred, time_occurred)
VALUES
(
'Athens Coastal Pine Fire',
'A carelessly discarded cigarette on a suburban Athens beach ignited pine needles piled against seawall rocks. The flame spread upslope through Aleppo pine into a hillside subdivision where unpermitted roof decks and plastic pergolas accelerated fire growth. Holiday traffic gridlock on Poseidonos Avenue hampered engine access while onshore breezes funneled embers inland toward an archaeological park containing fifth-century ruins. Beaches packed with tourists complicated evacuation messaging.',
'The Hellenic Fire Service initiated the Attica WUI Action Protocol. Aerial priority was given to two CL-415 scoopers cycling from the Saronic Gulf. On the ground, municipal brigades executed the “box and burn” tactic, driving dozers to punch line above the subdivision while voluntary civil-protection groups cleared gutters and brushed-roof balconies. Coast Guard patrol boats broadcast multilingual evacuation notices via loud-hailer and used inflatable ribs to shuttle beachgoers to a marina refuge. Culture Ministry archaeologists wrapped marble columns in fire-resistant blankets and positioned sprinkler kits fed by tanker shuttle. Within sixteen hours the coastal flank was contained; mop-up focused on smouldering deck materials.',
'2 CL-415s; 5 municipal pumpers; 2 dozers; Coast Guard patrol; archaeological sprinkler kits',
'High',
'Discarded cigarette',
'Hellenic Fire Service; Coast Guard; Civil Protection Greece',
'Vouliagmeni, Athens, Greece',
'36 °C, 13 % RH, sea breeze 30 km/h',
'2025-08-18',
'15:26'
);

/* ---------- ROW 20 ---------- */
INSERT INTO wildfire_emergencies
(threat_name, threat_summary, steps_followed, resources, priority, cause,
 first_responders, location, weather, date_occurred, time_occurred)
VALUES
(
'Caldera de Taburiente Rim Fire',
'On La Palma, Canary Islands, a glass bottle left by hikers focused sunlight onto dry pine duff along the rim trail of the Caldera de Taburiente National Park. The ignition sat atop near-vertical cliffs, making ground approach hazardous. High winds from an African calima event carried embers across drainages toward a solar-observatory complex at Roque de los Muchachos. Ash fall threatened telescope mirror integrity worth hundreds of millions of euros. Concurrent airline traffic was alerted to a towering smoke column adjacent to flight corridors serving Tenerife and Gran Canaria.',
'The Cabildo de La Palma activated the “INFOPAL” Level 2 plan, requesting state air assets. Two Kamov Ka-32 helicopters with 4 500 L buckets sourced seawater while a coordinated rappel crew secured anchor points on the cliff edge using rock-climbing anchors. Parque Nacional staff implemented a “defensive observation dome” strategy: aluminium foil wraps and portable sprinklers protected telescope domes, coupled with positive-pressure HVAC to keep ash out. The Guardia Civil Montaña unit closed all trails and performed rope-assisted evacuations. Remote-controlled ignition spheres were launched from a drone to burn out inaccessible ledges below the rim. By the third operational period, cooler marine air and bucket saturation sealed remaining hotspots.',
'2 Ka-32 helicopters; rappel crew; drone PSD unit; observatory sprinkler cache; Guardia Civil Montaña',
'High',
'Sunlight concentrated by glass bottle',
'INFOCA; Cabildo de La Palma; Guardia Civil',
'La Palma, Canary Islands, Spain',
'33 °C, 12 % RH, calima winds 45 km/h E',
'2025-10-07',
'12:02'
);

