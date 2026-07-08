import { useState, useRef } from "react";
import { sendMessage, uploadDocument } from "../services/api";
import type { ChatMessage } from "../types/chat";


export default function Chat() {

  const [messages, setMessages] = useState<ChatMessage[]>([]);

  const [input, setInput] = useState("");

  const [loading, setLoading] = useState(false);

  const [conversationId, setConversationId] =
    useState<string | null>(null);

  const [uploadStatus, setUploadStatus] =
    useState("");

  const fileInputRef =
    useRef<HTMLInputElement | null>(null);



  const handleSend = async () => {

    if (!input.trim() || loading)
      return;


    const userText = input;


    setMessages((prev) => [
      ...prev,
      {
        role: "user",
        content: userText
      }
    ]);


    setInput("");

    setLoading(true);



    try {

      const response = await sendMessage({

        message: userText,

        conversation_id: conversationId

      });



      setConversationId(
        response.conversation_id
      );



      setMessages((prev) => [

        ...prev,

        {
          role: "assistant",
          content: response.reply
        }

      ]);



    } catch {


      setMessages((prev)=>[

        ...prev,

        {
          role:"assistant",
          content:"Something went wrong."
        }

      ]);

    }


    setLoading(false);

  };






  const handleUpload = async(
    e: React.ChangeEvent<HTMLInputElement>
  ) => {


    const file = e.target.files?.[0];


    if(!file)
      return;



    try {


      await uploadDocument(file);


      setUploadStatus(
        `✅ ${file.name} uploaded`
      );



    } catch {


      setUploadStatus(
        "❌ Upload failed"
      );


    }


  };






  return (

    <div className="chat-container">


      <div className="chat-header">

        <h1>
          🤖 Smart Support Assistant
        </h1>

        <p>
          Ask questions from your documents
        </p>

      </div>





      <div className="messages">


        {
          messages.length === 0 && (

            <div className="welcome">

              <h2>
                Welcome 👋
              </h2>

              <p>
                Upload a document and ask questions about it.
              </p>

            </div>

          )
        }



        {
          messages.map((msg,index)=>(

            <div

              key={index}

              className={
                msg.role === "user"
                ?
                "message user-message"
                :
                "message assistant-message"
              }

            >

              {msg.content}

            </div>

          ))
        }


      </div>





      {
        uploadStatus && (

          <div className="upload-status">

            {uploadStatus}

          </div>

        )
      }






      <div className="input-area">


        <input

          type="file"

          hidden

          ref={fileInputRef}

          accept=".pdf,.txt"

          onChange={handleUpload}

        />



        <button

          className="upload-btn"

          onClick={() =>
            fileInputRef.current?.click()
          }

        >

          📎

        </button>





        <input

          type="text"

          placeholder="Ask something..."

          value={input}

          onChange={(e)=>
            setInput(e.target.value)
          }


          onKeyDown={(e)=>{

            if(e.key==="Enter")
              handleSend();

          }}

        />





        <button

          className="send-btn"

          onClick={handleSend}

          disabled={loading}

        >

          {
            loading
            ?
            "..."
            :
            "➤"
          }


        </button>



      </div>



    </div>

  );

}