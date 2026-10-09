# RWAL defect ledger

| ID | Status | Evidence / limit |
|---|---|---|
| L01 | Implemented; runtime unverified | Three enemy classes now award differentiated loot on destruction |
| L02 | Implemented; runtime unverified | Caches spawn at destruction point, drift, expire and collect on proximity |
| L03 | Implemented; runtime unverified | Inventory and per-ship upgrades persist via localStorage |
| L04 | Implemented; runtime unverified | Upgrade recipes scale with level, limited to 5 |
| L05 | Implemented; runtime unverified | Shield/hull capacities and fire rate/damage depend on selected ship |
| L06 | Open | Enemy type visual distinction is CSS modifiers, not independent detailed meshes |
| L07 | Open | Browser combat, mobile layout, game balance and persistence reload not playtested |
| L08 | Open | Shield recharge UI uses inherited logic; full interaction regression pending |
| L09 | Verified by static check | JS syntax, required code paths and archive integrity |