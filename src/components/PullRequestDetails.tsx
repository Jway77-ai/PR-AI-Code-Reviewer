"use client";
import React, { useEffect, useState } from "react";

interface PullRequest {
  id: number;
  title: string;
  status: string;
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
      setLoading(true);
      try {
        console.log(prId);
        const response = await fetch(`/api/pr/${prId}`);
        if (!response.ok) {
          throw new Error(
            `Failed to fetch pull request details: ${response.status} ${response.statusText}`
          );
        }
        const data = await response.json();
        setPrDetails(data);
      } catch (err) {
        // Use a type guard to narrow down the type of `err`
        if (err instanceof Error) {
          setError(`Error fetching data from backend: ${err.message}`);
          console.error("Error details:", err.message); // Log the error message
        } else {
          setError("An unknown error occurred.");
          console.error("Error details:", err); // Log the full error object if it is not an instance of Error
        }
      } finally {
        setLoading(false);
      }
    };

    fetchData();
  }, [prId]);

  return (
    <div className="max-w-3xl mx-auto p-8 bg-white shadow-lg rounded-lg">
      {loading && (
        <div className="flex justify-center items-center h-64">
          <div className="animate-spin rounded-full h-16 w-16 border-t-2 border-b-2 border-blue-500"></div>
        </div>
      )}
      {error && (
        <div
          className="bg-red-100 border-l-4 border-red-500 text-red-700 p-4 mb-6"
          role="alert"
        >
          <p className="font-bold">Error</p>
          <p>{error}</p>
        </div>
      )}
      {prDetails && (
        <div>
          <h2 className="text-4xl font-bold mb-6 text-gray-800 border-b pb-4">
            Pull Request #{prDetails.pr_id}
          </h2>
          <div className="grid grid-cols-2 gap-6 mb-8">
            <div>
              <h3 className="text-lg font-semibold text-gray-700 mb-2">
                Source Branch
              </h3>
              <p className="text-gray-600 bg-gray-100 p-2 rounded">
                {prDetails.sourceBranchName}
              </p>
            </div>
            <div>
              <h3 className="text-lg font-semibold text-gray-700 mb-2">
                Target Branch
              </h3>
              <p className="text-gray-600 bg-gray-100 p-2 rounded">
                {prDetails.targetBranchName}
              </p>
            </div>
          </div>
          <div className="grid grid-cols-2 gap-6 mb-8">
            <div>
              <h3 className="text-lg font-semibold text-gray-700 mb-2">
                Date Created
              </h3>
              <p className="text-gray-600">
                {new Date(prDetails.date_created).toLocaleString()}
              </p>
            </div>
            <div>
              <h3 className="text-lg font-semibold text-gray-700 mb-2">
                Status
              </h3>
              <p className="text-gray-600">{prDetails.status}</p>
            </div>
          </div>
          <div className="mb-8">
            <h3 className="text-lg font-semibold text-gray-700 mb-2">
              Content
            </h3>
            <div className="mt-2 space-y-4 bg-gray-50 p-4 rounded-lg border border-gray-200">
              {prDetails.content}
            </div>
          </div>
          <div className="mb-8">
            <h3 className="text-lg font-semibold text-gray-700 mb-2">
              Feedback
            </h3>
            <p className="mt-2 text-gray-600 bg-yellow-50 p-4 rounded-lg border border-yellow-200">
              {prDetails.feedback}
            </p>
          </div>
        </div>
      )}
    </div>
  );
};

export default PullRequestDetails;
