"use client";
import Link from "next/link";
import React, { useEffect, useState } from "react";
import { PullRequest } from "./Dashboard";
import { getStatusColor } from "./Dashboard";
import DateInfo from "./DateInfo";
import FilesChanged from "./FilesChanged";
import ReactMarkdown from "react-markdown";
import remarkGfm from "remark-gfm";

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
        console.log(data);
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
    <div className="max-w-3xl mx-auto p-8 mt-5 bg-white shadow-lg rounded-lg">
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
          <h2 className="text-4xl font-bold text-gray-800 border-b pb-4">
            <Link
              href={prUrl}
              className="text-black-600 hover:bg-purple-200 py-1 px-2 rounded hover:text-black hover:cursor-pointer transition-all duration-300"
              target="_blank"
              rel="noopener noreferrer"
            >
              {prDetails.title}
            </Link>
            <span className="ml-2">#{prDetails.pr_id}</span>
          </h2>
          <div className="flex flex-row items-center">
            <p className="text-gray-600 bg-gray-100 py-1 px-2 rounded hover:bg-purple-200 hover:text-black hover:cursor-pointer transition-all duration-300">
              {prDetails.sourceBranchName}
            </p>
            <span>
              <svg
                width="24"
                height="24"
                viewBox="0 0 24 24"
                role="presentation"
              >
                <path
                  fill="currentColor"
                  fillRule="evenodd"
                  d="M11.793 5.793a1 1 0 0 0 0 1.414L15.586 11H6a1 1 0 0 0 0 2h9.586l-3.793 3.793a1 1 0 0 0 0 1.414c.39.39 1.024.39 1.415 0l5.499-5.5a1 1 0 0 0 .293-.679v-.057a1 1 0 0 0-.293-.678l-5.499-5.5a1 1 0 0 0-1.415 0"
                ></path>
              </svg>
            </span>
            <p className="text-gray-600 bg-gray-100 py-1 px-2 rounded hover:bg-purple-200 hover:text-black hover:cursor-pointer transition-all duration-300">
              {prDetails.targetBranchName}
            </p>
            <p
              className={`ml-2 px-3 py-1 inline-flex text-sm font-semibold rounded-full text-white ${getStatusColor(
                prDetails.status
              )}`}
            >
              {prDetails.status}
            </p>
          </div>
          <div>
            <DateInfo
              createdDate={prDetails.created_date}
              lastModified={prDetails.last_modified}
            />
          </div>
          <div className="mb-8">
            <FilesChanged content={prDetails.content} />
          </div>
          <div className="mb-8">
            <div className="mt-2 text-gray-600 bg-yellow-50 p-4 rounded-lg border border-yellow-200">
              <div className="mt-4">
                <ReactMarkdown
                  remarkPlugins={[remarkGfm]}
                  className={`whitespace-pre-wrap`}
                  components={{
                    code({ node, inline, className, children, ...props }: any) {
                      return !inline ? (
                        <code
                          className={`p-2 whitespace-pre-wrap ${className}`}
                          {...props}
                        >
                          {children}
                        </code>
                      ) : (
                        <code className={`p-1 whitespace-pre-wrap ${className}`} {...props}>
                          {children}
                        </code>
                      );
                    },
                  }}
                >
                  {prDetails.feedback}
                </ReactMarkdown>
              </div>
            </div>
          </div>
        </div>
      )}
    </div>
  );
};

export default PullRequestDetails;
