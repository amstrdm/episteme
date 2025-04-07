import React from "react";

const MetricCard = ({ label, value, className = "", valueClassName = "" }) => {
  const baseLayoutClasses = "flex-1 shrink font-medium basis-0";

  const colorClass = valueClassName || "text-white-text";

  return (
    <div
      className={`flex flex-col grow shrink justify-center self-stretch px-4 py-4 rounded-lg bg-dark-background min-h-12 ${className}`}
    >
      <div className="flex gap-2 items-start w-full">
        <span className="text-light-text">{label}</span>

        <span
          className={`${baseLayoutClasses} ${colorClass}`}
        >
          {value}
        </span>
      </div>
    </div>
  );
};

export default MetricCard;