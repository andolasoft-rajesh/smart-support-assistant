import { useState } from "react";
import "./App.css";

import Chat from "./components/Chat";
import ChatHistory from "./components/ChatHistory";

function App() {

  const [selectedConversation, setSelectedConversation] =
    useState<string | null>(null);

  const [historyRefresh, setHistoryRefresh] =
    useState(0);

  // Trigger to reset Chat component when starting a new chat
  const [newChatTrigger, setNewChatTrigger] =
    useState(0);

  const refreshHistory = () => {

    setHistoryRefresh(
      (prev) => prev + 1
    );

  };

  const startNewChat = () => {

    setSelectedConversation(null);

    setNewChatTrigger(
      (prev) => prev + 1
    );

  };

  return (

    <div className="app-layout">

      <aside className="sidebar">

        <div className="brand">

          <h2>
            Smart Support
          </h2>

          <p>
            Your AI-powered knowledge assistant
          </p>

        </div>

        <button
          className="new-chat-btn"
          onClick={startNewChat}
        >
          + New Chat
        </button>

        <ChatHistory
          onSelectConversation={setSelectedConversation}
          refresh={historyRefresh}
        />

      </aside>

      <main className="chat-area">

        <Chat
          conversationId={selectedConversation}
          setConversationId={setSelectedConversation}
          onHistoryUpdate={refreshHistory}
          
        />

      </main>

    </div>

  );

}

export default App;