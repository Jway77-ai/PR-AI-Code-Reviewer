import { notFound } from 'next/navigation'; // Use for handling not found scenarios
import PullRequestDetails from '@/components/PullRequestDetails'; // Adjust the import path as necessary
import Header from '@/components/Header';
import Footer from '@/components/Footer';

interface PullRequest {
  prNumber: number;
  repo: string;
  dateAdded: string;
  details: string; // Example field for PR details
}

interface Props {
  params: {
    id: string;
  };
}

const PullRequestPage = async ({ params }: Props) => {
  const { id } = params;

  // Dummy data
  const dummyData: Record<string, PullRequest> = {
    "1": {
      prNumber: 1,
      repo: "Repo1",
      dateAdded: "2023-09-01T08:00:00Z",
      details: "Details for PR #1",
    },
    "2": {
      prNumber: 2,
      repo: "Repo2",
      dateAdded: "2023-09-05T08:00:00Z",
      details: "Details for PR #2",
    },
    "12345": {
      prNumber: 12345,
      repo: "WIP",
      dateAdded: "2023-09-05T08:00:00Z",
      details: "Still WIP. Hardcoded",
    }
  };

  const pullRequest = dummyData[id] || null;

  if (!pullRequest) {
    notFound(); // Redirect to a 404 page if the PR is not found
  }

  return (

    <div className='flex flex-col min-h-screen'>
        <Header />
        <div className="p-6 max-w-4xl mx-auto flex-grow">
          <h1 className="text-3xl font-bold mb-4">Pull Request Details</h1>
          <PullRequestDetails pullRequest={pullRequest} />
        </div>
        <Footer />
    </div>
  );
};

export default PullRequestPage;
