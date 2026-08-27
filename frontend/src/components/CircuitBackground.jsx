// src/components/CircuitBackground.jsx
// Continuous animated PCB circuit-board trace background layer.
// Recreates the exact technical circuit pattern from the reference image:
// Right-angle traces with rounded corners, illuminated glowing circular nodes/halos,
// and continuous traveling data/signal pulses.

export default function CircuitBackground() {
  return (
    <div className="circuit-canvas-container" aria-hidden="true">
      <svg
        className="circuit-svg"
        viewBox="0 0 1600 900"
        preserveAspectRatio="xMidYMid slice"
        xmlns="http://www.w3.org/2000/svg"
      >
        <defs>
          {/* Radial gradient for glowing node halos matching reference image */}
          <radialGradient id="node-halo-grad" cx="50%" cy="50%" r="50%">
            <stop offset="0%" stopColor="#FFF8E1" stopOpacity="0.85" />
            <stop offset="25%" stopColor="#DFBE54" stopOpacity="0.45" />
            <stop offset="60%" stopColor="#C9A227" stopOpacity="0.15" />
            <stop offset="100%" stopColor="#C9A227" stopOpacity="0" />
          </radialGradient>

          {/* Pulse glow filter for high-visibility light pulses */}
          <filter id="circuit-pulse-glow" x="-100%" y="-100%" width="300%" height="300%">
            <feGaussianBlur stdDeviation="4" result="blur" />
            <feMerge>
              <feMergeNode in="blur" />
              <feMergeNode in="SourceGraphic" />
            </feMerge>
          </filter>

          {/* Line glow filter */}
          <filter id="trace-glow" x="-20%" y="-20%" width="140%" height="140%">
            <feGaussianBlur stdDeviation="1" result="blur" />
            <feMerge>
              <feMergeNode in="blur" />
              <feMergeNode in="SourceGraphic" />
            </feMerge>
          </filter>
        </defs>

        {/* ── Group 1: Left & Upper Circuit Traces ── */}
        <g className="circuit-trace-group" filter="url(#trace-glow)">
          <path
            id="trace-1"
            className="circuit-path"
            d="M 40 80 L 160 80 Q 190 80 190 110 L 190 260 Q 190 290 220 290 L 380 290 Q 410 290 410 320 L 410 490"
          />
          <path
            id="trace-2"
            className="circuit-path"
            d="M 100 30 L 100 180 Q 100 210 130 210 L 290 210 Q 320 210 320 240 L 320 380 Q 320 410 350 410 L 540 410"
          />
          <path
            id="trace-3"
            className="circuit-path"
            d="M 240 50 L 240 150 Q 240 180 270 180 L 440 180 Q 470 180 470 210 L 470 330 Q 470 360 500 360 L 640 360"
          />
          <path
            id="trace-4"
            className="circuit-path"
            d="M 50 300 L 140 300 Q 170 300 170 330 L 170 470 Q 170 500 200 500 L 360 500 Q 390 500 390 530 L 390 720"
          />
          <path
            id="trace-5"
            className="circuit-path"
            d="M 180 520 L 180 620 Q 180 650 210 650 L 430 650 Q 460 650 460 680 L 460 810 Q 460 840 490 840 L 700 840"
          />
          <path
            id="trace-6"
            className="circuit-path"
            d="M 320 120 L 510 120 Q 540 120 540 150 L 540 270 Q 540 300 570 300 L 760 300"
          />
          <path
            id="trace-7"
            className="circuit-path"
            d="M 30 430 L 130 430 Q 160 430 160 460 L 160 570 Q 160 600 190 600 L 340 600"
          />
          <path
            id="trace-left-bridge"
            className="circuit-path"
            d="M 500 360 L 500 540 Q 500 570 530 570 L 720 570"
          />
        </g>

        {/* ── Group 2: Center & Right Circuit Traces ── */}
        <g className="circuit-trace-group" filter="url(#trace-glow)">
          <path
            id="trace-8"
            className="circuit-path"
            d="M 880 100 L 1080 100 Q 1110 100 1110 130 L 1110 290 Q 1110 320 1140 320 L 1360 320 Q 1390 320 1390 350 L 1390 500"
          />
          <path
            id="trace-9"
            className="circuit-path"
            d="M 990 200 L 1200 200 Q 1230 200 1230 230 L 1230 400 Q 1230 430 1260 430 L 1540 430"
          />
          <path
            id="trace-10"
            className="circuit-path"
            d="M 1060 40 L 1060 170 Q 1060 200 1090 200 L 1300 200 Q 1330 200 1330 230 L 1330 350 Q 1330 380 1360 380 L 1580 380"
          />
          <path
            id="trace-11"
            className="circuit-path"
            d="M 860 360 L 1020 360 Q 1050 360 1050 390 L 1050 560 Q 1050 590 1080 590 L 1290 590 Q 1320 590 1320 620 L 1320 800"
          />
          <path
            id="trace-12"
            className="circuit-path"
            d="M 1120 460 L 1120 610 Q 1120 640 1150 640 L 1400 640 Q 1430 640 1430 670 L 1430 850"
          />
          <path
            id="trace-13"
            className="circuit-path"
            d="M 780 680 L 970 680 Q 1000 680 1000 710 L 1000 820 Q 1000 850 1030 850 L 1250 850"
          />
          <path
            id="trace-14"
            className="circuit-path"
            d="M 1240 680 L 1380 680 Q 1410 680 1410 710 L 1410 880"
          />
          <path
            id="trace-center-link"
            className="circuit-path"
            d="M 640 360 L 800 360 Q 830 360 830 390 L 830 520 Q 830 550 860 550 L 1050 550"
          />
        </g>

        {/* ── Group 3: Illuminated Glowing Node Halos (Matching Reference Image) ── */}
        <g className="circuit-halos">
          {/* Key Halo 1: Upper-left node */}
          <circle cx="190" cy="110" r="32" fill="url(#node-halo-grad)" className="halo-breathe-1" />
          
          {/* Key Halo 2: Mid-left hub */}
          <circle cx="410" cy="490" r="42" fill="url(#node-halo-grad)" className="halo-breathe-2" />
          
          {/* Key Halo 3: Lower-left endpoint */}
          <circle cx="390" cy="720" r="38" fill="url(#node-halo-grad)" className="halo-breathe-3" />
          
          {/* Key Halo 4: Mid-center junction */}
          <circle cx="540" cy="410" r="36" fill="url(#node-halo-grad)" className="halo-breathe-1" />
          
          {/* Key Halo 5: Upper-right hub */}
          <circle cx="1110" cy="130" r="34" fill="url(#node-halo-grad)" className="halo-breathe-2" />
          
          {/* Key Halo 6: Right-center hub */}
          <circle cx="1390" cy="500" r="44" fill="url(#node-halo-grad)" className="halo-breathe-3" />
          
          {/* Key Halo 7: Lower-right hub */}
          <circle cx="1320" cy="800" r="40" fill="url(#node-halo-grad)" className="halo-breathe-1" />
        </g>

        {/* ── Group 4: Circuit Nodes & Terminal Dots ── */}
        <g className="circuit-nodes">
          {/* Left Cluster Nodes */}
          <circle cx="40" cy="80" r="4.5" className="circuit-node-dot" />
          <circle cx="190" cy="110" r="5" className="circuit-node-dot active-node" />
          <circle cx="410" cy="490" r="6" className="circuit-node-dot active-node" />
          <circle cx="100" cy="30" r="4" className="circuit-node-dot" />
          <circle cx="540" cy="410" r="5.5" className="circuit-node-dot active-node" />
          <circle cx="240" cy="50" r="4.5" className="circuit-node-dot" />
          <circle cx="640" cy="360" r="5" className="circuit-node-dot" />
          <circle cx="50" cy="300" r="4" className="circuit-node-dot" />
          <circle cx="390" cy="720" r="6" className="circuit-node-dot active-node" />
          <circle cx="180" cy="520" r="4" className="circuit-node-dot" />
          <circle cx="700" cy="840" r="5.5" className="circuit-node-dot active-node" />
          <circle cx="320" cy="120" r="4" className="circuit-node-dot" />
          <circle cx="760" cy="300" r="5" className="circuit-node-dot" />
          <circle cx="30" cy="430" r="4" className="circuit-node-dot" />
          <circle cx="340" cy="600" r="5" className="circuit-node-dot" />
          <circle cx="720" cy="570" r="5" className="circuit-node-dot" />

          {/* Right Cluster Nodes */}
          <circle cx="880" cy="100" r="4.5" className="circuit-node-dot" />
          <circle cx="1110" cy="130" r="5.5" className="circuit-node-dot active-node" />
          <circle cx="1390" cy="500" r="6.5" className="circuit-node-dot active-node" />
          <circle cx="990" cy="200" r="4" className="circuit-node-dot" />
          <circle cx="1540" cy="430" r="5.5" className="circuit-node-dot active-node" />
          <circle cx="1060" cy="40" r="4.5" className="circuit-node-dot" />
          <circle cx="1580" cy="380" r="5" className="circuit-node-dot" />
          <circle cx="860" cy="360" r="4" className="circuit-node-dot" />
          <circle cx="1320" cy="800" r="6" className="circuit-node-dot active-node" />
          <circle cx="1120" cy="460" r="4" className="circuit-node-dot" />
          <circle cx="1430" cy="850" r="5" className="circuit-node-dot active-node" />
          <circle cx="780" cy="680" r="4.5" className="circuit-node-dot" />
          <circle cx="1250" cy="850" r="5" className="circuit-node-dot" />
          <circle cx="1240" cy="680" r="4" className="circuit-node-dot" />
          <circle cx="1410" cy="880" r="5" className="circuit-node-dot" />
          <circle cx="1050" cy="550" r="5" className="circuit-node-dot" />
        </g>

        {/* ── Group 5: Continuous Animated Traveling Pulses (Signal Flow) ── */}
        <g className="circuit-signals" filter="url(#circuit-pulse-glow)">
          {/* Signal 1 on Trace 1 */}
          <circle r="4.5" className="signal-pulse signal-pulse-gold">
            <animateMotion
              dur="6.5s"
              repeatCount="indefinite"
              path="M 40 80 L 160 80 Q 190 80 190 110 L 190 260 Q 190 290 220 290 L 380 290 Q 410 290 410 320 L 410 490"
            />
          </circle>

          {/* Signal 2 on Trace 2 */}
          <circle r="4" className="signal-pulse signal-pulse-white">
            <animateMotion
              dur="7.8s"
              begin="1.2s"
              repeatCount="indefinite"
              path="M 100 30 L 100 180 Q 100 210 130 210 L 290 210 Q 320 210 320 240 L 320 380 Q 320 410 350 410 L 540 410"
            />
          </circle>

          {/* Signal 3 on Trace 4 */}
          <circle r="4.5" className="signal-pulse signal-pulse-gold">
            <animateMotion
              dur="7.2s"
              begin="2.8s"
              repeatCount="indefinite"
              path="M 50 300 L 140 300 Q 170 300 170 330 L 170 470 Q 170 500 200 500 L 360 500 Q 390 500 390 530 L 390 720"
            />
          </circle>

          {/* Signal 4 on Trace 8 (Right side) */}
          <circle r="5" className="signal-pulse signal-pulse-white">
            <animateMotion
              dur="6.8s"
              begin="0.5s"
              repeatCount="indefinite"
              path="M 880 100 L 1080 100 Q 1110 100 1110 130 L 1110 290 Q 1110 320 1140 320 L 1360 320 Q 1390 320 1390 350 L 1390 500"
            />
          </circle>

          {/* Signal 5 on Trace 11 (Right side) */}
          <circle r="4" className="signal-pulse signal-pulse-gold">
            <animateMotion
              dur="8.2s"
              begin="1.9s"
              repeatCount="indefinite"
              path="M 860 360 L 1020 360 Q 1050 360 1050 390 L 1050 560 Q 1050 590 1080 590 L 1290 590 Q 1320 590 1320 620 L 1320 800"
            />
          </circle>

          {/* Signal 6 on Trace 5 (Bottom left) */}
          <circle r="4.5" className="signal-pulse signal-pulse-white">
            <animateMotion
              dur="8.8s"
              begin="3.6s"
              repeatCount="indefinite"
              path="M 180 520 L 180 620 Q 180 650 210 650 L 430 650 Q 460 650 460 680 L 460 810 Q 460 840 490 840 L 700 840"
            />
          </circle>

          {/* Signal 7 on Trace 13 (Bottom right) */}
          <circle r="4.5" className="signal-pulse signal-pulse-gold">
            <animateMotion
              dur="7.5s"
              begin="1s"
              repeatCount="indefinite"
              path="M 780 680 L 970 680 Q 1000 680 1000 710 L 1000 820 Q 1000 850 1030 850 L 1250 850"
            />
          </circle>

          {/* Signal 8 on Center Link */}
          <circle r="4" className="signal-pulse signal-pulse-white">
            <animateMotion
              dur="6.4s"
              begin="2.2s"
              repeatCount="indefinite"
              path="M 640 360 L 800 360 Q 830 360 830 390 L 830 520 Q 830 550 860 550 L 1050 550"
            />
          </circle>
        </g>
      </svg>
    </div>
  )
}
