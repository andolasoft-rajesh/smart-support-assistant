import type { ChatRequest, ChatResponse } from "../types/chat";


const API_URL = "http://127.0.0.1:8000";


// Chat API
export async function sendMessage(
  request: ChatRequest
): Promise<ChatResponse> {

  const response = await fetch(
    `${API_URL}/chat`,
    {
      method: "POST",
      headers:{
        "Content-Type":"application/json",
      },

      body: JSON.stringify(request),
    }
  );


  if(!response.ok){
    throw new Error("Failed to connect to backend");
  }


  return response.json();

}




// Upload document API
export async function uploadDocument(
  file: File
){

  const formData = new FormData();


  formData.append(
    "file",
    file
  );


  const response = await fetch(
    `${API_URL}/documents/upload`,
    {
      method:"POST",
      body:formData,
    }
  );


  if(!response.ok){

    throw new Error(
      "Upload failed"
    );

  }


  return response.json();

}




// Get uploaded documents API
export async function getDocuments(){

  const response = await fetch(
    `${API_URL}/documents/`
  );


  if(!response.ok){

    throw new Error(
      "Failed to fetch documents"
    );

  }


  return response.json();

}