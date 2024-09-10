"use client";
import { useState } from "react";
import { Tabs, TabsContent, TabsList, TabsTrigger } from "@/components/ui/tabs";
import Image from "next/image";
import teamLogo from "@/images/team_logo.jpg"; // Correctly using the public folder in Next.js
import { FaExternalLinkAlt, FaTrash } from "react-icons/fa";

const Dashboard: React.FC = () => {
  const [prData, setPrData] = useState<string | null>(null);
  const [error, setError] = useState<string | null>(null);
  const [loading, setLoading] = useState<boolean>(false);

  // Function to fetch data from Flask API through Next.js API route
  const fetchData = async () => {
    setLoading(true); // Set loading state to true when fetching data
    try {
      const response = await fetch("/api/summary"); // Fetch data from the Next.js API route
      if (!response.ok) {
        throw new Error("Error fetching data from backend.");
      }
      const data = await response.json();
      setPrData(data);
      setError(null); // Clear any previous errors
    } catch (err) {
      setError("Error fetching data from backend.");
      console.error(err);
    } finally {
      setLoading(false); // Set loading state back to false after fetching data
    }
  };

  // Dummy data for PR list
  const dummyPRs = [
    { prNumber: 1, repo: "Repo1", dateAdded: "2023-09-01", link: "#" },
    { prNumber: 2, repo: "Repo2", dateAdded: "2023-09-05", link: "#" },
  ];

  const handleDelete = (prNumber: number) => {
    console.log(`Delete PR #${prNumber}`);
    // Here you would typically make an API call to delete the PR from the database
  };

  return (
    <div className="p-6 max-w-5xl mx-auto">
      <div className="flex flex-col items-center">
        <Tabs defaultValue="dashboard" className="w-full mb-6">
          <TabsList className="flex justify-around">
            <TabsTrigger
              value="dashboard"
              className="p-2 text-lg font-medium border-b-2 border-transparent hover:border-blue-500"
            >
              Dashboard
            </TabsTrigger>
            <TabsTrigger
              value="pr-detail"
              className="p-2 text-lg font-medium border-b-2 border-transparent hover:border-blue-500"
            >
              PR Detail
            </TabsTrigger>
            <TabsTrigger
              value="feedback"
              className="p-2 text-lg font-medium border-b-2 border-transparent hover:border-blue-500"
            >
              Feedback
            </TabsTrigger>
          </TabsList>
          <TabsContent value="dashboard" className="mt-4">
            <h1 className="text-3xl font-bold mb-4">Code Review Dashboard</h1>
            <div className="flex justify-center">
              <button
                className="bg-blue-500 text-white py-2 px-4 rounded hover:bg-blue-600"
                onClick={fetchData}
              >
                Fetch Latest PR Review
              </button>
            </div>
            {loading && <p className="text-blue-500 mt-4">Loading...</p>}
            {error && <p className="text-red-500 mt-4">{error}</p>}
            {prData && (
              <div className="mt-6">
                <h2 className="text-xl font-semibold mb-2">
                  Latest Pull Request Review:
                </h2>
                <pre className="bg-gray-100 p-4 rounded">
                  {JSON.stringify(prData, null, 2)}
                </pre>
              </div>
            )}
            <div className="mt-6">
              <h2 className="text-xl font-semibold mb-2">
                Pull Requests [Dummy Data Now]
              </h2>
              <table className="w-full text-left border-collapse">
                <thead>
                  <tr>
                    <th className="border-b-2 p-2">Pull Request</th>
                    <th className="border-b-2 p-2">Date Added</th>
                    <th className="border-b-2 p-2">Action</th>
                  </tr>
                </thead>
                <tbody>
                  {dummyPRs.map((pr) => (
                    <tr key={pr.prNumber}>
                      <td className="border-b p-2">{`${pr.repo} #${pr.prNumber}`}</td>
                      <td className="border-b p-2">
                        {new Date(pr.dateAdded).toLocaleString()}
                      </td>
                      <td className="border-b p-2">
                        <a
                          href={pr.link}
                          target="_blank"
                          rel="noopener noreferrer"
                          className="text-blue-500 mr-2"
                        >
                          <FaExternalLinkAlt />
                        </a>
                        <button
                          onClick={() => handleDelete(pr.prNumber)}
                          className="text-red-500"
                        >
                          <FaTrash />
                        </button>
                      </td>
                    </tr>
                  ))}
                </tbody>
              </table>
            </div>
          </TabsContent>
          <TabsContent value="pr-detail" className="mt-4">
            <h2 className="text-2xl font-bold mb-2">PR Detail Page</h2>
            <p>Content for PR Detail page goes here.</p>
          </TabsContent>
          <TabsContent value="feedback" className="mt-4">
            <h2 className="text-2xl font-bold mb-2">Feedback Page</h2>
            <p>Content for Feedback page goes here.</p>
          </TabsContent>
        </Tabs>
      </div>
      <div className="flex items-center justify-center mt-8">
        <Image
          src={teamLogo}
          alt="Team Logo"
          width={200}
          height={200}
          className="rounded-full"
        />
      </div>
      <div className="flex justify-center mt-4">
        <a
          href="https://github.com/Jianwei07/debuggingDragons/tree/main"
          target="_blank"
          rel="noopener noreferrer"
          className="text-blue-500 underline"
        >
          GitHub Link
        </a>
      </div>
    </div>
  );
};

export default Dashboard;
