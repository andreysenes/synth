* VOZ-9 — ideal rails + load stubs (78M05 / ICL7660 not clocked)
*
* Call after defining node 0 as GND.
* Creates: V9, V5, VEE, 4V5, 1V8
*
* Usage: .include models/rails.mod
*        Xrails V9 V5 VEE 4V5 1V8 rails

.subckt rails V9 V5 VEE N4V5 N1V8
* External 9 V supply (after 1N5817) — ideal
Vrail V9 0 DC 9
* 78M05 ideal 5 V + ~75 mA PT2399 load
Vreg  V5 0 DC 5
RloadV5 V5 0 66.7
* ICL7660 ideal −9 V (no charge-pump ripple)
Vneg  VEE 0 DC -9
* Virtual ground 4V5 divider
R45a V9 N4V5 10k
R45b N4V5 0 10k
C45  N4V5 0 47u
* Bias 1V8: 22k + 5k6
R18a V9 N1V8 22k
R18b N1V8 0 5.6k
C18  N1V8 0 47u
.ends rails
