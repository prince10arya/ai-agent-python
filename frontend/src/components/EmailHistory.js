import React from 'react';
import { useEmailStore } from '../store/useEmailStore';
import '../styles/EmailHistory.css';

const EmailHistory = () => {
  const emailHistory = useEmailStore((state) => state.emailHistory);

  const formatDate = (dateString) => {
    return new Date(dateString).toLocaleString();
  };

  return (
    <div className="email-history">
      <h2>📨 Email History</h2>
      {emailHistory.length === 0 ? (
        <div className="no-emails">No emails sent yet</div>
      ) : (
        emailHistory.map((email) => (
          <div key={email.id} className="email-item">
            <div className="email-header">
              <div className="email-subject">{email.subject}</div>
              <div className={`email-status status-${email.status}`}>
                {email.status.toUpperCase()}
              </div>
            </div>
            <div className="email-meta">
              👤 To: {email.recipient} | 📅 {formatDate(email.created_at)}
            </div>
            <div className="email-content">
              <strong>Prompt:</strong> {email.prompt}
              <br /><br />
              <strong>Content:</strong><br />
              {email.content}
            </div>
          </div>
        ))
      )}
    </div>
  );
};

export default EmailHistory;
