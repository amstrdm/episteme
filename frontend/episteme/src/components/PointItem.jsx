import React, { useState } from "react";
import PointPreview from "./PointPreview";   // Ensure path is correct
import CriticismList from "./CriticismList"; // Ensure path is correct
import { motion, AnimatePresence } from "framer-motion";

const PointItem = ({ icon, point, index, isSelected, onPointClick }) => {
    const {
        content,
        criticisms = [],
        postUrl,
        postTitle,
        postSource,
        postDate,
        postAuthor,
        postImageUrl
    } = point;

    const criticismCount = criticisms.length;

    const [isCriticismExpanded, setIsCriticismExpanded] = useState(false);

    const darkBgClass = "bg-dark-background";
    const whiteTextClass = "text-white-text";

    const handlePreviewClick = () => {
        if (postUrl) {
            // Close criticisms section if it's open when opening preview
            setIsCriticismExpanded(false);
            // Notify parent list component to toggle selection state for this item's index
            onPointClick(index);
        }
    };

    const handleCriticismToggle = (event) => {
        event.stopPropagation(); // Prevent click from triggering handlePreviewClick
        if (criticismCount > 0) {
            if (!isCriticismExpanded) {
                onPointClick(-1); // Notify parent to close any open preview
            }
            // Toggle local state for criticism visibility
            setIsCriticismExpanded(prev => !prev);
        }
    };

    const mainCursorStyle = postUrl ? "cursor-pointer" : "cursor-default";
    const bubbleCursorStyle = criticismCount > 0 ? "cursor-pointer" : "cursor-default";

    const expandableVariant = {
        initial: { height: 0, opacity: 0, marginTop: 0 },
        animate: { height: 'auto', opacity: 1, marginTop: '0.5rem' },
        exit: { height: 0, opacity: 0, marginTop: 0 },
        transition: { duration: 0.2, ease: "easeInOut" }
    };

    return (
        <div className="flex flex-col gap-2">

            {/* --- Main Clickable Row (Point Content + Bubble) --- */}
            <div
                className={`flex gap-3 items-start w-full ${mainCursorStyle} transition duration-150 ease-in-out rounded p-1 -m-1 ${'hover:bg-gray-700 hover:bg-opacity-20'}`}
                onClick={handlePreviewClick}
                role={postUrl ? "button" : undefined}
                tabIndex={postUrl ? 0 : undefined}
                onKeyDown={(e) => { if (postUrl && (e.key === 'Enter' || e.key === ' ')) handlePreviewClick(); }} // Keyboard activation
            >
                {/* Point Icon */}
                <img
                    src={icon}
                    className="object-contain shrink-0 w-5 h-5 aspect-square mt-0.5"
                    alt={point.type === "bullish" ? "Bullish point" : "Bearish point"}
                />
                {/* Text Content and Criticism Toggle Bubble */}
                <div className="flex flex-1 justify-between items-start gap-3 min-w-0">
                    <h3 className={`text-sm font-medium ${whiteTextClass} leading-snug`}>
                        {content}
                    </h3>
                    {/* Criticism Count Bubble (acts as toggle button) */}
                    {criticismCount > 0 && (
                        <button
                            type="button"
                            onClick={handleCriticismToggle}
                            aria-expanded={isCriticismExpanded}
                            aria-controls={`criticisms-${index}`}
                            title={isCriticismExpanded ? "Hide criticisms" : "Show criticisms"}
                             className={`
                                flex items-center justify-center shrink-0
                                rounded-full h-5 w-5                           
                                text-xs font-semibold leading-none
                                ${bubbleCursorStyle}
                                hover:opacity-80 focus:outline-none
                                transition-colors duration-150 ease-in-out
                                ${isCriticismExpanded
                                    // Expanded/Selected State: Orange BG, Dark Text
                                    ? `bg-criticism-orange text-gray-900`
                                    // Default/Collapsed State: Dark BG, Orange Text
                                    : `${darkBgClass} text-criticism-orange`
                                }
                            `}
                        >
                            {criticismCount}
                        </button>
                    )}
                </div>
            </div>

            {/* --- Expandable Criticisms Section --- */}
            <AnimatePresence initial={false}> {/* initial=false prevents exit animation on first render */}
                {isCriticismExpanded && criticismCount > 0 && (
                    <motion.div
                        id={`criticisms-${index}`}
                        key={`criticisms-${index}`}
                        variants={expandableVariant}
                        initial="initial"
                        animate="animate"
                        exit="exit"
                        style={{ overflow: 'hidden' }} // Needed for height animation
                        className="ml-[calc(20px+0.75rem)]" // Indentation based on icon width + gap (20px w-5 icon + 0.75rem gap-3)
                    >
                        <CriticismList criticisms={criticisms} />
                    </motion.div>
                )}
            </AnimatePresence>

            {/* --- Expandable Post Preview Section --- */}
            <AnimatePresence initial={false}>
                {isSelected && postUrl && (
                     <motion.div
                        key={`preview-${index}`}
                        variants={expandableVariant}
                        initial="initial"
                        animate="animate"
                        exit="exit"
                        style={{ overflow: 'hidden' }} // Needed for height animation
                     >
                        <PointPreview
                            title={postTitle}
                            url={postUrl}
                            source={postSource}
                            author={postAuthor}
                            date={postDate}
                            imageUrl={postImageUrl}
                        />
                     </motion.div>
                 )}
              </AnimatePresence>
        </div>
    );
};

export default PointItem;