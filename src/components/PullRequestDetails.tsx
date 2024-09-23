"use client";
import Link from "next/link";
import React, { useEffect, useState } from "react";
import { PullRequest } from "./Dashboard";



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

  // Dynamically construct the PR URL
  const prUrl = `https://bitbucket.org/debugging-dragons/webhook-codedoc/pull-requests/${prId}`;

  return (
    <div className="max-w-3xl mx-auto p-8 bg-white shadow-lg rounded-lg">
      {loading && (
        <div className="flex justify-center items-center h-64">
          <div className="animate-spin rounded-full h-16 w-16 border-t-2 border-b-2 border-blue-500"></div>
        </div>
      )}
      {error && (
        <div className="bg-red-100 border-l-4 border-red-500 text-red-700 p-4 mb-6" role="alert">
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
                Title
              </h3>
              <p className="text-gray-600 bg-gray-100 p-2 rounded">
                {prDetails.title}
              </p>
            </div>
          </div>
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
            <div>
              <h3 className="text-lg font-semibold text-gray-700 mb-2">
                Status
              </h3>
              <p className="text-gray-600">{prDetails.status}</p>
            </div>
          </div>
          <div className="grid grid-cols-2 gap-6 mb-8">
            <div>
              <h3 className="text-lg font-semibold text-gray-700 mb-2">
                Date Created
              </h3>
              <p className="text-gray-600">
                {prDetails.created_date}
              </p>
            </div>
            <div>
              <h3 className="text-lg font-semibold text-gray-700 mb-2">
                Date Modified
              </h3>
              <p className="text-gray-600">
                {prDetails.last_modified}
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
              PR URL:
            </h3>
            <Link
              href={prUrl}
              className="text-blue-600 hover:underline"
              target="_blank"
              rel="noopener noreferrer"
            >
              {prUrl}
            </Link>
          </div>
          <div className="mb-8">
            <h3 className="text-lg font-semibold text-gray-700 mb-2">Content</h3>
            <div className="mt-2 space-y-4 bg-gray-50 p-4 rounded-lg border border-gray-200">
              {prDetails.content}
            </div>
          </div>
          <div className="mb-8">
            <h3 className="text-lg font-semibold text-gray-700 mb-2">Feedback</h3>
            <p className="mt-2 text-gray-600 bg-yellow-50 p-4 rounded-lg border border-yellow-200">{prDetails.feedback}</p>
          </div>
        </div>
      )}
    </div>
  );
};


export default PullRequestDetails;
