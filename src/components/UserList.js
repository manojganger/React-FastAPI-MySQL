import React, { useState, useEffect } from 'react';
import axios from 'axios';

function UserList() {
  const [users, setUsers] = useState([]);

  async function fetchUsers() {
    const response = await axios.get('http://localhost:8000/api/users');
    setUsers(response.data);
  }

  useEffect(() => {const eventSource = new EventSource('http://localhost:8000/api/events');
  
  
  

    eventSource.onmessage = event => {
      const newRecord = JSON.parse(event.data);
	 
      setUsers(prevUsers => [...prevUsers, newRecord]);
    };

    return () => {
      eventSource.close();
    };
	
  }, []);

  return (
    <div>
      <h2>User List</h2>
      <table>
        <thead>
          <tr>
            <th>ID</th>
            <th>Name</th>
          </tr>
        </thead>
        <tbody>
          {users.map(user => (
            <tr key={user.id}>
              <td>{user.id}</td>
              <td>{user.name}</td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
}

export default UserList;
