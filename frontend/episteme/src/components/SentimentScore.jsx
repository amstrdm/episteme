import React from "react";

const SentimentScore = ({ score }) => {
  const rawScore = typeof score === "number" ? score : 50;
  const validScore = Math.max(0, Math.min(100, rawScore));

  const getScoreColor = (scoreValue) => {
    if (scoreValue >= 60) return "#00E65F"; // Green
    if (scoreValue >= 40) return "#F29408"; // Orange
    return "#FF4D4D"; // Red
  };

  const scoreColor = getScoreColor(validScore);
  const emptyGaugeColor = "#404040";
  const textColor = "#FFFFFF";
  const labelColor = "text-gray-400";


  // --- SVG Parameters ---
  const viewBoxWidth = 200;
  const viewBoxHeight = 100;
  const svgHeight = 100;
  const strokeWidth = 16;
  const centerX = viewBoxWidth / 2;
  const arcCenterY = 100;
  const radius = viewBoxWidth / 2 - strokeWidth / 2;

  const startX = centerX - radius;
  const startY = arcCenterY;
  const endX = centerX + radius;
  const endY = arcCenterY;
  const arcPath = `M ${startX} ${startY} A ${radius} ${radius} 0 0 1 ${endX} ${endY}`;

  const arcLength = Math.PI * radius;
  const dashOffset = arcLength * (1 - validScore / 100);

  const backgroundClass = 'bg-dark-background';
  const outerTextClass = 'text-white-text';

  return (
    <section className={`flex flex-1 flex-col items-center justify-center p-6 text-xl font-medium ${outerTextClass} rounded-2xl ${backgroundClass} w-[270px] max-md:mt-6 max-md:w-full`}>
      <h2 className="mb-4 w-full text-center">Sentiment Score</h2>

      <div className={`relative w-[200px] h-[125px] mb-2`}>

        {/* SVG: Only draws the arcs, positioned at the top */}
        <svg
          viewBox={`0 0 ${viewBoxWidth} ${viewBoxHeight}`}
          width="200"
          height={svgHeight} // SVG height remains 100
          className="absolute top-0 left-0"
          style={{ display: 'block', overflow: 'visible' }}
        >
          {/* Background Arc Path */}
          <path
            d={arcPath}
            fill="none"
            stroke={emptyGaugeColor}
            strokeWidth={strokeWidth}
            strokeLinecap="round"
          />
          {/* Foreground Arc Path (Score Fill) */}
          <path
            d={arcPath}
            fill="none"
            stroke={scoreColor}
            strokeWidth={strokeWidth}
            strokeDasharray={arcLength}
            strokeDashoffset={dashOffset}
            strokeLinecap="round"
            style={{ transition: 'stroke-dashoffset 0.3s ease-out' }}
          />
        </svg>

        {/* HTML Score Text: Positioned absolutely */}
        <p
          className="absolute bottom-[30px] left-1/2 -translate-x-1/2 text-3xl font-semibold" // Fine-tune this value if needed
          style={{ color: textColor }}
        >
          {validScore.toFixed(1)}%
        </p>

        <span
           // Align to absolute bottom-left, no indent
           className={`absolute bottom-0 left-0 text-xs ${labelColor}`}
        >
          0%
        </span>

        <span
           className={`absolute bottom-0 right-0 text-xs ${labelColor}`}
        >
           100%
        </span>
      </div>
    </section>
  );
};

export default SentimentScore;