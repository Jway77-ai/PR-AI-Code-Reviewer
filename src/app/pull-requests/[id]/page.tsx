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
      <div className="flex flex-1 overflow-hidden">
        <div className="flex-1 overflow-auto max-h-[calc(100vh-4rem)] p-8"> {/* Adjusting to account for the header and footer */}
          <PullRequestDetails prId={id} />
        </div>
        <div className="w-1/4 border-l border-gray-200 flex flex-col max-h-[calc(100vh-4rem)]">
          <div className="flex-1 overflow-y-auto p-2 pb-16"> {/* Added bottom padding for the chatbot */}
            <Chatbot prId={id} />
          </div>
        </div>
      </div>
      <Footer className="fixed bottom-0 left-0 right-0" />
    </div>
  );
};

export default PullRequestPage;
