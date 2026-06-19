// OpenGoldSDR — parametric Rail SAR gantry (OpenSCAD)
// A linear rail that steps an SDR/FMCW antenna along a precise track to synthesize an aperture.
// Edit the params, render (F6), export STL/DXF. For a conversational/text-to-CAD pass use Zoo (zoo.dev)
// or generate CadQuery; this OpenSCAD model is the no-dependency parametric baseline.

/* ---- parameters (mm) ---- */
rail_length     = 1500;   // travel = aperture length; longer = finer cross-range resolution
extrusion       = 20;     // 2020 aluminum extrusion cross-section
carriage_len    = 80;     // antenna carriage block along rail
carriage_w      = 60;
carriage_h      = 25;
antenna_post    = 120;    // height of antenna stand-off above the rail
nema17          = 42.3;   // NEMA17 face size
belt_clear      = 6;      // GT2 belt channel

/* ---- aluminum extrusion rail ---- */
module rail() color("silver")
    translate([0,-extrusion/2,-extrusion/2]) cube([rail_length, extrusion, extrusion]);

/* ---- NEMA17 stepper at the drive end ---- */
module stepper() color("dimgray")
    translate([-nema17, -nema17/2, -nema17/2]) cube([nema17, nema17, nema17]);

/* ---- moving carriage + antenna post ---- */
module carriage(pos=300) color("steelblue") translate([pos,0,0]) {
    translate([-carriage_len/2,-carriage_w/2, extrusion/2]) cube([carriage_len, carriage_w, carriage_h]);
    // antenna stand-off post
    translate([0,0, extrusion/2 + carriage_h])
        cylinder(h=antenna_post, d=12, $fn=32);
    // antenna mount plate (where the SDR horn/can bolts on)
    translate([0,0, extrusion/2 + carriage_h + antenna_post])
        cube([70, 70, 4], center=true);
}

/* ---- end-stop / homing switch (position datum = SAR phase reference) ---- */
module endstop() color("red")
    translate([rail_length-5, extrusion/2, 0]) cube([8, 10, 12]);

rail();
stepper();
carriage(pos = rail_length*0.3);   // change pos to animate a scan step
endstop();

// NOTE: position repeatability at each step IS the measurement. Use a stepper + lead screw or GT2 belt,
// home against the end-stop every run, and log encoder/step count alongside each IQ capture.
