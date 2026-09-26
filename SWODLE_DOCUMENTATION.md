# SWODLE / SWORDS — Software Documentation & User Guide

> SWODLE is a multiplayer, browser-based naval
> surface warfare simulation. Teams of students each run one ship's watch stations (Bridge, JOOD,
> Contact Manager, CIC and Intel). An instructor (Staff) and a squadron commander (DESCON) oversee
> the exercise. The builds and the in-game title use the name **SWORDS**.

| | |
|---|---|
| **Engine** | Unity 6 (`6000.6.3f1`) |
| **Platform** | WebGL (runs in the browser), plus the Unity Editor for development |
| **Networking (current)** | Photon PUN 2.42 (Photon Cloud) |
| **Networking (planned)** | Custom C WebSocket server on a VPS. See [`Server/SERVER_SPEC.md`](../Server/SERVER_SPEC.md) |
| **Scenario data** | AWS API Gateway (`GetContactsBySetID`) with a Firebase user ID |
| **Known issues** | [`Docs/BUGS.md`](BUGS.md) |

---

## Contents

1. [Quick Start for Instructors](#1-quick-start-for-instructors)
2. [User Guide by Station](#2-user-guide-by-station)
3. [Game Rules Reference](#3-game-rules-reference)
4. [System Architecture](#4-system-architecture)
5. [Scenes & Application Flow](#5-scenes--application-flow)
6. [Script Reference](#6-script-reference)
7. [Data Formats](#7-data-formats)
8. [Network Message Reference (Legacy / Photon)](#8-network-message-reference-legacy--photon)
9. [Network Protocol (Planned Server)](#9-network-protocol-planned-server)
10. [Building & Deploying](#10-building--deploying)
11. [Troubleshooting](#11-troubleshooting)
12. [Glossary](#12-glossary)

---

## 1. Quick Start for Instructors

**Before class**
1. Build the scenario (the contact set) on the SWODLE website and note its **Set ID**.
2. Decide on the operating area's corner coordinates: top-left and bottom-right, in `D M'S"` format.
3. Decide which ships are in play. Players choose ships **0–4**. Each friendly contact in the
   scenario becomes a player ship, and its contact number is the ship ID.

**Starting an exercise.** Order matters with the current Photon build.

| Step | Who | Action |
|---|---|---|
| 1 | Staff | Open the game URL. At the lobby, type a room name and press **Create**. |
| 2 | Staff | On the start screen, enter the Staff password and press **Staff**. |
| 3 | Staff | Enter the **Set ID** and press **Enter Code**. The code indicator turns green. |
| 4 | Staff | Enter the four corner coordinates and press **Set Cords**. The coordinate indicator turns green. |
| 5 | Staff | Press the Staff start button. Player ships spawn and the Staff dashboard opens. |
| 6 | Students | Open the URL, type the **same room name**, and press **Join**. Pick your ship, then your screen. |
| 7 | DESCON | Join the room, enter the DESCON password, and press **DESCON**. |
| 8 | Staff | When the Staff grid shows every station green, press **Start**. The clock starts and contacts begin spawning. |

> ⚠ **Current build:** students must join **after** Staff completes step 4. Players read the
> map coordinates when they join the room. If Staff leaves or drops, the exercise ends for everyone.
> Both problems go away with the planned server.

---

## 2. User Guide by Station

Every player first selects a **ship** and then a **screen**. The top of the screen shows your
ship and station. The clock at the top shows exercise time (`HH:MM:SS`, starting at 00:00:00).

### 2.1 Bridge (Commanding Officer / OOD)
The Bridge controls the ship and approves weapons release.

| Task | How |
|---|---|
| **Look around** | Hold the on-screen turn buttons, or use **← →** (pan) and **↑ ↓** (tilt). |
| **Change course/speed** | Enter **Heading** (0–359° true) and **Speed** (knots, maximum 25), then press the course button. The order goes to Staff and takes effect for everyone. |
| **Submit a position fix** | Enter your calculated **Lat** and **Long** in `D M'S"` format (for example `11 02'10"`), then submit. |
| **Approve a firing solution** | When CIC sends a solution, a popup lists the contact and the rounds per weapon. Press **Fire** to shoot, or **Deny** to reject it and tell CIC. |
| **Message CIC** | Type in the message box and press send. |

**Navigation checks:** Every **5 minutes** of exercise time, the Bridge must have submitted a
position fix since the last check. A missing or inaccurate fix costs **−5 points**, and the
correct position is then shown on screen.

### 2.2 JOOD (Junior Officer of the Deck)
JOOD is a **read-only** situational log. It shows:
- contact reports from Contact Manager
- firing solutions from CIC
- messages sent to the Bridge

The newest message is at the top.

### 2.3 Contact Manager (Radar)
Contact Manager shows a radar display centered on your ship, with contacts within sensor range
drawn as vectors. Your own ship is **white**.

1. **Click a contact** to see its number, lat/lon, heading, speed and type.
2. Fill in the report fields: **Type, Speed, Heading, Lat, Lon**. These are your own
   assessments, and you are graded on reporting, so the game does not auto-fill them.
3. Press **Send** to forward the report to CIC, JOOD and TAO.

### 2.4 CIC (Combat Information Center)
CIC builds firing solutions.

1. Enter the target's **contact number** and press set.
2. Use **+ / −** on each weapon to choose rounds. *Shots Left* shows the remaining magazine.
3. Press **Send Firing Solution**. It goes to the Bridge for approval.
4. The two message panels show traffic from the **Bridge** and incoming contact reports.

Weapons depend on your ship class (see [§3.1](#31-ship-classes--magazines)).

### 2.5 Intel
- **E-2 Hawkeye** and **Reaper Drone** searches: enter a contact number and choose an asset to
  get that contact's intelligence report and image. Each asset has **10 uses**.
- **Intel feed:** a new intelligence message arrives every **5 minutes**.

### 2.6 DESCON (Squadron Commander)
DESCON sees the **whole operating area**. It is password protected.

| Task | How |
|---|---|
| View any contact | Click its vector to see number, speed, bearing, lat/lon and type. |
| Color-tag contacts | Select a contact, then pick one of five colors. Tags are local to your screen. Friendly contacts default to green, others to blue. |
| Maneuver the carrier | Enter heading and speed and press update. *(Known issue: this currently has no effect. See BUGS B07.)* |
| Intel | The **Intel** button opens the Intel screen. |

### 2.7 Staff (Instructor)
Staff runs the exercise. It is password protected.

- **Setup:** Set ID and coordinates (see [§1](#1-quick-start-for-instructors)).
- **Screen status grid:** one row per ship and one column per station (Bridge, JOOD, Contact,
  CIC, and the fifth screen). Red means nobody has joined; green means someone has.
- **Scores:** a running score per ship.
- **Fire log:** every shot fired, with its solution and damage, newest first.
- **Start:** starts the clock and the contact timeline.

---

## 3. Game Rules Reference

### 3.1 Ship Classes & Magazines

| Ship ID | Class | Slot 0 | Slot 1 | Slot 2 |
|---|---|---|---|---|
| 0 | Cruiser (CG) | 5-inch gun ×600 | CIWS ×5 | SAM ×50 |
| 1, 2 | Destroyer (DDG) | SAM ×600 | Tomahawk ×90 | Torpedo ×10 |
| 3 | *undefined (see BUGS B15)* | — | — | — |
| 4 | Littoral Combat Ship (LCS) | Machine gun ×15 | RAM ×50 | Torpedo ×10 |

### 3.2 Weapon Effectiveness

A round fired at a target type its weapon cannot engage does **no damage**.

| Weapon | Effective against |
|---|---|
| 5-inch / main gun | DDGs, cargo, carriers, FAC, shore battery, civilian |
| SAM | Aircraft, drones, missiles, helicopters |
| Tomahawk | Everything that the main gun or SAM can hit |
| Torpedo | DDGs, cargo, carriers, submarines |
| CIWS | Aircraft (enemy), drones, missiles, helicopters |
| Machine gun | Cargo, civilian, FAC |
| RAM | Aircraft, drones, missiles, helicopters |

### 3.3 Damage
- Every contact starts with **1000 health**.
- Each round does `base × random(0.5 – 1.0)`. Base is **250** for slot 0 and **500** for slots 1–2.
- At 0 health the contact is destroyed and removed from every screen.

### 3.4 Scoring
| Event | Points |
|---|---|
| Missed or inaccurate 5-minute navigation fix | −5 |

### 3.5 Contact Types

| ID | Type | Scenario `type` keyword |
|---|---|---|
| 0 | Friendly DDG | `Friendly` |
| 1 | Friendly carrier | `FriendlyCarrier` |
| 2 | Submarine | `Sub` |
| 3 | Cargo | `Cargo` |
| 4 | Russian carrier | `RussianCarrier` |
| 5 | Russian aircraft | `EnemyPlane` |
| 6 | Russian DDG | `RussianDDG` |
| 7 | Iranian DDG | `IranDDG` |
| 8 | Fast attack craft | `FAC` |
| 9 | Drone | `Drone` |
| 10 | Shore battery | `Battery` |
| 11 | Helicopter | `Helio` |
| 12 | Missile | `Missile` |
| 13 | Aircraft | `Plane` |
| 14 | Civilian (random model) | `Random` |

---

## 4. System Architecture

### 4.1 Current (Photon)

```
                 Photon Cloud (relay)
   ┌──────────────────┼───────────────────────────┐
   │                  │                           │
 STAFF client      Student clients            DESCON client
 (Master Client)   Bridge/JOOD/Contact/CIC/Intel
 - owns all entities (PhotonNetwork.Instantiate)
 - streams transforms (PhotonTransformView)
 - runs the clock (RPC every second)
 - applies damage, scores, spawns
```

- **All authority lives on the Staff client.** Other clients display what Staff sends.
- Game messages go through one buffered RPC as comma-separated strings (see [§8](#8-network-message-reference-legacy--photon)).
- Ship positions are streamed continuously by Photon's transform sync.

### 4.2 Planned (Custom Server)

```
 Browser clients ──wss:// (443)──▶ Caddy (TLS) ──▶ swodle-server (C, VPS) ──▶ room snapshots on disk
```

- The server owns entities, the clock, combat, scoring and nav checks.
- Clients send commands and **dead-reckon** motion locally from each entity's position, heading,
  speed and timestamp. The server sends updates only when something changes, plus a sync every 5 s.
- Any client can drop and **resume automatically**, including Staff.
- Full spec: [`Server/SERVER_SPEC.md`](../Server/SERVER_SPEC.md).

---

## 5. Scenes & Application Flow

Build Settings order:

| # | Scene | Purpose | Key scripts |
|---|---|---|---|
| 0 | `LoadingScene` | Connects to Photon and joins the lobby | `ConnectToServer` |
| 1 | `Lobby` | Create or join a room by name | `CreateAndJoinRooms` |
| 2 | `MainOcean` | The whole game: start screen, every station canvas, and the 3D ocean | `GameController` and all station controllers |

Not in the build: `MainOcean 1`, `StartScreen` (an old prototype) and `Website` (account/purchase pages).

```
LoadingScene ──ConnectUsingSettings──▶ JoinLobby ──▶ Lobby
Lobby ──Create/Join room──▶ (read op-area room properties) ──LoadLevel──▶ MainOcean
MainOcean StartScreenCanvas
   ├─ Ship 0–4 ─▶ Screen select (Bridge=2, JOOD=3, Contact=4, CIC=5, Intel=6) ─▶ station canvas
   ├─ DESCON (password) ─▶ DESCONCanvas
   └─ Staff  (password) ─▶ Staff setup ─▶ Staff dashboard
```

**Station canvases (`GameController.canvi`).** Index = `ScreenType + 1`:

| Index | Canvas | ScreenType |
|---|---|---|
| 0 | StartScreenCanvas | — |
| 1 | DESCONCanvas | DESCON (0) |
| 2 | Staff canvas | STAFF (1) |
| 3 | BridgeCanvas | BRIDGE (2) |
| 4 | JODCanvas | JOOD (3) |
| 5 | ContactManagerCanvas | Contact (4) |
| 6 | CICCanvas | CIC (5) |
| 7 | IntelCanvas | INTEL (6) |

`ScreenType.TAO` (7) has no canvas. See BUGS B26.

---

## 6. Script Reference

All game code is in `Assets/Scripts/`.

### 6.1 Core

| Script | Responsibility |
|---|---|
| `Controllers/GameController.cs` | Singleton. Holds the player's `shipID`, `screenID` and `gameType`. Switches canvases. **Sends and routes every game message** (`sendMessage` → buffered RPC → message queue → dispatch in `Update`). Defines the `ScreenType` and `ShipName` enums. |
| `Controllers/StartScreenControl.cs` | Ship, screen, DESCON and Staff selection buttons. Checks the DESCON/Staff passwords. |
| `Ships/Entity.cs` | A networked ship or contact. Holds type, speed, heading and health (health only matters on Staff). Moves forward each frame once the game starts. Activates the child model for its type. Defines the `EntityType` enum. |
| `Ships/FleetControl.cs` | Spawns the player ships (friendly contacts) as `Ship<number>`. |
| `Ships/Missile.cs` | Missile visual (launch, then home on target). Currently unused. |
| `Contacts/MainCollider.cs` | Sensor trigger sphere attached to your ship. Keeps the list of contacts in range for radar. |

### 6.2 Stations

| Script | Station | Sends | Receives |
|---|---|---|---|
| `StaffController.cs` | Staff | 8, 9, 10 | 0, 4, 5, 12 |
| `BridgeController.cs` | Bridge | 3, 4, 5, 6, 12 | 2 |
| `JOODController.cs` | JOOD | — | 1, 2, 3 |
| `ContactManagerController.cs` | Contact | 1 | — |
| `CICController.cs` | CIC | 2 | 1, 3, 6 |
| `IntelController.cs` | Intel | — | 10 (start message timer) |
| `TAOController.cs` | TAO (unreachable) | 3 | 1, 2, 3 |
| `DESCONController.cs` | DESCON | 12 | — (reads entities directly) |

### 6.3 World, Setup & UI

| Script | Responsibility |
|---|---|
| `RealWorld/LatLonControl.cs` | Converts between lat/lon (DMS strings) and Unity world coordinates, using three corner markers (NW, NE, SW) and the op-area corners. Also converts knots to Unity units per second. |
| `RealWorld/ClockManager.cs` | Staff-side clock coroutine. Broadcasts time every second and flags a Bridge nav check every 5 minutes. |
| `RealWorld/Clock.cs` | Displays the time. |
| `Staff Control/StaffSetup.cs` | Staff setup panel: op-area coordinates (published as room properties) and the start button. |
| `Staff Control/DatabaseManager.cs` | Fetches the contact set from AWS, splits out friendlies and sorts by start time. Defines `Contact`. |
| `Staff Control/AuthManager.cs` | Gets the Firebase user UUID from the hosting web page (WebGL JS interop). |
| `Photon/ConnectToServer.cs` | Connects to Photon and loads the Lobby. |
| `Photon/CreateAndJoinRooms.cs` | Room create/join. Copies op-area room properties into `PlayerPrefs`. |
| `Photon/OnlineIndicator.cs` | Shows the disconnected state. |
| `UI/Vector.cs` | Data holder for a radar/plot vector (ship, speed, heading, type). |
| `UI/ShipLabel.cs` | Shows ship and station on screen. |
| `UI/TurnButton.cs` | Hold-to-press button (Bridge camera turn). |
| `Website/*` | Unity Authentication account, password rules and purchase pages. Not part of the game build. |

---

## 7. Data Formats

### 7.1 Coordinates (DMS strings)
Format: `D M'S"`. There is a space between degrees and minutes, then `'` and `"`. Examples:
`11 45'00"` and `67 50'00"`.
The current parser needs integers in every field and has no hemisphere support (north/east
assumed). See BUGS B22.

### 7.2 Operating Area
Four corners, set by Staff and stored as Photon room properties and `PlayerPrefs`:

| Key | Meaning |
|---|---|
| `tlLat` | Top-left (NW) latitude |
| `tlLon` | Top-left (NW) longitude |
| `brLat` | Bottom-right (SE) latitude |
| `brLon` | Bottom-right (SE) longitude |

Editor default: `11 45'00"`, `67 50'00"` → `10 35'00"`, `65 55'00"`.

### 7.3 Contact Set (AWS API)
`GET https://…/GetContactsBySetID?uuid=<firebaseUid>&setId=<setId>` returns:

```json
{
  "count": 2,
  "contacts": [
    { "number": 1, "type": "Friendly", "latStr": "11 20'00\"", "lonStr": "66 10'00\"",
      "lat": 11.333, "lon": 66.166, "speed": 15, "heading": 90, "startTime": "00:00",
      "weapon": "", "setId": "ABC", "UserID": "…", "ContactID": 17, "id": 17, "updatedAt": "…" },
    { "number": 1047, "type": "Cargo", "latStr": "11 00'00\"", "lonStr": "66 40'00\"",
      "speed": 12, "heading": 45, "startTime": "00:05", "weapon": "" }
  ]
}
```

| Field | Use |
|---|---|
| `number` | Contact number players reference. For `Friendly` contacts it is also the **ship ID** (0–4). |
| `type` | Mapped to `EntityType` by keyword (see [§3.5](#35-contact-types)). Order matters: `EnemyPlane` is checked before `Plane`, and `FriendlyCarrier` before `Friendly`. |
| `latStr` / `lonStr` | Spawn position (DMS). |
| `speed` / `heading` | Knots / degrees true. |
| `startTime` | `HH:MM` exercise time at which the contact appears. |

---

## 8. Network Message Reference (Legacy / Photon)

### 8.1 Photon RPCs

| RPC | On | Target | Arguments | Purpose |
|---|---|---|---|---|
| `sendServerMessage` | `GameController` | AllBuffered | `string message` | Carries every game message in §8.2 |
| `setHeadingSpeed` | `Entity` | All | `int heading, int speed` | Course/speed change (applied on Staff) |
| `RPC_ChangeGroundName` | `Entity` | All | `string name` | Sync the GameObject name |
| `RPC_setEntity` | `Entity` | All | `"speed,heading,type,variant,name"` | Sync type, model and speed |
| `setCurrentClock` | `ClockManager` | All | `string time, bool checkBridge` | Clock tick every second, plus the 5-minute nav check flag |

Room custom properties: `tlLat`, `tlLon`, `brLat`, `brLon` (see [§7.2](#72-operating-area)).
Transform sync: `PhotonTransformView` on `Resources/Entity.prefab` (position and rotation).

### 8.2 Game Message Format

```
<senderShipID>,<senderScreenID>,<msgType>,<payload…>
```

`GameController.sendMessage(payload)` prepends the header. Screen IDs: 0 DESCON/Staff,
2 Bridge, 3 JOOD, 4 Contact, 5 CIC, 6 Intel.

**Routing** (`GameController.Update`):
1. Types **7, 8, 9, 10** are handled globally first. Each client acts on them itself.
2. Otherwise a client handles the message if **(sender ship == my ship AND sender screen ≠ my
   screen)** or **I am Staff**.
3. The message is then passed to the controller for the *receiving* client's screen.

### 8.3 Message Codes

| Code | Name | Sender | Payload | Handled by | Example (full string) |
|---|---|---|---|---|---|
| **0** | Screen online | Any station (on selection) | `shipID,screenID,1` | Staff → marks grid cell green | `1,2,0,1,2,1` |
| **1** | Contact report | Contact | `type,speed,heading,lat,lon,contactName` | CIC, JOOD, TAO (display) | `1,4,1,Cargo,12,045,11 00'00",66 40'00",1047` |
| **2** | Firing solution | CIC | `contactNumber,shipClass,rounds0,rounds1,rounds2` | Bridge (popup), JOOD, TAO | `1,5,2,1047,0,0,2,0` |
| **3** | Text message | Bridge, TAO | `text,recipientFlag` (0 = CIC, 1 = Bridge/JOOD) | CIC (flag 0), JOOD (flag 1), TAO | `1,2,3,Turning to 270,0` |
| **4** | Score change | Bridge | `shipID,delta` | Staff → `scores[ship] += delta` | `1,2,4,1,-5` |
| **5** | Shot fired | Bridge | `logText,damage,targetName` | Staff → fire log, apply damage, destroy at ≤0 | `1,2,5,Ship 1 has fired…,812.4,1047` |
| **6** | Solution denied / return ammo | Bridge | `a:b:c:d` | CIC → adds rounds back | `1,2,6,0:2:0:0` |
| **7** | Spawn entity | Staff | `name,x:y:z,type,y,speed,heading,variant` | All clients → set up the matching entity | `0,0,7,1047,512.3:0:-88.1,3,65,12,45,0` |
| **8** | Entity name list | Staff | `name1,name2,…` | All clients (once) | `0,0,8,Ship0,Ship1,1047` |
| **9** | Entity type list | Staff | `type1,type2,…` | All clients (once) | `0,0,9,0,0,3` |
| **10** | Start exercise | Staff | *(none)* | All; Intel starts its message timer | `0,0,10` |
| **12** | Course/speed order | Bridge, DESCON | `ship\|DESRON,heading,speed` | Staff → `Entity.setHeadingSpeed` | `1,2,12,1,270,15` |

> Codes 11 and 13+ are unused.
> ⚠ User text containing commas breaks this format. See BUGS B02/B03.

---

## 9. Network Protocol (Planned Server)

The replacement uses JSON over secure WebSocket. Each message has a `t` (type) field. The full
reference is in [`Server/SERVER_SPEC.md` §8](../Server/SERVER_SPEC.md#8-wire-protocol-json-over-websocket).
Mapping from the legacy codes:

| Legacy | New (client → server) | New (server → client) |
|---|---|---|
| 0 | `hello` | `welcome`, `snapshot`, `roster` |
| 1 | `contact_report` | `contact_report` |
| 2 | `fire_propose` | `fire_solution` |
| 3 | `chat` | `chat` |
| 4 | *(server-computed)* / `score_adjust` | `score` |
| 5 | `fire_decide{accept:true}` | `fire_result`, `entity_damage`, `entity_remove` |
| 6 | `fire_decide{accept:false}` | `fire_denied`, `ammo` |
| 7, 8, 9 | `spawn_entity` (Staff) / `scenario_load` | `entity_spawn`, `snapshot` |
| 10 | `sim_control{start}` | `sim_state` |
| 12 | `set_course` | `entity_update` |
| clock RPC | `ping` | `pong`, `sim_state`, `sync` |
| nav check | `nav_fix` | `nav_check`, `nav_result` |

---

## 10. Building & Deploying

### 10.1 Client (WebGL)
1. Open the project in **Unity 6000.6.3f1**.
2. **File → Build Settings → WebGL**. Scenes: `LoadingScene`, `Lobby`, `MainOcean` (in that order).
3. Build. The output folder contains `index.html`, `Build/` (`.data`, `.wasm`, `.framework.js`,
   `.loader.js`) and `TemplateData/`. Past builds are archived as `Build/SWORDS-<version>.zip`.
4. Host the folder on a static web server. The hosting page must provide `GetFirebaseUser()` and
   call `OnRecieveUUID` on the `AuthManager` object, so Staff can load contact sets.
   - If compression is on, the server must send the correct `Content-Encoding` for `.gz`/`.br` files.

### 10.2 Photon (current)
Photon App ID and region settings: `Assets/Photon/PhotonUnityNetworking/Resources/PhotonServerSettings.asset`.

### 10.3 Game Server & Website Hosting
Live on orthanc-industries.com (nginx + the `swodle` systemd service). How to run an exercise,
ship a new build or server update, and troubleshoot: [`DEPLOYMENT.md`](DEPLOYMENT.md).

---

## 11. Troubleshooting

| Symptom | Likely cause | What to do |
|---|---|---|
| Everything disappears mid-exercise | Staff's connection dropped (B01) | Staff re-creates the room and everyone rejoins. The planned server fixes this. |
| A screen stops updating but the clock still runs | A bad message jammed the queue (B02), often a message with a comma (B03) | Reload that screen. Avoid commas in messages. |
| Positions or lat/lon look wrong for students but right for Staff | Joined before Staff set coordinates, or the SE longitude bug (B10) | Staff sets coordinates first, then students reload and rejoin. |
| Radar centered on the wrong ship | Ship lookup mismatch (B05) | Known bug. Use the Bridge view to confirm your own position. |
| CIC screen blank or broken on ship 3 | No class defined for ship 3 (B15) | Use ships 0, 1, 2 or 4. |
| Deny doesn't return rounds to CIC | B08 | Known bug. Staff can note it. |
| DESCON course change does nothing | B07 | Known bug. |
| Staff code indicator never turns green | Bad Set ID, not logged in on the website, or network | Check the browser console for the AWS error. |
| Red "COMMS ARE OFFLINE" / "YOU ARE OFFLINE" | Disconnected from Photon | Reload and rejoin the same room. The planned server reconnects automatically. |

The full list is in [`Docs/BUGS.md`](BUGS.md).

---

## 12. Glossary

| Term | Meaning |
|---|---|
| **Bridge** | Ship's control station. The CO/OOD drives the ship and approves weapons release. |
| **CIC** | Combat Information Center. Builds firing solutions. |
| **CIWS** | Close-In Weapon System. Last-ditch anti-air/anti-missile gun. |
| **Contact** | Any tracked surface, subsurface or air object, identified by a contact number. |
| **DDG** | Guided-missile destroyer. |
| **CG** | Guided-missile cruiser. |
| **LCS** | Littoral Combat Ship. |
| **DESCON / DESRON** | Destroyer Squadron commander. Oversees all ships and the carrier. |
| **DMS** | Degrees-minutes-seconds coordinate format. |
| **FAC** | Fast Attack Craft. |
| **JOOD** | Junior Officer of the Deck. |
| **Nav fix** | A position the Bridge calculates and submits, graded against true position. |
| **RAM** | Rolling Airframe Missile. Short-range anti-air. |
| **SAM** | Surface-to-Air Missile. |
| **Set ID** | Identifier of a scenario (contact set) built on the SWODLE website. |
| **Staff** | Instructor/exercise controller. |
| **TAO** | Tactical Action Officer (station exists in code but is not reachable). |
| **Tomahawk** | Long-range land-attack/anti-ship cruise missile. |
