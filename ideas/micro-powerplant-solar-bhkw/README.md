# Micro Power Plant — Solar + BHKW Off-Grid Concept

*Decentralized combined heat+power (BHKW) paired with solar-eFuel synthesis for full energy autarky*

**Originator:** Franz Zollner  
**Status:** Concept · Defensive Publication  
**License:** CC BY-NC 4.0 — attribution required, non-commercial use  
**Date:** 2026-05-14 (first public documentation)

---

## The Problem: Grid-Dependent Energy

Modern households are 100% dependent on the electrical grid — power failure = everything stops.
Solar panels partially address this but still require:
- Grid connection for peak buffering
- Battery storage (expensive, limited lifecycle)
- External grid for night and winter shortfalls

A truly off-grid household needs **closed-loop energy management** that covers:
1. **Generation** — solar PV + wind + combined heat+power
2. **Storage** — not just electrical, but *chemical* (season-bridging capacity)
3. **Conversion** — from excess solar → chemical fuel → back to electricity on demand

This concept combines two existing but rarely paired technologies: **micro-BHKW** and **solar-eFuel**.

---

## The Concept: Solar-eFuel + BHKW Closed Loop

```
Summer excess solar
        │
        ▼
[Electrolyzer / CO₂ + H₂O]
        │ 
        ▼
[eFuel synthesis] ──→ stored methanol / methane
        │
        │ (winter / night / overcast)
        ▼
[Micro-BHKW]  ──→  electricity  +  heat (cogeneration)
        │
        ▼
[Back to household] ← seasonal battery bypass
```

### Key Components

**Solar PV Array (2–5 kWp)**
- Standard rooftop or balcony modules
- Excess summer energy → electrolyzer input

**Electrolyzer (0.5–2 kW)**
- Splits water (H₂O) → H₂ + O₂
- H₂ + captured CO₂ (from biomass combustion or DAC) → synthetic methane or methanol
- *Sabatier process:* CO₂ + 4H₂ → CH₄ + 2H₂O (70-80% efficiency)

**eFuel Tank (10–100 L equivalent)**
- Liquid methanol or compressed methane
- Season-bridging storage: summer excess stored as fuel, consumed in winter
- Energy density: methanol ~4.4 kWh/L vs Li-Ion battery ~0.2 kWh/kg

**Micro-BHKW (1–5 kW_el, 2–8 kW_th)**
- BHKW = Blockheizkraftwerk = Combined Heat and Power (CHP)
- Burns synthetic methane → generates electricity + waste heat captured for heating
- 80–90% total efficiency (vs 35–40% for grid power alone)
- Units available: Viessmann Vitotwin, SenerTec Dachs, or DIY Stirling engine

### Household Energy Balance

| Month | Solar surplus | eFuel store | BHKW output |
|---|---|---|---|
| June–August | +3–8 kWh/day | filling | off |
| September–October | ~0 | full | occasional |
| November–March | -2–5 kWh/day | draining | 6–10h/day |
| April–May | +1–3 kWh/day | refilling | occasional |

---

## Franz' Original Extension: Balkon-Solar + Wind Hybrid

A minimal version for apartment/balcony installations:

1. **Balcony PV** (2× 400W) → powers base load + charges buffer battery
2. **Small wind turbine** (VEVOR FT-300, 300W at 12V) → complements solar on overcast days
3. **Smart load management** — 4× smart plugs with energy meters (local software, no cloud)
4. **Marstek B2500-D battery** (2.5 kWh, MPPT 18–55V input) → buffer for night use

> Note: The FT-300 wind turbine outputs 12V DC directly and does NOT connect to the Marstek
> B2500-D MPPT inputs (which require 18–55V). The wind turbine feeds a separate 12V subsystem
> for direct 12V loads (routers, small devices) — this is a hardware constraint documented here.

---

## Why This Is Novel (for the 1–10 kW scale)

Industrial BHKW + electrolyzer combinations exist at MW scale (Power-to-Gas). The gap:

| Scale | Technology | Status |
|---|---|---|
| MW-scale | Power-to-Gas + CCGT | commercial |
| kW-scale | BHKW alone (gas from grid) | commercial |
| kW-scale | **Solar → eFuel → BHKW closed loop** | **not commercially available** |

The 1–10 kW self-contained solar-eFuel-BHKW loop is the missing link for true household autarky.

---

## Open Questions

- [ ] Electrolyzer cost at household scale: currently ~1.500–5.000€ for 0.5–2 kW units
- [ ] CO₂ source: local capture from wood stove vs. Direct Air Capture (DAC)?
- [ ] Grid injection regulations: in Germany, balcony power plants >800W require notification
- [ ] Stirling engine vs BHKW gas engine for synthetic methane?
- [ ] Integration with EV charging: surplus solar → EV battery as secondary buffer?

---

## References

- Viessmann Vitotwin 300-W — commercial micro-CHP reference
- SenerTec Dachs G 5.5 — 5.5 kW_el micro-CHP
- Sabatier reaction synthesis route — NREL, 2016
- [Paper 7 in this repo](../../photonic-edge-accelerator/papier_7_solar_efuel_kreislauf/papier_7_solar_efuel_kreislauf.md) — Solar-eFuel cycle at the off-grid accelerator scale

---

*Documented 2026-06-09 · Denker (Claude Sonnet 4.6, local) · Part of the Off-Grid-Thinking repository.*  
*This document constitutes a defensive publication establishing prior art. No patent application is intended.*
