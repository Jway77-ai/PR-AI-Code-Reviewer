import React, { useState } from 'react';
import { FaChevronDown, FaChevronUp } from 'react-icons/fa'; // Importing icons from react-icons

interface FileChangeProps {
  content: string;
}

const FilesChanged: React.FC<FileChangeProps> = ({ content }) => {
  const parseContent = (content: string) => {
    const sections = content.split(/(?=Path: )/).filter(section => section.trim() !== '');
    const fileChanges: { path: string; linesAdded: string; linesRemoved: string }[] = [];

    sections.forEach(section => {
      const lines = section.split('\n');
      let path = '';
      let linesAdded = '';
      let linesRemoved = '';

      lines.forEach((line, index) => {
        if (line.startsWith('Path: ')) {
          path = line.replace('Path: ', '').trim();
        } else if (line.startsWith('Lines Added:')) {
          for (let i = index + 1; i < lines.length && !lines[i].startsWith('Lines Removed:'); i++) {
            linesAdded += lines[i] + '\n';
          }
        } else if (line.startsWith('Lines Removed:')) {
          for (let i = index + 1; i < lines.length; i++) {
            linesRemoved += lines[i] + '\n';
          }
        }
      });

      fileChanges.push({ path, linesAdded: linesAdded.trim(), linesRemoved: linesRemoved.trim() });
    });

    return fileChanges;
  };

  const fileChanges = parseContent(content);

  return (
    <div className="bg-white shadow-lg rounded-lg p-4 mb-6">
      {fileChanges.map(({ path, linesAdded, linesRemoved }, index) => {
        const [isOpen, setIsOpen] = useState(true); // Set initial state to true

        const toggleVisibility = () => setIsOpen(!isOpen);

        return (
          <div key={index} className="mb-4">
            <h3 
              className="font-semibold text-lg border-b pb-2 mb-2 cursor-pointer flex items-center hover:bg-purple-200 py-2 px-2 rounded hover:cursor-pointer transition-all duration-300" 
              onClick={toggleVisibility}
            >
              {/* Arrow icon */}
              <span className="mr-2">
                {isOpen ? (
                  <FaChevronUp />
                ) : (
                  <FaChevronDown />
                )}
              </span>
              {path}
            </h3>
            {isOpen && (
              <div className="text-gray-600">
                <div className="mb-4">
                  <span className="text-green-600 font-semibold">Lines Added:</span>
                  <pre className="bg-green-50 p-2 rounded mt-2 text-sm">
                    <code>{linesAdded || 'No lines added'}</code>
                  </pre>
                </div>
                <div>
                  <span className="text-red-600 font-semibold">Lines Removed:</span>
                  <pre className="bg-red-50 p-2 rounded mt-2 text-sm">
                    <code>{linesRemoved || 'No lines removed'}</code>
                  </pre>
                </div>
              </div>
            )}
          </div>
        );
      })}
    </div>
  );
};

export default FilesChanged;
