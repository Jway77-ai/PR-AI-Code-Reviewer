"use client";
import { useState, useEffect } from "react";
import { FaSync, FaExternalLinkAlt } from "react-icons/fa";
import Link from "next/link";

export interface PullRequest {
  pr_id: number;
  title: string;
  status: string;
  sourceBranchName: string;
  targetBranchName: string;
  created_date: string;
  last_modified: string;
  content: string;
  feedback: string;
}

export const getStatusColor = (status: string) => {
  switch (status.toLowerCase()) {
    case "open":
      return "bg-green-500";
    case "merged":
      return "bg-purple-500";
    case "declined":
      return "bg-red-500";
    default:
      return "bg-gray-500";
  }
};

const Dashboard: React.FC = () => {
  const [prData, setPrData] = useState<PullRequest[] | null>(null);
  const [error, setError] = useState<string | null>(null);
  const [loading, setLoading] = useState<boolean>(false);

  const fetchData = async () => {
    setLoading(true);
    try {
      const response = await fetch("/api/summary");
      if (!response.ok) {
        throw new Error("Error fetching data from backend.");
      }
      const data = await response.json();
      if (data.entries && Array.isArray(data.entries)) {
        console.log(data);
        const fetchedData = data.entries.sort(
          (a: PullRequest, b: PullRequest) =>
            new Date(b.last_modified).getTime() -
            new Date(a.last_modified).getTime()
        );
        setPrData(fetchedData);
      } else {
        setError("Invalid data format received from the API.");
      }
    } catch (err) {
      setError("Error fetching data from backend.");
      console.error(err);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchData();
  }, []);

  const formatDate = (dateString: string) => {
    const options: Intl.DateTimeFormatOptions = {
      year: "numeric",
      month: "short",
      day: "numeric",
      hour: "2-digit",
      minute: "2-digit",
      hour12: true,
    };
    return new Date(dateString).toLocaleString("en-US", options);
  };

  return (
    <div className="p-6 max-w-7xl mx-auto flex-grow">
      <div className="flex flex-col items-center">
        <h1 className="text-3xl font-bold mb-6 text-gray-800">Code Review Dashboard</h1>
        
        <button
          className="bg-blue-500 text-white py-2 px-4 rounded-full hover:bg-blue-600 transition duration-300 flex items-center space-x-2 mb-6"
          onClick={fetchData}
          disabled={loading}
        >
          <FaSync className={`${loading ? 'animate-spin' : ''}`} />
          <span>{loading ? 'Fetching...' : 'Fetch Latest PR Reviews'}</span>
        </button>

        {error && (
          <div className="bg-red-100 border-l-4 border-red-500 text-red-700 p-4 mb-6 rounded" role="alert">
            <p>{error}</p>
          </div>
        )}

        {prData && (
          <div className="w-full bg-white shadow-md rounded-lg overflow-hidden">
            <div className="px-6 py-2 bg-gray-50">
              <h2 className="text-xl font-semibold text-gray-800">Latest Pull Request Reviews</h2>
            </div>
            <div className="px-6 py-4 bg-gray-50 border-b border-gray-200">
              <Link href={`https://bitbucket.org/debugging-dragons/webhook-codedoc/src/main/`} className="hover:underline">
                <div className="text-sm font-medium text-blue-600">Bitbucket Repo: webhook-codeDoc</div>
              </Link>
            </div>
            <div className="overflow-x-auto">
              <table className="w-full text-left">
                <thead className="bg-gray-100">
                  <tr>
                    <th className="px-6 py-3 text-xs font-medium text-gray-500 uppercase tracking-wider">
                      Pull Request Title
                    </th>
                    <th className="px-6 py-3 text-xs font-medium text-gray-500 uppercase tracking-wider">
                      PR ID
                    </th>
                    <th className="px-6 py-3 text-xs font-medium text-gray-500 uppercase tracking-wider">
                      Status
                    </th>
                    <th className="px-6 py-3 text-xs font-medium text-gray-500 uppercase tracking-wider">
                      Created Date
                    </th>
                    <th className="px-6 py-3 text-xs font-medium text-gray-500 uppercase tracking-wider">
                      Last Modified
                    </th>
                    <th className="px-6 py-3 text-xs font-medium text-gray-500 uppercase tracking-wider">
                      Code Review
                    </th>
                  </tr>
                </thead>
                <tbody className="divide-y divide-gray-200">
                  {prData?.length > 0 ? (
                    prData.map((pr) => (
                      <tr key={pr.pr_id} className="hover:bg-gray-50">
                        <td className="px-6 py-4 whitespace-normal">
                          <Link
                            href={`https://bitbucket.org/debugging-dragons/webhook-codedoc/pull-requests/${pr.pr_id}`}
                            className="hover:underline"
                          >
                            <div className="text-sm font-medium text-blue-600">
                              {pr.title}
                            </div>
                          </Link>
                        </td>
                        <td className="px-6 py-4 whitespace-normal">
                          <div className="text-sm text-gray-500">
                            #{pr.pr_id}
                          </div>
                        </td>
                        <td className="px-6 py-4 whitespace-nowrap">
                          <span
                            className={`px-2 inline-flex text-xs leading-5 font-semibold rounded-full text-white ${getStatusColor(
                              pr.status
                            )}`}
                          >
                            {pr.status}
                          </span>
                        </td>
                        <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-500">
                          {formatDate(pr.created_date)}
                        </td>
                        <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-500">
                          {formatDate(pr.last_modified)}
                        </td>
                        <td className="px-6 py-4 whitespace-nowrap text-right text-sm font-medium">
                          <Link href={`/pull-requests/${pr.pr_id}`} className="text-blue-600 hover:text-blue-900">
                            <FaExternalLinkAlt className="inline mr-1" />
                            View
                          </Link>
                        </td>
                      </tr>
                    ))
                  ) : (
                    <tr>
                      <td
                        colSpan={6}
                        className="px-6 py-4 text-center text-sm text-gray-500"
                      >
                        No pull requests available.
                      </td>
                    </tr>
                  )}
                </tbody>
              </table>
            </div>
          </div>
        )}
      </div>
    </div>
  );
};

export default Dashboard;
