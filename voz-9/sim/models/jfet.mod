* VOZ-9 — JFET models (typical mid parts; Vgs(off) spreads in real silicon)
*
* Pin order for .model NJF: D G S when used as Jxxx D G S model

* MMBFJ201 / J201 — N-channel JFET (VCF, VCA, FM, noise, buffer)
* Vto ~ -0.8 V typical; Idss ~ 0.5–1 mA mid bin
.model J201 NJF(Vto=-0.8 Beta=1.2e-3 Lambda=2e-2 Rd=10 Rs=10 Cgs=4p Cgd=4p Is=1e-14 N=1)

* MMBF5457 / 2N5457 — N-channel JFET (phase-shift LFO)
* Vto ~ -1.5 V; used as phase-shift oscillator active element
.model J5457 NJF(Vto=-1.5 Beta=1.0e-3 Lambda=2e-2 Rd=15 Rs=15 Cgs=5p Cgd=5p Is=1e-14 N=1)
