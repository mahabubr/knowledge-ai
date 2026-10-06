"use client";

import MarkdownUploader from "@/components/MarkdownUploader";
import { useState } from "react";

const page = () => {
  const [file, setFile] = useState<File | null>(null);
  const [loading, setLoading] = useState(false);


  const uploadFile = async () => {
    if (!file) {
      alert("Please select a file");
      return;
    }

    const formData = new FormData();

    formData.append("file", file);

    try {
      setLoading(true);

      const res = await fetch("http://localhost:8000/information", {
        method: "POST",
        body: formData,
      });

      await res.json();

      window.location.reload();
    } catch (error) {
      console.error(error);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="flex h-full w-full flex-col items-center justify-center">
      <MarkdownUploader onFileSelect={(file) => setFile(file)} />

      <button
        onClick={uploadFile}
        disabled={loading}
        className="mt-4 rounded bg-black px-4 py-2 text-white"
      >
        {loading ? "Uploading..." : "Upload"}
      </button>
    </div>
  );
};

export default page;
