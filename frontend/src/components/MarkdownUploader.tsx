"use client";

import { useState, ChangeEvent } from "react";
import ReactMarkdown from "react-markdown";

interface IProps {
  onFileSelect: (file: File) => void;
}

const MarkdownUploader = ({ onFileSelect }: IProps) => {
  const [fileName, setFileName] = useState<string>("");
  const [content, setContent] = useState<string>("");

  const handleUpload = (e: ChangeEvent<HTMLInputElement>) => {
    const file = e.target.files?.[0];

    if (!file) return;

    if (!file.name.endsWith(".md")) {
      alert("Please upload a markdown (.md) file");
      return;
    }

    setFileName(file.name);
    onFileSelect(file);

    const reader = new FileReader();

    reader.onload = (event: ProgressEvent<FileReader>) => {
      const text = event.target?.result;

      if (typeof text === "string") {
        setContent(text);
      }
    };

    reader.readAsText(file);
  };

  return (
    <div className="mx-auto max-w-3xl p-6">
      <div className="rounded-lg border p-5 shadow">
        <h2 className="mb-4 text-xl font-bold">Upload Markdown File</h2>

        <input
          type="file"
          accept=".md"
          onChange={handleUpload}
          className="mb-4"
        />

        {fileName && (
          <p className="mb-4 text-sm text-gray-600">Uploaded: {fileName}</p>
        )}

        {content && (
          <div className="border-t pt-4">
            <h3 className="mb-3 font-semibold">Preview</h3>

            <div className="prose max-w-none">
              <ReactMarkdown>{content}</ReactMarkdown>
            </div>
          </div>
        )}
      </div>
    </div>
  );
};

export default MarkdownUploader;
