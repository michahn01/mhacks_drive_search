import React, { useState } from 'react';
import axios from 'axios';

function App() {
  const [inputText, setInputText] = useState('');
  const [link, setLink] = useState(''); // State to store the received link
  const [isLoading, setIsLoading] = useState(false);

  const handleInputChange = (e) => {
    setInputText(e.target.value);
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    setIsLoading(true);
    try {
      const response = await axios.post('https://somerestapi.com', { data: inputText });
      console.log(response.data); // Assuming response.data contains the link
      setLink(response.data.link); // Update state with the link
    } catch (error) {
      console.error('Error posting data:', error);
      setLink(''); // Reset or handle error
    }
    setIsLoading(false);
  };

  return (
    <div style={{ fontFamily: 'Arial, sans-serif', padding: 20 }}>
      <h1 style={{ color: '#4285F4' }}>Searchmini</h1>
      <form onSubmit={handleSubmit}>
        <input
          type="text"
          value={inputText}
          onChange={handleInputChange}
          style={{ width: '50%', height: 20, fontSize: 16, padding: 10, marginBottom: 10 }}
          placeholder="Enter a large amount of text..."
        />
        <button type="submit" style={{ padding: 10, fontSize: 16 }} disabled={isLoading}>
          {isLoading ? 'Loading...' : 'Submit'}
        </button>
      </form>
      {link && (
        <p>Response Link: <a href={link} target="_blank" rel="noopener noreferrer">{link}</a></p>
      )}
    </div>
  );
}

export default App;
