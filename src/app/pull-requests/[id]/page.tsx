import Chatbot from '@/components/Chatbot';
import Footer from '@/components/Footer';
import Header from '@/components/Header';
import PullRequestDetails from '@/components/PullRequestDetails';

const PullRequestPage = async ({ params }: {
  params: {
    id: string;
  }
}) => {
  const { id } = params;

  return (
    <div className='flex flex-col min-h-screen'>
        <Header />
        <PullRequestDetails prId={id} />
        <Chatbot />
        <Footer />
    </div>
  );
};

export default PullRequestPage;
