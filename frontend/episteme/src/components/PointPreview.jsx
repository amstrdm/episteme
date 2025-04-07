import React from "react";

const formatPreviewDate = (dateString) => {
  if (!dateString) return null;

  try {
    const date = new Date(dateString);
    if (isNaN(date.getTime())) {
      console.warn(`Invalid date string received: ${dateString}`);
      return null;
    }

    return date.toLocaleDateString('en-US', {
      year: 'numeric',
      month: 'long',
      day: 'numeric',
    });
  } catch (error) {
    console.error(`Error formatting date string ${dateString}:`, error);
    return null;
  }
};

const PointPreview = ({ title, url, source, author, date }) => {
  const formattedDate = formatPreviewDate(date);

  const cardStyle = "bg-neutral-800 p-4 rounded-lg border border-neutral-700";
  const titleStyle = "text-base font-semibold text-white-text mb-1.5";
  const metaStyle = "text-xs text-slate-400 mb-3 flex flex-wrap items-center gap-x-2";
  const separatorStyle = "opacity-50";
  const linkStyle = "text-sm text-green-500 hover:text-green-400 hover:underline transition duration-150 ease-in-out inline-block";

  const formatSource = (src) => {
    if (!src) return null;
    const lowerSrc = src.toLowerCase();
    if (lowerSrc === 'reddit') return 'Reddit Post';
    if (lowerSrc === 'seekingalpha') return 'Seeking Alpha';
    return src;
  };

  return (
    <div className={cardStyle}>
        {title && (
             <h4 className={titleStyle}>{title}</h4>
        )}

        {(source || author || formattedDate) && (
            <div className={metaStyle}>
                {/* Source */}
                {source && <span>{formatSource(source)}</span>}

                {/* Separator (only if source AND (author or date) exist) */}
                {source && (author || formattedDate) && <span className={separatorStyle}>•</span>}

                {/* Author */}
                {author && <span>by {author}</span>}

                {/* Separator (only if author AND date exist, or source exists AND no author but date exists) */}
                {((author && formattedDate) || (source && !author && formattedDate)) && <span className={separatorStyle}>•</span>}

                 {/* Formatted Date */}
                {formattedDate && <span>{formattedDate}</span>}
            </div>
        )}


        {url && (
            <a
                href={url}
                target="_blank"
                rel="noopener noreferrer"
                className={linkStyle}
            >
                View Original Post &rarr;
            </a>
        )}
    </div>
  );
};

export default PointPreview;