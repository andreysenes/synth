* VOZ-9 — diode models
*
* 1N4148 / 1N4148WS — Si switching
.model D4148 D(Is=2.5e-9 Rs=0.6 N=1.8 Cjo=4p M=0.33 Tt=12n Bv=100 Ibv=100u)

* SS14 / 1N5817 — Schottky 40 V 1 A (power polarity)
.model DSS14 D(Is=1e-6 Rs=0.05 N=1.1 Cjo=160p M=0.4 Bv=40 Ibv=1m)

* 1N34A — Ge detector (stand-in for MP20 clipper / tape sat)
* Soft knee, low Vf ~0.2–0.3 V
.model D1N34A D(Is=2e-7 Rs=15 N=1.9 Cjo=0.8p M=0.33 Bv=60 Ibv=100u)

* LED red 0805 — rough DC drop for pilot
.model DLEDRED D(Is=1e-20 Rs=5 N=2.0 Cjo=20p Bv=5 Ibv=10u)
