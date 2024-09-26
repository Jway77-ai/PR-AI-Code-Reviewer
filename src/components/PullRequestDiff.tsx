import React, { useEffect } from 'react';
import * as Diff2Html from 'diff2html';
import 'diff2html/bundles/css/diff2html.min.css';

interface PullRequestDiffProps {
  pullRequestDiff: string; 
}

const PullRequestDiff: React.FC<PullRequestDiffProps> = ({ pullRequestDiff }) => {
  useEffect(() => {
    if (pullRequestDiff) {
      console.log('Raw diff data:', pullRequestDiff);
      const diffHtml = Diff2Html.html(pullRequestDiff, {
        matching: 'lines',
        drawFileList: true
      });
      document.getElementById('diffContainer')!.innerHTML = diffHtml; // Set the HTML content of the diff container
    }
    else {
      console.log('No Raw diff data:');
    }
  }, [pullRequestDiff]);

  return (
    <div className="relative overflow-auto max-h-[500px]"> {/* Control overflow and max height */}
      <div id="diffContainer" className="bg-white shadow-lg rounded-lg p-4"></div>
    </div>
  );
};

export default PullRequestDiff;