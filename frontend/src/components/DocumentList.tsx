import { useEffect, useState, useCallback } from "react";
import { getDocuments } from "../services/api";

interface Document {
  id: string;
  filename: string;
  uploaded_at: string;
  chunk_count: number;
}

export default function DocumentList() {

  const [documents, setDocuments] =
    useState<Document[]>([]);

  const loadDocuments = useCallback(async () => {

    try {

      const data = await getDocuments();

      setDocuments(data);

    } catch (error) {

      console.log(
        "Error loading documents",
        error
      );

    }

  }, []);

  useEffect(() => {

    loadDocuments();

  }, [loadDocuments]);

  return (

    <div className="card">

      <h2>
        History
      </h2>

      {

        documents.length === 0 ? (

          <p>
            No documents uploaded
          </p>

        ) : (

          documents.map((doc) => (

            <div
              key={doc.id}
              className="document-item"
            >

              📄 {doc.filename}

            </div>

          ))

        )

      }

    </div>

  );

}