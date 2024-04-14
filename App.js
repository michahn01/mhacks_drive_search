import React, { useState , useEffect} from 'react';
import axios from 'axios';
import './App.css'; // Importing CSS

function App() {
  const [inputText, setInputText] = useState('');
  const [links, setLinks] = useState([]);
  const [isLoading, setIsLoading] = useState(false);

  const handleInputChange = (e) => {
    setInputText(e.target.value);
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    setIsLoading(true);
  
    // Create the body of the request with inputText
    const data = { inputText: inputText };
  
    try {
      const response = await axios.put('http://localhost:5000/', data);
      setLinks(response.data.links); // Assuming the JSON response has a 'links' key
  
    } catch (error) {
      console.error('Error fetching data:', error);
      setLinks([]); // Reset to empty array on error
    } finally {
      setIsLoading(false);
    }
  };
  
  
  
const TypingAnimation = ({ messages = ["Hello", "World", "Welcome"], speed = 30 }) => {
  const [index, setIndex] = useState(0);
  const [subIndex, setSubIndex] = useState(0);
  const [reverse, setReverse] = useState(false);

  // Typing effect
  useEffect(() => {
      if (subIndex === messages[index].length + 1 && !reverse) {
          setReverse(true);
          return;
      }

      if (subIndex === 0 && reverse) {
          setReverse(false);
          setIndex((prevIndex) => (prevIndex + 1) % messages.length);
          return;
      }

      const timeout = setTimeout(() => {
          setSubIndex((prevSubIndex) => prevSubIndex + (reverse ? -1 : 1));
      }, speed);

      return () => clearTimeout(timeout);
  }, [subIndex, index, reverse]);

  return (
      <div className="typing-animation">
          <p>{`${messages[index].substring(0, subIndex)}${subIndex === messages[index].length ? '' : '|'}`}</p>
      </div>
  );
};
  return (
    <div className="app">
      <div className="logo-bar">
        <div className='logos-left'>
          <img src="Archive.png" alt="logo" className="logo-archive"/>
        </div>
        
        <div className='logos-right'>
        <img src="googledrive.png" alt="Logo 3" className="logo" />
          <button className="mount-button">Upload</button>
        </div>
        
      </div>
      <main className="main-content">
        <div className="left-side">
          <div className="logo-power">
            <h1 className="logo-power h1">Powered by </h1>
            <img src="gemini.png" alt="logo-gemini" className="logo-gemini"/>
            
          </div>
          <div className="example-prompt">
          <h2 className='example-prompt h2'>I want to see the picture from my trip to the Grand Canyon last summer!</h2>
          <h2 className='example-prompt h2'>I want to see my photo with my teammates at Google X MHack hackathon!</h2>
        </div>
          
          <TypingAnimation messages={
            [ "I want to see my dog...",
              "I want to see my cat...",
              "I want to see my elephant...",
          ]
            } speed={100} />

        </div>

        <div className="right-side">
          <form className="search-form" onSubmit={handleSubmit}>
            <input
              type="text"
              className='search-input'
              value={inputText}
              onChange={handleInputChange}
              placeholder="Ask your heart's desire..."
            />
            <button type="submit" className="search-button" disabled={isLoading}>
              {isLoading ? 'Loading...' : 'Submit'}
            </button>
          </form>
          <div className="place-holder">
            {links.length > 0 ? (
              links.map((link, index) => (
                <a key={index} className="search-results" href={link} target="_blank" rel="noopener noreferrer">
                  {link}
                </a>
              ))
            ) : (
              <div style={{color: 'gray'}}>Life is too short for scrolling</div>  // Default text when there are no links
            )}
          </div>
          
        </div>
        
      </main>
    </div>
  );
}

export default App;
