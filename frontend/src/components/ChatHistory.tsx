import { useEffect, useState } from "react";
import {
  getConversations,
  getDocuments,
  getConversationByDocument
} from "../services/api";


interface Conversation {
  id: string;
  title: string;
  created_at: string;
}


interface Document {
  id: string;
  filename: string;
}


interface Props {

  onSelectConversation: (id: string) => void;

  refresh: number;

}



export default function ChatHistory({

  onSelectConversation,
  refresh

}: Props) {


  const [conversations, setConversations] =
    useState<Conversation[]>([]);


  const [documents, setDocuments] =
    useState<Document[]>([]);



  useEffect(() => {


    const loadHistory = async () => {


      try {


        const chats = await getConversations();

        setConversations(chats);



        const docs = await getDocuments();

        setDocuments(docs);



      } catch(error) {


        console.log(
          "History loading error",
          error
        );


      }


    };



    loadHistory();


  }, [refresh]);





  return (

    <div className="card">


      <h2>
        History
      </h2>




      {
        conversations.map((chat)=>(


          <div

            key={chat.id}

            className="document-item"

            onClick={() =>
              onSelectConversation(chat.id)
            }

          >

            💬 {chat.title}


          </div>


        ))

      }






      {
  documents.map((doc)=>(

    <div

      key={doc.id}

      className="document-item"

      onClick={async()=>{

        try{

          const data =
            await getConversationByDocument(
              doc.id
            );


          onSelectConversation(
            data.conversation_id
          );


        }catch(error){

          console.log(
            "No chat found for document",
            error
          );

        }

      }}

    >

      📄 {doc.filename}

    </div>

  ))
}




      {
        conversations.length === 0 &&
        documents.length === 0 &&
        (

          <p>
            No history yet
          </p>

        )

      }



    </div>

  );

}