import { useEffect, useState } from "react";
import { getConversations, getDocuments } from "../services/api";


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
}


export default function ChatHistory({
  onSelectConversation
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

  }, []);



  return (

    <div className="card">


      <h2>
        History
      </h2>



      {
        conversations.map((chat) => (

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
        documents.map((doc) => (

          <div
            key={doc.id}
            className="document-item"
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