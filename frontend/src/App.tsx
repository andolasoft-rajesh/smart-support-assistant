import "./App.css";

import Chat from "./components/Chat";
import DocumentList from "./components/DocumentList";


function App() {

  return (

    <div className="app-layout">


      <aside className="sidebar">

        <div className="brand">

          <h2>
             Smart Support
          </h2>

          <p>
            AI Document Assistant
          </p>

        </div>


        <DocumentList />


      </aside>



      <main className="chat-area">

        <Chat />

      </main>


    </div>

  );

}


export default App;