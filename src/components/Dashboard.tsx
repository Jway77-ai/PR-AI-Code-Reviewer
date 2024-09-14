"use client";
import { useState, useEffect } from "react";
import { FaExternalLinkAlt, FaTrash } from "react-icons/fa";
import Link from "next/link";

interface PullRequest {
  id: number;
  pr_id: string;
  sourceBranchName: string;
  targetBranchName: string;
  date_created: string;
  content: string;
  feedback: string;
}

const Dashboard: React.FC = () => {
  const [prData, setPrData] = useState<PullRequest[] | null>(null);
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
      console.log(data);
      if (data.entries && Array.isArray(data.entries)) {
        const fetchedData = data.entries;
        setPrData(fetchedData);
        localStorage.setItem("prData", JSON.stringify(fetchedData)); // Save data to localStorage
      } else {
        setError("Invalid data format received from the API.");
      }
    } catch (err) {
      setError("Error fetching data from backend.");
      console.error(err);
    } finally {
      setLoading(false); // Set loading state back to false after fetching data
    }
  };

  // Automatically fetch data on component load
  useEffect(() => {
    fetchData();
  }, []);

  const handleDelete = (prId: number) => {
    console.log(`Delete PR #${prId}`);
    // Here you would typically make an API call to delete the PR from the database
  };

  return (
    <div className="p-6 max-w-5xl mx-auto flex-grow">
      <div className="flex flex-col items-center">
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
            <h2 className="text-xl font-semibold mb-2">Latest Pull Request Review:</h2>
            <table className="w-full text-left border-collapse">
              <thead>
                <tr>
                  <th className="border-b-2 p-2">Pull Request</th>
                  <th className="border-b-2 p-2">Date Added</th>
                  <th className="border-b-2 p-2">Action</th>
                </tr>
              </thead>
              <tbody>
                {prData?.length > 0 ? (
                  prData.map((pr) => (
                    <tr key={pr.id}>
                      <td className="border-b p-2">{`${pr.sourceBranchName} to ${pr.targetBranchName} (#${pr.pr_id})`}</td>
                      <td className="border-b p-2">
                        {new Date(pr.date_created).toLocaleString()}
                      </td>
                      <td className="border-b p-2 flex flex-row">
                        <Link href={`/pull-requests/${pr.pr_id}`}>
                          <FaExternalLinkAlt />
                        </Link>
                        <button
                          onClick={() => handleDelete(pr.id)}
                          className="text-red-500 ml-2"
                        >
                          <FaTrash />
                        </button>
                      </td>
                    </tr>
                  ))
                ) : (
                  <p className="text-gray-500 mt-4">No pull requests available.</p>
                )}
              </tbody>
            </table>
          </div>
        )}
      </div>
    </div>
  );
};

export default Dashboard;
