import React, { useState } from 'react';
import { FaChevronDown, FaChevronUp } from 'react-icons/fa'; // Importing icons from react-icons

interface FileChangeProps {
  content: string;
}

const FilesChanged: React.FC<FileChangeProps> = ({ content }) => {
  const parseContent = (content: string) => {
    const sections = content.split(/(?=Path: )/).filter(section => section.trim() !== '');
    const fileChanges: { path: string; originalContents: string; }[] = [];

    sections.forEach(section => {
      const lines = section.split('\n');
      let path = '';
      let originalContents = '';

      lines.forEach((line, index) => {
        if (line.startsWith('Path: ')) {
          path = line.replace('Path: ', '').trim();
        } else if (line.startsWith('Original Contents of file:')) {
          for (let i = index + 1; i < lines.length && !lines[i].startsWith('Lines Added:'); i++) {
            originalContents += lines[i] + '\n';
          }
        } 
      });

      fileChanges.push({ path, originalContents: originalContents.trim() });
    });

    return fileChanges;
  };

  const fileChanges = parseContent(content);
  const [openStates, setOpenStates] = useState<boolean[]>(Array(fileChanges.length).fill(false)); // Track open states

  const toggleVisibility = (index: number) => {
    setOpenStates(prev => {
      const newStates = [...prev];
      newStates[index] = !newStates[index];
      return newStates;
    });
  };

  return (
    <div className="bg-white shadow-lg rounded-lg p-4 mb-6">
      {fileChanges.map(({ path, originalContents }, index) => (
        <div key={index} className="mb-4">
          <h3 
            className="font-semibold text-lg border-b pb-2 mb-2 cursor-pointer flex items-center hover:bg-purple-200 py-2 px-2 rounded transition-all duration-300" 
            onClick={() => toggleVisibility(index)} // Toggle the specific file change
          >
            {/* Arrow icon */}
            <span className="mr-2">
              {openStates[index] ? (
                <FaChevronUp />
              ) : (
                <FaChevronDown />
              )}
            </span>
            {path}
          </h3>
          {openStates[index] && (
            <div className="text-gray-600">
              <div>
                <pre className="bg-blue-50 p-2 rounded mt-2 text-sm">
                  <code>{originalContents || 'This is a new file with no original contents'}</code>
                </pre>
              </div>
            </div>
          )}
        </div>
      ))}
    </div>
  );
};

export default FilesChanged;
