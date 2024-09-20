import Chatbot from "@/components/Chatbot";
import Footer from "@/components/Footer";
import Header from "@/components/Header";
import PullRequestDetails from "@/components/PullRequestDetails";

const PullRequestPage = async ({
  params,
}: {
  params: {
    id: string;
  };
}) => {
  const { id } = params;

  if (!id) {
    return <div>Error: No PR ID provided</div>;
  }

  return (
    <div className="flex flex-col min-h-screen">
      <Header />
      <PullRequestDetails prId={id} />
      <Chatbot prId={id} />
      <Footer />
    </div>
  );
};

export default PullRequestPage;
