'use client'
import React, { useEffect, useState } from 'react';


interface PullRequest {
  id: number;
  pr_id: string;
  sourceBranchName: string;
  targetBranchName: string;
  date_created: string;
  content: string;
  feedback: string;
}

interface Props {
  prId: string;
}

const PullRequestDetails: React.FC<Props> = ({ prId }) => {
  const [prDetails, setPrDetails] = useState<PullRequest | null>(null);
  const [loading, setLoading] = useState<boolean>(false);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    const fetchData = async () => {
      setLoading(true); // Set loading state to true when fetching data
      try {
        console.log(prId);
        const response = await fetch(`/api/pr/${prId}`);
        if (!response.ok) {
          throw new Error("Failed to fetch pull request details.");
        }
        const data = await response.json();
        setPrDetails(data);
      } catch (err) {
        setError("Error fetching data from backend.");
        console.error(err);
      } finally {
        setLoading(false); // Set loading state back to false after fetching data
      }
    };

    fetchData(); // Call the async function inside useEffect
  }, [prId]);


  return (
    <div className="p-6 bg-white shadow-md rounded-lg">
      {loading && <p className="text-blue-500 mt-4">Loading...</p>}
      {error && <p className="text-red-500 mt-4">{error}</p>}
      {prDetails && (
        <div>
          <h2 className="text-3xl font-bold mb-4 text-gray-800">Pull Request #{prDetails.pr_id}</h2>
          <div className="mb-4">
            <span className="font-semibold text-gray-700">Source Branch:</span> {prDetails.sourceBranchName}
          </div>
          <div className="mb-4">
            <span className="font-semibold text-gray-700">Target Branch:</span> {prDetails.targetBranchName}
          </div>
          <div className="mb-4">
            <span className="font-semibold text-gray-700">Date Created:</span> {new Date(prDetails.date_created).toLocaleString()}
          </div>
          <div className="mb-4">
            <span className="font-semibold text-gray-700">Content:</span>
            <div className="mt-2 space-y-4">
              {prDetails.content}
            </div>
          </div>
          <div className="mb-4">
            <span className="font-semibold text-gray-700">Feedback:</span>
            <p className="mt-2 text-gray-700">{prDetails.feedback}</p>
          </div>
        </div>

      )}
    </div>
  );
};


export default PullRequestDetails;
