import { useState } from "react";
import { uploadDocument } from "../services/api";


export default function UploadDocument(){

  const [file,setFile] = useState<File | null>(null);
  const [message,setMessage] = useState("");


  const handleUpload = async () => {

    if(!file){
      setMessage("Select a file first");
      return;
    }


    try{

      await uploadDocument(file);

      setMessage(
        "✅ Document uploaded successfully"
      );

    }
    catch{

      setMessage(
        "❌ Upload failed"
      );

    }

  };


  return(

    <div className="card upload-card">


      <h2>
        📂 Upload Document
      </h2>



      <input

        type="file"

        accept=".txt,.pdf"

        onChange={(e)=>
          setFile(
            e.target.files?.[0] || null
          )
        }

      />



      <button onClick={handleUpload}>

        Upload

      </button>



      <p>
        {message}
      </p>


    </div>

  );

}