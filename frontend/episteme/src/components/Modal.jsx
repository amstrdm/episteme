// src/components/Modal.js
import React from "react";

const Modal = ({
  isOpen,
  onClose,
  message,
  existingAnalysis,
  onYes,
  onNo = onClose,
  onAccessExisting,
  onCreateNew,
  isGenerating
}) => {
  if (!isOpen) return null;

  const buttonBaseClasses = "px-4 py-2 rounded-md font-medium transition duration-150 ease-in-out disabled:opacity-50 disabled:cursor-not-allowed cursor-pointer";

  // Primary / Positive actions use the theme's green accent
  const confirmButtonClasses = `${buttonBaseClasses} bg-green-500 hover:bg-green-600 text-white`;

  // Secondary / Alternative actions use the darker background, similar to inner containers
  const secondaryButtonClasses = `${buttonBaseClasses} bg-dark-background hover:bg-slate-700 text-light-text border border-slate-600 hover:border-slate-500`;

  return (
    <div
      className="fixed inset-0 backdrop-blur-sm z-[60] flex justify-center items-center p-4"
      onClick={onClose}
    >
      <div
        className="bg-widget-background text-light-text p-6 rounded-2xl shadow-xl max-w-md w-full"
        onClick={(e) => e.stopPropagation()}
      >
        {/* Message Text */}
        <p className="mb-5 text-base text-white-text">{message || "Something went wrong."}</p>

        {/* Button Container */}
        <div className="flex justify-end gap-3">
          {existingAnalysis === false ? (
            // Buttons for "Generate New?" scenario
            <>
              <button
                onClick={onNo}
                disabled={isGenerating}
                className={secondaryButtonClasses} // Use secondary style for "No"
              >
                No
              </button>
              <button
                onClick={onYes}
                disabled={isGenerating}
                className={confirmButtonClasses} // Use confirm style for "Yes"
              >
                {isGenerating ? "Generating..." : "Yes"}
              </button>
            </>
          ) : (
            // Buttons for "Existing Found" scenario
            <>
              <button
                onClick={onAccessExisting}
                disabled={isGenerating}
                className={secondaryButtonClasses} // Use confirm style for "Access Existing"
              >
                Access Existing
              </button>

              <button
                onClick={onCreateNew}
                 disabled={isGenerating}
                 className={confirmButtonClasses} // Use secondary style for "Create New"
              >
                 {isGenerating ? "Generating..." : "Create New"}
              </button>
            </>
          )}
        </div>
      </div>
    </div>
  );
};

export default Modal;