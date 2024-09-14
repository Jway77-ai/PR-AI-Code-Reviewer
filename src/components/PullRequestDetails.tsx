import React from 'react';


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
  pullRequest: PullRequest;
}

const PullRequestDetails: React.FC<Props> = ({ pullRequest }) => {
  return (
    <div className="p-6 bg-white shadow-md rounded-lg">
      <h2 className="text-3xl font-bold mb-4 text-gray-800">Pull Request #{pullRequest.pr_id}</h2>
      <div className="mb-4">
        <span className="font-semibold text-gray-700">Source Branch:</span> {pullRequest.sourceBranchName}
      </div>
      <div className="mb-4">
        <span className="font-semibold text-gray-700">Target Branch:</span> {pullRequest.targetBranchName}
      </div>
      <div className="mb-4">
        <span className="font-semibold text-gray-700">Date Created:</span> {new Date(pullRequest.date_created).toLocaleString()}
      </div>
      <div className="mb-4">
        <span className="font-semibold text-gray-700">Content:</span>
        <div className="mt-2 space-y-4">
          {pullRequest.content}
        </div>
      </div>
      <div className="mb-4">
        <span className="font-semibold text-gray-700">Feedback:</span>
        <p className="mt-2 text-gray-700">{pullRequest.feedback}</p>
      </div>
    </div>
  );
};


export default PullRequestDetails;
