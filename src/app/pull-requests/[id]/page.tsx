import Chatbot from '@/components/Chatbot';
import Footer from '@/components/Footer';
import Header from '@/components/Header';
import PullRequestDetails from '@/components/PullRequestDetails'; // Adjust the import path as necessary
import { notFound } from 'next/navigation'; // Use for handling not found scenarios

interface PullRequest {
  id: number;
  pr_id: string;
  sourceBranchName: string;
  targetBranchName: string;
  date_created: string;
  content: string;
  feedback: string;
}

const PullRequestPage = async ({ params }: {
  params: {
    id: string;
  }
}) => {
  const { id } = params;

  // Dummy data
  const dummyData: Record<string, PullRequest> = {
    [id]: {
      id: Number([id]),
      pr_id: id,
      sourceBranchName: "feature/test",
      targetBranchName: "main",
      date_created: "2023-09-01T08:00:00Z",
      content: "this is a test",
      feedback: "Well done! All changes look good.",
    }
  };

  const pullRequest = dummyData[id] || null;

  if (!pullRequest) {
    notFound(); // Redirect to a 404 page if the PR is not found
  }

  return (
    <div className='flex flex-col min-h-screen'>
        <Header />
        <PullRequestDetails pullRequest={pullRequest} />
        <Chatbot />
        <Footer />
    </div>
  );
};

export default PullRequestPage;
