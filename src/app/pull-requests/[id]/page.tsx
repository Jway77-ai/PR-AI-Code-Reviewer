import Chatbot from '@/components/Chatbot';
import Footer from '@/components/Footer';
import Header from '@/components/Header';
import PullRequestDetails from '@/components/PullRequestDetails'; // Adjust the import path as necessary
import { notFound } from 'next/navigation'; // Use for handling not found scenarios

interface PullRequestContent {
  filePath: string;
  changes: {
    added: string[];
    removed: string[];
  };
}

interface PullRequest {
  id: number;
  pr_id: string;
  sourceBranchName: string;
  targetBranchName: string;
  date_created: string;
  content: PullRequestContent[];
  feedback: string;
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
    "123456": {
      id: 1,
      pr_id: "123456",
      sourceBranchName: "feature/test",
      targetBranchName: "test",
      date_created: "2024-09-12T15:49:25.378715",
      content: [
        {
          filePath: "src/main.py",
          changes: {
            added: [
              "print('Hello, world!')",
              "print('Bye, world!')"
            ],
            removed: [
              "print('Remove me')"
            ]
          }
        },
        {
          filePath: "src/quickMaths.py",
          changes: {
            added: [
              "x = 1",
              "y = 2",
              "z = 3"
            ],
            removed: []
          }
        }
      ],
      feedback: "Well done! All changes look good."
    },
    "12345": {
      id: 1,
      pr_id: "12345",
      sourceBranchName: "feature/branch",
      targetBranchName: "main",
      date_created: "2024-09-12T15:49:25.378715",
      content: [
        {
          filePath: "src/main.py",
          changes: {
            added: [
              "print('Hello, world!')",
              "print('Bye, world!')"
            ],
            removed: [
              "print('Remove me')"
            ]
          }
        },
        {
          filePath: "src/quickMaths.py",
          changes: {
            added: [
              "x = 1",
              "y = 2",
              "z = 3"
            ],
            removed: []
          }
        }
      ],
      feedback: "Well done! All changes look good."
    }
  };

  const pullRequest = dummyData[id] || null;

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
