* VOZ-9 — dual op-amp behavioral models (TL072 / NE5532)
*
* Subckt pins: IN+ IN- OUT VCC VEE
* Simple voltage-controlled voltage source + output resistance.
* Enough for oscillators, NAB EQ, mic pre DC bias checks — not RF or slew contests.

.subckt TL072_HALF INP INM OUT VCC VEE
* open-loop gain ~100k, Aol pole ~10 Hz → GBW ~1 MHz class
Rin  INP INM  10Meg
Eol  mid 0    INP INM  1e5
Rp   mid 0    1k
Cp   mid 0    15.9u
Rout mid OUT  100
Rload OUT 0   100Meg
.ends TL072_HALF

.subckt TL072 INP1 INM1 OUT1 INP2 INM2 OUT2 VCC VEE
X1 INP1 INM1 OUT1 VCC VEE TL072_HALF
X2 INP2 INM2 OUT2 VCC VEE TL072_HALF
.ends TL072

.subckt NE5532_HALF INP INM OUT VCC VEE
Rin  INP INM  100k
Eol  mid 0    INP INM  1e5
Rp   mid 0    1k
Cp   mid 0    1.59u
Rout mid OUT  75
Rload OUT 0   100Meg
.ends NE5532_HALF

.subckt NE5532 INP1 INM1 OUT1 INP2 INM2 OUT2 VCC VEE
X1 INP1 INM1 OUT1 VCC VEE NE5532_HALF
X2 INP2 INM2 OUT2 VCC VEE NE5532_HALF
.ends NE5532
