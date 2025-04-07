import React from 'react';


// Warning Icon for the header
const WarningIcon = () => (
    <svg
        xmlns="http://www.w3.org/2000/svg"
        fill="none"
        viewBox="0 0 24 24"
        strokeWidth={1.5}
        stroke="currentColor"
        className="size-5 mr-2 shrink-0"
    >
      <path strokeLinecap="round" strokeLinejoin="round" d="M12 9v3.75m-9.303 3.376c-.866 1.5.217 3.374 1.948 3.374h14.71c1.73 0 2.813-1.874 1.948-3.374L13.949 3.378c-.866-1.5-3.032-1.5-3.898 0L2.697 16.126ZM12 15.75h.007v.008H12v-.008Z" />
    </svg>
);

// Link Icon to appear after linked criticism content
const LinkIcon = () => (
    <svg
        xmlns="http://www.w3.org/2000/svg"
        viewBox="0 0 16 16"
        fill="currentColor"
        className="w-4 h-4 inline-block align-text-bottom ml-1 opacity-80 group-hover:opacity-100 transition-opacity duration-150"
    >
      <path d="M9.25 4.75a.75.75 0 0 1 .75-.75h1.5a.75.75 0 0 1 .75.75v1.5a.75.75 0 0 1-1.5 0V6.56l-3.22 3.22a.75.75 0 1 1-1.06-1.06l3.22-3.22H10a.75.75 0 0 1-.75-.75Z" />
      <path d="M3.75 2A2.75 2.75 0 0 0 1 4.75v6.5A2.75 2.75 0 0 0 3.75 14h6.5A2.75 2.75 0 0 0 13 11.25v-2.5a.75.75 0 0 0-1.5 0v2.5a1.25 1.25 0 0 1-1.25 1.25h-6.5A1.25 1.25 0 0 1 2.5 11.25v-6.5A1.25 1.25 0 0 1 3.75 3.5h2.5a.75.75 0 0 0 0-1.5h-2.5Z" />
    </svg>
);


const getValidityStyle = (score) => {
    const numericScore = Number(score);
    if (isNaN(numericScore) || score === null || score === undefined) {
      return { textClass: 'text-slate-500', label: 'N/A' };
    }

    let label = `${numericScore.toFixed(0)}% Validity`;
    let textClass = 'text-red-500';

    // Set color based on thresholds
    if (numericScore >= 75) {
        textClass = 'text-green-500'; // High validity
    } else if (numericScore >= 50) {
        textClass = 'text-yellow-500'; // Medium validity
    }

    return { textClass, label };
};


const CriticismList = ({ criticisms = [] }) => {
    if (!criticisms || criticisms.length === 0) {
        return null;
    }

    const darkBgClass = "bg-dark-background";
    const criticismTitleColorClass = "text-criticism-orange";
    const criticismTextColorClass = "text-slate-200";
    const linkHoverColorClass = "hover:text-green-400";
    const transitionClasses = "transition-colors duration-150 ease-in-out";

    return (
        <div className={`${darkBgClass} p-5 rounded-lg`}>
            <h4 className={`text-lg font-semibold ${criticismTitleColorClass} mb-4 flex items-center`}>
                <WarningIcon />
                Criticism:
            </h4>
            <ol className="space-y-5">
                {criticisms.map((criticism, index) => {
                    const { textClass: validityColor, label: validityLabel } = getValidityStyle(criticism.validityScore);

                    return (
                        <li key={criticism.commentUrl || index} className={`text-base ${criticismTextColorClass} leading-relaxed`}>

                            <div className="mb-2">
                                {criticism.commentUrl ? (
                                    <a
                                        href={criticism.commentUrl}
                                        target="_blank"
                                        rel="noopener noreferrer"
                                        title="View source comment"
                                        className={`inline ${criticismTextColorClass} ${linkHoverColorClass} ${transitionClasses} group`}
                                    >
                                        {criticism.content}
                                        <LinkIcon />
                                    </a>
                                ) : (
                                    <span>{criticism.content}</span>
                                )}
                            </div>

                            {(criticism.validityScore !== undefined && criticism.validityScore !== null) && (
                                <div className="flex items-center text-sm mt-1">
                                    <span className={`font-medium ${validityColor}`}>
                                        {validityLabel}
                                    </span>
                                </div>
                            )}
                        </li>
                    );
                })}
            </ol>
        </div>
    );
};

export default CriticismList;