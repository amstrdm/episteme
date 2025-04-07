import React, { useState, useMemo } from "react";
import PointItem from "./PointItem";

const PointsList = ({ title, points = [], type }) => {
  const iconUrl =
    type === "bullish"
      ? "/green_check.svg" // Green Check
      : "/red_cross.svg"; // Red X

  const validPoints = points || [];

  const backgroundClass = 'bg-widget-background';
  const whiteTextClass = 'text-white-text';

  const [selectedPointIndex, setSelectedPointIndex] = useState(-1);

  const handlePointClick = (index) => {
    setSelectedPointIndex(prevIndex => (prevIndex === index ? -1 : index));
  };

  const [leftColumnPoints, rightColumnPoints] = useMemo(() => {
    const left = [];
    const right = [];
    // Iterate through points and distribute them into left/right columns
    validPoints.forEach((point, index) => {
      const pointWithIndex = { ...point, originalIndex: index };
      if (index % 2 === 0) { // Even index goes to left column
        left.push(pointWithIndex);
      } else { // Odd index goes to right column
        right.push(pointWithIndex);
      }
    });
    return [left, right];
  }, [validPoints]); // Dependency array: re-run only if validPoints changes

  return (
    <section className={`flex flex-col p-8 w-full tracking-wide rounded-2xl ${backgroundClass} min-h-[306px] max-md:px-5 max-md:mt-6 max-md:max-w-full`}>

      <h2 className={`text-xl font-medium leading-tight ${whiteTextClass} mb-6`}>
        {title}
      </h2>

      {/* --- Flexbox Container for Columns --- */}
      <div className="flex flex-col md:flex-row gap-x-8">

        {/* Left Column Container */}
        <div className="flex-1 flex flex-col gap-y-4">
          {leftColumnPoints.map((point) => (
            <PointItem
              key={point.post_url + point.originalIndex || point.originalIndex}
              icon={iconUrl}
              point={point}
              index={point.originalIndex}
              isSelected={selectedPointIndex === point.originalIndex}
              onPointClick={handlePointClick}
            />
          ))}
        </div>

        {/* Right Column Container */}
        <div className="flex-1 flex flex-col gap-y-4">
          {rightColumnPoints.map((point) => (
            <PointItem
              key={point.post_url + point.originalIndex || point.originalIndex}
              icon={iconUrl}
              point={point}
              index={point.originalIndex}
              isSelected={selectedPointIndex === point.originalIndex}
              onPointClick={handlePointClick}
            />
          ))}

          {leftColumnPoints.length === 0 && rightColumnPoints.length === 0 && (
              <p className="text-gray-500 text-sm">
                  No {type} points available.
              </p>
          )}
        </div>
      </div>
    </section>
  );
};

export default PointsList;