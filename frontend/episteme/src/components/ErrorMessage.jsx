import React from 'react';

const ErrorIcon = (props) => (
  <svg
    xmlns="http://www.w3.org/2000/svg"
    fill="none"
    viewBox="0 0 24 24"
    strokeWidth={1.5}
    stroke="currentColor"
    // Pass down className and other props
    {...props}
  >
    <path
      strokeLinecap="round"
      strokeLinejoin="round"
      d="M12 9v3.75m-9.303 3.376c-.866 1.5.217 3.374 1.948 3.374h14.71c1.73 0 2.813-1.874 1.948-3.374L13.949 3.378c-.866-1.5-3.032-1.5-3.898 0L2.697 16.126ZM12 15.75h.008v.008H12v-.008Z"
    />
  </svg>
);


const ErrorMessage = ({ message }) => {
  const displayMessage = message || "An unexpected error occurred. Please try again later.";

  const errorBorderColor = "border-red-500/40";
  const errorBgColor = "bg-red-900/20";
  const errorTextColor = "text-red-400";
  const errorIconColor = "text-red-500";

  return (
    <div
      role="alert"
      className={`
        w-full max-w-md         
        p-4                      
        rounded-lg               
        border                   
        ${errorBorderColor}      
        ${errorBgColor}          
        ${errorTextColor}        
        text-sm                  
      `}
    >
      <div className="flex items-center gap-3">
         <ErrorIcon className={`w-5 h-5 shrink-0 ${errorIconColor}`} aria-hidden="true" />

         <span className="font-medium">{displayMessage}</span>
      </div>
    </div>
  );
};

export default ErrorMessage;