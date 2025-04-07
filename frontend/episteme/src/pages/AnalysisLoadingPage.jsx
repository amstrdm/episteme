import React, { useState, useEffect, useRef } from 'react';
import { useParams, useNavigate } from 'react-router-dom';
import apiClient from '../api/axiosinstance';

const AnalysisLoadingPage = () => {
  const { taskId, ticker } = useParams();
  const navigate = useNavigate();
  const [statusMessage, setStatusMessage] = useState('Initializing analysis...');
  const [errorMessage, setErrorMessage] = useState(null);
  const [progressValue, setProgressValue] = useState(0);
  const intervalRef = useRef(null);

  useEffect(() => {
    if (!taskId) {
      setErrorMessage('Missing analysis task ID.');
      return;
    }

    const checkStatus = async () => {
      try {
        const response = await apiClient.get('/analysis-status', {
          params: { task_id: taskId },
        });
        const data = response.data;

        console.log('Analysis Status:', data);

        if (data.error) {
          setErrorMessage(data.error);
          setStatusMessage('');
          setProgressValue(0);
          clearInterval(intervalRef.current);
        } else {
          setStatusMessage(data.status || 'Processing...');
          const currentProgress = Math.max(0, Math.min(10, Number(data.progress ?? 0)));
          setProgressValue(currentProgress);
          setErrorMessage(null);

          if (currentProgress === 10) {
            clearInterval(intervalRef.current);
            console.log(`Analysis complete for ${ticker}. Redirecting...`);
            navigate(`/stock/${ticker || data.ticker}`);
          }
        }
      } catch (error) {
        console.error('Failed to fetch analysis status:', error);
        const errorText = error.response?.data?.detail || error.response?.data?.error || error.message || 'Failed to fetch status.';
        setErrorMessage(`Error checking status: ${errorText}`);
        setStatusMessage('');
        setProgressValue(0);
        clearInterval(intervalRef.current);
      }
    };

    checkStatus();
    intervalRef.current = setInterval(checkStatus, 3000);

    // Cleanup
    return () => {
      if (intervalRef.current) {
        clearInterval(intervalRef.current);
      }
    };
  }, [taskId, navigate, ticker]);

  const progressPercentage = (progressValue / 10) * 100;

  return (
    <div className="min-h-screen flex flex-col justify-center items-center bg-dark-background p-4">

      {/* Status/Error Message */}
      {errorMessage ? (
        <div className="mt-4 font-medium text-red-400 bg-red-900 bg-opacity-30 border border-red-500 px-4 py-2 rounded-lg max-w-lg text-center">
             {errorMessage}
        </div>
      ) : (
        <>
            {/* CSS Loader */}
            <div className="loader ml-8"></div>

            {/* Progress Bar*/}
            <div className="w-4/5 max-w-sm h-2 bg-slate-700 rounded-full mt-6 overflow-hidden">
                <div
                    className="h-full bg-green-500 rounded-full transition-all duration-300 ease-in-out "
                    style={{ width: `${progressPercentage}%` }}
                ></div>
            </div>

            <div className="mt-4 text-lg text-slate-400 min-h-[1.75rem] text-center">
                {statusMessage}
            </div>
        </>

      )}

      {/* Back Button on Error */}
      {errorMessage && (
         <button
            onClick={() => navigate(-1)}
            className="mt-6 px-4 py-2 cursor-pointer rounded-md font-medium transition duration-150 ease-in-out bg-dark-background hover:bg-slate-700 text-light-text border border-slate-600 hover:border-slate-500"
         >
            Go Back
         </button>
      )}
    </div>
  );
};

export default AnalysisLoadingPage;