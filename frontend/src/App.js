import React, { useEffect } from 'react';
import { useEmail } from './hooks/useEmail';
import EmailForm from './components/EmailForm';
import EmailHistory from './components/EmailHistory';
import Message from './components/Message';
import './styles/App.css';

function App() {
  const { fetchEmailHistory, fetchTemplates } = useEmail();

  useEffect(() => {
    fetchEmailHistory();
    fetchTemplates();
  }, []);

  return (
    <div className="app-container">
      <div className="app-header">
        <h1>🤖 AI Email Agent</h1>
        <p>Draft and send emails with AI assistance</p>
      </div>

      <Message />
      
      <div className="app-content">
        <EmailForm />
        <EmailHistory />
      </div>
    </div>
  );
}

export default App;
