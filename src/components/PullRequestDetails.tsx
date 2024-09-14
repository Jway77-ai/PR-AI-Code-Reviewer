import { FC } from 'react';

interface PullRequest {
  prNumber: number;
  repo: string;
  dateAdded: string;
  details: string; // Example field for PR details
}

interface Props {
  pullRequest: PullRequest;
}

const PullRequestDetails: FC<Props> = ({ pullRequest }) => {
  return (
    <div className="bg-white p-6 rounded shadow-md ">
      <h2 className="text-2xl font-semibold mb-2">{`${pullRequest.repo} #${pullRequest.prNumber}`}</h2>
      <p className="text-gray-700 mb-2"><strong>Date Added:</strong> {new Date(pullRequest.dateAdded).toLocaleString()}</p>
      <p className="text-gray-700 mb-4"><strong>Details:</strong> {pullRequest.details}</p>
    </div>
  );
};

export default PullRequestDetails;
