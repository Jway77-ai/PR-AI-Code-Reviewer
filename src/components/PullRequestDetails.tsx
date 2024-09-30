"use client";
import Link from "next/link";
import React, { useEffect, useState } from "react";
import { PullRequest, getStatusColor } from "@/components/Dashboard";
import DateInfo from "@/components/DateInfo";
import FilesChanged from "@/components/FilesChanged";
import PullRequestDiff from "@/components/PullRequestDiff";

interface Props {
  prId: string;
}

// Function to escape HTML in code blocks
const escapeHtml = (str: string) => {
  return str
    .replace(/&/g, "&amp;")
    .replace(/</g, "&lt;")
    .replace(/>/g, "&gt;")
    .replace(/"/g, "&quot;")
    .replace(/'/g, "&#039;");
};

// Extended markdown parser to handle code blocks with styling
const parseMarkdown = (text: string) => {
  // Replace code blocks ```code``` with styled <pre><code> block
  text = text.replace(
    /```([\s\S]*?)```/g,
    (match, p1) =>
      `<pre class="bg-gray-100 p-4 rounded-lg overflow-x-auto"><code>${escapeHtml(
        p1
      )}</code></pre>`
  );

  // Replace inline code `code` with <code> and escape HTML
  text = text.replace(/`([^`]+)`/g, (match, p1) => `<code>${escapeHtml(p1)}</code>`);

  // Replace bold syntax **bold** with <strong>bold</strong>
  text = text.replace(/\*\*(.*?)\*\*/g, "<strong>$1</strong>");

  // Replace italics syntax *italic* with <em>italic</em>
  text = text.replace(/\*(.*?)\*/g, "<em>$1</em>");

  // Replace line breaks with <br />
  text = text.replace(/\n/g, "<br />");

  return text;
};

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
    <div className="max-w-full mx-auto p-8 mt-5 bg-white shadow-lg rounded-lg">
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
            <span className="ml-2">
              #{prDetails.pr_id}
            </span>
          </h2>
          <div className="flex flex-row items-center mt-3">
            <p className="text-gray-600 py-1 px-2 rounded hover:bg-purple-200 hover:text-black hover:cursor-pointer transition-all duration-300">
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
            <p className="text-gray-600 py-1 px-2 rounded hover:bg-purple-200 hover:text-black hover:cursor-pointer transition-all duration-300">
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
          <div className="mb-3">
            <DateInfo createdDate={prDetails.created_date} lastModified={prDetails.last_modified} />
          </div>
          <div className="mb-8">
            <PullRequestDiff pullRequestDiff={prDetails.rawDiff} />
          </div>
          <div className="mb-8">
            <h3 className="text-lg font-semibold text-gray-700 mb-2">
              Original Contents:
            </h3>
            <FilesChanged content={prDetails.content} />
          </div>
          <div className="mb-8">
            <h3 className="text-lg font-semibold text-gray-700 mb-2">
              Feedback
            </h3>
            <div className="mt-2 text-gray-600 bg-yellow-50 p-4 rounded-lg border border-yellow-200">
              <div className="mt-4">
                <div
                  dangerouslySetInnerHTML={{ __html: parseMarkdown(prDetails.feedback) }}
                >
                </div>
              </div>
            </div>
          </div>
        </div>
      )}
    </div>
  );
};

export default PullRequestDetails;
