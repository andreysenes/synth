* VOZ-9 — AS3340 exponential scale (27 °C), not a full chip model.
*
* Pins: FCI (15, virtual ground), SCALE (14, hang Rs to GND), SAW (probe).
* 1 V into 100 kΩ at FCI moves 10 µA through Rs.
* 10 µA × 1.793 kΩ = 17.93 mV = VT·ln(2) = one octave.
* Internal offset 50 µA: +5.000 V on that 100 kΩ lands on C6 (1046.5 Hz).

.subckt AS3340_EXPO FCI SCALE SAW
Vfci FCI 0 DC 0
Brs SCALE 0 I={50e-6 - I(Vfci)}
Bsaw SAW 0 V={4*sin(6.283185307*1046.5*pow(2, V(SCALE)/0.01793)*time)}
.ends
