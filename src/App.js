import React from 'react';
import './App.css';
import UserList from './components/UserList'; // Import the UserList component

function App() {
  return (
    <div className="App">
      <header className="App-header">
        <h1>CRUD Application</h1>
      </header>
      <main>
        <UserList /> {/* Render the UserList component */}
      </main>
    </div>
  );
}

export default App;
