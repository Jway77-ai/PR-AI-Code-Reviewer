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
    <div className="min-h-screen">
      <Header />
      <div className="flex flex-row flex-1 overflow-hidden">
        <div className="flex-1 w-max overflow-auto max-h-[calc(100vh-4rem)] p-8"> {/* Adjusting to account for the header and footer */}
          <PullRequestDetails prId={id} />
        </div>
        <div className="w-1/4 border-l border-gray-200 flex flex-col max-h-[calc(100vh-4rem)]">
          <div className="flex-1 overflow-y-auto p-2 pb-16">
            <Chatbot prId={id} />
          </div>
        </div>
      </div>
      <Footer />
    </div>
  );
};

export default PullRequestPage;
