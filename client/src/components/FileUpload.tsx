import React from "react";
import { useState } from "react";

export default function FileUpload({
  onFileUpload,
}: {
  onFileUpload: (file: File) => Promise<boolean>;
}) {
  const [file, setFile] = useState<File | null>(null);
  const [message, setMessage] = useState<string | null>(null);
  const [renderKey, setRenderKey] = useState<Date>(new Date());

  const handleFileChange = async (event: React.ChangeEvent<HTMLInputElement>) => {
    const selectedFile = event.target.files?.[0];
    if (selectedFile) {
      if (selectedFile.type !== "text/csv") {
        setRenderKey(new Date());
        setMessage(`Invalid file type (${selectedFile.type}). Please select a CSV file.`);
        setFile(null);
        return;
      }
      setFile(selectedFile);
      const valid = await onFileUpload(selectedFile);
      if (!valid) {
        setRenderKey(new Date());
        setMessage("Invalid file");
        setFile(null);
        return;
      }
      setMessage(`File selected on ${renderKey.toLocaleTimeString()}: ${selectedFile.name}`);
    } else {
      setMessage("No file selected");
      setFile(null);
      setRenderKey(new Date());
    }
  };

  return (
    <div>
      <h2>Upload a File</h2>
      <form>
        <input
          type="file"
          key={renderKey.toISOString()}
          accept=".csv"
          onChange={(e) => {
            handleFileChange(e);
          }}
        />
        <button
          type="button"
          onClick={() => {
            if (file) {
              onFileUpload(file);
            }
          }}
        >
          Upload
        </button>
      </form>
      {message && <p>{message}</p>}
    </div>
  );
}
