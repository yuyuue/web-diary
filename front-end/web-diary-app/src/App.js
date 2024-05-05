import React, { useState, useEffect } from 'react';
import axios from 'axios';
import 'bootstrap/dist/css/bootstrap.min.css';

function App() {
  const [entries, setEntries] = useState([]);
  const [content, setContent] = useState('');

  useEffect(() => {
    axios.get('http://localhost:5000/entries')
      .then(response => setEntries(response.data))
      .catch(error => console.error('Error:', error));
  }, []);

  const addEntry = () => {
    axios.post('http://localhost:5000/entries', { content })
      .then(response => {
        setEntries([...entries, response.data]);
        setContent('');
      })
      .catch(error => console.error('Error:', error));
  };

  return (
    <div className="container mt-3">
      <h2>日記アプリ</h2>
      <div>
        <textarea className="form-control mb-2" placeholder="何か書いてください..."
          value={content} onChange={e => setContent(e.target.value)} rows="3"></textarea>
        <button className="btn btn-primary" onClick={addEntry}>エントリを追加</button>
      </div>
      <ul className="list-group mt-3">
        {entries.map(entry => (
          <li key={entry.id} className="list-group-item">{entry.content}</li>
        ))}
      </ul>
    </div>
  );
}

export default App;
