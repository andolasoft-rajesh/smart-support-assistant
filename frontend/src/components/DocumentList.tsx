import { useEffect, useState } from "react";
import { getDocuments } from "../services/api";


interface Document {
  id: string;
  filename: string;
  uploaded_at: string;
  chunk_count: number;
}


export default function DocumentList() {

  const [documents, setDocuments] = useState<Document[]>([]);


  useEffect(() => {

    const loadDocuments = async () => {

      try {

        const data = await getDocuments();

        setDocuments(data);

      } catch (error) {

        console.log(
          "Error loading documents",
          error
        );

      }

    };


    loadDocuments();

  }, []);



  return (

    <div className="card">

      <h2>
        📄 Uploaded Documents
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

              <br />

              <small>
                Chunks: {doc.chunk_count}
              </small>


            </div>

          ))

        )
      }


    </div>

  );

}